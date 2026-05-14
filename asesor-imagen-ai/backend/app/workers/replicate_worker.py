"""
ARQ worker: Replicate Virtual Try-On inference.

Triggered by try_on_service.create_try_on().

Pipeline:
  1. Double-check try_on_cache (race condition guard).
  2. Call Replicate model (stub for Sprint 0.3 — returns placeholder URL).
  3. Upload result to Supabase Storage → R2 CDN.
  4. Update try_ons table: status=completed, result_cdn_url.
  5. Write to try_on_cache (TTL 90 days — ADR-004).

Sprint 0.5 integrates Replicate real API.
"""

from __future__ import annotations

import logging

from arq import func

logger = logging.getLogger(__name__)


async def process_try_on(
    ctx: dict,  # type: ignore[type-arg]
    try_on_id: str,
    content_hash: str,
) -> dict:  # type: ignore[type-arg]
    """
    Execute a virtual try-on inference job.

    Steps:
      1. Double-check cache for race-condition guard.
      2. Call Replicate (stubbed in 0.3).
      3. Update try_ons row with result.
      4. Write to try_on_cache.

    Sprint 0.5 integrates replicate.run(settings.REPLICATE_MODEL_VERSION, ...).
    """
    logger.info("process_try_on started: try_on_id=%s hash=%s", try_on_id, content_hash[:16])

    # TODO(Sprint 0.5): replicate.run call
    # import replicate
    # output = replicate.run(settings.REPLICATE_MODEL_VERSION, input={...})

    result_cdn_url = f"https://placeholder.r2.dev/try_on_{try_on_id}.webp"

    # TODO(Sprint 0.5): upload to Supabase Storage → R2 CDN
    # TODO(Sprint 0.5): update try_ons row via AdminClient
    # TODO(Sprint 0.5): write to try_on_cache

    logger.info("process_try_on completed: try_on_id=%s", try_on_id)
    return {
        "try_on_id": try_on_id,
        "status": "completed",
        "result_cdn_url": result_cdn_url,
    }


class WorkerSettings:
    """ARQ worker configuration for the Replicate worker process."""

    functions = [
        func(process_try_on, timeout=300),  # type: ignore[call-overload]
    ]
    redis_settings = None  # type: ignore[assignment]

    @classmethod
    def from_settings(cls) -> "WorkerSettings":
        """Configure redis_settings from app config at worker startup."""
        from arq.connections import RedisSettings  # type: ignore[import-not-found]

        from app.config import get_settings  # noqa: PLC0415

        settings = get_settings()
        cls.redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)
        return cls()
