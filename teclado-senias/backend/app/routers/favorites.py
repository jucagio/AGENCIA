"""User favorites endpoints.

All endpoints require authentication. RLS policies in Supabase
ensure that users can only read/write their own favorites.

SECURITY:
- Every request validated against JWT
- Supabase RLS enforces row-level ownership
- Duplicate favorites handled gracefully (409, not 500)
"""

import logging
import re

from fastapi import APIRouter, Depends, HTTPException, status

from app.db.supabase import add_favorite, fetch_user_favorites, remove_favorite
from app.dependencies import get_current_user
from app.models.schemas import APIResponse, ErrorResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/favorites", tags=["favorites"])


def _validate_uuid(value: str, field_name: str = "ID") -> None:
    """Raise 422 if value is not a valid UUID v4 format."""
    uuid_pattern = re.compile(
        r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
        re.IGNORECASE,
    )
    if not uuid_pattern.match(value):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid {field_name} format",
        )


@router.get(
    "",
    response_model=APIResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"},
    },
)
async def list_favorites(current_user: dict = Depends(get_current_user)):
    """List all favorite signs for the authenticated user.

    Returns favorites with joined sign data, sorted by most recently
    added first.
    """
    try:
        favorites = fetch_user_favorites(current_user["user_id"])
    except Exception as exc:
        logger.error(
            "Failed to fetch favorites for user=%s: %s",
            current_user["user_id"],
            exc,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve favorites",
        )

    return APIResponse(
        success=True,
        data=favorites,
        message=f"Retrieved {len(favorites)} favorite(s)",
    )


@router.post(
    "/{sign_id}",
    response_model=APIResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"},
        409: {"model": ErrorResponse, "description": "Already in favorites"},
        422: {"model": ErrorResponse, "description": "Invalid sign ID"},
    },
)
async def add_to_favorites(
    sign_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Add a sign to the user's favorites.

    Idempotent-ish: if the sign is already a favorite, returns 409
    instead of creating a duplicate.
    """
    _validate_uuid(sign_id, "sign_id")

    try:
        result = add_favorite(
            user_id=current_user["user_id"],
            sign_id=sign_id,
        )
    except Exception as exc:
        error_msg = str(exc).lower()
        # Supabase unique constraint violation
        if "duplicate" in error_msg or "unique" in error_msg or "23505" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Sign is already in your favorites",
            )
        # Foreign key violation -- sign_id does not exist
        if "foreign" in error_msg or "23503" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sign with id '{sign_id}' not found",
            )
        logger.error(
            "Failed to add favorite user=%s sign=%s: %s",
            current_user["user_id"],
            sign_id,
            exc,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to add favorite",
        )

    return APIResponse(
        success=True,
        data={"sign_id": sign_id},
        message="Added to favorites",
    )


@router.delete(
    "/{sign_id}",
    response_model=APIResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"},
        404: {"model": ErrorResponse, "description": "Favorite not found"},
        422: {"model": ErrorResponse, "description": "Invalid sign ID"},
    },
)
async def remove_from_favorites(
    sign_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Remove a sign from the user's favorites.

    Returns 404 if the sign was not in favorites.
    """
    _validate_uuid(sign_id, "sign_id")

    try:
        deleted = remove_favorite(
            user_id=current_user["user_id"],
            sign_id=sign_id,
        )
    except Exception as exc:
        logger.error(
            "Failed to remove favorite user=%s sign=%s: %s",
            current_user["user_id"],
            sign_id,
            exc,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to remove favorite",
        )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sign was not in your favorites",
        )

    return APIResponse(
        success=True,
        data={"sign_id": sign_id},
        message="Removed from favorites",
    )
