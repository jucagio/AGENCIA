import datetime
import logging
import pytz
from typing import Callable, Awaitable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import redis.asyncio as aioredis
from slowapi import Limiter
from slowapi.util import get_remote_address
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from prometheus_client import Counter, Histogram

from app.config import get_settings

logger = logging.getLogger(__name__)

# --- Metrics (Sprint 0.4 Task A1) ---
RATE_LIMIT_HITS = Counter(
    "rate_limit_hits_total",
    "Number of times a rate limit was hit",
    ["endpoint", "user_tier"]
)
RATE_LIMIT_FALLBACK = Counter(
    "rate_limit_redis_fallback_total",
    "Number of times Redis rate limiter degraded to Postgres"
)
RATE_LIMIT_LATENCY = Histogram(
    "rate_limit_redis_latency_seconds",
    "Latency of Redis operations for rate limiting",
    buckets=(0.01, 0.05, 0.1, 0.25, 0.5, 1.0)
)
IDEMPOTENCY_CACHE_HITS = Counter(
    "rate_limit_idempotency_cache_hits",
    "Number of times idempotency cache intercepted a request"
)

settings = get_settings()

# Basic SlowAPI limiter for trivial endpoints
limiter = Limiter(key_func=get_remote_address)

# Lua script for CR-1 (Atomic INCR with CAP and TTL)
# Returns {1, new_val} if allowed
# Returns {0, current} if blocked
INCR_WITH_CAP_LUA = """
local current = redis.call('GET', KEYS[1])
local limit = tonumber(ARGV[1])
if current and tonumber(current) >= limit then
    return {0, tonumber(current)}
end
local new_val = redis.call('INCR', KEYS[1])
if tonumber(new_val) == 1 then
    redis.call('EXPIREAT', KEYS[1], tonumber(ARGV[2]))
end
return {1, tonumber(new_val)}
"""

def get_bogota_sunday_reset_timestamp() -> int:
    """CR-2: ISO_WEEK computed in America/Bogota timezone."""
    bogota = pytz.timezone('America/Bogota')
    now = datetime.datetime.now(bogota)
    # Calculate days ahead to get to Sunday (6 = Sunday in Python weekday(), 0 = Monday)
    days_ahead = 6 - now.weekday()
    if days_ahead < 0:
        days_ahead += 7
    next_sunday = now + datetime.timedelta(days_ahead)
    # Set to 23:59:59
    next_sunday_end = next_sunday.replace(hour=23, minute=59, second=59, microsecond=0)
    return int(next_sunday_end.timestamp())

def get_bogota_iso_week() -> str:
    """Returns YYYY-WW in Bogota timezone."""
    bogota = pytz.timezone('America/Bogota')
    now = datetime.datetime.now(bogota)
    year, week, _ = now.isocalendar()
    return f"{year}-W{week:02d}"

class TryOnRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis_pool: aioredis.Redis = None):
        super().__init__(app)
        self.redis = redis_pool or aioredis.from_url(settings.REDIS_URL, decode_responses=True)
        self.limit = settings.RATE_LIMITS.get("try_ons", {}).get("limit", 3)
        self.lua_script_sha = None

    async def _load_lua_script(self):
        if not self.lua_script_sha:
            try:
                self.lua_script_sha = await self.redis.script_load(INCR_WITH_CAP_LUA)
            except Exception as exc:
                logger.error("Failed to load Lua script: %s", exc)

    async def _fallback_to_postgres(self, user_id: str, request: Request) -> bool:
        """CR-4: Atomic fallback to Postgres with row lock."""
        try:
            # Requires access to AdminClient or raw Postgres connection
            ctx = getattr(request.state, "admin_client", None)
            if not ctx:
                # If middleware doesn't have supabase client injected, we might need a direct call
                logger.error("No DB client available for fallback")
                return False

            # Execute the RPC created in Migration 006 (CR-4)
            res = await ctx.rpc("increment_weekly_tryon_usage", {"p_user_id": user_id, "p_cap": self.limit}).execute()
            if res.data is not None:
                new_usage = res.data
                if new_usage <= self.limit:
                    return True # Allowed
            return False # Blocked
        except Exception as exc:
            logger.error("Postgres fallback failed: %s", exc)
            return False

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if request.url.path == "/api/v1/try-ons" and request.method == "POST":
            # 1. Get user_id (assume authenticated via AuthMiddleware before this)
            user_id = getattr(request.state, "user_id", None)
            if not user_id:
                # If no user_id, let auth middleware block it or handle anonymous
                return await call_next(request)

            # 2. Check Rate Limit
            iso_week = get_bogota_iso_week()
            rate_limit_key = f"user:{user_id}:tryons:week:{iso_week}"
            reset_ts = get_bogota_sunday_reset_timestamp()
            
            await self._load_lua_script()
            
            headers = {
                "X-RateLimit-Limit": str(self.limit),
                "X-RateLimit-Reset": str(reset_ts)
            }

            try:
                # Evaluate Lua Script (CR-1)
                import time
                t0 = time.perf_counter()
                
                lua_res = await self.redis.evalsha(self.lua_script_sha, 1, rate_limit_key, self.limit, reset_ts)
                
                RATE_LIMIT_LATENCY.observe(time.perf_counter() - t0)
                
                allowed, current_usage = lua_res[0], lua_res[1]
                
                headers["X-RateLimit-Remaining"] = str(max(0, self.limit - current_usage))
                
                if not allowed:
                    RATE_LIMIT_HITS.labels(endpoint="/api/v1/try-ons", user_tier="free").inc()
                    # Append headers and return 429
                    response = JSONResponse(
                        status_code=429, 
                        content={"detail": "Weekly cap reached. Resets Sunday 23:59 UTC-5."}
                    )
                    for k, v in headers.items():
                        response.headers[k] = v
                    response.headers["Retry-After"] = str(max(0, reset_ts - int(datetime.datetime.now(pytz.utc).timestamp())))
                    return response

            except Exception as exc:
                logger.error("rate_limit_redis_fallback: %s", exc)
                RATE_LIMIT_FALLBACK.inc()
                # Fallback to Postgres (CR-4)
                success = await self._fallback_to_postgres(user_id, request)
                if not success:
                    RATE_LIMIT_HITS.labels(endpoint="/api/v1/try-ons", user_tier="free").inc()
                    # Q2: 503 Service Unavailable (fail-closed)
                    return JSONResponse(
                        status_code=503,
                        content={"detail": "Service Unavailable. Rate limit verification failed."}
                    )
                # If fallback succeeded, we continue

            response = await call_next(request)
            
            # Inject headers
            for k, v in headers.items():
                response.headers[k] = v
                
            return response

        return await call_next(request)
