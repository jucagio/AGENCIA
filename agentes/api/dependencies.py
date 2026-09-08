"""Dependency injection for API endpoints."""

from fastapi import Depends, HTTPException, status, Header
from typing import Optional

from api.security.jwt import JWTHandler
from api.security.permissions import PermissionChecker, ROLE_PERMISSIONS


async def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    """
    Dependency to get current user from JWT token.

    Args:
        authorization: Authorization header

    Returns:
        User data from token

    Raises:
        HTTPException if token is invalid or missing
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = JWTHandler.get_token_from_header(authorization)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format. Use 'Bearer <token>'",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = JWTHandler.verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing user identifier",
        )

    return {
        "user_id": user_id,
        "role": payload.get("role", "viewer"),
        "permissions": payload.get("permissions", []),
    }


def require_permission(required_permission: str):
    """
    Dependency factory to check permissions.

    Args:
        required_permission: Permission required (e.g., "agents:execute")

    Returns:
        Dependency function
    """

    async def permission_checker(current_user: dict = Depends(get_current_user)) -> dict:
        """Check if user has required permission."""
        user_role = current_user.get("role", "viewer")

        if not PermissionChecker.check_permission(user_role, required_permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User role '{user_role}' lacks permission '{required_permission}'",
            )

        return current_user

    return permission_checker
