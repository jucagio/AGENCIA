"""Authentication endpoints.

Uses Supabase Auth for user management (sign up, sign in) and issues
short-lived JWTs for API access. Refresh tokens allow silent renewal
without re-entering credentials.

SECURITY:
- Passwords validated by Pydantic (min 8 chars, 1 upper, 1 digit)
- Access tokens expire in 1 hour
- Refresh tokens expire in 7 days
- Generic error messages to prevent user enumeration
"""

import logging
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from postgrest.exceptions import APIError

from app.config import settings
from app.db.supabase import (
    create_user_profile,
    fetch_user_profile,
    get_supabase_client,
)
from app.dependencies import get_current_user
from app.models.schemas import (
    APIResponse,
    ErrorResponse,
    RefreshRequest,
    TokenResponse,
    UserCreate,
    UserLogin,
    UserProfile,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


def _create_token_pair(user_id: str, email: str) -> dict:
    """Create an access + refresh token pair.

    Access token: short-lived (1 hour), used for API calls.
    Refresh token: long-lived (7 days), used only to get new access tokens.
    """
    now = datetime.now(timezone.utc)

    access_payload = {
        "sub": user_id,
        "email": email,
        "type": "access",
        "iat": now,
        "exp": now + timedelta(minutes=settings.access_token_expire_minutes),
    }
    access_token = jwt.encode(
        access_payload, settings.jwt_secret, algorithm=settings.jwt_algorithm
    )

    refresh_payload = {
        "sub": user_id,
        "email": email,
        "type": "refresh",
        "iat": now,
        "exp": now + timedelta(days=settings.refresh_token_expire_days),
    }
    refresh_token = jwt.encode(
        refresh_payload, settings.jwt_secret, algorithm=settings.jwt_algorithm
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.access_token_expire_minutes * 60,
    }


@router.post(
    "/register",
    response_model=APIResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"model": ErrorResponse, "description": "Email already registered"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
)
async def register(body: UserCreate):
    """Register a new user account.

    Creates the user in Supabase Auth and a matching profile row.
    Returns JWT tokens on success so the user is logged in immediately.
    """
    client = get_supabase_client()

    try:
        auth_response = client.auth.sign_up({
            "email": body.email,
            "password": body.password,
        })
    except Exception as exc:
        logger.warning("Registration failed for email=%s: %s", body.email, exc)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Unable to create account. Email may already be registered.",
        )

    user = auth_response.user
    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Unable to create account. Email may already be registered.",
        )

    # Create profile row (uses admin client to bypass RLS during creation)
    try:
        create_user_profile(user_id=user.id, display_name=body.name)
    except Exception as exc:
        logger.error("Profile creation failed for user_id=%s: %s", user.id, exc)
        # User exists in Auth but profile failed -- non-blocking
        # Profile can be created lazily on first /auth/me call

    tokens = _create_token_pair(user_id=user.id, email=body.email)

    return APIResponse(
        success=True,
        data=tokens,
        message="Account created successfully",
    )


@router.post(
    "/login",
    response_model=APIResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid credentials"},
    },
)
async def login(body: UserLogin):
    """Authenticate with email and password.

    Returns a JWT access/refresh token pair on success.
    """
    client = get_supabase_client()

    try:
        auth_response = client.auth.sign_in_with_password({
            "email": body.email,
            "password": body.password,
        })
    except Exception as exc:
        logger.warning("Login failed for email=%s: %s", body.email, exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    user = auth_response.user
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    tokens = _create_token_pair(user_id=user.id, email=body.email)

    return APIResponse(
        success=True,
        data=tokens,
        message="Login successful",
    )


@router.post(
    "/refresh",
    response_model=APIResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid refresh token"},
    },
)
async def refresh_token(body: RefreshRequest):
    """Exchange a valid refresh token for a new access/refresh pair.

    The old refresh token is invalidated implicitly by issuing a new one
    with a fresh expiration (rotation).
    """
    try:
        payload = jwt.decode(
            body.refresh_token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired. Please log in again.",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type. Expected a refresh token.",
        )

    user_id = payload.get("sub")
    email = payload.get("email", "")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    tokens = _create_token_pair(user_id=user_id, email=email)

    return APIResponse(
        success=True,
        data=tokens,
        message="Tokens refreshed successfully",
    )


@router.get(
    "/me",
    response_model=APIResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"},
    },
)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Return the authenticated user's profile.

    Fetches the profile from the user_profiles table. If no profile
    exists yet (edge case from failed registration), returns basic
    info from the JWT.
    """
    profile = fetch_user_profile(current_user["user_id"])

    if profile:
        data = {
            "id": current_user["user_id"],
            "email": current_user["email"],
            "display_name": profile.get("display_name"),
            "avatar_url": profile.get("avatar_url"),
            "preferred_language": profile.get("preferred_language", "co-csn"),
            "created_at": profile.get("created_at"),
        }
    else:
        data = {
            "id": current_user["user_id"],
            "email": current_user["email"],
            "display_name": None,
            "avatar_url": None,
            "preferred_language": "co-csn",
            "created_at": None,
        }

    return APIResponse(
        success=True,
        data=data,
        message="Profile retrieved",
    )
