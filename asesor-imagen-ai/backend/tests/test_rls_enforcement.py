"""
RLS enforcement tests — Sprint 0.2 patch.

These tests verify the AdminClient guard pattern (Cyber Neo H3):
  - with_user_check() auto-injects user_id filter → cross-tenant reads return nothing
  - with_user_check(id_column="id") works for tables where PK == user id (profiles)
  - direct AdminClient.table() access raises PermissionDeniedError
  - trusted() allows cross-user operations (webhook context)
  - BaseRepository CRUD methods enforce ownership via with_user_check()
  - [M1] _BoundAdminClient.schema() preserves guard state
  - [H5] ProfileRepository uses id_column="id" guard
  - [H6] RecommendationItemRepository verifies parent ownership before acting
  - [L1] UsageCounterRepository.increment handles concurrent calls

All tests use unittest.mock — no live Supabase connection required.
Coverage target: 80%+ across app/core/admin_client.py + app/repositories/

Run:
    pytest tests/test_rls_enforcement.py -v --cov=app
"""

from __future__ import annotations

import asyncio
from typing import Any
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4

import pytest
from pydantic import BaseModel, ConfigDict

from app.core.admin_client import AdminClient, _BoundAdminClient
from app.core.exceptions import NotFoundError, PermissionDeniedError
from app.repositories.base import BaseRepository
from app.repositories.repos import (
    ProfileRepository,
    RecommendationItemRepository,
    UsageCounterRepository,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

USER_A = uuid4()
USER_B = uuid4()
RECORD_ID = uuid4()
RECO_ID = uuid4()


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
        admin.with_user_check(user_id=USER_A).table("wardrobe_items")

        # Verify the builder had user_id injected (default column = "user_id")
        builder.eq.assert_called_once_with("user_id", str(USER_A))

    def test_with_user_check_custom_id_column(self):
        """
        [H5] with_user_check(id_column="id") must inject .eq("id", str(user_id))
        on the builder — used by ProfileRepository where PK == user_id.
        """
        builder = MagicMock()
        builder.eq.return_value = builder

        pg = MagicMock()
        pg.table.return_value = builder

        admin = AdminClient(pg)
        admin.with_user_check(user_id=USER_A, id_column="id").table("profiles")

        builder.eq.assert_called_once_with("id", str(USER_A))

    def test_trusted_does_not_inject_user_id_filter(self):
        """trusted().table() must NOT call .eq("user_id", ...) on the builder."""
        builder = MagicMock()
        pg = MagicMock()
        pg.table.return_value = builder

        admin = AdminClient(pg)
        admin.trusted().table("subscriptions")

        builder.eq.assert_not_called()


# ---------------------------------------------------------------------------
# [M1] schema() guard preservation tests
# ---------------------------------------------------------------------------


class TestAdminClientSchemaGuard:
    """
    [M1] _BoundAdminClient.schema() must return a new _BoundAdminClient that
    preserves user_id and trusted flags — not a raw AsyncPostgrestClient.
    """

    def test_schema_on_user_check_returns_bound_client(self):
        pg = MagicMock()
        pg.schema.return_value = MagicMock()

        admin = AdminClient(pg)
        bound = admin.with_user_check(user_id=USER_A)
        result = bound.schema("custom_schema")

        assert isinstance(result, _BoundAdminClient), (
            "schema() must return _BoundAdminClient, not raw pg client"
        )

    def test_schema_preserves_user_id(self):
        """After .schema(), the user_id filter must still be applied on .table()."""
        inner_builder = MagicMock()
        inner_builder.eq.return_value = inner_builder

        switched_pg = MagicMock()
        switched_pg.table.return_value = inner_builder

        pg = MagicMock()
        pg.schema.return_value = switched_pg

        admin = AdminClient(pg)
        admin.with_user_check(user_id=USER_A).schema("other").table("wardrobe_items")

        inner_builder.eq.assert_called_once_with("user_id", str(USER_A))

    def test_schema_on_trusted_returns_bound_client(self):
        pg = MagicMock()
        pg.schema.return_value = MagicMock()

        admin = AdminClient(pg)
        result = admin.trusted().schema("analytics")

        assert isinstance(result, _BoundAdminClient)

    def test_schema_on_trusted_no_user_filter(self):
        """schema() on a trusted client must still not inject user_id."""
        inner_builder = MagicMock()
        switched_pg = MagicMock()
        switched_pg.table.return_value = inner_builder
        pg = MagicMock()
        pg.schema.return_value = switched_pg

        admin = AdminClient(pg)
        admin.trusted().schema("analytics").table("audit_log")

        inner_builder.eq.assert_not_called()


# ---------------------------------------------------------------------------
# Cross-tenant isolation tests (two users, RLS at app layer)
# ---------------------------------------------------------------------------


class TestCrossTenantIsolation:
    """
    Verify that a record belonging to USER_A is unreachable when querying
    as USER_B, even through the AdminClient (service-role).
    """

    @pytest.mark.anyio
    async def test_get_by_id_raises_not_found_for_wrong_user(self):
        """
        Simulates: USER_B tries to read USER_A's record.
        PostgREST returns empty (user_id filter excluded it).
        BaseRepository must raise NotFoundError, NOT return USER_A's data.
        """
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


# ---------------------------------------------------------------------------
# [H5] ProfileRepository — id_column="id" guard
# ---------------------------------------------------------------------------


class TestProfileRepositoryIdColumn:
    """ProfileRepository must scope queries using column 'id', not 'user_id'."""

    @pytest.mark.anyio
    async def test_get_profile_uses_id_column(self):
        """get_profile must inject .eq('id', user_id) not .eq('user_id', ...)."""
        from datetime import datetime, timezone

        profile_row = {
            "id": str(USER_A),
            "first_name": "Alice",
            "last_name": "Smith",
            "preferred_language": "es",
            "notification_preferences": {"push": True, "email": True},
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "deleted_at": None,
            "avatar_url": None,
            "date_of_birth": None,
            "country_code": None,
        }

        response = make_postgrest_response(data=profile_row)
        builder = make_pg_chain(response)
        pg = MagicMock()
        pg.table.return_value = builder
        admin = AdminClient(pg)

        repo = ProfileRepository(admin)
        result = await repo.get_profile(user_id=USER_A)

        # The first .eq() call on the builder must use "id", not "user_id"
        first_eq_call = builder.eq.call_args_list[0]
        assert first_eq_call.args[0] == "id", (
            f"ProfileRepository must use id_column='id', got '{first_eq_call.args[0]}'"
        )
        assert result is not None

    @pytest.mark.anyio
    async def test_upsert_profile_no_spurious_user_id_key(self):
        """upsert_profile must NOT inject a 'user_id' key into the payload."""
        from datetime import datetime, timezone

        profile_row = {
            "id": str(USER_A),
            "first_name": "Bob",
            "last_name": None,
            "preferred_language": "es",
            "notification_preferences": {"push": True, "email": True},
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "deleted_at": None,
            "avatar_url": None,
            "date_of_birth": None,
            "country_code": None,
        }

        response = make_postgrest_response(data=profile_row)
        builder = make_pg_chain(response)
        pg = MagicMock()
        pg.table.return_value = builder
        admin = AdminClient(pg)

        repo = ProfileRepository(admin)
        await repo.upsert_profile(user_id=USER_A, data={"first_name": "Bob"})

        # Inspect the payload passed to .upsert()
        upsert_call = builder.upsert.call_args
        assert upsert_call is not None
        payload = upsert_call.args[0]
        assert "id" in payload, "upsert payload must contain 'id'"
        assert "user_id" not in payload, (
            "upsert payload must NOT contain spurious 'user_id' "
            "(profiles table has no user_id column)"
        )


# ---------------------------------------------------------------------------
# [H6] RecommendationItemRepository — ownership verification
# ---------------------------------------------------------------------------


class TestRecommendationItemOwnership:
    """
    [H6] list_for_recommendation and bulk_create must verify parent ownership.
    """

    def _make_reco_item_repo(self, verify_response, items_response=None):
        """
        Build a RecommendationItemRepository whose mock returns:
          - verify_response: for the ownership verification query
          - items_response: for the actual items query
        """
        verify_resp = make_postgrest_response(data=verify_response)
        verify_builder = make_pg_chain(verify_resp)

        pg = MagicMock()

        if items_response is not None:
            items_resp = make_postgrest_response(data=items_response)
            items_builder = make_pg_chain(items_resp)
            # First call to pg.table is verification, second is item fetch
            pg.table.side_effect = [verify_builder, items_builder]
        else:
            pg.table.return_value = verify_builder

        return RecommendationItemRepository(AdminClient(pg))

    @pytest.mark.anyio
    async def test_list_raises_not_found_when_reco_belongs_to_other_user(self):
        """USER_B cannot list items from USER_A's recommendation."""
        repo = self._make_reco_item_repo(verify_response=None)

        with pytest.raises(NotFoundError):
            await repo.list_for_recommendation(
                user_id=USER_B, recommendation_id=RECO_ID
            )

    @pytest.mark.anyio
    async def test_bulk_create_raises_not_found_when_reco_belongs_to_other_user(self):
        """USER_B cannot add items to USER_A's recommendation."""
        repo = self._make_reco_item_repo(verify_response=None)

        with pytest.raises(NotFoundError):
            await repo.bulk_create(
                user_id=USER_B,
                recommendation_id=RECO_ID,
                items=[{"wardrobe_item_id": str(uuid4()), "position": 1}],
            )

    @pytest.mark.anyio
    async def test_list_succeeds_when_reco_is_owned(self):
        """list_for_recommendation returns items when ownership check passes."""
        from app.models.recommendation import RecommendationItem

        verify_row = {"id": str(RECO_ID)}
        item_row = {
            "recommendation_id": str(RECO_ID),
            "wardrobe_item_id": str(uuid4()),
            "position": 1,
            "role": "top",
        }

        repo = self._make_reco_item_repo(
            verify_response=verify_row,
            items_response=[item_row],
        )

        items = await repo.list_for_recommendation(
            user_id=USER_A, recommendation_id=RECO_ID
        )
        assert len(items) == 1
        assert isinstance(items[0], RecommendationItem)


# ---------------------------------------------------------------------------
# [L1] UsageCounterRepository — concurrent increment safety
# ---------------------------------------------------------------------------


class TestUsageCounterConcurrency:
    """
    [L1] increment() must be safe for concurrent callers.
    Since we mock PostgREST, we verify that 10 concurrent calls all
    succeed and each resolves to the expected model (no exceptions).
    The actual atomicity guarantee comes from the stored procedure in the DB.
    """

    @pytest.mark.anyio
    async def test_concurrent_increments_all_succeed(self):
        """10 concurrent increments must all complete without exceptions."""
        from datetime import date

        from app.models.usage_counter import UsageCounter

        counter_row = {
            "user_id": str(USER_A),
            "period_start": date.today().replace(day=1).isoformat(),
            "try_ons_used": 10,
            "recommendations_used": 0,
            "body_analyses_used": 0,
        }

        # Each call gets its own builder mock to simulate concurrent execution
        def make_repo():
            response = make_postgrest_response(data=counter_row)
            builder = make_pg_chain(response)
            pg = MagicMock()
            pg.table.return_value = builder
            return UsageCounterRepository(AdminClient(pg))

        results = await asyncio.gather(
            *[
                make_repo().increment(user_id=USER_A, field="try_ons_used")
                for _ in range(10)
            ]
        )

        assert len(results) == 10
        for result in results:
            assert isinstance(result, UsageCounter)
            assert result.try_ons_used == 10  # reflects mocked DB response

    def test_increment_rejects_invalid_field(self):
        """increment() must raise ValueError for unlisted field names."""
        pg = MagicMock()
        repo = UsageCounterRepository(AdminClient(pg))

        with pytest.raises(ValueError, match="field must be one of"):
            # Not awaited — ValueError is raised synchronously before any I/O
            coro = repo.increment(user_id=USER_A, field="quota_bypass_attempt")
            # Trigger the coroutine to hit the validation line
            try:
                coro.send(None)
            except StopIteration:
                pass
            except ValueError:
                raise  # re-raise so pytest.raises catches it
            finally:
                coro.close()
