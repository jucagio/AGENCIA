"""
Webhook endpoints — Stripe and MercadoPago payment notifications.

Both routes are in PUBLIC_ROUTES (no JWT required — validated by provider signature).
Stripe-Signature HMAC-SHA256 validation is enforced in SubscriptionService.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, Header, Request, Response

from app.core.admin_client import AdminClient
from app.core.exceptions import AuthenticationError
from app.services.subscription_service import SubscriptionService

logger = logging.getLogger(__name__)
router = APIRouter()


def _get_admin_client(request: Request) -> AdminClient:
    """Get AdminClient from app state (no user auth context for webhooks)."""
    raw_pg = getattr(request.app.state, "supabase_admin", None)
    return AdminClient(raw_pg)  # type: ignore[arg-type]


@router.post(
    "/stripe",
    status_code=200,
    summary="Stripe webhook receiver",
)
async def stripe_webhook(
    request: Request,
    stripe_signature: str | None = Header(default=None, alias="Stripe-Signature"),
) -> dict:  # type: ignore[type-arg]
    """
    Receive and process Stripe webhook events.

    Validates the Stripe-Signature header (HMAC-SHA256).
    Returns 400 if signature is invalid.
    """
    payload = await request.body()

    if not stripe_signature:
        logger.warning("Stripe webhook received without Stripe-Signature header")
        return Response(  # type: ignore[return-value]
            content="Missing Stripe-Signature",
            status_code=400,
            media_type="text/plain",
        )

    try:
        admin = _get_admin_client(request)
        svc = SubscriptionService(admin)
        await svc.handle_stripe_webhook(payload=payload, signature=stripe_signature)
    except AuthenticationError as exc:
        logger.warning("Stripe webhook signature validation failed: %s", exc)
        return Response(  # type: ignore[return-value]
            content=str(exc),
            status_code=400,
            media_type="text/plain",
        )
    except Exception as exc:  # noqa: BLE001
        logger.error("Stripe webhook processing error: %s", exc)
        # Return 200 to prevent Stripe from retrying (log the error separately)
        return {"status": "error", "detail": "Internal processing error"}

    return {"status": "ok"}


@router.post(
    "/mercadopago",
    status_code=200,
    summary="MercadoPago webhook receiver",
)
async def mp_webhook(
    request: Request,
    x_signature: str | None = Header(default=None, alias="x-signature"),
    x_request_id: str | None = Header(default=None, alias="x-request-id"),
) -> dict:  # type: ignore[type-arg]
    """
    Receive and process MercadoPago webhook notifications.

    Validates the x-signature header.
    Returns 400 if signature is invalid.
    """
    payload = await request.body()

    try:
        admin = _get_admin_client(request)
        svc = SubscriptionService(admin)
        await svc.handle_mp_webhook(
            payload=payload,
            x_signature=x_signature or "",
            x_request_id=x_request_id or "",
        )
    except AuthenticationError as exc:
        logger.warning("MercadoPago webhook signature validation failed: %s", exc)
        return Response(  # type: ignore[return-value]
            content=str(exc),
            status_code=400,
            media_type="text/plain",
        )
    except Exception as exc:  # noqa: BLE001
        logger.error("MercadoPago webhook processing error: %s", exc)
        return {"status": "error", "detail": "Internal processing error"}

    return {"status": "ok"}
