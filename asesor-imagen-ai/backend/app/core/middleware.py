"""
Application middleware: CORS, structured JSON logging, security headers,
idempotency (placeholder), auth (placeholder).

Security notes:
- CORS is restricted to ALLOWED_ORIGINS in production (never wildcard).
- Security headers follow OWASP recommendations (April 2026).
- Request logging never logs sensitive data (tokens, passwords, PII).
- Idempotency-Key middleware (ADR-003) is wired here but logic lands in 0.2.
- Auth middleware (ADR-001 — Supabase JWKS) is wired here but logic lands in 0.2.

References:
    - OWASP Secure Headers Project (2026)
    - https://supabase.com/docs/guides/auth/jwts (JWKS validation)
"""

from __future__ import annotations

import json
import logging
import sys
import time
from typing import Awaitable, Callable
from uuid import uuid4

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Structured JSON Logging (Railway-friendly)
# ---------------------------------------------------------------------------

class JsonLogFormatter(logging.Formatter):
    """Emit log records as single-line JSON for log aggregators (Railway, Datadog).

    Never serializes Authorization headers, request bodies, or PII.
    """

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, object] = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        # Attach extras supplied via logger.info(..., extra={...}).
        for key in ("request_id", "method", "path", "status", "duration_ms", "user_id"):
            value = getattr(record, key, None)
            if value is not None:
                payload[key] = value
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str)


def configure_logging() -> None:
    """Set up the root logger with JSON formatter in prod, plain in dev.

    Idempotent — safe to call multiple times.
    """
    settings = get_settings()
    root = logging.getLogger()
    # Wipe handlers added by uvicorn/pytest so our format wins.
    root.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    if settings.is_development:
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)-7s %(name)s :: %(message)s")
        )
    else:
        handler.setFormatter(JsonLogFormatter())

    root.addHandler(handler)
    root.setLevel(settings.LOG_LEVEL)

    # Quiet noisy libraries.
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)


# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------

def setup_cors(app: FastAPI) -> None:
    """Configure CORS middleware based on environment."""
    settings = get_settings()

    if settings.is_production:
        origins = settings.allowed_origins_list
        if not origins:
            # Fail loud: prod CORS misconfig is a security issue.
            raise RuntimeError(
                "ALLOWED_ORIGINS must be set in production (no wildcard allowed)."
            )
    else:
        origins = settings.allowed_origins_list or [
            "http://localhost:3000",
            "http://localhost:8080",
        ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=[
            "Authorization",
            "Content-Type",
            "X-Request-ID",
            "Idempotency-Key",
        ],
        expose_headers=["X-Request-ID"],
        max_age=600,
    )


# ---------------------------------------------------------------------------
# Per-request middlewares
# ---------------------------------------------------------------------------

# Type alias for the ASGI call_next callable.
CallNext = Callable[[Request], Awaitable[Response]]


async def request_logging_middleware(request: Request, call_next: CallNext) -> Response:
    """Log every request with timing + request ID (structured fields).

    Honors a client-supplied X-Request-ID header for distributed tracing.
    """
    request_id = request.headers.get("X-Request-ID") or uuid4().hex[:12]
    request.state.request_id = request_id
    start = time.perf_counter()

    response: Response = await call_next(request)

    duration_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "request",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "duration_ms": round(duration_ms, 2),
        },
    )

    response.headers["X-Request-ID"] = request_id
    return response


async def security_headers_middleware(request: Request, call_next: CallNext) -> Response:
    """Add OWASP-recommended security headers to every response."""
    response: Response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "0"  # Modern browsers: CSP replaces this
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Cache-Control"] = "no-store"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"

    if get_settings().is_production:
        response.headers["Strict-Transport-Security"] = (
            "max-age=63072000; includeSubDomains; preload"
        )

    return response


# ---------------------------------------------------------------------------
# Idempotency-Key (ADR-003) — PLACEHOLDER for Entrega 0.2/0.3
# ---------------------------------------------------------------------------

# Endpoints where Idempotency-Key MUST be required (ADR-003).
IDEMPOTENT_ENDPOINTS: frozenset[tuple[str, str]] = frozenset({
    ("POST", "/api/v1/try-ons"),
    ("POST", "/api/v1/payments"),
    # Webhook routes are added once their paths are finalized.
})


async def idempotency_middleware(request: Request, call_next: CallNext) -> Response:
    """Enforce Idempotency-Key header on cost-sensitive POSTs (ADR-003).

    🚧 ENTREGA 0.1: header presence check only (no replay logic yet).
    🚧 ENTREGA 0.2: store (key, response) in `idempotency_keys` table TTL 24h
                    and return cached response on duplicate key.

    See: backend/docs/DECISIONES_PENDIENTES.md (item ADR-003).
    """
    if (request.method, request.url.path) in IDEMPOTENT_ENDPOINTS:
        if not request.headers.get("Idempotency-Key"):
            from app.core.exceptions import ValidationError  # avoid circular import
            raise ValidationError(
                message="Idempotency-Key header is required for this endpoint",
                fields={"Idempotency-Key": "missing"},
            )
    return await call_next(request)


# ---------------------------------------------------------------------------
# Auth middleware (ADR-001) — PLACEHOLDER for Entrega 0.2
# ---------------------------------------------------------------------------

# Routes that bypass auth entirely. Everything else under /api/v1 requires
# a valid Supabase JWT once Entrega 0.2 lands.
PUBLIC_ROUTES: frozenset[str] = frozenset({
    "/",
    "/health",
    "/health/ready",
    "/docs",
    "/redoc",
    "/openapi.json",
})


async def auth_middleware(request: Request, call_next: CallNext) -> Response:
    """Validate Supabase-issued JWTs against JWKS (ADR-001).

    🚧 ENTREGA 0.1: pass-through. Documents the contract.
    🚧 ENTREGA 0.2: implement
        1. Skip PUBLIC_ROUTES.
        2. Read Authorization: Bearer <token>.
        3. Fetch JWKS from settings.supabase_jwks_url (cached TTL 600s).
        4. Validate ES256 signature, exp, aud=authenticated, iss.
        5. Attach payload to request.state.user (sub = auth.users.id).

    See: backend/docs/DECISIONES_PENDIENTES.md (item ADR-001).
    """
    return await call_next(request)


# ---------------------------------------------------------------------------
# Wiring helper
# ---------------------------------------------------------------------------

def install_middleware(app: FastAPI) -> None:
    """Install all middlewares in the correct order (outermost first).

    Order matters: CORS must wrap everything; logging must wrap auth so we
    log even unauthorized attempts; idempotency runs after auth so we know
    the user identity.

    Starlette executes BaseHTTPMiddleware in reverse-add order:
        last add()  -> innermost (runs nearest to the route).
        first add() -> outermost (runs first on request, last on response).
    """
    from starlette.middleware.base import BaseHTTPMiddleware

    # Innermost first (closest to the endpoint).
    app.add_middleware(BaseHTTPMiddleware, dispatch=idempotency_middleware)
    app.add_middleware(BaseHTTPMiddleware, dispatch=auth_middleware)
    app.add_middleware(BaseHTTPMiddleware, dispatch=security_headers_middleware)
    app.add_middleware(BaseHTTPMiddleware, dispatch=request_logging_middleware)
    # CORS goes last so it ends up outermost (handles preflight before logging).
    setup_cors(app)
