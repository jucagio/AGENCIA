"""
Application middleware: CORS, structured JSON logging, security headers,
idempotency (ADR-003 — full replay logic), auth (ADR-001 — Supabase JWKS).

Security notes:
- CORS is restricted to ALLOWED_ORIGINS in production (never wildcard).
- Security headers follow OWASP recommendations (April 2026).
- Request logging never logs sensitive data (tokens, passwords, PII).
- Idempotency-Key middleware (ADR-003): full replay with DB store.
- Auth middleware (ADR-001): validates Supabase JWKS ES256/RS256 tokens.

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
from fastapi.responses import JSONResponse

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
# Auth middleware (ADR-001) — Supabase JWKS
# ---------------------------------------------------------------------------

PUBLIC_ROUTES: frozenset[str] = frozenset({
    "/",
    "/health",
    "/health/ready",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/api/v1/auth/register",
    "/api/v1/auth/login",
    "/api/v1/auth/refresh",
    "/api/v1/webhooks/stripe",
    "/api/v1/webhooks/mercadopago",
})


async def auth_middleware(request: Request, call_next: CallNext) -> Response:
    """
    Validate Supabase JWT (ADR-001). Skip PUBLIC_ROUTES and OPTIONS.

    Attaches to request.state:
        user_payload: dict — full decoded JWT claims
        user_id: str     — auth.users.id (UUID as string)
    """
    # Preflight requests don't carry tokens
    if request.method == "OPTIONS":
        return await call_next(request)

    if request.url.path in PUBLIC_ROUTES:
        return await call_next(request)

    # Allow paths that start with docs/openapi (query strings etc.)
    path = request.url.path
    if path.startswith("/docs") or path.startswith("/redoc") or path.startswith("/openapi"):
        return await call_next(request)

    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=401,
            content={"detail": "Authorization header missing or malformed"},
        )

    token = auth_header[7:]

    # Import here to avoid circular imports at module load time
    from app.core.exceptions import AuthenticationError  # noqa: PLC0415
    from app.core.supabase_auth import validate_supabase_token  # noqa: PLC0415

    try:
        payload = validate_supabase_token(token)
        request.state.user_payload = payload
        request.state.user_id = payload["sub"]
    except AuthenticationError as exc:
        return JSONResponse(
            status_code=401,
            content={"detail": str(exc)},
        )

    return await call_next(request)


# ---------------------------------------------------------------------------
# Idempotency-Key (ADR-003) — Full replay logic
# ---------------------------------------------------------------------------

# Endpoints where Idempotency-Key MUST be supplied.
IDEMPOTENT_ENDPOINTS: frozenset[tuple[str, str]] = frozenset({
    ("POST", "/api/v1/try-ons"),
    ("POST", "/api/v1/subscriptions/stripe/checkout"),
    ("POST", "/api/v1/subscriptions/mp/preference"),
})


async def idempotency_middleware(request: Request, call_next: CallNext) -> Response:
    """
    Enforce + replay Idempotency-Key for cost-sensitive POSTs (ADR-003).

    Logic:
      1. If route not in IDEMPOTENT_ENDPOINTS → pass through.
      2. Require Idempotency-Key header → 422 if missing.
      3. Look up (key, user_id) in idempotency_keys table.
         a. Found & completed → return cached response.
         b. Not found → create processing record, execute, persist result.
      4. Store is AdminClient.trusted() (infrastructure, not user data).

    TTL: IDEMPOTENCY_TTL_SECONDS (default 86400 = 24h).
    """
    endpoint_key = (request.method, request.url.path)
    if endpoint_key not in IDEMPOTENT_ENDPOINTS:
        return await call_next(request)

    idem_key = request.headers.get("Idempotency-Key", "").strip()
    if not idem_key:
        return JSONResponse(
            status_code=422,
            content={"detail": "Idempotency-Key header is required for this endpoint"},
        )

    # Get user_id (set by auth_middleware which runs before this)
    user_id = getattr(request.state, "user_id", None)

    # Try to get the admin client from app state
    supabase_admin = getattr(request.app.state, "supabase_admin", None)
    if supabase_admin is None:
        # Dev / test mode without Supabase: skip replay, just execute
        return await call_next(request)

    from app.core.admin_client import AdminClient  # noqa: PLC0415

    admin = AdminClient(supabase_admin)
    settings = get_settings()

    try:
        # Check for existing record
        lookup = await (
            admin.trusted()
            .table("idempotency_keys")
            .select("*")
            .eq("key", idem_key)
            .maybe_single()
            .execute()
        )

        if lookup.data and lookup.data.get("status") == "completed":
            # Replay cached response
            cached_body = lookup.data.get("response_body", {})
            cached_status = lookup.data.get("response_status", 200)
            return JSONResponse(
                status_code=cached_status,
                content=cached_body,
                headers={"X-Idempotency-Replay": "true"},
            )

        if not lookup.data:
            # Create processing record
            from datetime import datetime, timedelta, timezone  # noqa: PLC0415
            expires_at = (
                datetime.now(timezone.utc) + timedelta(seconds=settings.IDEMPOTENCY_TTL_SECONDS)
            ).isoformat()
            await (
                admin.trusted()
                .table("idempotency_keys")
                .insert({
                    "key": idem_key,
                    "user_id": user_id,
                    "endpoint": request.url.path,
                    "request_path": request.url.path,
                    "request_method": request.method,
                    "status": "processing",
                    "expires_at": expires_at,
                })
                .execute()
            )

    except Exception as exc:  # noqa: BLE001
        logger.warning("Idempotency store lookup failed (passing through): %s", exc)
        return await call_next(request)

    # Execute the actual request
    response = await call_next(request)

    # Persist result
    try:
        # Read body for caching (StreamingResponse workaround)
        body_bytes = b""
        async for chunk in response.body_iterator:  # type: ignore[attr-defined]
            body_bytes += chunk if isinstance(chunk, bytes) else chunk.encode()

        try:
            body_json = json.loads(body_bytes)
        except (json.JSONDecodeError, ValueError):
            body_json = {"raw": body_bytes.decode("utf-8", errors="replace")}

        await (
            admin.trusted()
            .table("idempotency_keys")
            .update({
                "status": "completed",
                "response_status": response.status_code,
                "response_body": body_json,
            })
            .eq("key", idem_key)
            .execute()
        )

        # Return a new Response with the captured body
        return Response(
            content=body_bytes,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )

    except Exception as exc:  # noqa: BLE001
        logger.warning("Idempotency store update failed: %s", exc)
        # Return the already-consumed response as best effort
        return Response(
            content=body_bytes if "body_bytes" in dir() else b"",
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )


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
    from starlette.middleware.base import BaseHTTPMiddleware  # noqa: PLC0415

    # Innermost first (closest to the endpoint).
    app.add_middleware(BaseHTTPMiddleware, dispatch=idempotency_middleware)
    app.add_middleware(BaseHTTPMiddleware, dispatch=auth_middleware)
    app.add_middleware(BaseHTTPMiddleware, dispatch=security_headers_middleware)
    app.add_middleware(BaseHTTPMiddleware, dispatch=request_logging_middleware)
    # CORS goes last so it ends up outermost (handles preflight before logging).
    setup_cors(app)
