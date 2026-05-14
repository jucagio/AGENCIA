"""
User service — profile management and account operations.
"""

from __future__ import annotations

import logging
from uuid import UUID

import httpx

from app.config import get_settings
from app.core.admin_client import AdminClient
from app.models.body_analysis import BodyAnalysis
from app.models.profile import Profile
from app.repositories.repos import BodyAnalysisRepository, ProfileRepository
from app.schemas.profile import ProfileUpdateRequest

logger = logging.getLogger(__name__)


class UserService:
    """Profile and account management."""

    def __init__(self, admin: AdminClient) -> None:
        self._profile_repo = ProfileRepository(admin)
        self._body_repo = BodyAnalysisRepository(admin)
        self._settings = get_settings()

    async def get_profile(self, *, user_id: UUID) -> Profile | None:
        """Return the user's profile, or None if not yet created."""
        return await self._profile_repo.get_profile(user_id=user_id)

    async def update_profile(
        self,
        *,
        user_id: UUID,
        update: ProfileUpdateRequest,
    ) -> Profile:
        """Upsert profile data for user_id."""
        data = update.model_dump(exclude_unset=True)
        return await self._profile_repo.upsert_profile(user_id=user_id, data=data)

    async def ensure_profile(self, *, user_id: UUID) -> Profile:
        """Return existing profile or create a minimal one.

        Called after registration to guarantee the profiles row exists.
        """
        existing = await self._profile_repo.get_profile(user_id=user_id)
        if existing:
            return existing
        return await self._profile_repo.upsert_profile(user_id=user_id, data={})

    async def delete_account(self, *, user_id: UUID) -> None:
        """
        Soft-delete the user's profile and request Supabase Auth deletion.

        The Supabase Auth deletion is done via the Admin REST API (service role).
        Profiles get deleted_at set; the auth.users row is removed by Supabase.

        Note: In dev (no SUPABASE_URL), the GoTrue call is skipped gracefully.
        """
        from datetime import datetime, timezone  # noqa: PLC0415

        # Soft-delete the profile
        try:
            await self._profile_repo.upsert_profile(
                user_id=user_id,
                data={"deleted_at": datetime.now(timezone.utc).isoformat()},
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning("Profile soft-delete failed for %s: %s", user_id, exc)

        # Request Supabase Auth deletion (Admin API)
        settings = self._settings
        if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_ROLE_KEY:
            logger.warning("Skipping Supabase Auth user deletion — not configured")
            return

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.delete(
                    f"{settings.SUPABASE_URL}/auth/v1/admin/users/{user_id}",
                    headers={
                        "apikey": settings.SUPABASE_SERVICE_ROLE_KEY,
                        "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY}",
                    },
                )
            if resp.status_code not in (200, 204):
                logger.warning(
                    "Supabase Auth user deletion returned %s for %s",
                    resp.status_code,
                    user_id,
                )
        except httpx.HTTPError as exc:
            logger.error("Supabase Auth user deletion failed for %s: %s", user_id, exc)

    async def get_body_analysis(self, *, user_id: UUID) -> BodyAnalysis | None:
        """Return the latest body analysis for user_id."""
        return await self._body_repo.get_latest(user_id=user_id)
