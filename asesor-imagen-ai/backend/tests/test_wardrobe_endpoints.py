"""
Tests for wardrobe endpoints.
"""

from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from tests.conftest import AUTH_HEADERS, TEST_USER_ID


def _make_item(item_id=None):
    return {
        "id": str(item_id or uuid4()),
        "user_id": str(TEST_USER_ID),
        "image_url": "https://example.com/img.jpg",
        "cdn_url": None,
        "primary_color": None,
        "detected_style": None,
        "category": "top",
        "size": "M",
        "brand": "Nike",
        "storage_path": None,
        "secondary_colors": None,
        "detected_occasion": None,
        "price_paid": None,
        "currency": None,
        "purchase_date": None,
        "condition": None,
        "user_tags": [],
        "user_notes": None,
        "metadata": {},
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "deleted_at": None,
    }


@pytest.mark.anyio
class TestWardrobeList:
    async def test_list_requires_auth(self, unauthed_client) -> None:
        resp = await unauthed_client.get("/api/v1/wardrobe/items")
        assert resp.status_code == 401

    async def test_list_returns_200(self, client, mock_admin_pg) -> None:
        mock_admin_pg.table.return_value.is_.return_value.order.return_value.range.return_value.execute = AsyncMock(
            return_value=type("R", (), {"data": [_make_item()], "count": 1})()
        )
        resp = await client.get("/api/v1/wardrobe/items", headers=AUTH_HEADERS)
        assert resp.status_code == 200

    async def test_list_empty_returns_200(self, client, mock_admin_pg) -> None:
        mock_admin_pg.table.return_value.is_.return_value.order.return_value.range.return_value.execute = AsyncMock(
            return_value=type("R", (), {"data": [], "count": 0})()
        )
        resp = await client.get("/api/v1/wardrobe/items", headers=AUTH_HEADERS)
        assert resp.status_code == 200


@pytest.mark.anyio
class TestWardrobeCreate:
    async def test_create_returns_201(self, client, mock_admin_pg) -> None:
        item = _make_item()
        mock_admin_pg.table.return_value.insert.return_value.single.return_value.execute = AsyncMock(
            return_value=type("R", (), {"data": item})()
        )
        resp = await client.post(
            "/api/v1/wardrobe/items",
            headers=AUTH_HEADERS,
            json={"image_url": "https://example.com/img.jpg", "category": "top"},
        )
        assert resp.status_code == 201
        assert resp.json()["category"] == "top"

    async def test_create_requires_image_url(self, client) -> None:
        resp = await client.post(
            "/api/v1/wardrobe/items",
            headers=AUTH_HEADERS,
            json={"category": "top"},  # missing image_url
        )
        assert resp.status_code == 422


@pytest.mark.anyio
class TestWardrobeGetUpdateDelete:
    async def test_get_item_returns_200(self, client, mock_admin_pg) -> None:
        item_id = uuid4()
        item = _make_item(item_id)
        mock_admin_pg.table.return_value.eq.return_value.maybe_single.return_value.execute = AsyncMock(
            return_value=type("R", (), {"data": item})()
        )
        resp = await client.get(
            f"/api/v1/wardrobe/items/{item_id}", headers=AUTH_HEADERS
        )
        assert resp.status_code == 200

    async def test_delete_item_returns_204(self, client, mock_admin_pg) -> None:
        item_id = uuid4()
        item = _make_item(item_id)
        _tbl = mock_admin_pg.table.return_value
        _chain = _tbl.eq.return_value.update.return_value.eq.return_value.single.return_value
        _chain.execute = AsyncMock(return_value=type("R", (), {"data": item})())
        # Also mock the simpler chain used by update
        mock_admin_pg.table.return_value.update.return_value.eq.return_value.single.return_value.execute = AsyncMock(
            return_value=type("R", (), {"data": item})()
        )
        resp = await client.delete(
            f"/api/v1/wardrobe/items/{item_id}", headers=AUTH_HEADERS
        )
        assert resp.status_code == 204
