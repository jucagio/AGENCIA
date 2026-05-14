"""
Subscription service — manages subscription lifecycle and payment provider webhooks.

Sprint 0.3: Stripe + MercadoPago integration stubs.
Sprint 0.5: full Stripe checkout + webhook signature validation.
"""

from __future__ import annotations

import hashlib
import hmac
import logging
import time
from uuid import UUID

from app.config import get_settings
from app.core.admin_client import AdminClient
from app.core.exceptions import AuthenticationError, ValidationError
from app.models.subscription import Subscription
from app.repositories.repos import SubscriptionRepository

logger = logging.getLogger(__name__)

# Pricing tiers (cents) — source of truth for checkout creation
PLAN_PRICES: dict[str, dict[str, int]] = {
    "estilo": {"monthly": 1999, "yearly": 19990},  # COP cents
    "imagen": {"monthly": 3999, "yearly": 39990},
}


class SubscriptionService:
    """Payment provider integration + subscription lifecycle."""

    def __init__(self, admin: AdminClient) -> None:
        self._repo = SubscriptionRepository(admin)
        self._settings = get_settings()

    async def get_current(self, *, user_id: UUID) -> Subscription | None:
        """Return the active/trialing subscription for user_id, or None."""
        return await self._repo.get_active(user_id=user_id)

    async def create_stripe_checkout(
        self,
        *,
        user_id: UUID,
        tier: str,
        yearly: bool = False,
    ) -> str:
        """
        Create a Stripe checkout session for the requested tier.

        Returns:
            Stripe checkout URL.

        Sprint 0.3 stub: returns a placeholder URL.
        Sprint 0.5: real stripe.checkout.Session.create() call.
        """
        if tier not in PLAN_PRICES:
            raise ValidationError(
                message=f"Invalid plan tier: {tier}",
                fields={"tier": f"Must be one of {list(PLAN_PRICES)}"},
            )

        settings = self._settings
        if not settings.STRIPE_SECRET_KEY:
            # Dev/test: return placeholder URL
            return f"https://checkout.stripe.com/stub/{tier}/{'yearly' if yearly else 'monthly'}"

        # TODO(Sprint 0.5): replace stub with real Stripe checkout
        # import stripe; stripe.api_key = settings.STRIPE_SECRET_KEY
        # session = await asyncio.to_thread(stripe.checkout.Session.create, ...)
        # return session.url

        return f"https://checkout.stripe.com/stub/{tier}"

    async def create_mp_preference(
        self,
        *,
        user_id: UUID,
        tier: str,
        yearly: bool = False,
    ) -> str:
        """
        Create a MercadoPago preference for the requested tier.

        Returns:
            MercadoPago init_point URL.

        Sprint 0.3 stub: returns a placeholder URL.
        """
        if tier not in PLAN_PRICES:
            raise ValidationError(
                message=f"Invalid plan tier: {tier}",
                fields={"tier": f"Must be one of {list(PLAN_PRICES)}"},
            )

        settings = self._settings
        if not settings.MERCADO_PAGO_ACCESS_TOKEN:
            return f"https://www.mercadopago.com/checkout/v1/redirect/stub/{tier}"

        # TODO(Sprint 0.5): real MercadoPago SDK call
        return f"https://www.mercadopago.com/checkout/v1/redirect/stub/{tier}"

    def _verify_stripe_signature(self, payload: bytes, signature_header: str) -> None:
        """
        Validate Stripe-Signature header (HMAC-SHA256).

        Raises:
            AuthenticationError: if signature is missing, invalid, or timestamp
                                 is outside the 5-minute tolerance.
        """
        secret = self._settings.STRIPE_WEBHOOK_SECRET
        if not secret:
            # Reject when secret is not configured — cannot validate, must deny
            raise AuthenticationError(
                "Stripe webhook signature cannot be validated: STRIPE_WEBHOOK_SECRET not configured"
            )

        if not signature_header:
            raise AuthenticationError("Missing Stripe-Signature header")

        # Parse timestamp and signatures from Stripe-Signature header
        # Format: t=<timestamp>,v1=<sig1>,v1=<sig2>,...
        parts: dict[str, list[str]] = {}
        for item in signature_header.split(","):
            if "=" in item:
                k, _, v = item.partition("=")
                parts.setdefault(k.strip(), []).append(v.strip())

        timestamp_str = (parts.get("t") or [""])[0]
        v1_sigs = parts.get("v1", [])

        if not timestamp_str or not v1_sigs:
            raise AuthenticationError("Invalid Stripe-Signature format")

        # Reject if timestamp is older than 5 minutes (replay attack prevention)
        try:
            ts = int(timestamp_str)
        except ValueError as exc:
            raise AuthenticationError("Invalid Stripe-Signature timestamp") from exc

        if abs(time.time() - ts) > 300:
            raise AuthenticationError("Stripe-Signature timestamp too old (replay attack?)")

        # Compute expected signature
        signed_payload = f"{timestamp_str}.{payload.decode('utf-8', errors='replace')}"
        expected = hmac.new(
            secret.encode("utf-8"),
            signed_payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        if not any(hmac.compare_digest(expected, sig) for sig in v1_sigs):
            raise AuthenticationError("Invalid Stripe signature")

    def _verify_mp_signature(self, payload: bytes, x_signature: str, x_request_id: str) -> None:
        """
        Validate MercadoPago x-signature header.

        Raises:
            AuthenticationError: if signature is missing or invalid.
        """
        secret = self._settings.MERCADO_PAGO_WEBHOOK_SECRET
        if not secret:
            # Reject when secret is not configured — cannot validate, must deny
            raise AuthenticationError(
                "MercadoPago webhook signature cannot be validated: MERCADO_PAGO_WEBHOOK_SECRET not configured"
            )

        if not x_signature:
            raise AuthenticationError("Missing x-signature header")

        # MP signature format: ts=<ts>,v1=<sig>
        parts: dict[str, str] = {}
        for item in x_signature.split(","):
            if "=" in item:
                k, _, v = item.partition("=")
                parts[k.strip()] = v.strip()

        ts = parts.get("ts", "")
        v1 = parts.get("v1", "")
        if not ts or not v1:
            raise AuthenticationError("Invalid x-signature format")

        signed_payload = f"id:{x_request_id};request-id:{x_request_id};ts:{ts};"
        expected = hmac.new(
            secret.encode("utf-8"),
            signed_payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(expected, v1):
            raise AuthenticationError("Invalid MercadoPago signature")

    async def handle_stripe_webhook(self, payload: bytes, signature: str) -> None:
        """
        Process a Stripe webhook event after verifying the signature.

        Supported events (Sprint 0.5 will add more):
          - checkout.session.completed
          - customer.subscription.updated
          - customer.subscription.deleted
        """
        self._verify_stripe_signature(payload, signature)

        import json  # noqa: PLC0415
        try:
            event = json.loads(payload)
        except (json.JSONDecodeError, ValueError) as exc:
            raise ValidationError(message="Invalid JSON payload", fields={}) from exc

        event_type: str = event.get("type", "")
        logger.info("Stripe webhook received: %s", event_type)

        # TODO(Sprint 0.5): handle specific event types
        # if event_type == "checkout.session.completed": ...

    async def handle_mp_webhook(
        self,
        payload: bytes,
        x_signature: str,
        x_request_id: str,
    ) -> None:
        """
        Process a MercadoPago webhook notification after verifying the signature.
        """
        self._verify_mp_signature(payload, x_signature, x_request_id)

        import json  # noqa: PLC0415
        try:
            event = json.loads(payload)
        except (json.JSONDecodeError, ValueError) as exc:
            raise ValidationError(message="Invalid JSON payload", fields={}) from exc

        topic: str = event.get("topic", event.get("type", ""))
        logger.info("MercadoPago webhook received: %s", topic)

        # TODO(Sprint 0.5): handle specific topics
