"""
Body analysis endpoints.
"""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Body

from app.api.deps import AdminDep, CurrentUser
from app.schemas.body_analysis import BodyAnalysisResponse
from app.services.body_analysis_service import BodyAnalysisService

router = APIRouter()


@router.post(
    "",
    status_code=202,
    summary="Start body analysis",
)
async def create_analysis(
    user_id: CurrentUser,
    admin: AdminDep,
    image_url: str | None = Body(default=None, embed=True),
) -> dict:  # type: ignore[type-arg]
    """
    Queue a body analysis job.

    Accepts an optional image_url (Sprint 0.3).
    Returns 202 with {analysis_id, status: "pending"}.
    Sprint 0.5: accept multipart/form-data image upload.
    """
    svc = BodyAnalysisService(admin)
    return await svc.create_analysis(user_id=user_id, image_url=image_url)


@router.get(
    "/{analysis_id}",
    response_model=BodyAnalysisResponse,
    summary="Get body analysis result",
)
async def get_analysis(
    analysis_id: UUID,
    user_id: CurrentUser,
    admin: AdminDep,
) -> BodyAnalysisResponse:
    """Return the result of a body analysis job."""
    svc = BodyAnalysisService(admin)
    analysis = await svc.get_analysis(user_id=user_id, analysis_id=analysis_id)
    return BodyAnalysisResponse.model_validate(analysis.model_dump())
