from datetime import date, datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class WardrobeItemBase(BaseModel):
    image_url: str
    storage_path: Optional[str] = None
    cdn_url: Optional[str] = None

    primary_color: Optional[str] = None
    primary_color_hex: Optional[str] = None
    secondary_colors: Optional[Dict[str, Any]] = None
    detected_style: Optional[str] = None
    detected_occasion: Optional[List[str]] = None
    category: Optional[str] = None

    size: Optional[str] = None
    brand: Optional[str] = None
    price_paid: Optional[float] = None
    currency: Optional[str] = None
    purchase_date: Optional[date] = None
    condition: Optional[str] = Field(None, pattern="^(new|like_new|good|fair)$")
    user_tags: Optional[List[str]] = None
    user_notes: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class WardrobeItemCreate(WardrobeItemBase):
    pass

class WardrobeItemUpdate(BaseModel):
    image_url: Optional[str] = None
    storage_path: Optional[str] = None
    cdn_url: Optional[str] = None
    primary_color: Optional[str] = None
    primary_color_hex: Optional[str] = None
    secondary_colors: Optional[Dict[str, Any]] = None
    detected_style: Optional[str] = None
    detected_occasion: Optional[List[str]] = None
    category: Optional[str] = None
    size: Optional[str] = None
    brand: Optional[str] = None
    price_paid: Optional[float] = None
    currency: Optional[str] = None
    purchase_date: Optional[date] = None
    condition: Optional[str] = Field(None, pattern="^(new|like_new|good|fair)$")
    user_tags: Optional[List[str]] = None
    user_notes: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class WardrobeItem(WardrobeItemBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
