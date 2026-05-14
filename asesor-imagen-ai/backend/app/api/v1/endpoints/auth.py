"""
Auth endpoints — registration, login, token refresh, current user.

All routes except /me are in PUBLIC_ROUTES (no JWT required).
"""

from __future__ import annotations

from fastapi import APIRouter, Body

from app.api.deps import AdminDep, CurrentUser
from app.repositories.repos import ProfileRepository
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.profile import ProfileResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=201,
    summary="Register a new user via Supabase Auth",
)
async def register(req: RegisterRequest) -> TokenResponse:
    """
    Register a new user account.

    - Delegates to Supabase GoTrue /signup.
    - Returns access + refresh tokens on success.
    - 422 on duplicate email or validation failure.
    """
    svc = AuthService()
    return await svc.register(req)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login with email + password",
)
async def login(req: LoginRequest) -> TokenResponse:
    """
    Authenticate an existing user.

    - Delegates to Supabase GoTrue token?grant_type=password.
    - Returns access + refresh tokens on success.
    - 401 on invalid credentials.
    """
    svc = AuthService()
    return await svc.login(req)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Exchange refresh token for new access token",
)
async def refresh(
    refresh_token: str = Body(..., embed=True),
) -> TokenResponse:
    """
    Refresh an expired access token.

    Requires the refresh_token from a previous login/register response.
    - 401 if refresh_token is invalid or expired.
    """
    svc = AuthService()
    return await svc.refresh(refresh_token)


@router.get(
    "/me",
    response_model=ProfileResponse,
    summary="Get current user profile",
)
async def me(user_id: CurrentUser, admin: AdminDep) -> ProfileResponse:
    """
    Return the authenticated user's profile.

    Requires a valid Bearer JWT.
    Returns 404 if the profile has not been created yet.
    """
    repo = ProfileRepository(admin)
    profile = await repo.get_profile(user_id=user_id)
    if profile is None:
        from app.core.exceptions import NotFoundError  # noqa: PLC0415
        raise NotFoundError("profile")
    return ProfileResponse.model_validate(profile.model_dump())
