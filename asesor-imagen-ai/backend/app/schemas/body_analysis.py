from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BodyAnalysisCreateRequest(BaseModel):
    """Submit a body image for analysis (multipart handled at endpoint level)."""
    image_url: Optional[str] = None  # direct URL upload (mobile use case)


class BodyAnalysisResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    image_url: Optional[str] = None
    body_type: Optional[str] = None
    skin_tone_category: Optional[str] = None
    color_season: Optional[str] = None
    best_colors: Optional[List[str]] = None
    avoid_colors: Optional[List[str]] = None
    status: Optional[str] = None
    created_at: datetime
    updated_at: datetime
