"""JWT token management for API authentication."""

import jwt
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional

from api.config import settings


class JWTHandler:
    """Manages JWT token creation and verification."""

    @staticmethod
    def create_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT token.

        Args:
            data: Data to encode in token
            expires_delta: Custom expiration time

        Returns:
            JWT token string
        """
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(hours=settings.jwt_expiration_hours)

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )

        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode a JWT token.

        Args:
            token: JWT token string

        Returns:
            Decoded token data or None if invalid
        """
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None  # Token expired
        except jwt.InvalidTokenError:
            return None  # Invalid token

    @staticmethod
    def get_token_from_header(auth_header: Optional[str]) -> Optional[str]:
        """
        Extract token from Authorization header.

        Args:
            auth_header: Authorization header value (e.g., "Bearer token_here")

        Returns:
            Token string or None
        """
        if not auth_header:
            return None

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None

        return parts[1]
