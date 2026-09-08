"""
Centralized ARQ pool — Sprint 0.5 T2.

Why centralized?
    Before: every call to TryOnService.create_try_on() opened a new ARQ pool
    via `create_pool(RedisSettings.from_dsn(...))`. That meant one TCP
    connection per request to Redis, plus auth handshake. At 10 req/s this
    becomes the bottleneck before the workers do.

After this module:
    - One pool is created on app startup (lifespan) and stored on
      `app.state.queue` (an ArqRedis instance).
    - Services pull it via the `get_queue` dependency.
    - Workers are not affected — they keep their own RedisSettings on their
      WorkerSettings class.

Reference: https://arq-docs.helpmanual.io/#redis-connections
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Optional

from app.config import Settings, get_settings

if TYPE_CHECKING:
    from arq.connections import ArqRedis

logger = logging.getLogger(__name__)


async def create_queue_pool(settings: Optional[Settings] = None) -> "ArqRedis":
    """Create the long-lived ARQ pool used by all enqueue calls.

    Stored on `app.state.queue` by the FastAPI lifespan.

    Args:
        settings: Optional override (tests).

    Returns:
        ArqRedis pool ready to call `.enqueue_job(...)`.

    Raises:
        RuntimeError: when REDIS_URL is unset in production.
    """
    settings = settings or get_settings()

    if not settings.REDIS_URL:
        if settings.is_production:
            raise RuntimeError("REDIS_URL must be configured in production")
        logger.warning("REDIS_URL empty — queue pool not created (dev only).")
        return None  # type: ignore[return-value]

    # Lazy import keeps cold-start fast and avoids importing arq in tests
    # that don't need it.
    from arq import create_pool
    from arq.connections import RedisSettings

    pool = await create_pool(RedisSettings.from_dsn(settings.REDIS_URL))
    logger.info(
        "ARQ pool created: queue=%s redis=%s",
        settings.ARQ_QUEUE_NAME,
        # Don't log creds — only host portion.
        settings.REDIS_URL.split("@")[-1] if "@" in settings.REDIS_URL
        else settings.REDIS_URL,
    )
    return pool


async def close_queue_pool(pool: "ArqRedis | None") -> None:
    """Close pool on shutdown. Safe to call with None."""
    if pool is None:
        return
    try:
        await pool.close()
    except Exception as exc:  # noqa: BLE001 — best-effort shutdown
        logger.warning("ARQ pool close failed: %s", exc)


async def enqueue(
    pool: "ArqRedis | None",
    function: str,
    *args: object,
    **kwargs: object,
):
    """Thin wrapper so callers don't have to import arq types.

    Returns:
        The Job object returned by `pool.enqueue_job`, or None when pool is
        None (dev mode without Redis).
    """
    if pool is None:
        logger.warning("Queue not initialized — skipping enqueue of %s", function)
        return None
    return await pool.enqueue_job(function, *args, **kwargs)
