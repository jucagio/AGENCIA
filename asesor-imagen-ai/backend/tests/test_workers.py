"""
Tests for ARQ worker stubs.

Sprint 0.3: workers are stubs that validate the ARQ pipeline.
Sprint 0.5: real external API calls (Vision, Replicate, Claude).
"""

from __future__ import annotations

import pytest


@pytest.mark.anyio
async def test_vision_tag_wardrobe_stub() -> None:
    """vision_tag_wardrobe stub returns expected structure."""
    from app.workers.vision_worker import vision_tag_wardrobe

    result = await vision_tag_wardrobe({}, "item-123", "https://example.com/img.jpg")

    assert result["wardrobe_item_id"] == "item-123"
    assert result["status"] == "completed"
    assert "tags" in result
    assert isinstance(result["tags"], dict)


@pytest.mark.anyio
async def test_vision_analyze_body_stub() -> None:
    """vision_analyze_body stub returns expected structure."""
    from app.workers.vision_worker import vision_analyze_body

    result = await vision_analyze_body({}, "analysis-456", "https://example.com/body.jpg")

    assert result["body_analysis_id"] == "analysis-456"
    assert result["status"] == "completed"
    assert "result" in result
    assert result["result"]["body_type"] is not None


@pytest.mark.anyio
async def test_process_try_on_stub() -> None:
    """process_try_on stub returns expected structure with placeholder URL."""
    from app.workers.replicate_worker import process_try_on

    result = await process_try_on({}, "tryon-789", "sha256abc123")

    assert result["try_on_id"] == "tryon-789"
    assert result["status"] == "completed"
    assert "result_cdn_url" in result
    assert "tryon-789" in result["result_cdn_url"]


@pytest.mark.anyio
async def test_generate_reco_claude_stub() -> None:
    """generate_reco_claude stub returns expected structure."""
    from app.workers.claude_worker import generate_reco_claude

    result = await generate_reco_claude({}, "user-111", "reco-222")

    assert result["recommendation_id"] == "reco-222"
    assert result["status"] == "completed"
    assert result["count"] >= 0


def test_vision_worker_settings_has_functions() -> None:
    """WorkerSettings has the expected function list."""
    from app.workers.vision_worker import WorkerSettings

    assert len(WorkerSettings.functions) == 2


def test_replicate_worker_settings_has_functions() -> None:
    """WorkerSettings has the expected function list."""
    from app.workers.replicate_worker import WorkerSettings

    assert len(WorkerSettings.functions) == 1


def test_claude_worker_settings_has_functions() -> None:
    """WorkerSettings has the expected function list."""
    from app.workers.claude_worker import WorkerSettings

    assert len(WorkerSettings.functions) == 1
