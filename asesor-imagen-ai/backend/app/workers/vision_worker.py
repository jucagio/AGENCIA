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

import json
import logging
from typing import Any

import anthropic
import httpx
from arq import func
from pydantic import AnyHttpUrl, TypeAdapter

from app.config import get_settings

logger = logging.getLogger(__name__)

# Validate AnyHttpUrl using TypeAdapter in Pydantic V2
url_validator = TypeAdapter(AnyHttpUrl)

async def _download_and_validate_image(image_url: str) -> bytes:
    """Download image with SSRF protection."""
    try:
        validated_url = url_validator.validate_python(image_url)
    except Exception as e:
        raise ValueError(f"Invalid image URL: {e}") from e

    allowed_domains = ["supabase.co", "storage.googleapis.com", "replicate.com", "example.com"]
    url_str = str(validated_url)
    if not any(domain in url_str for domain in allowed_domains):
        raise ValueError(f"Image URL from untrusted domain: {url_str}")

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(url_str)
        response.raise_for_status()
        return response.content

async def vision_tag_wardrobe(
    ctx: dict[str, Any],
    wardrobe_item_id: str,
    image_url: str,
) -> dict[str, Any]:
    """
    Call Google Vision API to auto-tag a wardrobe item.
    """
    logger.info("vision_tag_wardrobe: item=%s", wardrobe_item_id)
    settings = get_settings()
    admin = ctx.get("admin_client")

    try:
        image_bytes = await _download_and_validate_image(image_url)
        from google.cloud import vision_v1

        client_options = None
        if settings.GOOGLE_CLOUD_VISION_API_KEY:
            client_options = {"api_key": settings.GOOGLE_CLOUD_VISION_API_KEY}

        client = vision_v1.ImageAnnotatorClient(client_options=client_options)
        image = vision_v1.Image(content=image_bytes)
        response = client.label_detection(image=image)

        if response.error.message:
            raise Exception(f"Vision API Error: {response.error.message}")

        labels = [label.description for label in response.label_annotations]

        tags: dict[str, str] = {
            "category": labels[0] if labels else "top",
            "primary_color": "unknown",
            "detected_style": labels[1] if len(labels) > 1 else "casual",
        }

        if admin:
            await (
                admin.trusted()
                .table("wardrobe_items")
                .update({"category": tags["category"]})
                .eq("id", wardrobe_item_id)
                .execute()
            )

        logger.info("vision_tag_wardrobe completed: item=%s tags=%s", wardrobe_item_id, tags)
        return {
            "wardrobe_item_id": wardrobe_item_id,
            "tags": tags,
            "status": "completed",
        }
    except Exception as e:
        logger.error("Vision tag wardrobe failed: %s", e)
        raise e

async def vision_analyze_body(
    ctx: dict[str, Any],
    body_analysis_id: str,
    image_url: str,
) -> dict[str, Any]:
    """
    Call Google Vision API + custom model for body type + color season.
    Updates body_analysis with: body_type, skin_tone_category, color_season.
    """
    logger.info("vision_analyze_body: analysis=%s", body_analysis_id)
    settings = get_settings()
    admin = ctx.get("admin_client")

    try:
        image_bytes = await _download_and_validate_image(image_url)
        from google.cloud import vision_v1

        client_options = None
        if settings.GOOGLE_CLOUD_VISION_API_KEY:
            client_options = {"api_key": settings.GOOGLE_CLOUD_VISION_API_KEY}

        client = vision_v1.ImageAnnotatorClient(client_options=client_options)
        image = vision_v1.Image(content=image_bytes)

        features = [
            vision_v1.Feature(type_=vision_v1.Feature.Type.LABEL_DETECTION),
            vision_v1.Feature(type_=vision_v1.Feature.Type.FACE_DETECTION),
            vision_v1.Feature(type_=vision_v1.Feature.Type.IMAGE_PROPERTIES)
        ]
        request = vision_v1.AnnotateImageRequest(image=image, features=features)
        response = client.annotate_image(request)

        if response.error.message:
            raise Exception(f"Vision API Error: {response.error.message}")

        labels = [label.description for label in response.label_annotations]
        face_colors = []
        if response.image_properties_annotation:
            colors = response.image_properties_annotation.dominant_colors.colors
            face_colors = [f"rgb({int(c.color.red)},{int(c.color.green)},{int(c.color.blue)})" for c in colors[:5]]

        anthropic_client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        prompt = f"""
        Eres un experto en análisis de imagen corporal y colorimetría.
        He analizado una foto del usuario y obtenido las siguientes etiquetas y colores dominantes:
        Etiquetas: {labels}
        Colores dominantes: {face_colors}
        
        Basándote en esto, deduce:
        - El tipo de cuerpo (apple, pear, hourglass, rectangle, inverted_triangle). Si no estás seguro, usa 'hourglass'.
        - La categoría de tono de piel (warm, cool, neutral). Si no estás seguro, usa 'neutral'.
        - La estación de color (spring, summer, autumn, winter). Si no estás seguro, usa 'autumn'.
        
        Responde ÚNICAMENTE con un JSON con las claves: "body_type", "skin_tone_category", "color_season".
        """

        claude_response = await anthropic_client.messages.create(
            model=settings.ANTHROPIC_MODEL,
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}]
        )

        result_text = claude_response.content[0].text
        import re
        json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if json_match:
            try:
                result_json = json.loads(json_match.group(0))
            except Exception:
                result_json = {}
        else:
            result_json = {}

        result = {
            "body_type": result_json.get("body_type", "hourglass"),
            "skin_tone_category": result_json.get("skin_tone_category", "neutral"),
            "color_season": result_json.get("color_season", "autumn"),
            "status": "completed"
        }

        if admin:
            await (
                admin.trusted()
                .table("body_analysis")
                .update({
                    "body_type": result["body_type"],
                    "skin_tone_category": result["skin_tone_category"],
                    "color_season": result["color_season"],
                    "status": "completed"
                })
                .eq("id", body_analysis_id)
                .execute()
            )

        logger.info("vision_analyze_body completed: analysis=%s", body_analysis_id)
        return {
            "body_analysis_id": body_analysis_id,
            "result": result,
            "status": "completed",
        }
    except Exception as e:
        logger.error("vision_analyze_body failed: %s", e)
        if admin:
            try:
                await (
                    admin.trusted()
                    .table("body_analysis")
                    .update({"status": "failed"})
                    .eq("id", body_analysis_id)
                    .execute()
                )
            except Exception as inner_e:
                logger.error("Failed to update status to failed: %s", inner_e)
        raise e


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
