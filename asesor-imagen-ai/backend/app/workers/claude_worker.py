"""
ARQ worker: Anthropic Claude outfit recommendations generation.

Triggered by recommendation_service.generate_recommendations().

Pipeline:
  1. Fetch user body_analysis + user_style_profile + wardrobe_items.
  2. Build structured prompt for Claude claude-opus-4-7.
  3. Parse JSON response → save recommendation_items.
  4. Update recommendation status.
"""

from __future__ import annotations

import json
import logging
from typing import Any

import anthropic
from arq import func

from app.config import get_settings

logger = logging.getLogger(__name__)


async def generate_reco_claude(
    ctx: dict[str, Any],
    user_id: str,
    recommendation_id: str,
) -> dict[str, Any]:
    """
    Generate AI outfit recommendations using Claude.
    """
    logger.info(
        "generate_reco_claude started: reco=%s user=%s",
        recommendation_id,
        user_id,
    )
    settings = get_settings()
    admin = ctx.get("admin_client")

    try:
        body_type = "hourglass"
        color_season = "autumn"
        occasion = "casual"
        wardrobe_items_json = "[]"

        if admin:
            # Fetch recommendation to get occasion/season
            reco_res = await admin.trusted().table("recommendations").select("*").eq("id", recommendation_id).single().execute()
            if reco_res.data:
                occasion = reco_res.data.get("occasion", occasion)

            # Fetch body_analysis
            body_res = await admin.trusted().table("body_analysis").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(1).execute()
            if body_res.data:
                body_type = body_res.data[0].get("body_type", body_type)
                color_season = body_res.data[0].get("color_season", color_season)

            # Fetch wardrobe items
            wardrobe_res = await admin.trusted().table("wardrobe_items").select("*").eq("user_id", user_id).execute()
            if wardrobe_res.data:
                wardrobe_items_json = json.dumps([
                    {"id": item["id"], "category": item.get("category"), "primary_color": item.get("primary_color")}
                    for item in wardrobe_res.data
                ])

        # Build prompt
        prompt = f"""
        Eres un asesor de estilo IA. Basándote en:
        - Tipo de cuerpo: {body_type}
        - Temporada de color: {color_season}
        - Ocasión: {occasion}
        - Prendas disponibles: {wardrobe_items_json}
        
        Genera 1 combinación de outfit (top, bottom, shoes) 
        que maximice armonía visual y comodidad.
        
        Devuelve JSON:
        {{
          "outfits": [
            {{
              "items": [
                 {{"id": "wardrobe_item_id", "role": "top"}}
              ],
              "why": "explicación breve por qué funciona",
              "confidence": 0.95
            }}
          ]
        }}
        """

        # Call Anthropic API
        anthropic_client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        response = await anthropic_client.messages.create(
            model=settings.ANTHROPIC_MODEL,
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}],
        )

        result_text = response.content[0].text
        import re
        json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
        outfits = []
        if json_match:
            try:
                result_json = json.loads(json_match.group(0))
                outfits = result_json.get("outfits", [])
            except Exception:
                pass

        if not outfits:
            outfits = [{"items": [], "why": "Default recommendation", "confidence": 0.5}]

        first_outfit = outfits[0]
        items = first_outfit.get("items", [])

        if admin:
            # Insert recommendation items
            for i, item in enumerate(items):
                item_id = item.get("id")
                role = item.get("role", "top")
                if item_id:
                    await (
                        admin.trusted()
                        .table("recommendation_items")
                        .insert({
                            "recommendation_id": recommendation_id,
                            "wardrobe_item_id": item_id,
                            "position": i + 1,
                            "role": role
                        })
                        .execute()
                    )

            # Update recommendation status
            await (
                admin.trusted()
                .table("recommendations")
                .update({
                    "status": "completed",
                    "reason": first_outfit.get("why", ""),
                })
                .eq("id", recommendation_id)
                .execute()
            )

        logger.info(
            "generate_reco_claude completed: reco=%s items=%d",
            recommendation_id,
            len(items),
        )

        return {
            "recommendation_id": recommendation_id,
            "status": "completed",
            "count": len(items),
        }
    except Exception as e:
        logger.error("generate_reco_claude failed: %s", e)
        if admin:
            try:
                await (
                    admin.trusted()
                    .table("recommendations")
                    .update({"status": "failed"})
                    .eq("id", recommendation_id)
                    .execute()
                )
            except Exception as inner_e:
                logger.error("Failed to update reco status to failed: %s", inner_e)
        raise e


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
