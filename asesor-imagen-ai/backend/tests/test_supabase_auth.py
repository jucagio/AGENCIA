"""
Tests for Supabase Auth JWKS validator (app/core/supabase_auth.py).

All external calls are mocked — no live Supabase connection required.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from app.core.exceptions import AuthenticationError
from app.core.supabase_auth import reset_jwks_client, validate_supabase_token


class TestValidateSupabaseToken:
    """Tests for validate_supabase_token()."""

    def setup_method(self) -> None:
        reset_jwks_client()

    def test_empty_token_raises(self) -> None:
        with pytest.raises(AuthenticationError, match="missing"):
            validate_supabase_token("")

    def test_none_like_raises(self) -> None:
        with pytest.raises(AuthenticationError):
            validate_supabase_token("   ")

    def test_missing_sub_raises(self) -> None:
        mock_key = MagicMock()
        mock_key.key = "mock"
        mock_client = MagicMock()
        mock_client.get_signing_key_from_jwt.return_value = mock_key

        with patch("app.core.supabase_auth._get_jwks_client", return_value=mock_client), \
             patch("app.core.supabase_auth.jwt_decode", return_value={"role": "authenticated"}):
            with pytest.raises(AuthenticationError, match="sub"):
                validate_supabase_token("valid.looking.token")

    def test_expired_token_raises(self) -> None:
        from jwt import ExpiredSignatureError

        mock_client = MagicMock()
        mock_client.get_signing_key_from_jwt.side_effect = ExpiredSignatureError("expired")

        with patch("app.core.supabase_auth._get_jwks_client", return_value=mock_client):
            with pytest.raises(AuthenticationError, match="expired"):
                validate_supabase_token("expired.token")

    def test_invalid_token_raises(self) -> None:
        from jwt import DecodeError

        mock_client = MagicMock()
        mock_client.get_signing_key_from_jwt.side_effect = DecodeError("bad token")

        with patch("app.core.supabase_auth._get_jwks_client", return_value=mock_client):
            with pytest.raises(AuthenticationError, match="Invalid"):
                validate_supabase_token("bad.token")

    def test_valid_token_returns_payload(self) -> None:
        from uuid import uuid4

        user_id = str(uuid4())
        payload = {"sub": user_id, "role": "authenticated", "aud": "authenticated"}

        mock_key = MagicMock()
        mock_key.key = "mock-key"
        mock_client = MagicMock()
        mock_client.get_signing_key_from_jwt.return_value = mock_key

        with patch("app.core.supabase_auth._get_jwks_client", return_value=mock_client), \
             patch("app.core.supabase_auth.jwt_decode", return_value=payload):
            result = validate_supabase_token("valid.token")

        assert result["sub"] == user_id
        assert result["role"] == "authenticated"

    def test_no_supabase_url_raises(self) -> None:
        """Without SUPABASE_URL, JWKS client raises AuthenticationError."""
        reset_jwks_client()
        with patch("app.core.supabase_auth.get_settings") as mock_settings:
            s = MagicMock()
            s.supabase_jwks_url = ""
            s.SUPABASE_JWKS_CACHE_TTL_SECONDS = 600
            mock_settings.return_value = s
            with pytest.raises(AuthenticationError, match="SUPABASE_URL"):
                validate_supabase_token("some.token")
