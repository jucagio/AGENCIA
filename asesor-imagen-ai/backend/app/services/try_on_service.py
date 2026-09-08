"""
Try-On service — virtual try-on pipeline with caching (ADR-004).

Sprint 0.5 changes (T2-T4):
  - Uses centralized ARQ pool (app.state.queue) instead of creating a new
    one per request.
  - Computes the cache key with FASHN mode included (per-tier isolation).
  - Resolves the user's subscription plan → FASHN mode before enqueue.
  - Records the initial FSM state ('queued') on the try-on row.

Cache strategy (ADR-004 + T4):
  SHA256(body_analysis_id + wardrobe_item_id + REPLICATE_MODEL_VERSION + fashn_mode)
  HOT cache TTL: 7 days (Redis)    — checked in replicate_worker.
  WARM cache TTL: 90 days (Postgres `try_on_cache`).
"""

from __future__ import annotations

import logging
from typing import Any
from uuid import UUID

from app.core.admin_client import AdminClient
from app.models.fsm import FSMState, plan_to_fashn_mode, plan_to_tier
from app.models.try_on import TryOn
from app.repositories.repos import TryOnRepository, UsageCounterRepository
from app.schemas.try_on import TryOnFeedbackRequest
from app.services.cache_service import compute_cache_key

logger = logging.getLogger(__name__)

FREE_TRY_ON_CAP = 5  # per month (legacy monthly cap — weekly cap is in rate_limiter)


class TryOnService:
    """Virtual try-on job management."""

    def __init__(self, admin: AdminClient, queue: Any = None) -> None:
        """
        Args:
            admin: AdminClient wrapper around service-role PostgREST.
            queue: ArqRedis pool from `app.state.queue` (Sprint 0.5 T2).
                   Optional in tests / dev — falls back to per-call create_pool.
        """
        self._repo = TryOnRepository(admin)
        self._usage_repo = UsageCounterRepository(admin)
        self._admin = admin
        self._queue = queue

    async def _resolve_user_plan(self, user_id: UUID) -> str:
        """Return the user's active plan ('free' | 'estilo' | 'imagen').

        Falls back to 'free' when no active subscription row is found.
        """
        try:
            res = await (
                self._admin.with_user_check(user_id=user_id)
                .table("subscriptions")
                .select("plan_type, status")
                .in_("status", ["active", "trialing"])
                .order("created_at", desc=True)
                .limit(1)
                .maybe_single()
                .execute()
            )
            if res and res.data:
                return res.data.get("plan_type") or "free"
        except Exception as exc:  # noqa: BLE001
            logger.warning("plan lookup failed for %s: %s", user_id, exc)
        return "free"

    async def create_try_on(
        self,
        *,
        user_id: UUID,
        wardrobe_item_id: UUID,
        body_analysis_id: UUID,
    ) -> dict:  # type: ignore[type-arg]
        """
        Initiate a try-on job with cache check (ADR-004) + FSM init.

        1. Resolve plan → fashn_mode (T4).
        2. Compute content_hash including fashn_mode.
        3. Check Postgres warm cache (try_on_cache) for fast path.
        4. If hit: create completed try_on, return immediately.
        5. If miss: create queued try_on (FSM state='queued'), enqueue worker.

        Returns:
            {try_on_id, status, cache_hit, fashn_mode, tier, estimated_seconds}
        """
        from app.config import get_settings  # noqa: PLC0415

        settings = get_settings()

        # Monthly legacy cap (weekly cap handled by rate_limiter middleware).
        counter = await self._usage_repo.get_current_period(user_id=user_id)
        if counter and counter.try_ons_used >= FREE_TRY_ON_CAP:
            from app.core.exceptions import ValidationError  # noqa: PLC0415
            raise ValidationError(
                message="Monthly try-on limit reached. Upgrade to continue.",
                fields={"limit": str(FREE_TRY_ON_CAP)},
            )

        plan = await self._resolve_user_plan(user_id)
        fashn_mode = plan_to_fashn_mode(plan)
        tier = plan_to_tier(plan)

        content_hash = compute_cache_key(
            body_analysis_id=str(body_analysis_id),
            wardrobe_item_id=str(wardrobe_item_id),
            model_version=settings.REPLICATE_MODEL_VERSION,
            fashn_mode=fashn_mode,
        )

        # Warm cache check (Postgres) — fast path.
        cache_hit = await self._repo.get_by_content_hash(
            user_id=user_id, content_hash=content_hash
        )

        if cache_hit:
            logger.info(
                "Cache hit (warm) for content_hash=%s tier=%s",
                content_hash[:16], tier,
            )
            return {
                "try_on_id": str(cache_hit.id),
                "status": "completed",
                "cache_hit": True,
                "fashn_mode": fashn_mode,
                "tier": tier,
                "result_cdn_url": cache_hit.result_cdn_url,
                "estimated_seconds": 0,
            }

        # Create queued try_on with FSM state.
        try_on = await self._repo.create(
            user_id=user_id,
            data={
                "wardrobe_item_id": str(wardrobe_item_id),
                "body_analysis_id": str(body_analysis_id),
                "content_hash": content_hash,
                "status": "pending",
                "cache_hit": False,
                "replicate_model_version": settings.REPLICATE_MODEL_VERSION,
                "fashn_mode": fashn_mode,
                "fsm_state": FSMState.QUEUED.value,
            },
        )

        # Increment usage counter (best-effort).
        try:
            await self._usage_repo.increment(user_id=user_id, field="try_ons_used")
        except Exception as exc:  # noqa: BLE001
            logger.warning("Usage counter increment failed: %s", exc)

        # Enqueue via centralized pool (T2) — falls back to ad-hoc pool if not wired.
        await self._enqueue_process_try_on(str(try_on.id), content_hash)

        logger.info(
            "Try-on created: try_on_id=%s user_id=%s tier=%s mode=%s",
            try_on.id, user_id, tier, fashn_mode,
        )

        return {
            "try_on_id": str(try_on.id),
            "status": "pending",
            "cache_hit": False,
            "fashn_mode": fashn_mode,
            "tier": tier,
            "estimated_seconds": 30,
        }

    async def _enqueue_process_try_on(self, try_on_id: str, content_hash: str) -> None:
        """Enqueue with centralized pool (preferred) or fall back to ad-hoc."""
        if self._queue is not None:
            await self._queue.enqueue_job("process_try_on", try_on_id, content_hash)
            return

        # Fallback path (dev, tests, or pool not yet wired at boot).
        try:
            from arq import create_pool  # noqa: PLC0415
            from arq.connections import RedisSettings  # noqa: PLC0415
            from app.config import get_settings  # noqa: PLC0415

            settings = get_settings()
            pool = await create_pool(RedisSettings.from_dsn(settings.REDIS_URL))
            await pool.enqueue_job("process_try_on", try_on_id, content_hash)
            await pool.close()
        except Exception as exc:  # noqa: BLE001
            logger.error("Failed to enqueue process_try_on: %s", exc)
            raise

    async def get_try_on(self, *, user_id: UUID, try_on_id: UUID) -> TryOn:
        """Return a specific try-on record owned by user_id."""
        return await self._repo.get_by_id(user_id=user_id, record_id=try_on_id)

    async def list_try_ons(
        self, *, user_id: UUID, page: int = 1, size: int = 20
    ) -> tuple[list[TryOn], int]:
        """Return paginated try-on history for user_id."""
        return await self._repo.list_for_user(user_id=user_id, page=page, per_page=size)

    async def submit_feedback(
        self,
        *,
        user_id: UUID,
        try_on_id: UUID,
        feedback: TryOnFeedbackRequest,
    ) -> TryOn:
        """Record user engagement feedback on a try-on result."""
        data = feedback.model_dump(exclude_unset=True, exclude_none=True)
        return await self._repo.update(
            user_id=user_id,
            record_id=try_on_id,
            data=data,
        )
