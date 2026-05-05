"""
Custom exception classes and global exception handlers.

Security note: Error responses to the client are generic.
Detailed error info goes to server logs only.
"""

import logging
from typing import Any

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Custom Exceptions
# ---------------------------------------------------------------------------

class AppException(Exception):
    """Base exception for application-level errors."""

    def __init__(
        self,
        message: str = "An internal error occurred",
        code: str = "INTERNAL_ERROR",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: dict[str, Any] | None = None,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(AppException):
    def __init__(self, message: str = "Validation failed", fields: dict[str, str] | None = None):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details={"fields": fields or {}},
        )


class NotFoundError(AppException):
    def __init__(self, resource: str = "Resource"):
        super().__init__(
            message=f"{resource} not found",
            code="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class AuthenticationError(AppException):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            code="AUTHENTICATION_ERROR",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class AuthorizationError(AppException):
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(
            message=message,
            code="AUTHORIZATION_ERROR",
            status_code=status.HTTP_403_FORBIDDEN,
        )


class PermissionDeniedError(AppException):
    """Raised when code tries to bypass the AdminClient guard."""

    def __init__(self, message: str = "Permission denied"):
        super().__init__(
            message=message,
            code="PERMISSION_DENIED",
            status_code=status.HTTP_403_FORBIDDEN,
        )


class RateLimitError(AppException):
    def __init__(self):
        super().__init__(
            message="Too many requests. Please try again later.",
            code="RATE_LIMIT_EXCEEDED",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        )


# ---------------------------------------------------------------------------
# Exception Handlers (registered in main.py)
# ---------------------------------------------------------------------------

async def app_exception_handler(_request: Request, exc: AppException) -> JSONResponse:
    """Handle application-level exceptions with structured response."""
    logger.warning(
        "AppException: code=%s message=%s details=%s",
        exc.code,
        exc.message,
        exc.details,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message,
                **({"fields": exc.details["fields"]} if "fields" in exc.details else {}),
            },
        },
    )


async def http_exception_handler(_request: Request, exc: HTTPException) -> JSONResponse:
    """Handle FastAPI HTTPException with our standard format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "HTTP_ERROR",
                "message": str(exc.detail),
            },
        },
    )


async def unhandled_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    """
    Catch-all for unhandled exceptions.

    Security: Never expose internal error details to the client.
    Log the full traceback server-side.
    """
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred. Please try again later.",
            },
        },
    )
