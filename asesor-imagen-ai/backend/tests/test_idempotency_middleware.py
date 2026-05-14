"""Tests for idempotency middleware."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from tests.conftest import AUTH_HEADERS


@pytest.mark.anyio
class TestIdempotencyMiddleware:
    async def test_missing_key_on_idempotent_endpoint_422(self, client) -> None:
        _params = {
            "wardrobe_item_id": "00000000-0000-0000-0000-000000000000",
            "body_analysis_id": "00000000-0000-0000-0000-000000000000",
        }
        resp = await client.post("/api/v1/try-ons", headers=AUTH_HEADERS, params=_params)
        assert resp.status_code == 422
        assert "Idempotency-Key header is required" in resp.json()["detail"]

    async def test_replay_cached_response(self, client, mock_admin_pg) -> None:
        _cached = {"status": "completed", "response_status": 202, "response_body": {"cached": True}}
        _chain = mock_admin_pg.table.return_value.select.return_value.eq.return_value.maybe_single.return_value
        _chain.execute = AsyncMock(return_value=type("R", (), {"data": _cached})())
        _params = {
            "wardrobe_item_id": "00000000-0000-0000-0000-000000000000",
            "body_analysis_id": "00000000-0000-0000-0000-000000000000",
        }
        resp = await client.post(
            "/api/v1/try-ons",
            headers={**AUTH_HEADERS, "Idempotency-Key": "cached-key"},
            params=_params,
        )
        assert resp.status_code == 202
        assert resp.json() == {"cached": True}
        assert resp.headers.get("X-Idempotency-Replay") == "true"
