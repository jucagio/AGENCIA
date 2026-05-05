"""
Async BaseRepository — the data-access foundation for Sprint 0.2.

Every concrete repository extends this class. It wraps an AdminClient
(service-role PostgREST) and enforces the Cyber Neo H3 guard pattern:
all queries must go through either .with_user_check() or .trusted().

Design decisions:
- Generic[ModelT] keeps concrete repos strongly typed.
- All methods are async (ADR-002).
- user_id is always UUID, never str, to prevent injection mistakes.
- Soft-delete is supported via an optional `deleted_at` column.
- NotFoundError is raised (not None) on get_by_id misses so service
  layers don't need null checks everywhere.

References:
  - ADR-001: Supabase Auth + RLS is auth source of truth.
  - ADR-002: All I/O must be async.
"""

from __future__ import annotations

import logging
from typing import Any, Generic, TypeVar
from uuid import UUID

from app.core.admin_client import AdminClient
from app.core.exceptions import NotFoundError

logger = logging.getLogger(__name__)

ModelT = TypeVar("ModelT")


class BaseRepository(Generic[ModelT]):
    """
    Async repository base class.

    Args:
        admin: AdminClient wrapping the service-role PostgREST client.
        table_name: PostgREST table name (must match the Postgres table).
        model_class: Pydantic model used to parse rows returned by PostgREST.
    """

    def __init__(
        self,
        admin: AdminClient,
        table_name: str,
        model_class: type[ModelT],
    ) -> None:
        self._admin = admin
        self._table = table_name
        self._model = model_class

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _parse(self, row: dict[str, Any]) -> ModelT:
        """Parse a raw PostgREST dict into a typed model instance."""
        return self._model.model_validate(row)  # type: ignore[attr-defined]

    def _parse_many(self, rows: list[dict[str, Any]]) -> list[ModelT]:
        return [self._parse(r) for r in rows]

    # ------------------------------------------------------------------
    # CRUD — user-scoped (RLS-equivalent at app layer)
    # ------------------------------------------------------------------

    async def get_by_id(self, *, user_id: UUID, record_id: UUID) -> ModelT:
        """
        Fetch a single record owned by *user_id*.

        Raises:
            NotFoundError: if the row doesn't exist or belongs to another user.
        """
        response = await (
            self._admin
            .with_user_check(user_id=user_id)
            .table(self._table)
            .select("*")
            .eq("id", str(record_id))
            .maybe_single()
            .execute()
        )
        if response.data is None:
            raise NotFoundError(self._table)
        return self._parse(response.data)

    async def list_for_user(
        self,
        *,
        user_id: UUID,
        page: int = 1,
        per_page: int = 20,
        filters: dict[str, Any] | None = None,
        order_by: str = "created_at",
        ascending: bool = False,
    ) -> tuple[list[ModelT], int]:
        """
        Return a paginated list of records owned by *user_id*.

        Returns:
            (items, total_count)
        """
        offset = (page - 1) * per_page

        # Build base query
        query = (
            self._admin
            .with_user_check(user_id=user_id)
            .table(self._table)
            .select("*", count="exact")
        )

        # Apply extra eq filters
        if filters:
            for col, val in filters.items():
                query = query.eq(col, val)

        # Apply ordering and pagination
        query = (
            query
            .order(order_by, desc=not ascending)
            .range(offset, offset + per_page - 1)
        )

        response = await query.execute()
        total = response.count or 0
        return self._parse_many(response.data or []), total

    async def create(self, *, user_id: UUID, data: dict[str, Any]) -> ModelT:
        """
        Insert a new record owned by *user_id*.

        The user_id is injected into *data* automatically so callers never
        forget to include it.
        """
        payload = {**data, "user_id": str(user_id)}
        response = await (
            self._admin
            .with_user_check(user_id=user_id)
            .table(self._table)
            .insert(payload)
            .single()
            .execute()
        )
        return self._parse(response.data)

    async def update(
        self,
        *,
        user_id: UUID,
        record_id: UUID,
        data: dict[str, Any],
    ) -> ModelT:
        """
        Partial-update a record owned by *user_id*.

        Only non-None values in *data* are sent (patch semantics).

        Raises:
            NotFoundError: if the row doesn't exist or belongs to another user.
        """
        # Strip None values for PATCH semantics
        payload = {k: v for k, v in data.items() if v is not None}
        if not payload:
            # Nothing to update — just return current state
            return await self.get_by_id(user_id=user_id, record_id=record_id)

        response = await (
            self._admin
            .with_user_check(user_id=user_id)
            .table(self._table)
            .update(payload)
            .eq("id", str(record_id))
            .single()
            .execute()
        )
        if response.data is None:
            raise NotFoundError(self._table)
        return self._parse(response.data)

    async def delete(self, *, user_id: UUID, record_id: UUID) -> None:
        """
        Hard-delete a record owned by *user_id*.

        For soft-delete, use soft_delete() instead.

        Raises:
            NotFoundError: if the row doesn't exist or belongs to another user.
        """
        response = await (
            self._admin
            .with_user_check(user_id=user_id)
            .table(self._table)
            .delete()
            .eq("id", str(record_id))
            .execute()
        )
        if not response.data:
            raise NotFoundError(self._table)

    async def soft_delete(self, *, user_id: UUID, record_id: UUID) -> ModelT:
        """
        Set deleted_at = now() on a record owned by *user_id*.

        Requires the table to have a `deleted_at` timestamptz column.

        Raises:
            NotFoundError: if the row doesn't exist or belongs to another user.
        """
        from datetime import datetime, timezone

        return await self.update(
            user_id=user_id,
            record_id=record_id,
            data={"deleted_at": datetime.now(timezone.utc).isoformat()},
        )

    # ------------------------------------------------------------------
    # Trusted server-side operations (webhooks, workers)
    # ------------------------------------------------------------------

    async def trusted_upsert(self, data: dict[str, Any]) -> ModelT:
        """
        Upsert a row without user scoping.

        Use ONLY from webhook handlers and background workers
        where the caller's identity has already been verified.
        """
        response = await (
            self._admin
            .trusted()
            .table(self._table)
            .upsert(data)
            .single()
            .execute()
        )
        return self._parse(response.data)

    async def trusted_get_by_user(self, *, user_id: UUID) -> ModelT | None:
        """
        Fetch a single row by user_id without the ownership double-check.

        Safe for background workers that need to look up any user's row.
        Returns None if not found.
        """
        response = await (
            self._admin
            .trusted()
            .table(self._table)
            .select("*")
            .eq("user_id", str(user_id))
            .maybe_single()
            .execute()
        )
        if response.data is None:
            return None
        return self._parse(response.data)
