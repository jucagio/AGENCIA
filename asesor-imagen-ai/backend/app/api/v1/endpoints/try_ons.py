"""
Try-on endpoints.

POST /try-ons requires Idempotency-Key header (enforced by idempotency_middleware).
"""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Header, Query

from app.api.deps import AdminDep, CurrentUser
from app.schemas.common import PaginationMeta, SuccessResponse
from app.schemas.try_on import TryOnFeedbackRequest, TryOnResponse
from app.services.try_on_service import TryOnService

router = APIRouter()


@router.post(
    "",
    status_code=202,
    summary="Start virtual try-on",
)
async def create_try_on(
    user_id: CurrentUser,
    admin: AdminDep,
    wardrobe_item_id: UUID = Query(...),
    body_analysis_id: UUID = Query(...),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
) -> dict:  # type: ignore[type-arg]
    """
    Initiate a virtual try-on job.

    Requires Idempotency-Key header (enforced by middleware — returns 422 if missing).
    Returns 202 with {try_on_id, status: "pending", estimated_seconds: 30}.
    Cache hits return {status: "completed", result_cdn_url} immediately.
    """
    svc = TryOnService(admin)
    return await svc.create_try_on(
        user_id=user_id,
        wardrobe_item_id=wardrobe_item_id,
        body_analysis_id=body_analysis_id,
    )


@router.get(
    "",
    response_model=SuccessResponse,
    summary="List try-on history",
)
async def list_try_ons(
    user_id: CurrentUser,
    admin: AdminDep,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
) -> SuccessResponse:
    """Return paginated try-on history for the authenticated user."""
    svc = TryOnService(admin)
    items, total = await svc.list_try_ons(user_id=user_id, page=page, size=size)
    pages = (total + size - 1) // size if total else 0
    return SuccessResponse(
        data=[TryOnResponse.model_validate(i.model_dump()) for i in items],
        pagination=PaginationMeta(page=page, per_page=size, total=total, pages=pages),
    )


@router.get(
    "/{try_on_id}",
    response_model=TryOnResponse,
    summary="Get try-on status/result",
)
async def get_try_on(
    try_on_id: UUID,
    user_id: CurrentUser,
    admin: AdminDep,
) -> TryOnResponse:
    """Return the status and result of a try-on job."""
    svc = TryOnService(admin)
    item = await svc.get_try_on(user_id=user_id, try_on_id=try_on_id)
    return TryOnResponse.model_validate(item.model_dump())


@router.post(
    "/{try_on_id}/feedback",
    response_model=TryOnResponse,
    summary="Submit try-on feedback",
)
async def submit_feedback(
    try_on_id: UUID,
    feedback: TryOnFeedbackRequest,
    user_id: CurrentUser,
    admin: AdminDep,
) -> TryOnResponse:
    """Record user engagement feedback (rating, fit, color, etc.) on a try-on result."""
    svc = TryOnService(admin)
    item = await svc.submit_feedback(
        user_id=user_id, try_on_id=try_on_id, feedback=feedback
    )
    return TryOnResponse.model_validate(item.model_dump())
