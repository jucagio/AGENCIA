"""
AdminClient wrapper — secure service-role PostgREST client.

Implements the Cyber Neo H3 guard pattern: every call through the admin
client MUST declare whether it is a cross-user operation (and why).

Usage:
    client = AdminClient(postgrest_client, settings)

    # Cross-tenant write — must supply user_id to confirm ownership check:
    result = await (
        client
        .with_user_check(user_id=user_uuid)
        .table("profiles")
        .select("*")
        .eq("id", str(user_uuid))
        .execute()
    )

    # Trusted server operation (webhooks, background jobs):
    result = await (
        client
        .trusted()
        .table("subscriptions")
        .upsert({...})
        .execute()
    )

ADR-001: This wrapper replaces the raw `create_admin_client()` usage so
that callers cannot accidentally bypass the user-ownership guard.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING
from uuid import UUID

from app.core.exceptions import PermissionDeniedError

if TYPE_CHECKING:
    from postgrest import AsyncPostgrestClient

logger = logging.getLogger(__name__)


class _BoundAdminClient:
    """
    An admin client scope that has been explicitly declared safe for use.

    Created by AdminClient.with_user_check() or AdminClient.trusted().
    Exposes the underlying PostgREST client's `table()` method so callers
    can chain queries normally.
    """

    def __init__(
        self,
        pg: "AsyncPostgrestClient",
        *,
        user_id: UUID | None = None,
        trusted: bool = False,
    ) -> None:
        self._pg = pg
        self._user_id = user_id
        self._trusted = trusted

    # ------------------------------------------------------------------
    # PostgREST passthrough
    # ------------------------------------------------------------------

    def table(self, name: str):  # type: ignore[return]
        """Return a query builder for *name*, optionally pre-filtered by user."""
        builder = self._pg.table(name)
        if self._user_id is not None:
            # Automatically scope to the declared user so we can't accidentally
            # return data belonging to another user.
            builder = builder.eq("user_id", str(self._user_id))
        return builder

    def schema(self, schema: str) -> "AsyncPostgrestClient":
        """Switch PostgREST schema (passthrough)."""
        return self._pg.schema(schema)


class AdminClient:
    """
    Cyber Neo H3 guard wrapper around the service-role AsyncPostgrestClient.

    Forces every call to explicitly declare intent, preventing accidental
    RLS bypass or cross-tenant data leaks in application code.

    Attributes:
        _pg: The raw service-role PostgREST client (NEVER expose directly).
    """

    def __init__(self, pg: "AsyncPostgrestClient") -> None:
        self._pg = pg

    # ------------------------------------------------------------------
    # Guard constructors
    # ------------------------------------------------------------------

    def with_user_check(self, *, user_id: UUID) -> _BoundAdminClient:
        """
        Declare that this admin query is scoped to a specific user.

        The returned client will inject `.eq("user_id", <id>)` on every
        `table()` call, ensuring cross-tenant data is never returned.

        Args:
            user_id: The authenticated user's UUID from the JWT.

        Returns:
            A _BoundAdminClient with automatic user_id filter applied.

        Example:
            rows = await (
                admin.with_user_check(user_id=uid)
                .table("wardrobe_items")
                .select("*")
                .execute()
            )
        """
        if not isinstance(user_id, UUID):
            raise TypeError(f"user_id must be a UUID, got {type(user_id)}")
        logger.debug("AdminClient: user-scoped query for user_id=%s", user_id)
        return _BoundAdminClient(self._pg, user_id=user_id)

    def trusted(self) -> _BoundAdminClient:
        """
        Declare that this admin query is a trusted server-side operation.

        Use ONLY for:
          - Stripe / Mercado Pago webhook handlers (signature already verified).
          - ARQ background workers (try-on processing, R2 replication).
          - Audit log writes with no user context.
          - Cross-user analytics (admin panel only).

        Returns:
            A _BoundAdminClient with NO automatic user_id filter.

        Example:
            await (
                admin.trusted()
                .table("subscriptions")
                .upsert(payload)
                .execute()
            )
        """
        logger.debug("AdminClient: trusted (no user filter) operation")
        return _BoundAdminClient(self._pg, trusted=True)

    # ------------------------------------------------------------------
    # Safety: block direct access to the raw client
    # ------------------------------------------------------------------

    def table(self, name: str):  # type: ignore[return]
        """
        Blocked — callers must use .with_user_check() or .trusted() first.

        Raises:
            PermissionDeniedError: always.
        """
        raise PermissionDeniedError(
            "Direct AdminClient.table() access is not allowed. "
            "Use .with_user_check(user_id=...) or .trusted() first."
        )
