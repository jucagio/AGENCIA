"""
User endpoints — profile management and account deletion.
"""

from __future__ import annotations

from fastapi import APIRouter, Response

from app.api.deps import AdminDep, CurrentUser
from app.schemas.profile import ProfileResponse, ProfileUpdateRequest
from app.services.user_service import UserService

router = APIRouter()


@router.get(
    "/profile",
    response_model=ProfileResponse,
    summary="Get current user profile",
)
async def get_profile(user_id: CurrentUser, admin: AdminDep) -> ProfileResponse:
    """Return the authenticated user's profile."""
    svc = UserService(admin)
    profile = await svc.get_profile(user_id=user_id)
    if profile is None:
        from app.core.exceptions import NotFoundError  # noqa: PLC0415
        raise NotFoundError("profile")
    return ProfileResponse.model_validate(profile.model_dump())


@router.put(
    "/profile",
    response_model=ProfileResponse,
    summary="Update current user profile",
)
async def update_profile(
    update: ProfileUpdateRequest,
    user_id: CurrentUser,
    admin: AdminDep,
) -> ProfileResponse:
    """Update the authenticated user's profile fields (partial update)."""
    svc = UserService(admin)
    profile = await svc.update_profile(user_id=user_id, update=update)
    return ProfileResponse.model_validate(profile.model_dump())


@router.delete(
    "/account",
    status_code=204,
    summary="Delete current user account",
)
async def delete_account(user_id: CurrentUser, admin: AdminDep) -> Response:
    """
    Permanently delete the authenticated user's account.

    - Soft-deletes the profile (sets deleted_at).
    - Calls Supabase Auth admin API to remove the auth.users row.
    - Returns 204 No Content on success.
    """
    svc = UserService(admin)
    await svc.delete_account(user_id=user_id)
    return Response(status_code=204)
