"""
Wardrobe endpoints — CRUD for wardrobe items.
"""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Query, Response

from app.api.deps import AdminDep, CurrentUser
from app.schemas.common import PaginationMeta, SuccessResponse
from app.schemas.wardrobe import (
    WardrobeItemCreateRequest,
    WardrobeItemResponse,
    WardrobeItemUpdateRequest,
)
from app.services.wardrobe_service import WardrobeService

router = APIRouter()


@router.get(
    "/items",
    response_model=SuccessResponse,
    summary="List wardrobe items",
)
async def list_items(
    user_id: CurrentUser,
    admin: AdminDep,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    category: str | None = Query(default=None),
) -> SuccessResponse:
    """Return paginated list of the authenticated user's wardrobe items."""
    svc = WardrobeService(admin)
    items, total = await svc.list_items(
        user_id=user_id, page=page, size=size, category=category
    )
    pages = (total + size - 1) // size if total else 0
    return SuccessResponse(
        data=[WardrobeItemResponse.model_validate(i.model_dump()) for i in items],
        pagination=PaginationMeta(page=page, per_page=size, total=total, pages=pages),
    )


@router.post(
    "/items",
    response_model=WardrobeItemResponse,
    status_code=201,
    summary="Add wardrobe item",
)
async def create_item(
    data: WardrobeItemCreateRequest,
    user_id: CurrentUser,
    admin: AdminDep,
) -> WardrobeItemResponse:
    """Create a new wardrobe item for the authenticated user."""
    svc = WardrobeService(admin)
    item = await svc.create_item(user_id=user_id, data=data)
    return WardrobeItemResponse.model_validate(item.model_dump())


@router.get(
    "/items/{item_id}",
    response_model=WardrobeItemResponse,
    summary="Get wardrobe item",
)
async def get_item(
    item_id: UUID,
    user_id: CurrentUser,
    admin: AdminDep,
) -> WardrobeItemResponse:
    """Return a specific wardrobe item owned by the authenticated user."""
    svc = WardrobeService(admin)
    item = await svc.get_item(user_id=user_id, item_id=item_id)
    return WardrobeItemResponse.model_validate(item.model_dump())


@router.put(
    "/items/{item_id}",
    response_model=WardrobeItemResponse,
    summary="Update wardrobe item",
)
async def update_item(
    item_id: UUID,
    update: WardrobeItemUpdateRequest,
    user_id: CurrentUser,
    admin: AdminDep,
) -> WardrobeItemResponse:
    """Update fields of a wardrobe item owned by the authenticated user."""
    svc = WardrobeService(admin)
    item = await svc.update_item(user_id=user_id, item_id=item_id, update=update)
    return WardrobeItemResponse.model_validate(item.model_dump())


@router.delete(
    "/items/{item_id}",
    status_code=204,
    summary="Delete wardrobe item",
)
async def delete_item(
    item_id: UUID,
    user_id: CurrentUser,
    admin: AdminDep,
) -> Response:
    """Soft-delete a wardrobe item (sets deleted_at)."""
    svc = WardrobeService(admin)
    await svc.delete_item(user_id=user_id, item_id=item_id)
    return Response(status_code=204)
