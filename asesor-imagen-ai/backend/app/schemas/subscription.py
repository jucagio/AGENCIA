"""
Subscription API request and response schemas.

Wire-format models for plan management, billing status, and webhooks.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Request schemas (client -> server)
# ---------------------------------------------------------------------------


class SubscriptionCreateRequest(BaseModel):
    """Initiate a new subscription (called by payment webhook handler)."""

    plan_type: str = Field(..., pattern="^(free|estilo|imagen)$")
    billing_provider: Optional[str] = Field(
        None, pattern="^(stripe|mercadopago)$"
    )
    external_subscription_id: Optional[str] = None
    external_customer_id: Optional[str] = None
    status: str = Field(..., pattern="^(trialing|active|past_due|canceled|expired)$")
    trial_ends_at: Optional[datetime] = None
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    currency: Optional[str] = Field(None, max_length=3, description="ISO 4217 code.")
    amount_cents: Optional[int] = Field(None, ge=0)


class SubscriptionUpdateRequest(BaseModel):
    """Update subscription state (webhook sync, user-initiated cancellation)."""

    status: Optional[str] = Field(
        None, pattern="^(trialing|active|past_due|canceled|expired)$"
    )
    plan_type: Optional[str] = Field(None, pattern="^(free|estilo|imagen)$")
    external_subscription_id: Optional[str] = None
    external_customer_id: Optional[str] = None
    trial_ends_at: Optional[datetime] = None
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    cancel_at_period_end: Optional[bool] = None
    canceled_at: Optional[datetime] = None
    currency: Optional[str] = Field(None, max_length=3)
    amount_cents: Optional[int] = Field(None, ge=0)


# ---------------------------------------------------------------------------
# Response schemas (server -> client)
# ---------------------------------------------------------------------------


class SubscriptionResponse(BaseModel):
    """Full subscription record returned to the client."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID

    plan_type: str
    billing_provider: Optional[str] = None
    external_subscription_id: Optional[str] = None
    external_customer_id: Optional[str] = None

    status: str
    trial_ends_at: Optional[datetime] = None
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    cancel_at_period_end: bool
    canceled_at: Optional[datetime] = None

    currency: Optional[str] = None
    amount_cents: Optional[int] = None

    created_at: datetime
    updated_at: datetime


class SubscriptionStatusResponse(BaseModel):
    """Lightweight status check — used by mobile app on launch."""

    plan: str  # renamed from plan_type to match client-facing API contract
    status: str
    is_active: bool
    trial_ends_at: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
