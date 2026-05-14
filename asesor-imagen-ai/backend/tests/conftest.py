"""
Test configuration and shared fixtures — Sprint 0.3.

Key design decisions:
  - validate_supabase_token is patched globally so auth_middleware passes in all
    endpoint tests. Tests that specifically test auth behavior unpatch it.
  - AdminClient is mocked per-test (no live Supabase needed).
  - httpx calls (GoTrue, Supabase Auth Admin) use respx for mocking.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient

# Patch validate_supabase_token before importing app so the module-level import
# in middleware.py picks up the mock.
TEST_USER_ID = uuid4()
TEST_USER_PAYLOAD: dict[str, Any] = {
    "sub": str(TEST_USER_ID),
    "role": "authenticated",
    "aud": "authenticated",
    "email": "test@example.com",
}
AUTH_HEADERS = {"Authorization": "Bearer mock.test.token"}


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def mock_validate_token():
    """Patch validate_supabase_token to always return TEST_USER_PAYLOAD."""
    with patch(
        "app.core.supabase_auth.validate_supabase_token",
        return_value=TEST_USER_PAYLOAD,
    ) as m:
        yield m


@pytest.fixture
def mock_admin_pg() -> MagicMock:
    """Mock PostgREST client — returns empty data by default."""
    pg = MagicMock()
    builder = MagicMock()
    for method in (
        "select", "eq", "neq", "in_", "is_", "not_",
        "order", "limit", "range", "single", "maybe_single",
        "insert", "update", "delete", "upsert",
    ):
        getattr(builder, method).return_value = builder

    builder.execute = AsyncMock(return_value=MagicMock(data=None, count=0))
    pg.table.return_value = builder
    pg.schema.return_value = pg
    return pg


@pytest.fixture
async def client(mock_validate_token, mock_admin_pg):
    """
    Async test client with:
      - JWT auth middleware mocked (validate_supabase_token patched)
      - app.state.supabase_admin set to mock_admin_pg
    """
    from app.main import app  # import after patch

    # Inject the mock admin client into app state
    app.state.supabase_admin = mock_admin_pg

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac


@pytest.fixture
async def unauthed_client():
    """Test client WITHOUT auth mock — for testing 401 behavior."""
    from app.main import app

    app.state.supabase_admin = None
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac
