"""Tests for try-on endpoints — including idempotency (ADR-003)."""
from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from tests.conftest import AUTH_HEADERS, TEST_USER_ID


def _make_try_on(tid=None):
    return {
        "id": str(tid or uuid4()), "user_id": str(TEST_USER_ID),
        "wardrobe_item_id": str(uuid4()), "body_analysis_id": str(uuid4()),
        "content_hash": "a" * 64, "cache_hit": False,
        "replicate_model_version": None, "replicate_prediction_id": None,
        "inference_time_ms": None, "status": "pending",
        "result_image_url": None, "result_storage_path": None,
        "result_cdn_url": None, "error_message": None,
        "confidence_score": None, "user_rating": None, "fit_feedback": None,
        "color_feedback": None, "occasion_fit": None, "would_buy": None,
        "liked": False, "view_duration_seconds": None, "shared": False,
        "saved_at": None,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "completed_at": None, "updated_at": datetime.now(timezone.utc).isoformat(),
    }


@pytest.mark.anyio
class TestTryOnCreate:
    async def test_missing_idempotency_key_returns_422(self, client) -> None:
        resp = await client.post(
            "/api/v1/try-ons",
            headers=AUTH_HEADERS,
            params={"wardrobe_item_id": str(uuid4()), "body_analysis_id": str(uuid4())},
        )
        assert resp.status_code == 422

    async def test_create_with_key_returns_202(self, client) -> None:
        tid = uuid4()
        with patch(
            "app.services.try_on_service.TryOnService.create_try_on",
            new_callable=AsyncMock,
            return_value={"try_on_id": str(tid), "status": "pending", "cache_hit": False, "estimated_seconds": 30},
        ):
            resp = await client.post(
                "/api/v1/try-ons",
                headers={**AUTH_HEADERS, "Idempotency-Key": "idem-key-1"},
                params={"wardrobe_item_id": str(uuid4()), "body_analysis_id": str(uuid4())},
            )
        assert resp.status_code == 202
        assert resp.json()["status"] == "pending"

    async def test_requires_auth(self, unauthed_client) -> None:
        resp = await unauthed_client.post("/api/v1/try-ons",
            params={"wardrobe_item_id": str(uuid4()), "body_analysis_id": str(uuid4())})
        assert resp.status_code == 401


@pytest.mark.anyio
class TestTryOnGet:
    async def test_get_returns_200(self, client, mock_admin_pg) -> None:
        tid = uuid4()
        mock_admin_pg.table.return_value.eq.return_value.maybe_single.return_value.execute = AsyncMock(
            return_value=type("R", (), {"data": _make_try_on(tid)})()
        )
        resp = await client.get(f"/api/v1/try-ons/{tid}", headers=AUTH_HEADERS)
        assert resp.status_code == 200


@pytest.mark.anyio
class TestTryOnFeedback:
    async def test_feedback_returns_200(self, client, mock_admin_pg) -> None:
        tid = uuid4()
        mock_admin_pg.table.return_value.update.return_value.eq.return_value.single.return_value.execute = AsyncMock(
            return_value=type("R", (), {"data": {**_make_try_on(tid), "user_rating": 4}})()
        )
        resp = await client.post(
            f"/api/v1/try-ons/{tid}/feedback",
            headers=AUTH_HEADERS, json={"user_rating": 4},
        )
        assert resp.status_code == 200
