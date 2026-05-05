from datetime import date
from pydantic import BaseModel, ConfigDict
from uuid import UUID

class UsageCounterBase(BaseModel):
    period_start: date
    try_ons_used: int = 0
    recommendations_used: int = 0
    body_analyses_used: int = 0

class UsageCounterCreate(UsageCounterBase):
    pass

class UsageCounterUpdate(BaseModel):
    try_ons_used: int | None = None
    recommendations_used: int | None = None
    body_analyses_used: int | None = None

class UsageCounter(UsageCounterBase):
    user_id: UUID

    model_config = ConfigDict(from_attributes=True)
