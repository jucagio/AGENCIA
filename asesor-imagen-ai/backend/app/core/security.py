"""
Security utilities: JWT token creation/validation, password hashing.

⚠️  STATUS: LEGACY (Entrega 0.1).
    Per ADR-001 (Alejo, 2026-04-25), production auth migrates to Supabase Auth
    nativo (ES256 + JWKS). This module is kept compatible during 0.1 → 0.2 to
    avoid breaking imports/tests. In Entrega 0.2 we replace it with
    `app.core.supabase_auth` (JWKS validation), and `password_hash`/bcrypt
    helpers are removed once the `users` table is migrated to `profiles`
    backed by `auth.users`.

Security notes (current legacy implementation):
- Passwords hashed with bcrypt directly (cost factor 12).
  passlib is unmaintained and incompatible with bcrypt>=5.0 (2026).
- JWT uses HS256 with short-lived access tokens + refresh tokens.
- Tokens include 'sub' (user ID), 'exp', and 'type' claims.
- All token validation failures raise AuthenticationError (no info leakage).

See: backend/docs/DECISIONES_PENDIENTES.md
"""

from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

from app.config import get_settings
from app.core.exceptions import AuthenticationError

# bcrypt cost factor (2^12 = 4096 iterations). OWASP recommends >= 10.
_BCRYPT_ROUNDS = 12


def hash_password(password: str) -> str:
    """Hash a plaintext password with bcrypt (cost factor 12)."""
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
    Create a short-lived JWT access token.

    Args:
        subject: User ID (UUID as string).
        extra_claims: Optional additional claims (e.g., role).

    Returns:
        Encoded JWT string.
    """
    settings = get_settings()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": subject,
        "exp": expire,
        "iat": now,
        "type": "access",
        **(extra_claims or {}),
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(subject: str) -> str:
    """
    Create a longer-lived JWT refresh token.

    Args:
        subject: User ID (UUID as string).

    Returns:
        Encoded JWT string.
    """
    settings = get_settings()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)

    payload = {
        "sub": subject,
        "exp": expire,
        "iat": now,
        "type": "refresh",
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str, expected_type: str = "access") -> dict:
    """
    Decode and validate a JWT token.

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
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except JWTError:
        raise AuthenticationError("Invalid or expired token")

    # Validate token type
    if payload.get("type") != expected_type:
        raise AuthenticationError("Invalid token type")

    # Validate subject exists
    if not payload.get("sub"):
        raise AuthenticationError("Invalid token payload")

    return payload
