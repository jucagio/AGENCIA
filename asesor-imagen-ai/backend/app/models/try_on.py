from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TryOnBase(BaseModel):
    wardrobe_item_id: Optional[UUID] = None
    body_analysis_id: Optional[UUID] = None

    content_hash: str
    cache_hit: bool = False
    cached_from_id: Optional[UUID] = None

    replicate_model_version: Optional[str] = None
    replicate_prediction_id: Optional[str] = None
    inference_time_ms: Optional[int] = None

    status: str = Field(..., pattern="^(pending|processing|completed|failed)$")
    result_image_url: Optional[str] = None
    result_storage_path: Optional[str] = None
    result_cdn_url: Optional[str] = None
    error_message: Optional[str] = None

    confidence_score: Optional[float] = None

    user_rating: Optional[int] = Field(None, ge=1, le=5)
    fit_feedback: Optional[str] = Field(None, pattern="^(too_loose|too_tight|perfect|ok)$")
    color_feedback: Optional[str] = Field(None, pattern="^(clashes|okay|harmonious|amazing)$")
    occasion_fit: Optional[str] = Field(None, pattern="^(too_casual|too_formal|just_right)$")
    would_buy: Optional[bool] = None
    liked: bool = False

    view_duration_seconds: Optional[int] = None
    shared: bool = False
    saved_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class TryOnCreate(BaseModel):
    wardrobe_item_id: Optional[UUID] = None
    body_analysis_id: Optional[UUID] = None
    content_hash: str
    status: str = Field(default="pending", pattern="^(pending|processing|completed|failed)$")

class TryOnUpdate(BaseModel):
    cache_hit: Optional[bool] = None
    cached_from_id: Optional[UUID] = None
    replicate_model_version: Optional[str] = None
    replicate_prediction_id: Optional[str] = None
    inference_time_ms: Optional[int] = None
    status: Optional[str] = Field(None, pattern="^(pending|processing|completed|failed)$")
    result_image_url: Optional[str] = None
    result_storage_path: Optional[str] = None
    result_cdn_url: Optional[str] = None
    error_message: Optional[str] = None
    confidence_score: Optional[float] = None
    user_rating: Optional[int] = Field(None, ge=1, le=5)
    fit_feedback: Optional[str] = Field(None, pattern="^(too_loose|too_tight|perfect|ok)$")
    color_feedback: Optional[str] = Field(None, pattern="^(clashes|okay|harmonious|amazing)$")
    occasion_fit: Optional[str] = Field(None, pattern="^(too_casual|too_formal|just_right)$")
    would_buy: Optional[bool] = None
    liked: Optional[bool] = None
    view_duration_seconds: Optional[int] = None
    shared: Optional[bool] = None
    saved_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class TryOn(TryOnBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
