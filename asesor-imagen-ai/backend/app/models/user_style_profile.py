"""
UserStyleProfile model — computed style preferences per user.

Maps to the `user_style_profile` table (Migration 004).
This is an upsert-only table; rows are created/updated by the
recommendation engine, not directly by the user.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserStyleProfile(BaseModel):
    """
    Read-only view of a user's computed style preferences.

    Populated by the AI recommendation engine; never directly mutated
    by the user. The primary key is user_id (1-to-1 with auth.users).
    """

    model_config = ConfigDict(from_attributes=True)

    user_id: UUID

    preferred_styles: Optional[dict[str, Any]] = None
    preferred_colors: Optional[dict[str, Any]] = None
    avoided_colors: Optional[dict[str, Any]] = None
    occasion_preferences: Optional[dict[str, Any]] = None
    favorite_brands: Optional[dict[str, Any]] = None

    avg_price_point: Optional[Decimal] = None
    budget_tier: Optional[str] = None  # "budget" | "mid" | "luxury"
    trend_score: Optional[Decimal] = None
    style_summary: Optional[str] = None

    calculated_at: datetime
    updated_at: datetime
