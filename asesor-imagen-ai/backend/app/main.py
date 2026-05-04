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

    yield

    logger.info("Shutting down %s", settings.APP_NAME)
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

    # Routers.
    app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)

    # Health endpoints (kept at root so load balancers / Railway can probe).
    @app.get("/health", tags=["Meta"])
    async def health_check() -> JSONResponse:
        """Liveness probe. Always returns 200 if process is up."""
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": {
                    "status": "ok",
                    "service": settings.APP_NAME,
                    "version": settings.APP_VERSION,
                    "environment": settings.ENVIRONMENT,
                },
            },
        )

    @app.get("/health/ready", tags=["Meta"])
    async def readiness(request: Request) -> JSONResponse:
        """Readiness probe — verifies critical dependencies are reachable.

        Entrega 0.1: checks Supabase admin client presence.
        Entrega 0.2+: add Redis ping, Replicate ping, etc.
        """
        supabase_ok = getattr(request.app.state, "supabase_admin", None) is not None
        ready = supabase_ok or settings.is_development
        return JSONResponse(
            status_code=200 if ready else 503,
            content={
                "success": ready,
                "data": {
                    "supabase": "ok" if supabase_ok else "not_initialized",
                },
            },
        )

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
