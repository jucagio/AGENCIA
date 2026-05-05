from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class SubscriptionBase(BaseModel):
    plan_type: str = Field(..., pattern="^(free|estilo|imagen)$")
    billing_provider: Optional[str] = Field(None, pattern="^(stripe|mercadopago)$")
    external_subscription_id: Optional[str] = None
    external_customer_id: Optional[str] = None
    status: str = Field(..., pattern="^(trialing|active|past_due|canceled|expired)$")
    trial_ends_at: Optional[datetime] = None
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    cancel_at_period_end: bool = False
    canceled_at: Optional[datetime] = None
    currency: Optional[str] = None
    amount_cents: Optional[int] = None

class SubscriptionCreate(SubscriptionBase):
    user_id: UUID

class SubscriptionUpdate(BaseModel):
    plan_type: Optional[str] = Field(None, pattern="^(free|estilo|imagen)$")
    billing_provider: Optional[str] = Field(None, pattern="^(stripe|mercadopago)$")
    external_subscription_id: Optional[str] = None
    external_customer_id: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(trialing|active|past_due|canceled|expired)$")
    trial_ends_at: Optional[datetime] = None
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    cancel_at_period_end: Optional[bool] = None
    canceled_at: Optional[datetime] = None
    currency: Optional[str] = None
    amount_cents: Optional[int] = None

class Subscription(SubscriptionBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
