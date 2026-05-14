"""
Recommendation service — Claude AI-powered outfit recommendations.

Sprint 0.3: Claude call is stubbed. Full pipeline in Sprint 0.5.
"""

from __future__ import annotations

import logging
from uuid import UUID

from app.core.admin_client import AdminClient
from app.models.recommendation import Recommendation
from app.repositories.repos import (
    RecommendationItemRepository,
    RecommendationRepository,
    UsageCounterRepository,
)

logger = logging.getLogger(__name__)

FREE_RECOMMENDATION_CAP = 10  # per month


class RecommendationService:
    """AI outfit recommendation management."""

    def __init__(self, admin: AdminClient) -> None:
        self._repo = RecommendationRepository(admin)
        self._item_repo = RecommendationItemRepository(admin)
        self._usage_repo = UsageCounterRepository(admin)

    async def generate_recommendations(
        self,
        *,
        user_id: UUID,
        occasion: str = "casual",
        season: str | None = None,
    ) -> dict:  # type: ignore[type-arg]
        """
        Generate AI outfit recommendations for user_id.

        Sprint 0.3 stub: creates a recommendation row, enqueues claude_worker.
        Sprint 0.5: direct Claude API integration within worker.

        Returns:
            {recommendation_id, status: "pending"}
        """
        # Usage cap check
        counter = await self._usage_repo.get_current_period(user_id=user_id)
        if counter and counter.recommendations_used >= FREE_RECOMMENDATION_CAP:
            from app.core.exceptions import ValidationError  # noqa: PLC0415
            raise ValidationError(
                message="Monthly recommendation limit reached. Upgrade to continue.",
                fields={"limit": str(FREE_RECOMMENDATION_CAP)},
            )

        # Create recommendation record
        from app.config import get_settings  # noqa: PLC0415
        settings = get_settings()

        data: dict[str, object] = {
            "occasion": occasion,
            "season": season,
            "claude_model_version": settings.ANTHROPIC_MODEL,
            "prompt_version": "0.3.0-stub",
        }
        reco = await self._repo.create(user_id=user_id, data=data)

        # Increment usage counter
        try:
            await self._usage_repo.increment(
                user_id=user_id, field="recommendations_used"
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning("Usage counter increment failed: %s", exc)

        # TODO(Sprint 0.5): enqueue claude_worker
        # await arq_pool.enqueue_job("generate_reco_claude", str(user_id), str(reco.id))

        logger.info("Recommendation queued: reco_id=%s user_id=%s", reco.id, user_id)

        return {
            "recommendation_id": str(reco.id),
            "status": "pending",
            "message": "Generating recommendations. Poll GET /recommendations/{id}.",
        }

    async def get_recommendations(
        self, *, user_id: UUID, page: int = 1, size: int = 20
    ) -> tuple[list[Recommendation], int]:
        """Return paginated recommendation history."""
        return await self._repo.list_for_user(user_id=user_id, page=page, per_page=size)

    async def get_recommendation(
        self, *, user_id: UUID, recommendation_id: UUID
    ) -> Recommendation:
        """Return a specific recommendation."""
        return await self._repo.get_by_id(user_id=user_id, record_id=recommendation_id)

    async def record_feedback(
        self,
        *,
        user_id: UUID,
        recommendation_id: UUID,
        clicked: bool | None = None,
        liked: bool | None = None,
        tried_on: bool | None = None,
    ) -> Recommendation:
        """Record engagement feedback on a recommendation."""
        return await self._repo.record_feedback(
            user_id=user_id,
            recommendation_id=recommendation_id,
            clicked=clicked,
            liked=liked,
            tried_on=tried_on,
        )
