"""
Tests for auth endpoints (register, login, refresh, me).
"""

from __future__ import annotations

from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from tests.conftest import AUTH_HEADERS, TEST_USER_ID


@pytest.mark.anyio
class TestAuthRegister:
    async def test_register_success(self, client) -> None:
        """POST /auth/register with valid data → 201 + TokenResponse."""
        with patch(
            "app.services.auth_service.AuthService.register",
            new_callable=AsyncMock,
        ) as mock_reg:
            from app.schemas.auth import TokenResponse
            mock_reg.return_value = TokenResponse(
                access_token="mock_access",
                refresh_token="mock_refresh",
                expires_in=3600,
                user_id=str(uuid4()),
            )
            resp = await client.post(
                "/api/v1/auth/register",
                json={"email": "new@example.com", "password": "SecurePass123!"},
            )
        assert resp.status_code == 201
        data = resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    async def test_register_invalid_email_422(self, client) -> None:
        resp = await client.post(
            "/api/v1/auth/register",
            json={"email": "not-an-email", "password": "pass123"},
        )
        assert resp.status_code == 422


@pytest.mark.anyio
class TestAuthLogin:
    async def test_login_success(self, client) -> None:
        from app.schemas.auth import TokenResponse
        with patch(
            "app.services.auth_service.AuthService.login",
            new_callable=AsyncMock,
            return_value=TokenResponse(
                access_token="acc", refresh_token="ref", expires_in=3600, user_id=str(uuid4())
            ),
        ):
            resp = await client.post(
                "/api/v1/auth/login",
                json={"email": "user@example.com", "password": "pass"},
            )
        assert resp.status_code == 200
        assert resp.json()["access_token"] == "acc"

    async def test_login_invalid_creds_401(self, client) -> None:
        from app.core.exceptions import AuthenticationError
        with patch(
            "app.services.auth_service.AuthService.login",
            new_callable=AsyncMock,
            side_effect=AuthenticationError("Invalid email or password"),
        ):
            resp = await client.post(
                "/api/v1/auth/login",
                json={"email": "user@example.com", "password": "wrong"},
            )
        assert resp.status_code == 401


@pytest.mark.anyio
class TestAuthRefresh:
    async def test_refresh_success(self, client) -> None:
        from app.schemas.auth import TokenResponse
        with patch(
            "app.services.auth_service.AuthService.refresh",
            new_callable=AsyncMock,
            return_value=TokenResponse(
                access_token="new_acc", refresh_token="new_ref", expires_in=3600, user_id=str(uuid4())
            ),
        ):
            resp = await client.post(
                "/api/v1/auth/refresh",
                json={"refresh_token": "old_refresh"},
            )
        assert resp.status_code == 200
        assert resp.json()["access_token"] == "new_acc"


@pytest.mark.anyio
class TestAuthMe:
    async def test_me_without_token_401(self, unauthed_client) -> None:
        """GET /auth/me without Authorization → 401."""
        resp = await unauthed_client.get("/api/v1/auth/me")
        assert resp.status_code == 401

    async def test_me_with_token_success(self, client, mock_admin_pg) -> None:
        from datetime import datetime, timezone
        profile_data = {
            "id": str(TEST_USER_ID),
            "first_name": "Test",
            "last_name": "User",
            "preferred_language": "es",
            "notification_preferences": {"push": True, "email": True},
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "deleted_at": None,
            "avatar_url": None,
            "date_of_birth": None,
            "country_code": None,
        }
        mock_admin_pg.table.return_value.eq.return_value.maybe_single.return_value.execute = AsyncMock(
            return_value=type("R", (), {"data": profile_data})()
        )
        resp = await client.get("/api/v1/auth/me", headers=AUTH_HEADERS)
        assert resp.status_code == 200

    async def test_me_returns_404_when_profile_missing(self, client, mock_admin_pg) -> None:
        mock_admin_pg.table.return_value.eq.return_value.maybe_single.return_value.execute = AsyncMock(
            return_value=type("R", (), {"data": None})()
        )
        resp = await client.get("/api/v1/auth/me", headers=AUTH_HEADERS)
        assert resp.status_code == 404
