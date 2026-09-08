"""
Worker observability — Prometheus + Sentry tags (Sprint 0.5 T4).

Exposes a single module-level registry of Counters / Histograms used by:
    - try_on_service
    - replicate_worker
    - vision_worker
    - rate_limiter (already defines its own, kept separate to avoid churn)

Naming convention
─────────────────
    <subsystem>_<measurement>_<unit>
    Counters end in `_total`.
    Histograms end in `_seconds` for latencies.

Sentry integration
──────────────────
Helpers in this module attach tags (`tier`, `endpoint`, `model_version`)
to the active Sentry scope, so Sentry filters match Prometheus labels.
"""

from __future__ import annotations

import logging
from contextlib import contextmanager
from typing import Iterator, Optional

try:
    from prometheus_client import Counter, Histogram
except ImportError:  # pragma: no cover — only hit in lean test envs
    # Minimal shims so importing this module doesn't blow up when
    # prometheus_client is absent (tests, lightweight scripts).
    class _NoOpMetric:  # type: ignore[too-many-instance-attributes]
        def __init__(self, *args, **kwargs) -> None:
            pass
        def labels(self, *args, **kwargs):  # noqa: D401
            return self
        def inc(self, *_args, **_kwargs) -> None:
            pass
        def observe(self, *_args, **_kwargs) -> None:
            pass

    Counter = Histogram = _NoOpMetric  # type: ignore[assignment,misc]

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────
# Rate limit observability (mirrored from rate_limiter.py for new tier dims)
# ─────────────────────────────────────────────────────────────
# We do NOT redefine `rate_limit_hits_total` here — it lives in
# app.core.rate_limiter to keep that module self-contained. Reference it
# from there. This file adds CACHE + FASHN metrics.

# ─────────────────────────────────────────────────────────────
# Cache observability
# ─────────────────────────────────────────────────────────────
CACHE_HITS_TOTAL = Counter(
    "cache_hits_total",
    "Number of cache hits.",
    ["endpoint", "cache_tier"],  # cache_tier = hot|warm
)

CACHE_MISS_TOTAL = Counter(
    "cache_miss_total",
    "Number of cache misses (full inference required).",
    ["endpoint"],
)

# ─────────────────────────────────────────────────────────────
# FASHN inference latency (T4)
# ─────────────────────────────────────────────────────────────
FASHN_INFERENCE_LATENCY = Histogram(
    "fashn_inference_latency_seconds",
    "Replicate FASHN model inference latency.",
    ["tier"],  # BASE|STD|PRO
    buckets=(0.5, 1.0, 2.0, 5.0, 10.0, 15.0, 20.0, 30.0, 60.0, 120.0),
)

FASHN_FALLBACK_TOTAL = Counter(
    "fashn_fallback_total",
    "Number of times PRO timed out and we retried with STD.",
    ["from_tier", "to_tier"],
)

# ─────────────────────────────────────────────────────────────
# FSM transitions
# ─────────────────────────────────────────────────────────────
FSM_TRANSITIONS_TOTAL = Counter(
    "fsm_transitions_total",
    "FSM state transitions for try-on jobs.",
    ["from_state", "to_state"],
)


# ─────────────────────────────────────────────────────────────
# Sentry helpers — tag the active scope so dashboards stay in sync.
# ─────────────────────────────────────────────────────────────
def tag_sentry(
    *,
    tier: Optional[str] = None,
    endpoint: Optional[str] = None,
    model_version: Optional[str] = None,
    user_id: Optional[str] = None,
) -> None:
    """Best-effort attach tags to the active Sentry scope.

    Silently no-ops if sentry_sdk isn't installed (dev / tests).
    """
    try:
        import sentry_sdk  # type: ignore[import-not-found]
    except ImportError:
        return
    with sentry_sdk.configure_scope() as scope:
        if tier:
            scope.set_tag("tier", tier)
        if endpoint:
            scope.set_tag("endpoint", endpoint)
        if model_version:
            scope.set_tag("model_version", model_version)
        if user_id:
            scope.set_user({"id": user_id})


@contextmanager
def observe_latency(metric: Histogram, **labels: str) -> Iterator[None]:
    """Convenience context manager: `with observe_latency(MY_HISTO, tier='PRO'): ...`"""
    import time
    t0 = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - t0
        try:
            (metric.labels(**labels) if labels else metric).observe(elapsed)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Failed to observe metric: %s", exc)
