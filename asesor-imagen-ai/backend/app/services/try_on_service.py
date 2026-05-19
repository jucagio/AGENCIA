"""
Try-On service — virtual try-on pipeline with caching (ADR-004).

Cache strategy (ADR-004):
  SHA256(body_analysis_id + wardrobe_item_id + REPLICATE_MODEL_VERSION) → content_hash
  Cache TTL: 90 days (in try_on_cache table).

Sprint 0.3: Replicate call is stubbed. Full integration in Sprint 0.5.
"""

from __future__ import annotations

import hashlib
import logging
from uuid import UUID

from app.core.admin_client import AdminClient
from app.models.try_on import TryOn
from app.repositories.repos import TryOnRepository, UsageCounterRepository
from app.schemas.try_on import TryOnFeedbackRequest

logger = logging.getLogger(__name__)

FREE_TRY_ON_CAP = 5  # per month


class TryOnService:
    """Virtual try-on job management."""

    def __init__(self, admin: AdminClient) -> None:
        self._repo = TryOnRepository(admin)
        self._usage_repo = UsageCounterRepository(admin)
        self._admin = admin

    def _compute_content_hash(
        self,
        body_analysis_id: str,
        wardrobe_item_id: str,
        model_version: str,
    ) -> str:
        """ADR-004: deterministic cache key for try-on results."""
        raw = f"{body_analysis_id}:{wardrobe_item_id}:{model_version}"
        return hashlib.sha256(raw.encode()).hexdigest()

    async def create_try_on(
        self,
        *,
        user_id: UUID,
        wardrobe_item_id: UUID,
        body_analysis_id: UUID,
    ) -> dict:  # type: ignore[type-arg]
        """
        Initiate a try-on job with cache check (ADR-004).

        1. Check monthly usage cap.
        2. Compute content_hash.
        3. Check try_on_cache for existing result.
        4. If cache hit: create try_on row as completed immediately.
        5. If cache miss: create pending try_on, enqueue replicate_worker.
        6. Increment usage counter.

        Returns:
            {try_on_id, status, cache_hit, estimated_seconds}
        """
        from app.config import get_settings  # noqa: PLC0415

        settings = get_settings()

        # Usage cap check
        counter = await self._usage_repo.get_current_period(user_id=user_id)
        if counter and counter.try_ons_used >= FREE_TRY_ON_CAP:
            from app.core.exceptions import ValidationError  # noqa: PLC0415
            raise ValidationError(
                message="Monthly try-on limit reached. Upgrade to continue.",
                fields={"limit": str(FREE_TRY_ON_CAP)},
            )

        content_hash = self._compute_content_hash(
            str(body_analysis_id),
            str(wardrobe_item_id),
            settings.REPLICATE_MODEL_VERSION,
        )

        # Check cache (ADR-004)
        cache_hit = await self._repo.get_by_content_hash(
            user_id=user_id, content_hash=content_hash
        )

        if cache_hit:
            logger.info("Cache hit for content_hash=%s", content_hash[:16])
            return {
                "try_on_id": str(cache_hit.id),
                "status": "completed",
                "cache_hit": True,
                "result_cdn_url": cache_hit.result_cdn_url,
                "estimated_seconds": 0,
            }

        # Create pending try_on
        try_on = await self._repo.create(
            user_id=user_id,
            data={
                "wardrobe_item_id": str(wardrobe_item_id),
                "body_analysis_id": str(body_analysis_id),
                "content_hash": content_hash,
                "status": "pending",
                "cache_hit": False,
                "replicate_model_version": settings.REPLICATE_MODEL_VERSION,
            },
        )

        # Increment usage counter
        try:
            await self._usage_repo.increment(user_id=user_id, field="try_ons_used")
        except Exception as exc:  # noqa: BLE001
            logger.warning("Usage counter increment failed: %s", exc)

        # Enqueue replicate_worker
        from arq import create_pool  # noqa: PLC0415
        from arq.connections import RedisSettings  # noqa: PLC0415

        pool = await create_pool(RedisSettings.from_dsn(settings.REDIS_URL))
        await pool.enqueue_job("process_try_on", str(try_on.id), content_hash)

        logger.info("Try-on created: try_on_id=%s user_id=%s", try_on.id, user_id)

        return {
            "try_on_id": str(try_on.id),
            "status": "pending",
            "cache_hit": False,
            "estimated_seconds": 30,
        }

    async def get_try_on(self, *, user_id: UUID, try_on_id: UUID) -> TryOn:
        """Return a specific try-on record owned by user_id."""
        return await self._repo.get_by_id(user_id=user_id, record_id=try_on_id)

    async def list_try_ons(
        self, *, user_id: UUID, page: int = 1, size: int = 20
    ) -> tuple[list[TryOn], int]:
        """Return paginated try-on history for user_id."""
        return await self._repo.list_for_user(user_id=user_id, page=page, per_page=size)

    async def submit_feedback(
        self,
        *,
        user_id: UUID,
        try_on_id: UUID,
        feedback: TryOnFeedbackRequest,
    ) -> TryOn:
        """Record user engagement feedback on a try-on result."""
        data = feedback.model_dump(exclude_unset=True, exclude_none=True)
        return await self._repo.update(
            user_id=user_id,
            record_id=try_on_id,
            data=data,
        )
