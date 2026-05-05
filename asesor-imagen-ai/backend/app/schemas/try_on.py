"""
TryOn API request and response schemas.

Separate from the internal model (app/models/try_on.py) — these are the
wire-format Pydantic models that FastAPI serializes to/from JSON.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Request schemas (client -> server)
# ---------------------------------------------------------------------------


class TryOnCreateRequest(BaseModel):
    """Payload to kick off a virtual try-on job."""

    wardrobe_item_id: Optional[UUID] = Field(
        None, description="Wardrobe item to try on (optional if using raw image)."
    )
    body_analysis_id: Optional[UUID] = Field(
        None, description="Body analysis to use as the base photo."
    )
    content_hash: str = Field(
        ...,
        min_length=16,
        description="SHA-256 hash of the input image bytes for cache dedup (ADR-004).",
    )


class TryOnFeedbackRequest(BaseModel):
    """User feedback submitted after viewing a try-on result."""

    user_rating: Optional[int] = Field(None, ge=1, le=5, description="1-5 star rating.")
    fit_feedback: Optional[str] = Field(
        None, pattern="^(too_loose|too_tight|perfect|ok)$"
    )
    color_feedback: Optional[str] = Field(
        None, pattern="^(clashes|okay|harmonious|amazing)$"
    )
    occasion_fit: Optional[str] = Field(
        None, pattern="^(too_casual|too_formal|just_right)$"
    )
    would_buy: Optional[bool] = None
    liked: Optional[bool] = None
    view_duration_seconds: Optional[int] = Field(None, ge=0)


# ---------------------------------------------------------------------------
# Response schemas (server -> client)
# ---------------------------------------------------------------------------


class TryOnResponse(BaseModel):
    """Full try-on record returned to the client."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID

    wardrobe_item_id: Optional[UUID] = None
    body_analysis_id: Optional[UUID] = None

    content_hash: str
    cache_hit: bool
    cached_from_id: Optional[UUID] = None

    replicate_model_version: Optional[str] = None
    replicate_prediction_id: Optional[str] = None
    inference_time_ms: Optional[int] = None

    status: str
    result_image_url: Optional[str] = None
    result_cdn_url: Optional[str] = None
    error_message: Optional[str] = None

    confidence_score: Optional[float] = None

    # Feedback fields
    user_rating: Optional[int] = None
    fit_feedback: Optional[str] = None
    color_feedback: Optional[str] = None
    occasion_fit: Optional[str] = None
    would_buy: Optional[bool] = None
    liked: bool

    shared: bool
    saved_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    created_at: datetime
    updated_at: datetime


class TryOnListResponse(BaseModel):
    """Paginated list of try-on records."""

    items: list[TryOnResponse]
    total: int
    page: int
    per_page: int
