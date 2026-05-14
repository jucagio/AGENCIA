from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class NotificationPreferences(BaseModel):
    push: bool = True
    email: bool = True

class ProfileBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
    date_of_birth: Optional[date] = None
    country_code: Optional[str] = Field(None, max_length=2)
    preferred_language: str = "es"
    notification_preferences: NotificationPreferences = Field(default_factory=NotificationPreferences)

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
    date_of_birth: Optional[date] = None
    country_code: Optional[str] = Field(None, max_length=2)
    preferred_language: Optional[str] = None
    notification_preferences: Optional[NotificationPreferences] = None

class Profile(ProfileBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
