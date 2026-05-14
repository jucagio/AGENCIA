"""Tests for webhook endpoints."""
from __future__ import annotations

import hashlib
import hmac
import time
from unittest.mock import patch

import pytest

from app.config import get_settings


@pytest.mark.anyio
class TestWebhooks:
    async def test_stripe_webhook_invalid_sig_400(self, unauthed_client) -> None:
        resp = await unauthed_client.post(
            "/api/v1/webhooks/stripe",
            content=b"{}", headers={"Stripe-Signature": "invalid"}
        )
        assert resp.status_code == 400

    async def test_stripe_webhook_valid_sig_200(self, unauthed_client) -> None:
        payload = b'{"type": "checkout.session.completed"}'
        settings = get_settings()
        secret = settings.STRIPE_WEBHOOK_SECRET
        if not secret:
            pytest.skip("No stripe secret set")
        ts = int(time.time())
        signed_payload = f"{ts}.{payload.decode('utf-8')}"
        expected = hmac.new(
            secret.encode("utf-8"), signed_payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()
        sig = f"t={ts},v1={expected}"

        # Patch handle_stripe_webhook to do nothing instead of trying to process the stub event
        with patch("app.services.subscription_service.SubscriptionService.handle_stripe_webhook", autospec=True):
            resp = await unauthed_client.post(
                "/api/v1/webhooks/stripe",
                content=payload, headers={"Stripe-Signature": sig}
            )
            assert resp.status_code == 200

    async def test_mp_webhook_invalid_sig_400(self, unauthed_client) -> None:
        resp = await unauthed_client.post(
            "/api/v1/webhooks/mercadopago",
            content=b"{}", headers={"x-signature": "invalid"}
        )
        assert resp.status_code == 400
