"""
AdminClient wrapper — secure service-role PostgREST client.

Implements the Cyber Neo H3 guard pattern: every call through the admin
client MUST declare whether it is a cross-user operation (and why).

Usage:
    client = AdminClient(postgrest_client, settings)

    # Cross-tenant write — must supply user_id to confirm ownership check.
    # For most tables the ownership column is "user_id" (default).
    # For the "profiles" table the PK *is* the user id (column "id"):
    result = await (
        client
        .with_user_check(user_id=user_uuid, id_column="id")
        .table("profiles")
        .select("*")
        .execute()
    )

    # Standard user-scoped table (default id_column="user_id"):
    result = await (
        client
        .with_user_check(user_id=user_uuid)
        .table("wardrobe_items")
        .select("*")
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

Security notes:
  - [M1] _BoundAdminClient.schema() returns a new _BoundAdminClient so
    the user_id / trusted flags are NOT lost when switching schemas.
  - [H5] id_column param lets ProfileRepository (id == user_id PK) share
    the same guard as tables that have a separate user_id FK column.
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

    Attributes:
        _pg: The underlying AsyncPostgrestClient (may be schema-switched).
        _user_id: UUID of the declared user, or None for trusted contexts.
        _id_column: Column name used to filter by user identity (default "user_id").
        _trusted: True when created via AdminClient.trusted().
    """

    def __init__(
        self,
        pg: "AsyncPostgrestClient",
        *,
        user_id: UUID | None = None,
        id_column: str = "user_id",
        trusted: bool = False,
    ) -> None:
        self._pg = pg
        self._user_id = user_id
        self._id_column = id_column
        self._trusted = trusted

    # ------------------------------------------------------------------
    # PostgREST passthrough
    # ------------------------------------------------------------------

    def table(self, name: str):  # type: ignore[return]
        """Return a query builder for *name*, optionally pre-filtered by user.

        If this client was created via with_user_check(), the builder will
        automatically have .eq(id_column, str(user_id)) applied so callers
        cannot accidentally return data belonging to another user.
        """
        builder = self._pg.table(name)
        if self._user_id is not None:
            builder = builder.eq(self._id_column, str(self._user_id))
        return builder

    def schema(self, schema_name: str) -> "_BoundAdminClient":
        """
        Switch PostgREST schema, preserving user_id / trusted guard state.

        [M1 fix] Returns a NEW _BoundAdminClient wrapping the schema-switched
        client — the original guard flags (user_id, id_column, trusted) are
        carried forward so the guard CANNOT be bypassed by calling .schema().
        """
        switched_pg = self._pg.schema(schema_name)
        return _BoundAdminClient(
            switched_pg,
            user_id=self._user_id,
            id_column=self._id_column,
            trusted=self._trusted,
        )


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

    def with_user_check(
        self,
        *,
        user_id: UUID,
        id_column: str = "user_id",
    ) -> _BoundAdminClient:
        """
        Declare that this admin query is scoped to a specific user.

        The returned client will inject `.eq(id_column, <id>)` on every
        `table()` call, ensuring cross-tenant data is never returned.

        Args:
            user_id: The authenticated user's UUID from the JWT.
            id_column: Column name that holds the user identity.
                - Default "user_id" for most tables (FK to auth.users).
                - Use "id" for the `profiles` table where the PK IS the
                  user id (no separate user_id FK column exists).

        Returns:
            A _BoundAdminClient with automatic id_column filter applied.

        Examples:
            # Standard table with user_id FK:
            rows = await (
                admin.with_user_check(user_id=uid)
                .table("wardrobe_items")
                .select("*")
                .execute()
            )

            # profiles table — PK is the user id:
            row = await (
                admin.with_user_check(user_id=uid, id_column="id")
                .table("profiles")
                .select("*")
                .execute()
            )
        """
        if not isinstance(user_id, UUID):
            raise TypeError(f"user_id must be a UUID, got {type(user_id)}")
        logger.debug(
            "AdminClient: user-scoped query for user_id=%s id_column=%s",
            user_id,
            id_column,
        )
        return _BoundAdminClient(self._pg, user_id=user_id, id_column=id_column)

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
