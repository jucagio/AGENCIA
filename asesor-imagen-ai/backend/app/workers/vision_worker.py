"""
ARQ worker: Google Vision API auto-tagging for wardrobe items and body analysis.

Triggered by:
  - wardrobe_service.create_item()   → vision_tag_wardrobe
  - body_analysis_service.create_analysis() → vision_analyze_body

Sprint 0.3: stubs that simulate successful processing.
Sprint 0.5: integrate Google Cloud Vision API.

References:
  https://cloud.google.com/vision/docs/reference/rest
  https://arq-docs.helpmanual.io/
"""

from __future__ import annotations

import logging

from arq import func

logger = logging.getLogger(__name__)


async def vision_tag_wardrobe(
    ctx: dict,  # type: ignore[type-arg]
    wardrobe_item_id: str,
    image_url: str,
) -> dict:  # type: ignore[type-arg]
    """
    Call Google Vision API to auto-tag a wardrobe item.

    Updates wardrobe_items with: category, primary_color, detected_style.

    Sprint 0.3 stub: simulates tag detection for pipeline validation.
    Sprint 0.5 integrates Vision API real call.
    """
    logger.info("vision_tag_wardrobe: item=%s", wardrobe_item_id)

    # TODO(Sprint 0.5): google.cloud.vision_v1 call
    # from google.cloud import vision_v1
    # client = vision_v1.ImageAnnotatorClient()
    # response = client.label_detection(image={"source": {"image_uri": image_url}})

    tags: dict[str, str] = {
        "category": "top",
        "primary_color": "blue",
        "detected_style": "casual",
    }

    # TODO(Sprint 0.5): update wardrobe_items via AdminClient
    # admin = ctx.get("admin_client") — injected via worker ctx setup

    logger.info("vision_tag_wardrobe completed: item=%s tags=%s", wardrobe_item_id, tags)
    return {
        "wardrobe_item_id": wardrobe_item_id,
        "tags": tags,
        "status": "completed",
    }


async def vision_analyze_body(
    ctx: dict,  # type: ignore[type-arg]
    body_analysis_id: str,
    image_url: str,
) -> dict:  # type: ignore[type-arg]
    """
    Call Google Vision API + custom model for body type + color season.

    Updates body_analysis with: body_type, skin_tone_category, color_season.

    Sprint 0.3 stub.
    Sprint 0.5 integrates Vision API + custom ML model.
    """
    logger.info("vision_analyze_body: analysis=%s", body_analysis_id)

    # TODO(Sprint 0.5): Vision API call + custom body type classifier
    result: dict[str, object] = {
        "body_type": "hourglass",
        "skin_tone_category": "warm",
        "color_season": "autumn",
    }

    logger.info("vision_analyze_body completed: analysis=%s", body_analysis_id)
    return {
        "body_analysis_id": body_analysis_id,
        "result": result,
        "status": "completed",
    }


class WorkerSettings:
    """ARQ worker configuration for the Vision worker process."""

    functions = [
        func(vision_tag_wardrobe, timeout=120),  # type: ignore[call-overload]
        func(vision_analyze_body, timeout=120),  # type: ignore[call-overload]
    ]
    # redis_settings is set at startup from settings.REDIS_URL
    redis_settings = None  # type: ignore[assignment]

    @classmethod
    def from_settings(cls) -> "WorkerSettings":
        """Configure redis_settings from app config at worker startup."""
        from arq.connections import RedisSettings  # type: ignore[import-not-found]

        from app.config import get_settings  # noqa: PLC0415

        settings = get_settings()
        cls.redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)
        return cls()
