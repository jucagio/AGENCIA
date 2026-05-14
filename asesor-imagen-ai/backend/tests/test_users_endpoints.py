"""
Tests for user endpoints (profile management + account deletion).
"""

from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest

from tests.conftest import AUTH_HEADERS, TEST_USER_ID


def _make_profile(user_id=None):
    uid = user_id or TEST_USER_ID
    return {
        "id": str(uid),
        "first_name": "Alice",
        "last_name": "Smith",
        "preferred_language": "es",
        "notification_preferences": {"push": True, "email": True},
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "deleted_at": None,
        "avatar_url": None,
        "date_of_birth": None,
        "country_code": "CO",
    }


@pytest.mark.anyio
class TestUsersProfile:
    async def test_get_profile_returns_200(self, client, mock_admin_pg) -> None:
        mock_admin_pg.table.return_value.eq.return_value.maybe_single.return_value.execute = AsyncMock(
            return_value=type("R", (), {"data": _make_profile()})()
        )
        resp = await client.get("/api/v1/users/profile", headers=AUTH_HEADERS)
        assert resp.status_code == 200
        data = resp.json()
        assert data["first_name"] == "Alice"

    async def test_get_profile_404_when_missing(self, client, mock_admin_pg) -> None:
        mock_admin_pg.table.return_value.eq.return_value.maybe_single.return_value.execute = AsyncMock(
            return_value=type("R", (), {"data": None})()
        )
        resp = await client.get("/api/v1/users/profile", headers=AUTH_HEADERS)
        assert resp.status_code == 404

    async def test_update_profile_returns_200(self, client, mock_admin_pg) -> None:
        updated = {**_make_profile(), "first_name": "Updated"}
        mock_admin_pg.table.return_value.eq.return_value.upsert.return_value.single.return_value.execute = AsyncMock(
            return_value=type("R", (), {"data": updated})()
        )
        # Also mock the upsert path used by ProfileRepository.upsert_profile
        mock_admin_pg.table.return_value.upsert.return_value.single.return_value.execute = AsyncMock(
            return_value=type("R", (), {"data": updated})()
        )
        resp = await client.put(
            "/api/v1/users/profile",
            headers=AUTH_HEADERS,
            json={"first_name": "Updated"},
        )
        assert resp.status_code == 200

    async def test_profile_requires_auth(self, unauthed_client) -> None:
        resp = await unauthed_client.get("/api/v1/users/profile")
        assert resp.status_code == 401


@pytest.mark.anyio
class TestDeleteAccount:
    async def test_delete_account_returns_204(self, client, mock_admin_pg) -> None:
        # upsert (soft-delete) + httpx call — both mocked
        mock_admin_pg.table.return_value.upsert.return_value.single.return_value.execute = AsyncMock(
            return_value=type("R", (), {"data": _make_profile()})()
        )
        import httpx
        import respx
        with respx.mock:
            respx.delete(
                f"http://testserver/auth/v1/admin/users/{TEST_USER_ID}"
            ).mock(return_value=httpx.Response(204))
            resp = await client.delete("/api/v1/users/account", headers=AUTH_HEADERS)
        assert resp.status_code == 204
