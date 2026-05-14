"""
Body Analysis service — vision-based body type + color season analysis.

Sprint 0.3: stub pipeline. Enqueues vision_worker via ARQ.
Sprint 0.5: integrates Google Vision API + custom body type model.
"""

from __future__ import annotations

import logging
from uuid import UUID

from app.core.admin_client import AdminClient
from app.models.body_analysis import BodyAnalysis
from app.repositories.repos import BodyAnalysisRepository, UsageCounterRepository

logger = logging.getLogger(__name__)

# Free tier cap for body analyses per month
FREE_BODY_ANALYSIS_CAP = 3


class BodyAnalysisService:
    """Manages body analysis creation and retrieval."""

    def __init__(self, admin: AdminClient) -> None:
        self._repo = BodyAnalysisRepository(admin)
        self._usage_repo = UsageCounterRepository(admin)

    async def create_analysis(
        self,
        *,
        user_id: UUID,
        image_bytes: bytes | None = None,
        image_url: str | None = None,
    ) -> dict:  # type: ignore[type-arg]
        """
        Queue a body analysis job.

        Verifies monthly usage cap (ADR-007 free tier).
        Returns {analysis_id, status: "pending", job_id}.

        Sprint 0.3: creates the DB row immediately as "pending",
        enqueues vision_worker stub.
        Sprint 0.5: real Vision API integration.
        """
        # Check usage cap
        counter = await self._usage_repo.get_current_period(user_id=user_id)
        if counter and counter.body_analyses_used >= FREE_BODY_ANALYSIS_CAP:
            from app.core.exceptions import ValidationError  # noqa: PLC0415
            raise ValidationError(
                message="Monthly body analysis limit reached. Upgrade to continue.",
                fields={"limit": str(FREE_BODY_ANALYSIS_CAP)},
            )

        # Create pending analysis record
        data: dict[str, object] = {
            "status": "pending" if not image_url else "processing",
        }
        if image_url:
            data["image_url"] = image_url

        analysis = await self._repo.create(user_id=user_id, data=data)

        # Increment usage counter
        try:
            await self._usage_repo.increment(
                user_id=user_id, field="body_analyses_used"
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning("Usage counter increment failed: %s", exc)

        # TODO(Sprint 0.5): enqueue vision_worker
        # await arq_pool.enqueue_job("vision_analyze_body", str(analysis.id), image_url or "")

        logger.info("Body analysis queued: analysis_id=%s user_id=%s", analysis.id, user_id)

        return {
            "analysis_id": str(analysis.id),
            "status": "pending",
            "job_id": f"stub-{analysis.id}",
            "message": "Analysis queued. Poll GET /body-analysis/{id} for results.",
        }

    async def get_analysis(self, *, user_id: UUID, analysis_id: UUID) -> BodyAnalysis:
        """Return a specific body analysis for user_id."""
        return await self._repo.get_by_id(user_id=user_id, record_id=analysis_id)
