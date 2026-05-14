"""Tests for recommendation endpoints."""
from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from tests.conftest import AUTH_HEADERS, TEST_USER_ID


def _make_reco(rid=None):
    return {
        "id": str(rid or uuid4()), "user_id": str(TEST_USER_ID),
        "occasion": "casual", "season": None, "status": "pending",
        "claude_model_version": "claude", "prompt_version": "0.3.0",
        "metadata": {}, "feedback_score": None, "items_tried_on": 0,
        "items_liked": 0, "items_clicked": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


@pytest.mark.anyio
class TestRecommendationsCreate:
    async def test_generate_returns_202(self, client) -> None:
        """Patch the service directly to avoid mock-chain collisions in the pg builder."""
        rid = uuid4()
        expected = {"recommendation_id": str(rid), "status": "pending",
                    "message": "Generating recommendations. Poll GET /recommendations/{id}."}
        with patch(
            "app.services.recommendation_service.RecommendationService.generate_recommendations",
            new_callable=AsyncMock,
            return_value=expected,
        ):
            resp = await client.post(
                "/api/v1/recommendations", headers=AUTH_HEADERS, params={"occasion": "casual"}
            )
        assert resp.status_code == 202

    async def test_requires_auth(self, unauthed_client) -> None:
        resp = await unauthed_client.post("/api/v1/recommendations")
        assert resp.status_code == 401


@pytest.mark.anyio
class TestRecommendationsListGet:
    async def test_list_returns_200(self, client, mock_admin_pg) -> None:
        mock_admin_pg.table.return_value.is_.return_value.order.return_value.range.return_value.execute = AsyncMock(
            return_value=type("R", (), {"data": [_make_reco()], "count": 1})()
        )
        resp = await client.get("/api/v1/recommendations", headers=AUTH_HEADERS)
        assert resp.status_code == 200

    async def test_get_returns_200(self, client, mock_admin_pg) -> None:
        rid = uuid4()
        mock_admin_pg.table.return_value.eq.return_value.maybe_single.return_value.execute = AsyncMock(
            return_value=type("R", (), {"data": _make_reco(rid)})()
        )
        resp = await client.get(f"/api/v1/recommendations/{rid}", headers=AUTH_HEADERS)
        assert resp.status_code == 200
