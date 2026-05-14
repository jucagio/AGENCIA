"""
ARQ worker: Anthropic Claude outfit recommendations generation.

Triggered by recommendation_service.generate_recommendations().

Pipeline:
  1. Fetch user body_analysis + user_style_profile.
  2. Build structured prompt for Claude claude-opus-4-7.
  3. Parse JSON response → save recommendation_items.
  4. Update recommendation status.

Sprint 0.5 integrates the full Claude pipeline.
"""

from __future__ import annotations

import logging

from arq import func

logger = logging.getLogger(__name__)


async def generate_reco_claude(
    ctx: dict,  # type: ignore[type-arg]
    user_id: str,
    recommendation_id: str,
) -> dict:  # type: ignore[type-arg]
    """
    Generate AI outfit recommendations using Claude.

    Sprint 0.3 stub: returns hardcoded demo data to validate the ARQ pipeline.
    Sprint 0.5 integrates anthropic.AsyncAnthropic().messages.create().
    """
    logger.info(
        "generate_reco_claude started: reco=%s user=%s",
        recommendation_id,
        user_id,
    )

    # TODO(Sprint 0.5): fetch body_analysis + style_profile
    # TODO(Sprint 0.5): build prompt with PromptBuilder
    # TODO(Sprint 0.5): call anthropic client
    # client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
    # response = await client.messages.create(
    #     model=settings.ANTHROPIC_MODEL,
    #     max_tokens=2048,
    #     messages=[{"role": "user", "content": prompt}],
    # )

    # Stub recommendation items
    demo_items = [
        {"position": i + 1, "role": role}
        for i, role in enumerate(["top", "bottom", "shoes", "accessory", "outerwear"])
    ]

    logger.info(
        "generate_reco_claude completed: reco=%s items=%d",
        recommendation_id,
        len(demo_items),
    )

    return {
        "recommendation_id": recommendation_id,
        "status": "completed",
        "count": len(demo_items),
    }


class WorkerSettings:
    """ARQ worker configuration for the Claude worker process."""

    functions = [
        func(generate_reco_claude, timeout=120),  # type: ignore[call-overload]
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
