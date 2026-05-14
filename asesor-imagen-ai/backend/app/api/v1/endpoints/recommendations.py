"""
Recommendation endpoints.
"""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Query

from app.api.deps import AdminDep, CurrentUser
from app.schemas.common import PaginationMeta, SuccessResponse
from app.schemas.recommendation import RecommendationResponse
from app.services.recommendation_service import RecommendationService

router = APIRouter()


@router.post(
    "",
    status_code=202,
    summary="Generate outfit recommendations",
)
async def generate_recommendations(
    user_id: CurrentUser,
    admin: AdminDep,
    occasion: str = Query(default="casual"),
    season: str | None = Query(default=None),
) -> dict:  # type: ignore[type-arg]
    """
    Request AI outfit recommendations.

    Returns 202 with {recommendation_id, status: "pending"}.
    Poll GET /recommendations/{id} for results.
    """
    svc = RecommendationService(admin)
    return await svc.generate_recommendations(
        user_id=user_id, occasion=occasion, season=season
    )


@router.get(
    "",
    response_model=SuccessResponse,
    summary="List recommendation history",
)
async def list_recommendations(
    user_id: CurrentUser,
    admin: AdminDep,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
) -> SuccessResponse:
    """Return paginated recommendation history."""
    svc = RecommendationService(admin)
    items, total = await svc.get_recommendations(user_id=user_id, page=page, size=size)
    pages = (total + size - 1) // size if total else 0
    return SuccessResponse(
        data=[RecommendationResponse.model_validate(i.model_dump()) for i in items],
        pagination=PaginationMeta(page=page, per_page=size, total=total, pages=pages),
    )


@router.get(
    "/{recommendation_id}",
    response_model=RecommendationResponse,
    summary="Get recommendation",
)
async def get_recommendation(
    recommendation_id: UUID,
    user_id: CurrentUser,
    admin: AdminDep,
) -> RecommendationResponse:
    """Return a specific recommendation."""
    svc = RecommendationService(admin)
    reco = await svc.get_recommendation(
        user_id=user_id, recommendation_id=recommendation_id
    )
    return RecommendationResponse.model_validate(reco.model_dump())
