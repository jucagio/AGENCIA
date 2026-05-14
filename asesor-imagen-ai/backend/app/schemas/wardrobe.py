from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import AnyHttpUrl, BaseModel, ConfigDict


class WardrobeItemCreateRequest(BaseModel):
    image_url: AnyHttpUrl  # SSRF prevention: must be a valid http/https URL
    category: Optional[str] = None
    size: Optional[str] = None
    brand: Optional[str] = None
    user_tags: Optional[List[str]] = None
    user_notes: Optional[str] = None


class WardrobeItemUpdateRequest(BaseModel):
    category: Optional[str] = None
    size: Optional[str] = None
    brand: Optional[str] = None
    user_tags: Optional[List[str]] = None
    user_notes: Optional[str] = None


class WardrobeItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    image_url: str
    cdn_url: Optional[str] = None
    primary_color: Optional[str] = None
    detected_style: Optional[str] = None
    category: Optional[str] = None
    size: Optional[str] = None
    brand: Optional[str] = None
    created_at: datetime
    updated_at: datetime
