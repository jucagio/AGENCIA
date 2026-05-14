"""Tests for body analysis endpoints."""
from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from tests.conftest import AUTH_HEADERS, TEST_USER_ID


def _make_analysis(aid=None):
    return {
        "id": str(aid or uuid4()), "user_id": str(TEST_USER_ID),
        "image_url": "https://example.com/body.jpg", "status": "pending",
        "body_type": None, "skin_tone_category": None, "color_season": None,
        "face_shape": None, "measurements": None, "metadata": {},
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


@pytest.mark.anyio
class TestBodyAnalysisCreate:
    async def test_create_returns_202(self, client) -> None:
        """Patch the service directly to avoid mock-chain collisions in the pg builder."""
        aid = uuid4()
        expected = {"analysis_id": str(aid), "status": "pending", "job_id": f"stub-{aid}",
                    "message": "Analysis queued. Poll GET /body-analysis/{id} for results."}
        with patch(
            "app.services.body_analysis_service.BodyAnalysisService.create_analysis",
            new_callable=AsyncMock,
            return_value=expected,
        ):
            resp = await client.post(
                "/api/v1/body-analysis",
                headers=AUTH_HEADERS,
                json={"image_url": "https://example.com/body.jpg"},
            )
        assert resp.status_code == 202
        assert resp.json()["status"] == "pending"

    async def test_requires_auth(self, unauthed_client) -> None:
        resp = await unauthed_client.post("/api/v1/body-analysis")
        assert resp.status_code == 401


@pytest.mark.anyio
class TestBodyAnalysisGet:
    async def test_get_returns_200(self, client, mock_admin_pg) -> None:
        aid = uuid4()
        mock_admin_pg.table.return_value.eq.return_value.maybe_single.return_value.execute = AsyncMock(
            return_value=type("R", (), {"data": _make_analysis(aid)})()
        )
        resp = await client.get(f"/api/v1/body-analysis/{aid}", headers=AUTH_HEADERS)
        assert resp.status_code == 200
