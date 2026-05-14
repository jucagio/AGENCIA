"""
Subscription endpoints — current plan + payment provider checkout.
"""

from __future__ import annotations

from fastapi import APIRouter, Query

from app.api.deps import AdminDep, CurrentUser
from app.schemas.subscription import SubscriptionStatusResponse
from app.services.subscription_service import SubscriptionService

router = APIRouter()


@router.get(
    "/current",
    response_model=SubscriptionStatusResponse,
    summary="Get current subscription",
)
async def get_current(user_id: CurrentUser, admin: AdminDep) -> SubscriptionStatusResponse:
    """Return the active or trialing subscription for the authenticated user."""
    svc = SubscriptionService(admin)
    sub = await svc.get_current(user_id=user_id)
    if sub is None:
        return SubscriptionStatusResponse(plan="free", status="active", is_active=True)
    return SubscriptionStatusResponse(
        plan=sub.plan_type,
        status=sub.status,
        is_active=sub.status in ("active", "trialing"),
        trial_ends_at=sub.trial_ends_at,
        current_period_end=sub.current_period_end,
    )


@router.post(
    "/stripe/checkout",
    summary="Create Stripe checkout session",
)
async def create_stripe_checkout(
    user_id: CurrentUser,
    admin: AdminDep,
    tier: str = Query(..., description="Plan tier: estilo | imagen"),
    yearly: bool = Query(default=False),
) -> dict:  # type: ignore[type-arg]
    """
    Create a Stripe checkout session for the selected plan.

    Returns {url: <checkout_url>} — redirect the user to this URL.
    """
    svc = SubscriptionService(admin)
    url = await svc.create_stripe_checkout(user_id=user_id, tier=tier, yearly=yearly)
    return {"url": url}


@router.post(
    "/mp/preference",
    summary="Create MercadoPago preference",
)
async def create_mp_preference(
    user_id: CurrentUser,
    admin: AdminDep,
    tier: str = Query(..., description="Plan tier: estilo | imagen"),
    yearly: bool = Query(default=False),
) -> dict:  # type: ignore[type-arg]
    """
    Create a MercadoPago preference for the selected plan.

    Returns {url: <init_point_url>} — redirect the user to this URL.
    """
    svc = SubscriptionService(admin)
    url = await svc.create_mp_preference(user_id=user_id, tier=tier, yearly=yearly)
    return {"url": url}
