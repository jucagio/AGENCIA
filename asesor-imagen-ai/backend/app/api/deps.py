"""
FastAPI dependency providers — Sprint 0.3.

Usage in endpoints:
    from app.api.deps import CurrentUser, get_admin_client

    @router.get("/me")
    async def get_me(user_id: CurrentUser, admin: AdminDep) -> ...:
        ...
"""

from __future__ import annotations

from uuid import UUID

from fastapi import Depends, Request

from app.core.admin_client import AdminClient
from app.core.exceptions import AuthenticationError


def get_current_user_id(request: Request) -> UUID:
    """
    Extract the authenticated user UUID from request state.

    auth_middleware attaches request.state.user_id (str) after validating the
    Supabase JWT. This dependency converts it to a typed UUID.

    Raises:
        AuthenticationError: if the user is not authenticated (middleware bug).
    """
    raw = getattr(request.state, "user_id", None)
    if not raw:
        raise AuthenticationError("User not authenticated")
    try:
        return UUID(str(raw))
    except ValueError as exc:
        raise AuthenticationError("Invalid user identity in token") from exc


def get_admin_client(request: Request) -> AdminClient:
    """
    Provide an AdminClient wrapping the long-lived service-role PostgREST client.

    The raw PostgREST client lives on app.state.supabase_admin (set in lifespan).
    This dependency wraps it in the AdminClient guard so endpoints MUST use
    .with_user_check() or .trusted() — never .table() directly.

    Returns a no-op client in dev/test when Supabase is not configured.
    """
    raw_pg = getattr(request.app.state, "supabase_admin", None)
    return AdminClient(raw_pg)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Typed aliases for use as FastAPI Depends annotations
# ---------------------------------------------------------------------------

from typing import Annotated  # noqa: E402 (must be after function defs)

CurrentUser = Annotated[UUID, Depends(get_current_user_id)]
AdminDep = Annotated[AdminClient, Depends(get_admin_client)]
