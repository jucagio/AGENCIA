"""
ARQ worker: Replicate Virtual Try-On inference (Sprint 0.5 T4).

Pipeline (Option F)
───────────────────
  1. Mark FSM state = cache_lookup.
  2. Two-layer cache lookup (HOT redis → WARM postgres).
        a. HIT → state = cache_hit → completed (no inference, no upload).
  3. MISS → state = inference_running.
        b. Call Replicate FASHN with tier-appropriate mode.
        c. If PRO times out (>15s) → fallback to STD, state = fallback_triggered.
  4. state = uploading. Persist result + write to BOTH cache layers.
  5. state = completed.

  Any exception → state = failed, status='failed', error_message recorded.

Tier routing (T4)
─────────────────
  Free   → BASE → fashn_mode = performance (fast, cheap)
  Estilo → STD  → fashn_mode = balanced
  Imagen → PRO  → fashn_mode = quality      (slow, expensive; fallback to STD on timeout)

Mock mode
─────────
  FEATURE_MOCK_WORKERS=true short-circuits the Replicate call and returns a
  canned response. Used in dev / CI / tests so credits aren't burned.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from datetime import datetime, timezone
from typing import Any, Optional

import httpx
from arq import func
from pydantic import AnyHttpUrl, TypeAdapter

from app.config import get_settings
from app.core.admin_client import AdminClient
from app.core.metrics import (
    CACHE_HITS_TOTAL,
    CACHE_MISS_TOTAL,
    FASHN_FALLBACK_TOTAL,
    FASHN_INFERENCE_LATENCY,
    FSM_TRANSITIONS_TOTAL,
    observe_latency,
    tag_sentry,
)
from app.models.fsm import FSMState, can_transition
from app.services.cache_service import CacheService

logger = logging.getLogger(__name__)

url_validator = TypeAdapter(AnyHttpUrl)

# Tier → FASHN mode mapping (mirror of app.models.fsm.TIER_TO_FASHN_MODE,
# duplicated here as a defensive fallback if a try_on row is missing fashn_mode).
_TIER_MODE_FALLBACK = {
    "BASE": "performance",
    "STD": "balanced",
    "PRO": "quality",
}


async def _download_and_validate_image(image_url: str) -> bytes:
    """Download image with SSRF protection (allowlist of domains)."""
    try:
        validated = url_validator.validate_python(image_url)
    except Exception as e:
        raise ValueError(f"Invalid image URL: {e}") from e

    allowed = [
        "supabase.co",
        "storage.googleapis.com",
        "replicate.com",
        "replicate.delivery",
        "example.com",
    ]
    url_str = str(validated)
    if not any(d in url_str for d in allowed):
        raise ValueError(f"Image URL from untrusted domain: {url_str}")

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(url_str)
        resp.raise_for_status()
        return resp.content


# ─────────────────────────────────────────────────────────────
# FSM persistence helper
# ─────────────────────────────────────────────────────────────
async def _set_fsm_state(
    admin: Optional[AdminClient],
    try_on_id: str,
    current_state: str,
    next_state: FSMState,
    *,
    meta: Optional[dict[str, Any]] = None,
    extra_fields: Optional[dict[str, Any]] = None,
) -> None:
    """Validate transition + persist next state + append history entry.

    Best-effort: logs and swallows errors so a flaky DB doesn't kill the job.
    """
    if not can_transition(current_state, next_state):
        logger.error(
            "Invalid FSM transition: %s -> %s on try_on_id=%s",
            current_state, next_state.value, try_on_id,
        )
        return
    FSM_TRANSITIONS_TOTAL.labels(
        from_state=current_state, to_state=next_state.value
    ).inc()

    if admin is None:
        return

    history_entry = {
        "state": next_state.value,
        "at": datetime.now(timezone.utc).isoformat(),
        "meta": meta or {},
    }
    payload: dict[str, Any] = {
        "fsm_state": next_state.value,
    }
    if extra_fields:
        payload.update(extra_fields)

    try:
        # 1. Read current history (Supabase has no native array append).
        row = await (
            admin.trusted().table("try_ons")
            .select("fsm_history")
            .eq("id", try_on_id)
            .single()
            .execute()
        )
        history = (row.data or {}).get("fsm_history") or []
        history.append(history_entry)
        payload["fsm_history"] = history

        await (
            admin.trusted().table("try_ons")
            .update(payload)
            .eq("id", try_on_id)
            .execute()
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning("FSM persist failed (%s): %s", next_state.value, exc)


# ─────────────────────────────────────────────────────────────
# Replicate call with tier + fallback
# ─────────────────────────────────────────────────────────────
async def _call_replicate(
    *,
    model_version: str,
    user_photo_url: str,
    garment_image_url: str,
    fashn_mode: str,
    timeout_seconds: float,
) -> Optional[str]:
    """Run a single Replicate inference. Returns the result image URL or None.

    Wrapped in `asyncio.wait_for` so PRO callers can enforce the 15s cap.
    """
    import replicate  # noqa: PLC0415

    settings = get_settings()

    def _sync_call() -> Optional[str]:
        client = replicate.Client(api_token=settings.REPLICATE_API_TOKEN)
        output = client.run(
            model_version,
            input={
                "person_image": user_photo_url,
                "garment_image": garment_image_url,
                # FASHN exposes a "mode" parameter on its tryon model versions.
                # Passing it is a no-op for older models that don't recognize it.
                "mode": fashn_mode,
            },
        )
        if output and isinstance(output, list):
            return output[0]
        if isinstance(output, str):
            return output
        return None

    return await asyncio.wait_for(
        asyncio.to_thread(_sync_call),
        timeout=timeout_seconds,
    )


async def _run_inference_with_fallback(
    *,
    try_on_id: str,
    tier: str,
    fashn_mode: str,
    model_version: str,
    user_photo_url: str,
    garment_image_url: str,
    admin: Optional[AdminClient],
) -> tuple[str, bool]:
    """Run Replicate. If PRO times out, retry once with STD ("balanced").

    Returns:
        (output_url, fallback_used)
    """
    settings = get_settings()

    with observe_latency(FASHN_INFERENCE_LATENCY, tier=tier):
        try:
            timeout = settings.FASHN_PRO_TIMEOUT_SECONDS if tier == "PRO" else 60.0
            output = await _call_replicate(
                model_version=model_version,
                user_photo_url=user_photo_url,
                garment_image_url=garment_image_url,
                fashn_mode=fashn_mode,
                timeout_seconds=timeout,
            )
            if output:
                return output, False
            raise ValueError("Replicate returned empty output")
        except asyncio.TimeoutError:
            if tier != "PRO":
                raise
            logger.warning(
                "PRO inference timed out for %s — falling back to STD",
                try_on_id,
            )
            FASHN_FALLBACK_TOTAL.labels(from_tier="PRO", to_tier="STD").inc()
            await _set_fsm_state(
                admin, try_on_id,
                FSMState.INFERENCE_RUNNING.value,
                FSMState.FALLBACK_TRIGGERED,
                meta={"reason": "pro_timeout"},
                extra_fields={"fallback_used": True},
            )
            await _set_fsm_state(
                admin, try_on_id,
                FSMState.FALLBACK_TRIGGERED.value,
                FSMState.INFERENCE_RUNNING,
                meta={"retry_tier": "STD"},
            )

    # Retry with STD/balanced (outside the first latency observation).
    with observe_latency(FASHN_INFERENCE_LATENCY, tier="STD"):
        output = await _call_replicate(
            model_version=model_version,
            user_photo_url=user_photo_url,
            garment_image_url=garment_image_url,
            fashn_mode="balanced",
            timeout_seconds=60.0,
        )
        if not output:
            raise ValueError("STD fallback inference returned empty output")
        return output, True


# ─────────────────────────────────────────────────────────────
# Main worker entry point
# ─────────────────────────────────────────────────────────────
async def process_try_on(
    ctx: dict[str, Any],
    try_on_id: str,
    content_hash: str,
) -> dict[str, Any]:
    """Execute a virtual try-on inference job."""
    settings = get_settings()
    raw_admin = ctx.get("admin_client")
    admin: Optional[AdminClient] = (
        AdminClient(raw_admin) if raw_admin and not isinstance(raw_admin, AdminClient)
        else raw_admin
    )
    redis = ctx.get("redis")

    logger.info(
        "process_try_on started: try_on_id=%s hash=%s mock=%s",
        try_on_id, content_hash[:16], settings.FEATURE_MOCK_WORKERS,
    )

    # ── State: queued → cache_lookup ───────────────────────────────────────
    await _set_fsm_state(admin, try_on_id, FSMState.QUEUED.value, FSMState.CACHE_LOOKUP)

    # Fetch the try_on row to learn fashn_mode + linked entity IDs.
    fashn_mode = "performance"
    tier = "BASE"
    user_id = "test-user"
    user_photo_url = "https://example.com/user.jpg"
    garment_image_url = "https://example.com/garment.jpg"

    try:
        if admin:
            row = await (
                admin.trusted().table("try_ons")
                .select("user_id, wardrobe_item_id, body_analysis_id, fashn_mode")
                .eq("id", try_on_id)
                .single()
                .execute()
            )
            try_on = row.data or {}
            user_id = try_on.get("user_id") or user_id
            fashn_mode = try_on.get("fashn_mode") or fashn_mode

            # Map fashn_mode → tier for metrics labels.
            tier = next(
                (t for t, m in _TIER_MODE_FALLBACK.items() if m == fashn_mode),
                "BASE",
            )

            wid, bid = try_on.get("wardrobe_item_id"), try_on.get("body_analysis_id")
            if bid:
                ba = await (
                    admin.trusted().table("body_analysis")
                    .select("image_url").eq("id", bid).single().execute()
                )
                if ba.data and ba.data.get("image_url"):
                    user_photo_url = ba.data["image_url"]
            if wid:
                wr = await (
                    admin.trusted().table("wardrobe_items")
                    .select("image_url").eq("id", wid).single().execute()
                )
                if wr.data and wr.data.get("image_url"):
                    garment_image_url = wr.data["image_url"]
    except Exception as exc:  # noqa: BLE001
        logger.warning("Failed to fetch try_on metadata: %s", exc)

    tag_sentry(
        tier=tier,
        endpoint="/api/v1/try-ons",
        model_version=settings.REPLICATE_MODEL_VERSION,
        user_id=str(user_id),
    )

    cache = CacheService(redis=redis, admin=admin)

    try:
        # ── Cache lookup (HOT + WARM) ──────────────────────────────────────
        lookup = await cache.lookup(content_hash)

        if lookup.hit:
            CACHE_HITS_TOTAL.labels(
                endpoint="/api/v1/try-ons", cache_tier=lookup.tier
            ).inc()
            await _set_fsm_state(
                admin, try_on_id,
                FSMState.CACHE_LOOKUP.value, FSMState.CACHE_HIT,
                meta={"cache_tier": lookup.tier},
                extra_fields={"cache_tier": lookup.tier, "cache_hit": True},
            )
            result_url = (lookup.payload or {}).get("result_cdn_url") \
                         or (lookup.payload or {}).get("result_image_url")
            await _finalize_completed(
                admin, try_on_id, result_url,
                model_version=settings.REPLICATE_MODEL_VERSION,
                from_state=FSMState.CACHE_HIT.value,
            )
            logger.info("process_try_on cache HIT (%s): try_on_id=%s", lookup.tier, try_on_id)
            return {
                "try_on_id": try_on_id,
                "status": "completed",
                "cache_hit": True,
                "cache_tier": lookup.tier,
                "result_cdn_url": result_url,
            }

        CACHE_MISS_TOTAL.labels(endpoint="/api/v1/try-ons").inc()

        # ── cache_lookup → inference_running ───────────────────────────────
        await _set_fsm_state(
            admin, try_on_id,
            FSMState.CACHE_LOOKUP.value, FSMState.INFERENCE_RUNNING,
            extra_fields={"cache_tier": "miss"},
        )

        # ── Inference ──────────────────────────────────────────────────────
        if settings.FEATURE_MOCK_WORKERS:
            output_url = f"https://example.com/mock-tryon/{try_on_id}.jpg"
            fallback_used = False
            logger.info("MOCK inference for %s (FEATURE_MOCK_WORKERS=true)", try_on_id)
        else:
            output_url, fallback_used = await _run_inference_with_fallback(
                try_on_id=try_on_id,
                tier=tier,
                fashn_mode=fashn_mode,
                model_version=settings.REPLICATE_MODEL_VERSION,
                user_photo_url=user_photo_url,
                garment_image_url=garment_image_url,
                admin=admin,
            )

        # ── inference_running → uploading ──────────────────────────────────
        await _set_fsm_state(
            admin, try_on_id,
            FSMState.INFERENCE_RUNNING.value, FSMState.UPLOADING,
            meta={"output_url": output_url, "fallback_used": fallback_used},
        )

        # Storage path (R2 / Supabase Storage). Upload itself is handled by
        # the Storage adapter in T1; here we just record the planned path.
        storage_path = f"try-ons/{user_id}/{try_on_id}.jpg"
        result_cdn_url = (
            f"{settings.SUPABASE_URL}/storage/v1/object/public/"
            f"{settings.TRYONS_BUCKET}/{storage_path}"
        )

        # Persist + write to BOTH cache layers.
        await cache.store(
            content_hash,
            {
                "result_cdn_url": result_cdn_url,
                "result_image_url": output_url,
            },
            model_version=settings.REPLICATE_MODEL_VERSION,
        )

        await _finalize_completed(
            admin, try_on_id, result_cdn_url,
            model_version=settings.REPLICATE_MODEL_VERSION,
            from_state=FSMState.UPLOADING.value,
            extra={"result_storage_path": storage_path, "fallback_used": fallback_used},
        )

        logger.info("process_try_on completed: try_on_id=%s tier=%s fallback=%s",
                    try_on_id, tier, fallback_used)
        return {
            "try_on_id": try_on_id,
            "status": "completed",
            "cache_hit": False,
            "result_cdn_url": result_cdn_url,
            "tier": tier,
            "fallback_used": fallback_used,
        }

    except Exception as exc:
        logger.error("process_try_on failed: %s", exc, exc_info=True)
        try:
            await _set_fsm_state(
                admin, try_on_id,
                # We don't know the exact current state in catastrophic paths.
                # Try inference_running first; the helper validates and noops
                # silently if the transition is invalid.
                FSMState.INFERENCE_RUNNING.value, FSMState.FAILED,
                meta={"error": str(exc)[:500]},
                extra_fields={
                    "status": "failed",
                    "error_message": str(exc)[:1000],
                },
            )
        except Exception as inner:  # noqa: BLE001
            logger.error("Failed to mark try_on failed: %s", inner)
        raise


async def _finalize_completed(
    admin: Optional[AdminClient],
    try_on_id: str,
    result_cdn_url: Optional[str],
    *,
    model_version: str,
    from_state: str,
    extra: Optional[dict[str, Any]] = None,
) -> None:
    """Common terminal-success path: persist row + FSM = completed."""
    fields: dict[str, Any] = {
        "status": "completed",
        "result_cdn_url": result_cdn_url,
        "result_image_url": result_cdn_url,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "replicate_model_version": model_version,
    }
    if extra:
        fields.update(extra)
    await _set_fsm_state(
        admin, try_on_id,
        from_state, FSMState.COMPLETED,
        extra_fields=fields,
    )


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
