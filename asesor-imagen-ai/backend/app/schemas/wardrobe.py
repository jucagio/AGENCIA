from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class WardrobeItemCreateRequest(BaseModel):
    image_url: str
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
    id: str
    user_id: str
    image_url: str
    cdn_url: Optional[str] = None
    primary_color: Optional[str] = None
    detected_style: Optional[str] = None
    category: Optional[str] = None
    size: Optional[str] = None
    brand: Optional[str] = None
    created_at: str
    updated_at: str
