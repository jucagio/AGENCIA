from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class ProfileUpdateRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
    country_code: Optional[str] = Field(None, max_length=2)
    preferred_language: Optional[str] = None
    notification_preferences: Optional[Dict[str, bool]] = None

class ProfileResponse(BaseModel):
    id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
    country_code: Optional[str] = None
    preferred_language: str
    notification_preferences: Dict[str, bool]
    created_at: str
    updated_at: str
