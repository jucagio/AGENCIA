"""
Schemas package — public API.

All request/response schemas for the FastAPI layer.
"""

from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.body_analysis import BodyAnalysisResponse
from app.schemas.common import ErrorDetail, ErrorResponse, PaginationMeta, SuccessResponse
from app.schemas.profile import ProfileResponse, ProfileUpdateRequest
from app.schemas.recommendation import (
    RecommendationCreateRequest,
    RecommendationFeedbackRequest,
    RecommendationItemResponse,
    RecommendationListResponse,
    RecommendationResponse,
)
from app.schemas.subscription import (
    SubscriptionCreateRequest,
    SubscriptionResponse,
    SubscriptionStatusResponse,
    SubscriptionUpdateRequest,
)
from app.schemas.try_on import (
    TryOnCreateRequest,
    TryOnFeedbackRequest,
    TryOnListResponse,
    TryOnResponse,
)
from app.schemas.wardrobe import (
    WardrobeItemCreateRequest,
    WardrobeItemResponse,
    WardrobeItemUpdateRequest,
)

__all__ = [
    # Auth
    "LoginRequest",
    "RegisterRequest",
    "TokenResponse",
    # Common
    "PaginationMeta",
    "SuccessResponse",
    "ErrorDetail",
    "ErrorResponse",
    # Profile
    "ProfileUpdateRequest",
    "ProfileResponse",
    # Wardrobe
    "WardrobeItemCreateRequest",
    "WardrobeItemUpdateRequest",
    "WardrobeItemResponse",
    # Body Analysis
    "BodyAnalysisResponse",
    # Recommendation
    "RecommendationCreateRequest",
    "RecommendationFeedbackRequest",
    "RecommendationItemResponse",
    "RecommendationResponse",
    "RecommendationListResponse",
    # Try-On
    "TryOnCreateRequest",
    "TryOnFeedbackRequest",
    "TryOnResponse",
    "TryOnListResponse",
    # Subscription
    "SubscriptionCreateRequest",
    "SubscriptionUpdateRequest",
    "SubscriptionResponse",
    "SubscriptionStatusResponse",
]
