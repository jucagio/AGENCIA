"""Sign language signs endpoints.

Public endpoints for browsing, searching, and translating text
into sequences of sign language signs. No authentication required
for reading; translation logs require auth.

SECURITY:
- All query parameters validated by Pydantic
- Supabase client uses parameterized queries (no SQL injection)
- Pagination capped at 50 items to prevent abuse
"""

import logging
import re

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.db.supabase import (
    fetch_sign_by_id,
    fetch_signs_by_words,
    fetch_signs_paginated,
    log_translation,
    search_signs,
)
from app.dependencies import get_current_user, get_current_user_optional
from app.models.schemas import (
    APIResponse,
    ErrorResponse,
    PaginatedResponse,
    SignTranslateRequest,
    SignTranslateResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/signs", tags=["signs"])

# Maximum page size to prevent large queries
MAX_PAGE_SIZE = 50


@router.get(
    "",
    response_model=PaginatedResponse,
)
async def list_signs(
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=20, ge=1, le=MAX_PAGE_SIZE, description="Items per page"),
    language_code: str = Query(default="co-csn", description="Sign language variant"),
):
    """List signs with pagination.

    Returns a paginated list of all available signs sorted alphabetically.
    No authentication required -- this is a public catalog.
    """
    try:
        result = fetch_signs_paginated(
            page=page,
            page_size=page_size,
            language_code=language_code,
        )
    except Exception as exc:
        logger.error("Failed to fetch signs: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve signs",
        )

    total = result["count"]
    total_pages = (total + page_size - 1) // page_size if total > 0 else 0

    return PaginatedResponse(
        success=True,
        data=result["data"],
        message="Signs retrieved",
        pagination={
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages,
        },
    )


@router.get(
    "/search",
    response_model=APIResponse,
    responses={
        422: {"model": ErrorResponse, "description": "Invalid search query"},
    },
)
async def search_signs_endpoint(
    q: str = Query(
        ...,
        min_length=1,
        max_length=200,
        description="Search term (partial match on word)",
    ),
    language_code: str = Query(default="co-csn", description="Sign language variant"),
):
    """Search signs by word.

    Performs a case-insensitive partial match on the sign word field.
    Returns up to 50 results sorted alphabetically.
    No authentication required.
    """
    # Sanitize: strip whitespace, limit to alphanumeric + spaces + accents
    q_clean = q.strip()
    if not q_clean:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Search query cannot be empty",
        )

    try:
        results = search_signs(query=q_clean, language_code=language_code)
    except Exception as exc:
        logger.error("Search failed for q=%s: %s", q_clean, exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Search failed",
        )

    return APIResponse(
        success=True,
        data=results,
        message=f"Found {len(results)} sign(s) matching '{q_clean}'",
    )


@router.get(
    "/{sign_id}",
    response_model=APIResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Sign not found"},
    },
)
async def get_sign(sign_id: str):
    """Get detailed information about a single sign.

    Returns the sign with all related video files.
    No authentication required.
    """
    # Basic UUID format validation
    uuid_pattern = re.compile(
        r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
        re.IGNORECASE,
    )
    if not uuid_pattern.match(sign_id):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid sign ID format",
        )

    try:
        sign = fetch_sign_by_id(sign_id)
    except Exception as exc:
        logger.error("Failed to fetch sign %s: %s", sign_id, exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve sign",
        )

    if not sign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sign with id '{sign_id}' not found",
        )

    return APIResponse(
        success=True,
        data=sign,
        message="Sign retrieved",
    )


@router.post(
    "/translate",
    response_model=APIResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Authentication required"},
    },
)
async def translate_text(
    body: SignTranslateRequest,
    current_user: dict = Depends(get_current_user),
):
    """Translate text into a sequence of sign language signs.

    Splits the input text into individual words, looks up each word
    in the signs database, and returns the ordered list of matching
    signs along with any words that have no sign equivalent.

    Requires authentication so that translations can be logged for
    analytics and personalization.
    """
    # Tokenize: split on whitespace and punctuation, lowercase, deduplicate order
    raw_words = re.split(r"[^\w]+", body.text.lower().strip())
    words = [w for w in raw_words if w]  # remove empty strings

    if not words:
        return APIResponse(
            success=True,
            data={
                "input_text": body.text,
                "words": [],
                "matched_signs": [],
                "unmatched_words": [],
            },
            message="No translatable words found in input",
        )

    try:
        matched_signs = fetch_signs_by_words(
            words=words,
            language_code=body.language_code,
        )
    except Exception as exc:
        logger.error("Translation lookup failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Translation failed",
        )

    # Build a lookup for matched words
    matched_words_set = {sign["word"].lower() for sign in matched_signs}
    unmatched = [w for w in words if w not in matched_words_set]

    # Order matched signs in the same order as input words
    sign_lookup = {sign["word"].lower(): sign for sign in matched_signs}
    ordered_signs = []
    for w in words:
        if w in sign_lookup:
            ordered_signs.append(sign_lookup[w])

    # Log translation for analytics (non-blocking -- don't fail if logging fails)
    try:
        log_translation(
            user_id=current_user["user_id"],
            input_text=body.text,
            signs_matched=[s["id"] for s in ordered_signs],
        )
    except Exception as exc:
        logger.warning("Translation logging failed: %s", exc)

    response_data = {
        "input_text": body.text,
        "words": words,
        "matched_signs": ordered_signs,
        "unmatched_words": unmatched,
    }

    return APIResponse(
        success=True,
        data=response_data,
        message=f"Translated {len(ordered_signs)}/{len(words)} words",
    )
