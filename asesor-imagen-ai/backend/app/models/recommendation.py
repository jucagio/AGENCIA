from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class RecommendationItemBase(BaseModel):
    wardrobe_item_id: UUID
    position: Optional[int] = None
    role: Optional[str] = Field(None, pattern="^(top|bottom|shoes|accessory|outerwear)$")

class RecommendationItemCreate(RecommendationItemBase):
    pass

class RecommendationItem(RecommendationItemBase):
    recommendation_id: UUID
    model_config = ConfigDict(from_attributes=True)

class RecommendationBase(BaseModel):
    occasion: str
    season: Optional[str] = None
    reason: Optional[str] = None
    color_harmony_score: Optional[float] = None
    body_fit_score: Optional[float] = None
    clicked: bool = False
    liked: bool = False
    tried_on: bool = False
    claude_model_version: Optional[str] = None
    prompt_version: Optional[str] = None
    feedback_at: Optional[datetime] = None

class RecommendationCreate(BaseModel):
    occasion: str
    season: Optional[str] = None
    claude_model_version: Optional[str] = None
    prompt_version: Optional[str] = None

class RecommendationUpdate(BaseModel):
    reason: Optional[str] = None
    color_harmony_score: Optional[float] = None
    body_fit_score: Optional[float] = None
    clicked: Optional[bool] = None
    liked: Optional[bool] = None
    tried_on: Optional[bool] = None
    feedback_at: Optional[datetime] = None

class Recommendation(RecommendationBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
