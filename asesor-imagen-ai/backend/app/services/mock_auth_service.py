"""
Mock Auth service — local-only HS256 JWT issuer.

Activated when SUPABASE_URL is empty AND ENVIRONMENT != production.
Replaces calls to Supabase GoTrue with locally-signed tokens using SECRET_KEY.

Purpose:
    Unblock end-to-end MVP testing on developer laptops without requiring a
    Supabase project to be provisioned. The mock issues real JWTs (HS256) that
    the auth middleware can validate locally — same sub/aud/exp shape as
    Supabase tokens.

Security:
    - Issuer is hard-coded to "mock-local" — production token validation refuses
      this issuer (see supabase_auth.validate_supabase_token guard).
    - Refused entirely when ENVIRONMENT=production. Fail-closed at AuthService.
    - User records are kept in an in-memory dict — wiped on restart. Password is
      stored as a salted bcrypt-like hash (hashlib.scrypt, stdlib-only).
    - No PII is logged.
"""

from __future__ import annotations

import hashlib
import hmac
import logging
import os
import time
import uuid
from typing import Any

import jwt as pyjwt

from app.config import get_settings
from app.core.exceptions import AuthenticationError
from app.core.exceptions import ValidationError as AppValidationError
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse

logger = logging.getLogger(__name__)

MOCK_ISSUER = "mock-local"

# In-memory user store {email_lower: {"id": uuid, "password_hash": bytes, "salt": bytes}}
_USERS: dict[str, dict[str, Any]] = {}

# Refresh token store {refresh_token: user_id}
_REFRESH_TOKENS: dict[str, str] = {}


def _hash_password(password: str, salt: bytes) -> bytes:
    """Scrypt-based password hashing — stdlib only, OWASP-compliant params."""
    return hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=2**14,  # CPU/memory cost
        r=8,
        p=1,
        dklen=64,
    )


def _verify_password(password: str, salt: bytes, expected: bytes) -> bool:
    return hmac.compare_digest(_hash_password(password, salt), expected)


def _issue_tokens(user_id: str, email: str) -> TokenResponse:
    """Issue an HS256 access token + opaque refresh token."""
    settings = get_settings()
    now = int(time.time())
    access_payload = {
        "sub": user_id,
        "email": email,
        "aud": settings.SUPABASE_JWT_AUDIENCE,
        "role": "authenticated",
        "iss": MOCK_ISSUER,
        "iat": now,
        "exp": now + settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }
    access_token = pyjwt.encode(
        access_payload, settings.SECRET_KEY, algorithm="HS256"
    )

    refresh_token = uuid.uuid4().hex + uuid.uuid4().hex  # 64-char opaque
    _REFRESH_TOKENS[refresh_token] = user_id

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token,
        expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user_id=user_id,
    )


def is_mock_token(token: str) -> bool:
    """Cheap check — decode without verification to inspect iss claim."""
    try:
        unverified = pyjwt.decode(token, options={"verify_signature": False})
        return unverified.get("iss") == MOCK_ISSUER
    except Exception:  # noqa: BLE001
        return False


def validate_mock_token(token: str) -> dict[str, Any]:
    """Validate a mock HS256 token. Raises AuthenticationError on failure."""
    settings = get_settings()
    if settings.is_production:
        raise AuthenticationError("Mock tokens are not accepted in production")
    try:
        payload = pyjwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
            audience=settings.SUPABASE_JWT_AUDIENCE,
            issuer=MOCK_ISSUER,
            options={"verify_exp": True, "require": ["sub", "exp", "iat"]},
        )
    except pyjwt.ExpiredSignatureError as exc:
        raise AuthenticationError("Token has expired") from exc
    except pyjwt.InvalidTokenError as exc:
        raise AuthenticationError(f"Invalid mock token: {exc}") from exc

    if not payload.get("sub"):
        raise AuthenticationError("Invalid token: missing sub claim")
    return payload


class MockAuthService:
    """Drop-in replacement for AuthService when SUPABASE_URL is empty."""

    def __init__(self) -> None:
        settings = get_settings()
        if settings.is_production:
            # Hard guard. This class must NEVER be instantiable in prod.
            raise RuntimeError(
                "MockAuthService is forbidden in production. Configure SUPABASE_URL."
            )
        logger.warning(
            "Using MockAuthService — local-only. Configure SUPABASE_URL for real auth."
        )

    async def register(self, req: RegisterRequest) -> TokenResponse:
        email_lower = req.email.lower()
        if email_lower in _USERS:
            raise AppValidationError(
                message="User already registered",
                fields={"email": "already exists"},
            )
        salt = os.urandom(16)
        password_hash = _hash_password(req.password, salt)
        user_id = str(uuid.uuid4())
        _USERS[email_lower] = {
            "id": user_id,
            "email": req.email,
            "salt": salt,
            "password_hash": password_hash,
        }
        logger.info("MockAuth: registered user_id=%s", user_id)
        return _issue_tokens(user_id, req.email)

    async def login(self, req: LoginRequest) -> TokenResponse:
        email_lower = req.email.lower()
        record = _USERS.get(email_lower)
        if record is None:
            raise AuthenticationError("Invalid email or password")
        if not _verify_password(req.password, record["salt"], record["password_hash"]):
            raise AuthenticationError("Invalid email or password")
        return _issue_tokens(record["id"], record["email"])

    async def refresh(self, refresh_token: str) -> TokenResponse:
        user_id = _REFRESH_TOKENS.pop(refresh_token, None)
        if user_id is None:
            raise AuthenticationError("Invalid or expired refresh token")
        # Find email for the user_id
        email = next(
            (rec["email"] for rec in _USERS.values() if rec["id"] == user_id),
            None,
        )
        if email is None:
            raise AuthenticationError("User no longer exists")
        return _issue_tokens(user_id, email)
