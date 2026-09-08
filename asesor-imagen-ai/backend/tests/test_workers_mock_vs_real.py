"""
Sprint 0.5 T7 — FEATURE_MOCK_WORKERS flag verification.

Two paths must produce schema-equivalent responses:
    PATH A (mock): FEATURE_MOCK_WORKERS=true   → workers return canned data.
    PATH B (real): FEATURE_MOCK_WORKERS=false  → workers call external APIs.

This test suite only exercises PATH A in CI (PATH B requires real Replicate +
Vision + Anthropic credentials, which CI must not have). PATH B is covered by
the staging smoke tests.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models.fsm import (
    ALLOWED_TRANSITIONS,
    FSMState,
    InvalidTransitionError,
    can_transition,
    is_terminal,
    plan_to_fashn_mode,
    plan_to_tier,
    transition,
)
from app.services.cache_service import (
    CacheLookupResult,
    CacheService,
    compute_cache_key,
)


# ─────────────────────────────────────────────────────────────
# FSM unit tests
# ─────────────────────────────────────────────────────────────
class TestFSM:
    def test_initial_transition_allowed(self) -> None:
        assert can_transition(FSMState.QUEUED, FSMState.CACHE_LOOKUP)

    def test_invalid_transition_rejected(self) -> None:
        # Cannot jump straight from queued to completed.
        assert not can_transition(FSMState.QUEUED, FSMState.COMPLETED)
        with pytest.raises(InvalidTransitionError):
            transition(FSMState.QUEUED, FSMState.COMPLETED)

    def test_terminal_states_have_no_outgoing(self) -> None:
        assert ALLOWED_TRANSITIONS[FSMState.COMPLETED] == set()
        assert ALLOWED_TRANSITIONS[FSMState.FAILED] == set()
        assert is_terminal(FSMState.COMPLETED)
        assert is_terminal(FSMState.FAILED)
        assert not is_terminal(FSMState.INFERENCE_RUNNING)

    def test_transition_returns_history_entry(self) -> None:
        entry = transition(FSMState.QUEUED, FSMState.CACHE_LOOKUP, meta={"foo": "bar"})
        assert entry.state == FSMState.CACHE_LOOKUP
        assert entry.meta == {"foo": "bar"}
        assert entry.to_jsonable()["state"] == "cache_lookup"

    def test_fallback_transition_path(self) -> None:
        assert can_transition(
            FSMState.INFERENCE_RUNNING, FSMState.FALLBACK_TRIGGERED
        )
        assert can_transition(
            FSMState.FALLBACK_TRIGGERED, FSMState.INFERENCE_RUNNING
        )

    def test_accepts_string_values(self) -> None:
        assert can_transition("queued", "cache_lookup")
        assert not can_transition("completed", "failed")


# ─────────────────────────────────────────────────────────────
# Plan → tier / mode
# ─────────────────────────────────────────────────────────────
class TestTierRouting:
    @pytest.mark.parametrize(
        "plan,tier,mode",
        [
            ("free", "BASE", "performance"),
            ("estilo", "STD", "balanced"),
            ("imagen", "PRO", "quality"),
            (None, "BASE", "performance"),
            ("unknown_plan", "BASE", "performance"),
        ],
    )
    def test_plan_mapping(self, plan, tier, mode) -> None:
        assert plan_to_tier(plan) == tier
        assert plan_to_fashn_mode(plan) == mode


# ─────────────────────────────────────────────────────────────
# Cache key + service
# ─────────────────────────────────────────────────────────────
class TestCacheKey:
    def test_deterministic(self) -> None:
        a = compute_cache_key(
            body_analysis_id="b1",
            wardrobe_item_id="w1",
            model_version="v1",
            fashn_mode="quality",
        )
        b = compute_cache_key(
            body_analysis_id="b1",
            wardrobe_item_id="w1",
            model_version="v1",
            fashn_mode="quality",
        )
        assert a == b
        assert len(a) == 64  # SHA256 hex

    def test_changes_when_mode_changes(self) -> None:
        """Per-tier isolation: PRO and BASE outputs MUST NOT share a key."""
        free = compute_cache_key(
            body_analysis_id="b1", wardrobe_item_id="w1",
            model_version="v1", fashn_mode="performance",
        )
        pro = compute_cache_key(
            body_analysis_id="b1", wardrobe_item_id="w1",
            model_version="v1", fashn_mode="quality",
        )
        assert free != pro

    def test_changes_when_model_version_changes(self) -> None:
        v1 = compute_cache_key(
            body_analysis_id="b1", wardrobe_item_id="w1",
            model_version="v1", fashn_mode="quality",
        )
        v2 = compute_cache_key(
            body_analysis_id="b1", wardrobe_item_id="w1",
            model_version="v2", fashn_mode="quality",
        )
        assert v1 != v2


class TestCacheServiceLookup:
    @pytest.mark.asyncio
    async def test_miss_when_no_backends(self) -> None:
        svc = CacheService(redis=None, admin=None)
        res = await svc.lookup("abc")
        assert res.hit is False
        assert res.tier == "miss"

    @pytest.mark.asyncio
    async def test_hot_hit(self) -> None:
        redis = MagicMock()
        redis.get = AsyncMock(return_value='{"result_cdn_url":"https://cdn/x.jpg"}')
        svc = CacheService(redis=redis, admin=None)
        res = await svc.lookup("abc")
        assert res.hit is True
        assert res.tier == "hot"
        assert res.payload == {"result_cdn_url": "https://cdn/x.jpg"}

    @pytest.mark.asyncio
    async def test_warm_hit_promotes_to_hot(self) -> None:
        redis = MagicMock()
        redis.get = AsyncMock(return_value=None)
        redis.set = AsyncMock()
        # Mock admin client chain.
        warm_payload = MagicMock(data={"result_cdn_url": "https://cdn/y.jpg"})
        chain = MagicMock()
        chain.select.return_value = chain
        chain.eq.return_value = chain
        chain.maybe_single.return_value = chain
        chain.execute = AsyncMock(return_value=warm_payload)
        admin = MagicMock()
        admin.trusted.return_value.table.return_value = chain

        svc = CacheService(redis=redis, admin=admin)
        res = await svc.lookup("abc")
        assert res.hit is True
        assert res.tier == "warm"
        # Hot promotion attempted.
        redis.set.assert_awaited_once()


# ─────────────────────────────────────────────────────────────
# Mock worker (PATH A) — replicate_worker.process_try_on
# ─────────────────────────────────────────────────────────────
class TestMockWorkerPath:
    @pytest.mark.asyncio
    async def test_mock_worker_returns_canned_response(self, monkeypatch) -> None:
        """When FEATURE_MOCK_WORKERS=true, no external calls happen."""
        # Force mock mode.
        from app.config import get_settings
        get_settings.cache_clear()
        monkeypatch.setenv("FEATURE_MOCK_WORKERS", "true")

        from app.workers.replicate_worker import process_try_on  # noqa: PLC0415

        # No admin, no redis — exercises the dev path.
        result = await process_try_on(
            ctx={"admin_client": None, "redis": None},
            try_on_id="00000000-0000-0000-0000-000000000001",
            content_hash="a" * 64,
        )

        assert result["status"] == "completed"
        # cache_hit False in mock path (no cache backend present).
        assert result["cache_hit"] is False
        # Path always includes the storage prefix; SUPABASE_URL host may be
        # absent in test env so we assert on the path suffix only.
        assert "/storage/v1/object/public/" in result["result_cdn_url"]
        assert result["result_cdn_url"].endswith(".jpg")

        # Clean up.
        monkeypatch.delenv("FEATURE_MOCK_WORKERS", raising=False)
        get_settings.cache_clear()
