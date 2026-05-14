"""Tests for subscription endpoints."""
from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from tests.conftest import AUTH_HEADERS, TEST_USER_ID


def _make_sub():
    """Mock subscription data matching the Subscription model field names."""
    return {
        "id": str(uuid4()), "user_id": str(TEST_USER_ID),
        "plan_type": "estilo", "billing_provider": "stripe",
        "external_subscription_id": "sub_123",
        "external_customer_id": "cus_123",
        "status": "active",
        "current_period_start": datetime.now(timezone.utc).isoformat(),
        "current_period_end": datetime.now(timezone.utc).isoformat(),
        "cancel_at_period_end": False, "canceled_at": None,
        "trial_ends_at": None, "currency": "COP", "amount_cents": 1999,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


@pytest.mark.anyio
class TestSubscriptionEndpoints:
    async def test_get_current_returns_200(self, client, mock_admin_pg) -> None:
        _chain = (
            mock_admin_pg.table.return_value.eq.return_value
            .in_.return_value.order.return_value.limit.return_value.maybe_single.return_value
        )
        _chain.execute = AsyncMock(return_value=type("R", (), {"data": _make_sub()})())
        resp = await client.get("/api/v1/subscriptions/current", headers=AUTH_HEADERS)
        assert resp.status_code == 200
        assert resp.json()["status"] == "active"

    async def test_get_current_empty_returns_free(self, client, mock_admin_pg) -> None:
        _chain = (
            mock_admin_pg.table.return_value.eq.return_value
            .in_.return_value.order.return_value.limit.return_value.maybe_single.return_value
        )
        _chain.execute = AsyncMock(return_value=type("R", (), {"data": None})())
        resp = await client.get("/api/v1/subscriptions/current", headers=AUTH_HEADERS)
        assert resp.status_code == 200
        assert resp.json()["plan"] == "free"

    async def test_create_stripe_checkout_returns_200(self, client) -> None:
        resp = await client.post(
            "/api/v1/subscriptions/stripe/checkout",
            headers={**AUTH_HEADERS, "Idempotency-Key": "k1"}, params={"tier": "estilo"}
        )
        assert resp.status_code == 200
        assert "url" in resp.json()

    async def test_create_mp_preference_returns_200(self, client) -> None:
        resp = await client.post(
            "/api/v1/subscriptions/mp/preference",
            headers={**AUTH_HEADERS, "Idempotency-Key": "k2"}, params={"tier": "imagen"}
        )
        assert resp.status_code == 200
        assert "url" in resp.json()
