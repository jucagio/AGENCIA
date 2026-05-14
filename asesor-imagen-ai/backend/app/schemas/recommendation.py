"""
Recommendation API request and response schemas.

Wire-format models for the AI outfit recommendation feature.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Sub-schemas
# ---------------------------------------------------------------------------


class RecommendationItemResponse(BaseModel):
    """A single wardrobe item included in a recommendation."""

    model_config = ConfigDict(from_attributes=True)

    wardrobe_item_id: UUID
    position: Optional[int] = None
    role: Optional[str] = Field(
        None,
        pattern="^(top|bottom|shoes|accessory|outerwear)$",
        description="Garment role in the outfit.",
    )


# ---------------------------------------------------------------------------
# Request schemas (client -> server)
# ---------------------------------------------------------------------------


class RecommendationCreateRequest(BaseModel):
    """Trigger a new AI outfit recommendation."""

    occasion: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Occasion context, e.g. 'casual friday', 'job interview'.",
    )
    season: Optional[str] = Field(
        None,
        pattern="^(spring|summer|autumn|winter)$",
        description="Target season (optional — inferred from locale if omitted).",
    )


class RecommendationFeedbackRequest(BaseModel):
    """User feedback on a recommendation."""

    clicked: Optional[bool] = None
    liked: Optional[bool] = None
    tried_on: Optional[bool] = None
    feedback_at: Optional[datetime] = None


# ---------------------------------------------------------------------------
# Response schemas (server -> client)
# ---------------------------------------------------------------------------


class RecommendationResponse(BaseModel):
    """Full recommendation record returned to the client."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID

    occasion: str
    season: Optional[str] = None
    reason: Optional[str] = None

    color_harmony_score: Optional[float] = None
    body_fit_score: Optional[float] = None

    clicked: bool
    liked: bool
    tried_on: bool
    feedback_at: Optional[datetime] = None

    claude_model_version: Optional[str] = None
    prompt_version: Optional[str] = None

    items: list[RecommendationItemResponse] = Field(default_factory=list)

    created_at: datetime


class RecommendationListResponse(BaseModel):
    """Paginated list of recommendations."""

    items: list[RecommendationResponse]
    total: int
    page: int
    per_page: int
