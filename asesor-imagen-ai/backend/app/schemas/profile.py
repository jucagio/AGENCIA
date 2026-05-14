from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProfileUpdateRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
    country_code: Optional[str] = Field(None, max_length=2)
    preferred_language: Optional[str] = None
    notification_preferences: Optional[Dict[str, bool]] = None


class ProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
    country_code: Optional[str] = None
    preferred_language: str = "es"
    notification_preferences: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime
