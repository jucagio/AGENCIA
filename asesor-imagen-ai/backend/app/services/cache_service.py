"""
Try-on result cache (SHA256) — Sprint 0.5 T4.

Two-layer cache
───────────────
    HOT  — Redis        (TTL 7 days, key = `tryon:cache:<sha256>`)
    WARM — Postgres     (TTL 90 days, `try_on_cache` table — ADR-004)
    COLD — Replicate API (fresh inference)

Hash formula (per spec)
───────────────────────
    SHA256(body_analysis_id + wardrobe_item_id + model_version + fashn_mode)

Why include fashn_mode?
    Two users with the same body+garment but different plans should get
    different quality outputs. They CANNOT share a cache key, otherwise a
    free user would receive PRO-grade output (and vice-versa).
"""

from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass
from typing import Any, Optional

logger = logging.getLogger(__name__)

# 7 days, in seconds. Matches CR-4 / ADR-004 short-tier guidance.
HOT_CACHE_TTL_SECONDS: int = 60 * 60 * 24 * 7


def compute_cache_key(
    *,
    body_analysis_id: str,
    wardrobe_item_id: str,
    model_version: str,
    fashn_mode: str,
) -> str:
    """Deterministic SHA256 of the inputs that uniquely identify a result.

    The four inputs are joined with ":" so the hash changes if ANY of them
    changes — including the FASHN quality tier.
    """
    raw = f"{body_analysis_id}:{wardrobe_item_id}:{model_version}:{fashn_mode}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@dataclass
class CacheLookupResult:
    """Outcome of a cache lookup. `tier` is what we report to metrics."""

    hit: bool
    tier: str  # 'hot' | 'warm' | 'miss'
    payload: Optional[dict[str, Any]] = None


class CacheService:
    """SHA256 cache for try-on results.

    Two backends:
      - `redis`: aioredis client (HOT, 7d).
      - `admin`: AdminClient (WARM, Postgres `try_on_cache`, 90d).

    Either may be None (degrades gracefully — caller treats as miss).
    """

    def __init__(self, redis: Any = None, admin: Any = None) -> None:
        self._redis = redis
        self._admin = admin

    # ──────────────────────────────────────────────────────────
    # Lookup
    # ──────────────────────────────────────────────────────────
    async def lookup(self, cache_key: str) -> CacheLookupResult:
        """Two-tier read. Returns the first hit found, or miss."""
        # HOT
        if self._redis is not None:
            try:
                raw = await self._redis.get(f"tryon:cache:{cache_key}")
                if raw:
                    payload = json.loads(raw)
                    logger.info("Cache HIT (hot): %s", cache_key[:16])
                    return CacheLookupResult(hit=True, tier="hot", payload=payload)
            except Exception as exc:  # noqa: BLE001
                logger.warning("Hot cache lookup failed: %s", exc)

        # WARM
        if self._admin is not None:
            try:
                res = await (
                    self._admin.trusted()
                    .table("try_on_cache")
                    .select("result_cdn_url, result_image_url, replicate_model_version, hit_count")
                    .eq("content_hash", cache_key)
                    .maybe_single()
                    .execute()
                )
                if res and res.data:
                    payload = dict(res.data)
                    logger.info("Cache HIT (warm): %s", cache_key[:16])
                    # Promote to HOT for next time.
                    await self._write_hot(cache_key, payload)
                    return CacheLookupResult(hit=True, tier="warm", payload=payload)
            except Exception as exc:  # noqa: BLE001
                logger.warning("Warm cache lookup failed: %s", exc)

        return CacheLookupResult(hit=False, tier="miss")

    # ──────────────────────────────────────────────────────────
    # Write
    # ──────────────────────────────────────────────────────────
    async def store(
        self,
        cache_key: str,
        payload: dict[str, Any],
        *,
        model_version: str,
    ) -> None:
        """Write result to BOTH layers (best-effort, non-fatal on error)."""
        await self._write_hot(cache_key, payload)
        await self._write_warm(cache_key, payload, model_version=model_version)

    async def _write_hot(self, cache_key: str, payload: dict[str, Any]) -> None:
        if self._redis is None:
            return
        try:
            await self._redis.set(
                f"tryon:cache:{cache_key}",
                json.dumps(payload, default=str),
                ex=HOT_CACHE_TTL_SECONDS,
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning("Hot cache write failed: %s", exc)

    async def _write_warm(
        self,
        cache_key: str,
        payload: dict[str, Any],
        *,
        model_version: str,
    ) -> None:
        if self._admin is None:
            return
        try:
            await (
                self._admin.trusted()
                .table("try_on_cache")
                .upsert(
                    {
                        "content_hash": cache_key,
                        "result_image_url": payload.get("result_image_url")
                            or payload.get("result_cdn_url"),
                        "result_cdn_url": payload.get("result_cdn_url"),
                        "replicate_model_version": model_version,
                    },
                    on_conflict="content_hash",
                )
                .execute()
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning("Warm cache write failed: %s", exc)
