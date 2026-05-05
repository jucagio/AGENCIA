"""
Repositories package — public API.

Import from here instead of the sub-modules:
    from app.repositories import ProfileRepository, WardrobeRepository, ...
"""

from app.repositories.base import BaseRepository
from app.repositories.repos import (
    BodyAnalysisRepository,
    ProfileRepository,
    RecommendationItemRepository,
    RecommendationRepository,
    SubscriptionRepository,
    TryOnRepository,
    UsageCounterRepository,
    WardrobeRepository,
)

__all__ = [
    "BaseRepository",
    "ProfileRepository",
    "WardrobeRepository",
    "BodyAnalysisRepository",
    "RecommendationRepository",
    "RecommendationItemRepository",
    "TryOnRepository",
    "SubscriptionRepository",
    "UsageCounterRepository",
]
