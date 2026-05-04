"""
Tests for security utilities: JWT and password hashing.
"""

import pytest

from app.core.exceptions import AuthenticationError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)


class TestPasswordHashing:
    def test_hash_and_verify(self):
        """Hashed password should verify against original."""
        password = "SecureP@ss123"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True

    def test_wrong_password_fails(self):
        """Wrong password should not verify."""
        hashed = hash_password("correct-password")
        assert verify_password("wrong-password", hashed) is False

    def test_hash_is_not_plaintext(self):
        """Hash should never equal the plaintext password."""
        password = "MyPassword123"
        hashed = hash_password(password)
        assert hashed != password


class TestJWT:
    def test_create_and_decode_access_token(self):
        """Access token should round-trip correctly."""
        user_id = "550e8400-e29b-41d4-a716-446655440000"
        token = create_access_token(user_id)
        payload = decode_token(token, expected_type="access")
        assert payload["sub"] == user_id
        assert payload["type"] == "access"

    def test_create_and_decode_refresh_token(self):
        """Refresh token should round-trip correctly."""
        user_id = "550e8400-e29b-41d4-a716-446655440000"
        token = create_refresh_token(user_id)
        payload = decode_token(token, expected_type="refresh")
        assert payload["sub"] == user_id
        assert payload["type"] == "refresh"

    def test_access_token_rejected_as_refresh(self):
        """Access token should fail when decoded as refresh."""
        token = create_access_token("some-user-id")
        with pytest.raises(AuthenticationError):
            decode_token(token, expected_type="refresh")

    def test_refresh_token_rejected_as_access(self):
        """Refresh token should fail when decoded as access."""
        token = create_refresh_token("some-user-id")
        with pytest.raises(AuthenticationError):
            decode_token(token, expected_type="access")

    def test_invalid_token_raises_error(self):
        """Garbage token should raise AuthenticationError."""
        with pytest.raises(AuthenticationError):
            decode_token("not.a.valid.token")

    def test_extra_claims_in_access_token(self):
        """Extra claims should be included in the token payload."""
        token = create_access_token("user-123", extra_claims={"role": "admin"})
        payload = decode_token(token, expected_type="access")
        assert payload["role"] == "admin"
