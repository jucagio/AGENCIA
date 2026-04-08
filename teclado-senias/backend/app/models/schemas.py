"""Pydantic v2 schemas for request/response validation.

Every field has explicit types, constraints, and examples so that
the auto-generated OpenAPI docs are useful for Brook when building
the Flutter frontend.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


# ---------------------------------------------------------------------------
# Standard API response wrappers
# ---------------------------------------------------------------------------

class APIResponse(BaseModel):
    """Standard success response wrapper."""
    success: bool = True
    data: dict | list | None = None
    message: str = ""

    model_config = {"from_attributes": True}


class PaginatedResponse(BaseModel):
    """Success response with pagination metadata."""
    success: bool = True
    data: list = Field(default_factory=list)
    message: str = ""
    pagination: dict = Field(default_factory=dict)

    model_config = {"from_attributes": True}


class ErrorDetail(BaseModel):
    """Structured error detail."""
    code: str
    message: str
    fields: dict[str, str] | None = None


class ErrorResponse(BaseModel):
    """Standard error response wrapper."""
    success: bool = False
    error: ErrorDetail


# ---------------------------------------------------------------------------
# Auth schemas
# ---------------------------------------------------------------------------

class UserCreate(BaseModel):
    """Schema for user registration."""
    email: EmailStr = Field(..., examples=["usuario@example.com"])
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        examples=["MiPassword123!"],
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        examples=["Maria Lopez"],
    )

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        """Enforce minimum password complexity."""
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr = Field(..., examples=["usuario@example.com"])
    password: str = Field(..., min_length=1, examples=["MiPassword123!"])


class UserProfile(BaseModel):
    """User profile returned by /auth/me."""
    id: str
    email: str
    display_name: str | None = None
    avatar_url: str | None = None
    preferred_language: str = "co-csn"
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    """JWT token pair returned after login/register."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(
        ...,
        description="Access token TTL in seconds",
        examples=[3600],
    )


class RefreshRequest(BaseModel):
    """Schema for token refresh."""
    refresh_token: str = Field(..., min_length=1)


# ---------------------------------------------------------------------------
# Sign schemas
# ---------------------------------------------------------------------------

class Sign(BaseModel):
    """A single sign language sign."""
    id: str
    word: str
    video_url: str
    description: str | None = None
    difficulty: str | None = Field(
        None,
        description="Difficulty level: beginner, intermediate, advanced",
    )
    language_code: str = "co-csn"
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class SignDetail(Sign):
    """Sign with related videos for the detail endpoint."""
    videos: list[dict] = Field(default_factory=list)


class SignSearchParams(BaseModel):
    """Query parameters for sign search."""
    q: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Search term",
        examples=["hola"],
    )
    language_code: str = Field(
        default="co-csn",
        description="ISO language code for sign language variant",
    )


class SignTranslateRequest(BaseModel):
    """Request body for text-to-signs translation."""
    text: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Text to translate into sign language",
        examples=["hola como estas"],
    )
    language_code: str = Field(
        default="co-csn",
        description="Target sign language variant",
    )


class SignTranslateResponse(BaseModel):
    """Response for a translation request."""
    input_text: str
    words: list[str]
    matched_signs: list[Sign]
    unmatched_words: list[str]


# ---------------------------------------------------------------------------
# Favorite schemas
# ---------------------------------------------------------------------------

class Favorite(BaseModel):
    """A user's favorite sign."""
    id: str
    sign: Sign | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class FavoriteCreate(BaseModel):
    """Response after adding a favorite."""
    sign_id: str
    message: str = "Added to favorites"
