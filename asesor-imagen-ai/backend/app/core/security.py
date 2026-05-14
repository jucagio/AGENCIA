"""
Security utilities: password hashing + legacy JWT helpers.

⚠️  STATUS: PARTIALLY LEGACY (Entrega 0.1 → 0.3).

Per ADR-001: production auth is now Supabase Auth (see app.core.supabase_auth).
bcrypt helpers are kept here because:
  1. test_security.py tests them and they cover the legacy migration path.
  2. They are called by nothing in the auth flow — Supabase handles passwords.
     Kept to avoid test breakage until the legacy tests are retired in 0.4.

The jwt functions (create_access_token, create_refresh_token, decode_token)
are kept for the legacy test suite only. New code MUST NOT use them.

REPLACED: python-jose (CVE-2024-33664, CVE-2024-33663) → PyJWT[crypto]
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt as pyjwt
from jwt import DecodeError, ExpiredSignatureError, InvalidTokenError

from app.config import get_settings
from app.core.exceptions import AuthenticationError

# bcrypt cost factor. OWASP 2026 recommends >= 12; we use 13.
_BCRYPT_ROUNDS = 13


def hash_password(password: str) -> str:
    """Hash a plaintext password with bcrypt (cost factor 13)."""
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=_BCRYPT_ROUNDS)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a bcrypt hash."""
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
    except (ValueError, TypeError):
        return False


def create_access_token(subject: str, extra_claims: dict | None = None) -> str:
    """
    Create a short-lived JWT access token (LEGACY — used in tests only).

    Args:
        subject: User ID (UUID as string).
        extra_claims: Optional additional claims (e.g., role).

    Returns:
        Encoded JWT string (HS256).
    """
    settings = get_settings()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    payload: dict[str, object] = {
        "sub": subject,
        "exp": expire,
        "iat": now,
        "type": "access",
        **(extra_claims or {}),
    }

    return pyjwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_refresh_token(subject: str) -> str:
    """
    Create a longer-lived JWT refresh token (LEGACY — used in tests only).

    Args:
        subject: User ID (UUID as string).

    Returns:
        Encoded JWT string (HS256).
    """
    settings = get_settings()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)

    payload: dict[str, object] = {
        "sub": subject,
        "exp": expire,
        "iat": now,
        "type": "refresh",
    }

    return pyjwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_token(token: str, expected_type: str = "access") -> dict:  # type: ignore[type-arg]
    """
    Decode and validate a JWT token (LEGACY — used in tests only).

    Args:
        token: The JWT string.
        expected_type: Expected token type ('access' or 'refresh').

    Returns:
        Decoded payload dict.

    Raises:
        AuthenticationError: If token is invalid, expired, or wrong type.
    """
    settings = get_settings()

    try:
        payload: dict[str, object] = pyjwt.decode(  # type: ignore[assignment]
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except (ExpiredSignatureError, DecodeError, InvalidTokenError) as exc:
        raise AuthenticationError("Invalid or expired token") from exc

    if payload.get("type") != expected_type:
        raise AuthenticationError("Invalid token type")

    if not payload.get("sub"):
        raise AuthenticationError("Invalid token payload")

    return payload
