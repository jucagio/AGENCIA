"""
ARQ cron job to reconcile Redis rate limit counters with Postgres source of truth.
"""

from __future__ import annotations

import logging
from typing import Any

from arq.cron import cron
import redis.asyncio as aioredis
from app.config import get_settings
from app.core.admin_client import AdminClient
from app.core.rate_limiter import get_bogota_iso_week

logger = logging.getLogger(__name__)

async def startup(ctx: dict[str, Any]) -> None:
    settings = get_settings()
    # Ensure admin_client is injected if not already
    if "admin_client" not in ctx:
        from app.core.database import create_admin_client
        ctx["admin_client"] = await create_admin_client(settings)
    if "redis" not in ctx:
        ctx["redis"] = aioredis.from_url(settings.REDIS_URL, decode_responses=True)

async def shutdown(ctx: dict[str, Any]) -> None:
    redis = ctx.get("redis")
    if redis:
        await redis.close()

async def reconcile_counters(ctx: dict[str, Any]) -> None:
    """
    ARQ Cron job (hourly) to detect race conditions and Redis evictions.
    Selects usage_this_week from Postgres and reconciles with Redis.
    """
    logger.info("Starting counter reconciliation job...")
    admin: AdminClient = AdminClient(ctx["admin_client"])
    redis: aioredis.Redis = ctx["redis"]
    
    current_week = get_bogota_iso_week()
    
    try:
        # Fetch all users that have a usage_this_week > 0 from Postgres
        # In a very large DB, we might batch this. For Sprint 0.4, we fetch active users.
        res = await admin.trusted().table("users").select("id, usage_this_week").gt("usage_this_week", 0).execute()
        users_in_pg = res.data or []
        
        discrepancy_count = 0
        
        for user in users_in_pg:
            user_id = user["id"]
            pg_usage = user["usage_this_week"]
            
            redis_key = f"user:{user_id}:tryons:week:{current_week}"
            redis_val = await redis.get(redis_key)
            redis_usage = int(redis_val) if redis_val else 0
            
            # If Postgres is ahead of Redis, it means Redis evicted the key or went down.
            # If Redis is ahead of Postgres, it means we have pending ARQ jobs that haven't finalized, or it's a transient race.
            # The prompt says: "Si discrepancia > 1 -> log + Sentry alert"
            diff = abs(pg_usage - redis_usage)
            
            if diff > 1:
                discrepancy_count += 1
                logger.error(
                    "Rate limit discrepancy detected for user %s: Postgres=%s, Redis=%s",
                    user_id, pg_usage, redis_usage,
                    extra={"user_id": user_id, "pg_usage": pg_usage, "redis_usage": redis_usage}
                )
                
                # Reconcile: Use Postgres as source of truth.
                # If Redis is lower, overwrite Redis to prevent exceeding cap
                if pg_usage > redis_usage:
                    from app.core.rate_limiter import get_bogota_sunday_reset_timestamp
                    await redis.set(redis_key, pg_usage)
                    await redis.expireat(redis_key, get_bogota_sunday_reset_timestamp())
                    logger.info("Reconciled Redis counter for user %s to %s", user_id, pg_usage)

        logger.info("Counter reconciliation finished. Discrepancies resolved: %s", discrepancy_count)
        
    except Exception as exc:
        logger.error("Reconciliation job failed: %s", exc)

class WorkerSettings:
    """Settings for the ARQ reconciliation worker."""
    functions = []
    cron_jobs = [
        cron(reconcile_counters, minute=0)  # run hourly at the top of the hour
    ]
    on_startup = startup
    on_shutdown = shutdown
