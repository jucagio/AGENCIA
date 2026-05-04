"""
Common response schemas used across all endpoints.

These enforce the standard API response format that Brook (frontend) expects.
"""

from typing import Any

from pydantic import BaseModel


class PaginationMeta(BaseModel):
    """Pagination metadata included in list responses."""
    page: int = 1
    per_page: int = 20
    total: int = 0
    total_pages: int = 0


class SuccessResponse(BaseModel):
    """Standard success response wrapper."""
    success: bool = True
    data: Any = None
    message: str = "Operation successful"
    pagination: PaginationMeta | None = None


class ErrorDetail(BaseModel):
    """Structured error detail."""
    code: str
    message: str
    fields: dict[str, str] | None = None


class ErrorResponse(BaseModel):
    """Standard error response wrapper."""
    success: bool = False
    error: ErrorDetail
