"""
Supabase Auth JWKS validator (ADR-001).

Fetches JWKS from Supabase, caches with TTL, validates ES256/RS256 tokens.
Replaces legacy python-jose (CVE-2024-33664, CVE-2024-33663).

References:
  https://supabase.com/docs/guides/auth/jwks
  https://pyjwt.readthedocs.io/en/stable/usage.html#retrieve-rsa-signing-keys-from-a-jwks-endpoint

Security notes:
  - Tokens must carry aud="authenticated" (Supabase default).
  - exp validation is always enforced (options["verify_exp"]=True).
  - sub claim must be present and non-empty (= auth.users.id).
  - We log validation failures at WARNING with no token content (PII-safe).
"""

from __future__ import annotations

import logging
import time

from jwt import DecodeError, ExpiredSignatureError, InvalidTokenError, PyJWKClient
from jwt import decode as jwt_decode

from app.config import get_settings
from app.core.exceptions import AuthenticationError

logger = logging.getLogger(__name__)

# Module-level JWKS client — cached internally by PyJWKClient.
_jwks_client: PyJWKClient | None = None
_jwks_last_refresh: float = 0.0


def _get_jwks_client() -> PyJWKClient:
    """Return a (re)initialized PyJWKClient, refreshing if TTL expired.

    Thread-safety: in asyncio there is no true concurrency here, so a simple
    module-level variable is safe. A race between two coroutines is benign —
    both would create equivalent clients.
    """
    global _jwks_client, _jwks_last_refresh  # noqa: PLW0603
    settings = get_settings()
    ttl = settings.SUPABASE_JWKS_CACHE_TTL_SECONDS
    now = time.monotonic()

    if _jwks_client is None or (now - _jwks_last_refresh) > ttl:
        jwks_url = settings.supabase_jwks_url
        if not jwks_url:
            raise AuthenticationError(
                "SUPABASE_URL not configured — cannot fetch JWKS"
            )
        _jwks_client = PyJWKClient(
            jwks_url,
            cache_jwk_set=True,
            lifespan=ttl,
        )
        _jwks_last_refresh = now
        logger.debug("JWKS client (re)initialized for %s", jwks_url)

    return _jwks_client


def validate_supabase_token(token: str) -> dict:  # type: ignore[type-arg]
    """
    Validate a Supabase-issued JWT against JWKS.

    Args:
        token: Raw Bearer token string (without the "Bearer " prefix).

    Returns:
        Decoded payload dict with:
          - 'sub': user UUID string (= auth.users.id)
          - 'role': "authenticated"
          - 'aud': "authenticated"
          - 'email': user email (optional — may be absent for OAuth)
          - 'exp', 'iat', 'iss': standard claims

    Raises:
        AuthenticationError: if token is missing, expired, signature invalid,
                             or sub claim is absent.
    """
    if not token:
        raise AuthenticationError("Authorization token missing")

    settings = get_settings()

    try:
        client = _get_jwks_client()
        signing_key = client.get_signing_key_from_jwt(token)
        payload: dict[str, object] = jwt_decode(  # type: ignore[assignment]
            token,
            signing_key.key,
            algorithms=["ES256", "RS256"],
            audience=settings.SUPABASE_JWT_AUDIENCE,
            options={"verify_exp": True},
        )
    except ExpiredSignatureError as exc:
        logger.warning("JWT validation failed: token expired")
        raise AuthenticationError("Token has expired") from exc
    except (DecodeError, InvalidTokenError) as exc:
        logger.warning("JWT validation failed: %s", type(exc).__name__)
        raise AuthenticationError(f"Invalid token: {exc}") from exc
    except AuthenticationError:
        raise
    except Exception as exc:  # noqa: BLE001
        # Covers network failures fetching JWKS (transient)
        logger.warning("JWKS fetch/validation error: %s", exc)
        raise AuthenticationError("Token validation unavailable") from exc

    sub = payload.get("sub")
    if not sub:
        raise AuthenticationError("Invalid token: missing sub claim")

    return payload  # type: ignore[return-value]


def reset_jwks_client() -> None:
    """Reset cached JWKS client — used in tests to force re-initialization."""
    global _jwks_client, _jwks_last_refresh  # noqa: PLW0603
    _jwks_client = None
    _jwks_last_refresh = 0.0
