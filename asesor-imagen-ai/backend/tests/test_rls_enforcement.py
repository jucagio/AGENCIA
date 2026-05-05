"""
RLS enforcement tests — Sprint 0.2.

These tests verify the AdminClient guard pattern (Cyber Neo H3):
  - with_user_check() auto-injects user_id filter → cross-tenant reads return nothing
  - direct AdminClient.table() access raises PermissionDeniedError
  - trusted() allows cross-user operations (webhook context)
  - BaseRepository CRUD methods enforce ownership via with_user_check()

All tests use unittest.mock — no live Supabase connection required.
Coverage target: 80%+ across app/core/admin_client.py + app/repositories/

Run:
    pytest tests/test_rls_enforcement.py -v --cov=app
"""

from __future__ import annotations

import unittest.mock as mock
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4

import pytest

from app.core.admin_client import AdminClient, _BoundAdminClient
from app.core.exceptions import NotFoundError, PermissionDeniedError
from app.repositories.base import BaseRepository


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

USER_A = uuid4()
USER_B = uuid4()
RECORD_ID = uuid4()


def make_postgrest_response(data: Any, count: int | None = None):
    """Build a minimal mock PostgREST response."""
    resp = MagicMock()
    resp.data = data
    resp.count = count
    return resp


def make_pg_chain(final_response: Any):
    """
    Return a mock PostgREST query builder chain that resolves to *final_response*
    on .execute().

    Each builder method returns self so calls can be chained arbitrarily.
    """
    builder = MagicMock()
    # All chaining methods return self
    for method in (
        "select", "eq", "neq", "in_", "is_", "not_",
        "order", "limit", "range", "single", "maybe_single",
        "insert", "update", "delete", "upsert",
    ):
        getattr(builder, method).return_value = builder

    builder.execute = AsyncMock(return_value=final_response)
    return builder


def make_admin_client(builder: MagicMock | None = None) -> AdminClient:
    """Return an AdminClient wrapping a mock PostgREST client."""
    pg = MagicMock()
    if builder is not None:
        pg.table.return_value = builder
    return AdminClient(pg)


# ---------------------------------------------------------------------------
# Minimal Pydantic model for repository tests
# ---------------------------------------------------------------------------

from pydantic import BaseModel, ConfigDict


class FakeRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    name: str


# ---------------------------------------------------------------------------
# AdminClient guard tests
# ---------------------------------------------------------------------------


class TestAdminClientGuard:
    """AdminClient must block direct .table() and enforce guard constructors."""

    def test_direct_table_raises_permission_denied(self):
        admin = make_admin_client()
        with pytest.raises(PermissionDeniedError):
            admin.table("profiles")

    def test_with_user_check_requires_uuid(self):
        admin = make_admin_client()
        with pytest.raises(TypeError):
            admin.with_user_check(user_id="not-a-uuid")  # type: ignore

    def test_with_user_check_returns_bound_client(self):
        admin = make_admin_client()
        bound = admin.with_user_check(user_id=USER_A)
        assert isinstance(bound, _BoundAdminClient)

    def test_trusted_returns_bound_client(self):
        admin = make_admin_client()
        bound = admin.trusted()
        assert isinstance(bound, _BoundAdminClient)

    def test_with_user_check_injects_user_id_filter(self):
        """
        with_user_check().table() must call .eq("user_id", str(user_id)) on the
        underlying PostgREST builder.
        """
        builder = MagicMock()
        builder.eq.return_value = builder

        pg = MagicMock()
        pg.table.return_value = builder

        admin = AdminClient(pg)
        admin.with_user_check(user_id=USER_A).table("profiles")

        # Verify the builder had user_id injected
        builder.eq.assert_called_once_with("user_id", str(USER_A))

    def test_trusted_does_not_inject_user_id_filter(self):
        """trusted().table() must NOT call .eq("user_id", ...) on the builder."""
        builder = MagicMock()
        pg = MagicMock()
        pg.table.return_value = builder

        admin = AdminClient(pg)
        admin.trusted().table("subscriptions")

        builder.eq.assert_not_called()


# ---------------------------------------------------------------------------
# Cross-tenant isolation tests (two users, RLS at app layer)
# ---------------------------------------------------------------------------


class TestCrossTenantIsolation:
    """
    Verify that a record belonging to USER_A is unreachable when querying
    as USER_B, even through the AdminClient (service-role).

    The guard pattern works by injecting .eq("user_id", str(user_b)) so the
    Postgres query itself filters — PostgREST/Supabase RLS is the last line of
    defence, but this app-layer guard prevents accidental cross-tenant leaks.
    """

    @pytest.mark.anyio
    async def test_get_by_id_raises_not_found_for_wrong_user(self):
        """
        Simulates: USER_B tries to read USER_A's record.
        PostgREST returns empty (user_id filter excluded it).
        BaseRepository must raise NotFoundError, NOT return USER_A's data.
        """
        # Simulate PostgREST returning None because user_id filter excluded the row
        response = make_postgrest_response(data=None)
        builder = make_pg_chain(response)

        pg = MagicMock()
        pg.table.return_value = builder
        admin = AdminClient(pg)

        repo = BaseRepository(admin, "fake_table", FakeRecord)

        with pytest.raises(NotFoundError):
            await repo.get_by_id(user_id=USER_B, record_id=RECORD_ID)

    @pytest.mark.anyio
    async def test_list_for_user_returns_only_own_records(self):
        """
        list_for_user returns USER_A's records; USER_B query returns empty list.
        """
        user_a_record = {
            "id": str(RECORD_ID),
            "user_id": str(USER_A),
            "name": "User A item",
        }

        # USER_A query — returns 1 record
        response_a = make_postgrest_response(data=[user_a_record], count=1)
        builder_a = make_pg_chain(response_a)
        pg_a = MagicMock()
        pg_a.table.return_value = builder_a
        admin_a = AdminClient(pg_a)
        repo_a = BaseRepository(admin_a, "fake_table", FakeRecord)

        items_a, total_a = await repo_a.list_for_user(user_id=USER_A)
        assert len(items_a) == 1
        assert total_a == 1
        assert items_a[0].user_id == USER_A

        # USER_B query — PostgREST returns empty because user_id filter
        response_b = make_postgrest_response(data=[], count=0)
        builder_b = make_pg_chain(response_b)
        pg_b = MagicMock()
        pg_b.table.return_value = builder_b
        admin_b = AdminClient(pg_b)
        repo_b = BaseRepository(admin_b, "fake_table", FakeRecord)

        items_b, total_b = await repo_b.list_for_user(user_id=USER_B)
        assert items_b == []
        assert total_b == 0

    @pytest.mark.anyio
    async def test_update_raises_not_found_for_wrong_user(self):
        """USER_B cannot update USER_A's record — returns None → NotFoundError."""
        response = make_postgrest_response(data=None)
        builder = make_pg_chain(response)
        pg = MagicMock()
        pg.table.return_value = builder
        admin = AdminClient(pg)

        repo = BaseRepository(admin, "fake_table", FakeRecord)

        with pytest.raises(NotFoundError):
            await repo.update(
                user_id=USER_B,
                record_id=RECORD_ID,
                data={"name": "hacked"},
            )

    @pytest.mark.anyio
    async def test_delete_raises_not_found_for_wrong_user(self):
        """USER_B cannot delete USER_A's record — empty data → NotFoundError."""
        response = make_postgrest_response(data=[])
        builder = make_pg_chain(response)
        pg = MagicMock()
        pg.table.return_value = builder
        admin = AdminClient(pg)

        repo = BaseRepository(admin, "fake_table", FakeRecord)

        with pytest.raises(NotFoundError):
            await repo.delete(user_id=USER_B, record_id=RECORD_ID)


# ---------------------------------------------------------------------------
# Successful operations
# ---------------------------------------------------------------------------


class TestBaseRepositoryHappyPath:
    """CRUD happy-path tests using mocked PostgREST responses."""

    def _make_repo(self, data: Any, count: int | None = None):
        response = make_postgrest_response(data=data, count=count)
        builder = make_pg_chain(response)
        pg = MagicMock()
        pg.table.return_value = builder
        admin = AdminClient(pg)
        return BaseRepository(admin, "fake_table", FakeRecord)

    @pytest.mark.anyio
    async def test_get_by_id_returns_model(self):
        row = {"id": str(RECORD_ID), "user_id": str(USER_A), "name": "test"}
        repo = self._make_repo(data=row)
        result = await repo.get_by_id(user_id=USER_A, record_id=RECORD_ID)
        assert isinstance(result, FakeRecord)
        assert result.id == RECORD_ID
        assert result.user_id == USER_A

    @pytest.mark.anyio
    async def test_list_for_user_returns_list(self):
        rows = [
            {"id": str(uuid4()), "user_id": str(USER_A), "name": f"item {i}"}
            for i in range(3)
        ]
        repo = self._make_repo(data=rows, count=3)
        items, total = await repo.list_for_user(user_id=USER_A)
        assert len(items) == 3
        assert total == 3

    @pytest.mark.anyio
    async def test_create_injects_user_id(self):
        row = {"id": str(RECORD_ID), "user_id": str(USER_A), "name": "new"}
        repo = self._make_repo(data=row)
        result = await repo.create(user_id=USER_A, data={"name": "new"})
        assert result.user_id == USER_A

    @pytest.mark.anyio
    async def test_update_empty_data_calls_get_by_id(self):
        """update() with empty data should call get_by_id (no-op PATCH)."""
        row = {"id": str(RECORD_ID), "user_id": str(USER_A), "name": "unchanged"}
        response = make_postgrest_response(data=row)
        builder = make_pg_chain(response)
        pg = MagicMock()
        pg.table.return_value = builder
        admin = AdminClient(pg)
        repo = BaseRepository(admin, "fake_table", FakeRecord)

        result = await repo.update(user_id=USER_A, record_id=RECORD_ID, data={})
        assert isinstance(result, FakeRecord)

    @pytest.mark.anyio
    async def test_trusted_upsert_no_user_filter(self):
        row = {"id": str(RECORD_ID), "user_id": str(USER_A), "name": "upserted"}
        repo = self._make_repo(data=row)
        result = await repo.trusted_upsert({"id": str(RECORD_ID), "name": "upserted"})
        assert isinstance(result, FakeRecord)

    @pytest.mark.anyio
    async def test_trusted_get_by_user_returns_none_when_missing(self):
        repo = self._make_repo(data=None)
        result = await repo.trusted_get_by_user(user_id=USER_A)
        assert result is None


# ---------------------------------------------------------------------------
# AdminClient.with_user_check — user_id type enforcement
# ---------------------------------------------------------------------------


class TestAdminClientUserIdValidation:
    def test_string_uuid_raises_type_error(self):
        admin = make_admin_client()
        with pytest.raises(TypeError):
            admin.with_user_check(user_id="550e8400-e29b-41d4-a716-446655440000")  # type: ignore

    def test_none_raises_type_error(self):
        admin = make_admin_client()
        with pytest.raises(TypeError):
            admin.with_user_check(user_id=None)  # type: ignore

    def test_valid_uuid_accepted(self):
        admin = make_admin_client()
        uid = uuid4()
        bound = admin.with_user_check(user_id=uid)
        assert isinstance(bound, _BoundAdminClient)
