"""
Asesor de Imagen AI — FastAPI application entry point.

Wiring:
    1. configure_logging()        — JSON logs in prod, plain in dev.
    2. assert_production_ready()  — fail fast if prod misconfigured.
    3. lifespan: init Supabase admin client, store on app.state.
    4. install_middleware()       — CORS + logging + sec headers + auth + idempotency.
    5. exception handlers         — uniform { success, error } JSON shape.
    6. routers                    — health, /api/v1.

Run locally:
    uvicorn app.main:app --reload --port 8000
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.api.v1.router import api_v1_router
from app.config import get_settings
from app.core.database import create_admin_client
from app.core.exceptions import (
    AppException,
    app_exception_handler,
    http_exception_handler,
    unhandled_exception_handler,
)
from app.core.middleware import configure_logging, install_middleware
from app.core.queue import close_queue_pool, create_queue_pool
from app.core.rate_limiter import limiter, TryOnRateLimitMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """App startup/shutdown hooks.

    Startup:
        - Configure logging (JSON in prod).
        - Validate production env (fail fast if misconfigured).
        - Initialize Supabase admin client → app.state.supabase_admin.

    Shutdown:
        - Drop client refs (httpx pools close on GC).
    """
    settings = get_settings()
    configure_logging()

    if settings.is_production:
        settings.assert_production_ready()

    logger.info(
        "Starting %s v%s in %s mode",
        settings.APP_NAME,
        settings.APP_VERSION,
        settings.ENVIRONMENT,
    )

    # Supabase admin client (service-role) — used by webhooks & workers.
    try:
        app.state.supabase_admin = await create_admin_client(settings)
    except Exception as exc:  # noqa: BLE001 — boot diagnostic
        if settings.is_production:
            raise
        logger.warning("Supabase admin client init skipped (dev): %s", exc)
        app.state.supabase_admin = None

    # ARQ pool — centralized in app.state.queue (Sprint 0.5 T2).
    try:
        app.state.queue = await create_queue_pool(settings)
    except Exception as exc:  # noqa: BLE001
        if settings.is_production:
            raise
        logger.warning("ARQ pool init skipped (dev): %s", exc)
        app.state.queue = None

    yield

    logger.info("Shutting down %s", settings.APP_NAME)
    await close_queue_pool(getattr(app.state, "queue", None))
    app.state.queue = None
    app.state.supabase_admin = None


def create_app() -> FastAPI:
    """Application factory — used by uvicorn and tests."""
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        description="Virtual Try-On & Wardrobe Assistant with AI Recommendations",
        version=settings.APP_VERSION,
        lifespan=lifespan,
        # Hide docs in production unless explicitly enabled.
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
        openapi_url="/openapi.json" if not settings.is_production else None,
    )

    # Middlewares (order managed inside install_middleware).
    install_middleware(app)

    # Exception handlers.
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Rate Limiting — gated by FEATURE_RATE_LIMIT_ENABLED flag (ADR-007 safe rollout).
    # When disabled (MVP default), middleware is not registered to avoid Redis
    # dependency at boot and to skip Lua script loading. Re-enable in production
    # by setting FEATURE_RATE_LIMIT_ENABLED=true once A1 ships fully.
    app.state.limiter = limiter
    if settings.FEATURE_RATE_LIMIT_ENABLED:
        app.add_middleware(TryOnRateLimitMiddleware)
        logger.info("Rate limiting middleware enabled (TryOnRateLimitMiddleware)")
    else:
        logger.info("Rate limiting middleware DISABLED (FEATURE_RATE_LIMIT_ENABLED=false)")

    # Routers.
    app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)

    # Health endpoints (kept at root so load balancers / Railway can probe).
    # Sprint 0.5 T3 — /health is the fast liveness probe (always 200 if up),
    # /ready (and legacy /health/ready) is the slow readiness probe that
    # verifies Redis + Supabase + ARQ queue.

    @app.get("/health", tags=["Meta"])
    async def health_check() -> JSONResponse:
        """Liveness probe. Always returns 200 if the process is up.

        Used by Kubernetes liveness probes. Does NOT touch dependencies —
        a Redis outage must NOT kill our pod, only depin it from the LB.
        """
        from datetime import datetime, timezone  # noqa: PLC0415
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": {
                    "status": "ok",
                    "service": settings.APP_NAME,
                    "version": settings.APP_VERSION,
                    "environment": settings.ENVIRONMENT,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
            },
        )

    async def _check_ready(request: Request) -> JSONResponse:
        """Shared implementation for /ready and /health/ready."""
        import asyncio  # noqa: PLC0415
        from datetime import datetime, timezone  # noqa: PLC0415

        results: dict[str, str] = {"db": "down", "redis": "down", "queue": "down"}

        # ── DB (Supabase) — 500ms ────────────────────────────────────────
        supabase_admin = getattr(request.app.state, "supabase_admin", None)
        if supabase_admin is not None:
            try:
                async def _db_ping() -> None:
                    # Minimal query — counts a known table with HEAD.
                    await (
                        supabase_admin
                        .from_("profiles")
                        .select("id", count="exact", head=True)
                        .limit(1)
                        .execute()
                    )
                await asyncio.wait_for(_db_ping(), timeout=0.5)
                results["db"] = "ok"
            except Exception as exc:  # noqa: BLE001
                logger.warning("Readiness: DB check failed: %s", exc)

        # ── Redis — 100ms ────────────────────────────────────────────────
        try:
            import redis.asyncio as aioredis  # noqa: PLC0415
            redis_client = aioredis.from_url(
                settings.REDIS_URL,
                socket_connect_timeout=0.1,
                socket_timeout=0.1,
            )
            pong = await asyncio.wait_for(redis_client.ping(), timeout=0.1)
            await redis_client.close()
            if pong:
                results["redis"] = "ok"
        except Exception as exc:  # noqa: BLE001
            logger.warning("Readiness: Redis check failed: %s", exc)

        # ── ARQ queue — pool must be alive (uses same Redis but separate check) ─
        pool = getattr(request.app.state, "queue", None)
        if pool is not None:
            try:
                # ArqRedis wraps redis-py; ping is cheap.
                await asyncio.wait_for(pool.ping(), timeout=0.2)
                results["queue"] = "ok"
            except Exception as exc:  # noqa: BLE001
                logger.warning("Readiness: ARQ queue check failed: %s", exc)
        elif settings.is_development:
            # In dev we tolerate missing queue (PATH A).
            results["queue"] = "ok"

        all_ok = all(v == "ok" for v in results.values())
        # In development we never return 503 — devs run without all deps.
        status_code = 200 if (all_ok or settings.is_development) else 503

        return JSONResponse(
            status_code=status_code,
            content={
                "success": all_ok,
                "data": {
                    **results,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
            },
        )

    @app.get("/ready", tags=["Meta"])
    async def readiness_v2(request: Request) -> JSONResponse:
        """Readiness probe (Sprint 0.5 T3). 200 when all deps OK, 503 otherwise."""
        return await _check_ready(request)

    @app.get("/health/ready", tags=["Meta"])
    async def readiness_legacy(request: Request) -> JSONResponse:
        """Legacy alias — kept for existing load balancer configs."""
        return await _check_ready(request)

    @app.get("/", tags=["Meta"])
    async def root() -> dict[str, str]:
        return {
            "message": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "docs": "/docs" if not settings.is_production else "disabled",
        }

    return app


# ASGI entry point.
app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
