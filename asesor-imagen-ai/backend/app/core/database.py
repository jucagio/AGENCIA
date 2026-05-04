"""
Supabase client initialization (async-first).

Per ADR-001 (Alejo): Supabase Auth nativo + RLS. FastAPI uses two clients:
  1. anon client  — bound to the user's JWT (RLS enforced as that user).
  2. service client — bypasses RLS for trusted server-side operations
                      (webhooks, background workers, audit log writes).

Per ADR-002: All DB access from request handlers must be async to avoid
blocking the event loop while we await Replicate / Anthropic calls.

We use `postgrest-py` directly instead of the full `supabase-py` package
to avoid the `pyiceberg` dependency which breaks installation on Windows.

Lifespan ownership:
    - Service client is initialized once on app startup and stored on
      app.state.supabase_admin (see main.py lifespan).
    - Per-request user-scoped clients are created on demand by a FastAPI
      dependency (added in Entrega 0.2 alongside auth middleware).

References:
    - https://supabase.com/docs/reference/python/introduction
    - https://github.com/supabase-community/postgrest-py
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from app.config import Settings, get_settings

if TYPE_CHECKING:
    # Type-only import to avoid hard runtime dep before requirements are pinned.
    from postgrest import AsyncPostgrestClient

logger = logging.getLogger(__name__)


class SupabaseClientError(RuntimeError):
    """Raised when Supabase client initialization fails."""


async def create_admin_client(settings: Settings | None = None) -> "AsyncPostgrestClient":
    """Create the long-lived service-role async Supabase client.

    Used for trusted server-side operations only:
      - Stripe / Mercado Pago webhook handlers (verifying & writing payments).
      - ARQ background workers (try-on processing, R2 replication).
      - Audit log writes that bypass RLS.

    NEVER expose this client's responses directly to end users — always
    re-check ownership at the application layer.

    Raises:
        SupabaseClientError: if SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY missing.
    """
    settings = settings or get_settings()

    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_ROLE_KEY:
        # In dev we let the app boot without Supabase to allow local FastAPI
        # iteration. assert_production_ready() blocks this in prod.
        if settings.is_production:
            raise SupabaseClientError(
                "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required in production"
            )
        logger.warning(
            "Supabase admin client not initialized — SUPABASE_URL or SERVICE_ROLE_KEY empty. "
            "DB operations will fail until configured. (OK in early dev.)"
        )
        return None  # type: ignore[return-value]

    # Lazy import keeps the test suite green even if postgrest isn't installed yet.
    from postgrest import AsyncPostgrestClient  # type: ignore[import-not-found]

    client = AsyncPostgrestClient(
        f"{settings.SUPABASE_URL}/rest/v1",
        headers={
            "apikey": settings.SUPABASE_SERVICE_ROLE_KEY,
            "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY}",
        }
    )
    logger.info("Supabase admin (service-role) client initialized via postgrest")
    return client


async def create_user_scoped_client(
    user_jwt: str,
    settings: Settings | None = None,
) -> "AsyncPostgrestClient":
    """Create a per-request Supabase client bound to a user's JWT.

    The returned client makes all PostgREST calls as that user, so
    Postgres RLS policies enforce isolation automatically.

    Wired up by the auth dependency in Entrega 0.2:
        async def get_supabase_user(
            credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        ) -> AsyncPostgrestClient:
            return await create_user_scoped_client(credentials.credentials)

    Args:
        user_jwt: The Supabase access token from the Authorization header.
        settings: Optional override (testing).

    Raises:
        SupabaseClientError: if SUPABASE_URL or SUPABASE_ANON_KEY missing.
    """
    settings = settings or get_settings()

    if not settings.SUPABASE_URL or not settings.SUPABASE_ANON_KEY:
        raise SupabaseClientError(
            "SUPABASE_URL and SUPABASE_ANON_KEY must be configured"
        )

    from postgrest import AsyncPostgrestClient  # type: ignore[import-not-found]

    client = AsyncPostgrestClient(
        f"{settings.SUPABASE_URL}/rest/v1",
        headers={
            "apikey": settings.SUPABASE_ANON_KEY,
        }
    )
    # Bind the user's JWT so RLS uses auth.uid() = <this user>.
    client.auth(user_jwt)
    return client
