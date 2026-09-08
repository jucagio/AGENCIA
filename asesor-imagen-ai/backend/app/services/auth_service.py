"""
Auth service — wraps Supabase GoTrue REST API.

ADR-001: usamos Supabase Auth nativo. No tabla users propia, no bcrypt en auth path.
Calls GoTrue endpoints:
  POST /auth/v1/signup
  POST /auth/v1/token?grant_type=password
  POST /auth/v1/token?grant_type=refresh_token

References:
  https://supabase.com/docs/reference/javascript/auth-signinwithpassword
"""

from __future__ import annotations

import logging

import httpx

from app.config import get_settings
from app.core.exceptions import AuthenticationError
from app.core.exceptions import ValidationError as AppValidationError
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse

logger = logging.getLogger(__name__)


class AuthService:
    """Wraps Supabase GoTrue REST API for auth operations.

    When SUPABASE_URL is empty and ENVIRONMENT != production, delegates to
    MockAuthService so local MVP testing works without a Supabase project.
    """

    def __init__(self) -> None:
        self._settings = get_settings()
        self._mock = None
        if not self._settings.SUPABASE_URL:
            if self._settings.is_production:
                raise RuntimeError(
                    "SUPABASE_URL is required in production. "
                    "Refusing to start AuthService."
                )
            # Lazy import to avoid circular dependency at module load time.
            from app.services.mock_auth_service import MockAuthService  # noqa: PLC0415
            self._mock = MockAuthService()
            self._base = ""
            self._headers = {}
            return
        self._base = f"{self._settings.SUPABASE_URL}/auth/v1"
        self._headers = {
            "apikey": self._settings.SUPABASE_ANON_KEY,
            "Content-Type": "application/json",
        }

    async def register(self, req: RegisterRequest) -> TokenResponse:
        """Register a new user via Supabase GoTrue /signup.

        Returns a TokenResponse on success (201 from GoTrue).
        Raises AppValidationError on duplicate email or weak password.
        """
        if self._mock is not None:
            return await self._mock.register(req)
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"{self._base}/signup",
                json={"email": req.email, "password": req.password},
                headers=self._headers,
            )

        if resp.status_code not in (200, 201):
            data = resp.json()
            msg: str = data.get("msg") or data.get("message") or "Registration failed"
            raise AppValidationError(message=msg, fields={"email": msg})

        return self._to_token_response(resp.json())

    async def login(self, req: LoginRequest) -> TokenResponse:
        """Authenticate via Supabase GoTrue password grant."""
        if self._mock is not None:
            return await self._mock.login(req)
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"{self._base}/token?grant_type=password",
                json={"email": req.email, "password": req.password},
                headers=self._headers,
            )

        if resp.status_code != 200:
            raise AuthenticationError("Invalid email or password")

        return self._to_token_response(resp.json())

    async def refresh(self, refresh_token: str) -> TokenResponse:
        """Exchange a refresh_token for a new access_token."""
        if self._mock is not None:
            return await self._mock.refresh(refresh_token)
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"{self._base}/token?grant_type=refresh_token",
                json={"refresh_token": refresh_token},
                headers=self._headers,
            )

        if resp.status_code != 200:
            raise AuthenticationError("Invalid or expired refresh token")

        return self._to_token_response(resp.json())

    @staticmethod
    def _to_token_response(data: dict) -> TokenResponse:  # type: ignore[type-arg]
        """Map GoTrue response dict to TokenResponse schema."""
        user = data.get("user") or {}
        return TokenResponse(
            access_token=data["access_token"],
            token_type="bearer",
            refresh_token=data.get("refresh_token", ""),
            expires_in=data.get("expires_in", 3600),
            user_id=str(user.get("id", "")),
        )
