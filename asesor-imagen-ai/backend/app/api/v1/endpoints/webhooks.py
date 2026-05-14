"""
Webhook endpoints — Stripe and MercadoPago payment notifications.

Both routes are in PUBLIC_ROUTES (no JWT required — validated by provider signature).
Stripe-Signature HMAC-SHA256 validation is enforced in SubscriptionService.

Security order (OWASP A09, A01):
  1. Verify provider signature  → 400 on auth failure
  2. Guard supabase_admin init  → 503 on infra failure (triggers provider retry)
  3. Process event              → 500 on runtime error (triggers provider retry)
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
    """Get AdminClient from app state (no user auth context for webhooks).

    Returns 503 if the DB client was never initialised — prevents silent data loss
    because both Stripe and MercadoPago retry on non-2xx (A01-H1, A09-MED1).
    """
    raw_pg = getattr(request.app.state, "supabase_admin", None)
    if raw_pg is None:
        raise LookupError("supabase_admin not initialised")
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
    Returns 400 if signature is invalid, 503 if DB unavailable, 500 on processing error.
    """
    payload = await request.body()

    if not stripe_signature:
        logger.warning("Stripe webhook received without Stripe-Signature header")
        return Response(  # type: ignore[return-value]
            content="Missing Stripe-Signature",
            status_code=400,
            media_type="text/plain",
        )

    # Step 1: validate signature — stateless, no DB needed
    # Use a throw-away service with a None admin just for auth validation
    try:
        SubscriptionService(AdminClient(None)).verify_stripe_signature(  # type: ignore[arg-type]
            payload, stripe_signature
        )
    except AuthenticationError as exc:
        logger.warning("Stripe webhook signature validation failed: %s", exc)
        return Response(  # type: ignore[return-value]
            content=str(exc),
            status_code=400,
            media_type="text/plain",
        )

    # Step 2: guard DB availability
    try:
        admin = _get_admin_client(request)
    except LookupError as exc:
        logger.error("Stripe webhook: DB unavailable: %s", exc)
        return Response(  # type: ignore[return-value]
            content="Service temporarily unavailable",
            status_code=503,
            media_type="text/plain",
        )

    # Step 3: process event
    try:
        svc = SubscriptionService(admin)
        await svc.handle_stripe_webhook(payload=payload, signature=stripe_signature)
    except Exception as exc:  # noqa: BLE001
        logger.error("Stripe webhook processing error: %s", exc)
        # 500 → Stripe retries (A09-MED1)
        return Response(  # type: ignore[return-value]
            content="Internal processing error",
            status_code=500,
            media_type="text/plain",
        )

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
    Returns 400 if signature is invalid, 503 if DB unavailable, 500 on processing error.
    """
    payload = await request.body()

    # Step 1: validate signature — stateless
    try:
        SubscriptionService(AdminClient(None)).verify_mp_signature(  # type: ignore[arg-type]
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

    # Step 2: guard DB availability
    try:
        admin = _get_admin_client(request)
    except LookupError as exc:
        logger.error("MercadoPago webhook: DB unavailable: %s", exc)
        return Response(  # type: ignore[return-value]
            content="Service temporarily unavailable",
            status_code=503,
            media_type="text/plain",
        )

    # Step 3: process event
    try:
        svc = SubscriptionService(admin)
        await svc.handle_mp_webhook(
            payload=payload,
            x_signature=x_signature or "",
            x_request_id=x_request_id or "",
        )
    except Exception as exc:  # noqa: BLE001
        logger.error("MercadoPago webhook processing error: %s", exc)
        # 500 → MP retries (A09-MED1)
        return Response(  # type: ignore[return-value]
            content="Internal processing error",
            status_code=500,
            media_type="text/plain",
        )

    return {"status": "ok"}
