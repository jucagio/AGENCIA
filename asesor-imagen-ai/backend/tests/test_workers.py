"""
Tests for ARQ worker stubs.

Sprint 0.3: workers are stubs that validate the ARQ pipeline.
Sprint 0.5: real external API calls (Vision, Replicate, Claude).
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.workers.claude_worker import generate_reco_claude
from app.workers.replicate_worker import process_try_on
from app.workers.vision_worker import vision_analyze_body, vision_tag_wardrobe


@pytest.fixture
def mock_ctx() -> dict:
    """Provides a mocked ARQ context with admin_client."""
    mock_admin = MagicMock()

    # Mock execute for updates and inserts
    mock_execute = AsyncMock(return_value=MagicMock(data=[{}]))
    mock_admin.trusted.return_value.table.return_value.update.return_value.eq.return_value.execute = mock_execute
    mock_admin.trusted.return_value.table.return_value.insert.return_value.execute = mock_execute

    # Mock execute for single selects
    mock_single = AsyncMock(return_value=MagicMock(data={"user_id": "test-user-id", "occasion": "party"}))
    mock_admin.trusted.return_value.table.return_value.select.return_value.eq.return_value.single.return_value.execute = mock_single

    # Mock execute for order limit selects
    mock_order = AsyncMock(return_value=MagicMock(data=[{"body_type": "apple"}]))
    mock_admin.trusted.return_value.table.return_value.select.return_value.eq.return_value.order.return_value.limit.return_value.execute = mock_order

    # Mock execute for list selects
    mock_list_execute = AsyncMock(return_value=MagicMock(data=[{"id": "item1", "category": "top"}]))
    mock_admin.trusted.return_value.table.return_value.select.return_value.eq.return_value.execute = mock_list_execute

    # Mock upsert
    mock_admin.trusted.return_value.table.return_value.upsert.return_value.execute = AsyncMock()

    return {"admin_client": mock_admin}


@pytest.mark.anyio
@patch("app.workers.vision_worker.httpx.AsyncClient.get")
@patch("app.workers.vision_worker.vision_v1.ImageAnnotatorClient")
async def test_vision_tag_wardrobe_valid_image(mock_vision_client: MagicMock, mock_get: AsyncMock, mock_ctx: dict) -> None:
    """Test successful vision tagging."""
    mock_resp = MagicMock()
    mock_resp.content = b"fakeimage"
    mock_resp.raise_for_status = MagicMock()
    mock_get.return_value = mock_resp

    mock_vision_instance = MagicMock()
    mock_label = MagicMock()
    mock_label.description = "T-shirt"
    mock_vision_instance.label_detection.return_value.label_annotations = [mock_label]
    mock_vision_instance.label_detection.return_value.error.message = ""
    mock_vision_client.return_value = mock_vision_instance

    result = await vision_tag_wardrobe(mock_ctx, "item-123", "https://example.com/img.jpg")

    assert result["wardrobe_item_id"] == "item-123"
    assert result["status"] == "completed"
    assert result["tags"]["category"] == "T-shirt"


@pytest.mark.anyio
async def test_vision_worker_invalid_url_raises(mock_ctx: dict) -> None:
    """Test SSRF protection and URL validation."""
    with pytest.raises(ValueError, match="Invalid image URL"):
        await vision_tag_wardrobe(mock_ctx, "item-123", "not-a-url")

    with pytest.raises(ValueError, match="Image URL from untrusted domain"):
        await vision_tag_wardrobe(mock_ctx, "item-123", "https://malicious.com/img.jpg")


@pytest.mark.anyio
@patch("app.workers.vision_worker.httpx.AsyncClient.get")
@patch("app.workers.vision_worker.vision_v1.ImageAnnotatorClient")
@patch("app.workers.vision_worker.anthropic.AsyncAnthropic")
async def test_vision_analyze_body(mock_anthropic: AsyncMock, mock_vision_client: MagicMock, mock_get: AsyncMock, mock_ctx: dict) -> None:
    """Test body analysis with Vision and Claude APIs."""
    mock_resp = MagicMock()
    mock_resp.content = b"fakeimage"
    mock_get.return_value = mock_resp

    mock_vision_instance = MagicMock()
    mock_vision_instance.annotate_image.return_value.error.message = ""
    mock_vision_instance.annotate_image.return_value.label_annotations = []
    mock_vision_instance.annotate_image.return_value.image_properties_annotation.dominant_colors.colors = []
    mock_vision_client.return_value = mock_vision_instance

    mock_anthropic_instance = AsyncMock()
    mock_msg = MagicMock()
    mock_msg.text = '{"body_type": "pear", "skin_tone_category": "warm", "color_season": "spring"}'
    mock_anthropic_instance.messages.create.return_value.content = [mock_msg]
    mock_anthropic.return_value = mock_anthropic_instance

    result = await vision_analyze_body(mock_ctx, "analysis-456", "https://example.com/body.jpg")

    assert result["body_analysis_id"] == "analysis-456"
    assert result["status"] == "completed"
    assert result["result"]["body_type"] == "pear"


@pytest.mark.anyio
@patch("app.workers.replicate_worker.httpx.AsyncClient.get")
@patch("app.workers.replicate_worker.replicate.Client")
@patch("app.workers.replicate_worker.anthropic.AsyncAnthropic")
async def test_replicate_worker_generates_image(mock_anthropic: AsyncMock, mock_replicate_client: MagicMock, mock_get: AsyncMock, mock_ctx: dict) -> None:
    """Test Replicate integration and storage upload."""
    mock_rep_instance = MagicMock()
    mock_rep_instance.run.return_value = ["https://replicate.delivery/out.jpg"]
    mock_replicate_client.return_value = mock_rep_instance

    mock_resp = MagicMock()
    mock_resp.content = b"fakeimage"
    mock_get.return_value = mock_resp

    mock_anthropic_instance = AsyncMock()
    mock_msg = MagicMock()
    mock_msg.text = '{"why_it_works": "test"}'
    mock_anthropic_instance.messages.create.return_value.content = [mock_msg]
    mock_anthropic.return_value = mock_anthropic_instance

    result = await process_try_on(mock_ctx, "tryon-789", "sha256abc123")

    assert result["try_on_id"] == "tryon-789"
    assert result["status"] == "completed"
    assert "result_cdn_url" in result


@pytest.mark.anyio
async def test_replicate_worker_invalid_payload(mock_ctx: dict) -> None:
    """Test Replicate worker handles errors correctly."""
    with pytest.raises(Exception):
        # Without mocks, it should try to fetch the bad URL or hit DB and fail
        await process_try_on(mock_ctx, "tryon-789", "sha256abc123")


@pytest.mark.anyio
@patch("app.workers.claude_worker.anthropic.AsyncAnthropic")
async def test_claude_worker_generates_recommendations(mock_anthropic: AsyncMock, mock_ctx: dict) -> None:
    """Test Claude recommendation worker."""
    mock_anthropic_instance = AsyncMock()
    mock_msg = MagicMock()
    mock_msg.text = '{"outfits": [{"items": [{"id": "item1", "role": "top"}], "why": "nice", "confidence": 0.9}]}'
    mock_anthropic_instance.messages.create.return_value.content = [mock_msg]
    mock_anthropic.return_value = mock_anthropic_instance

    result = await generate_reco_claude(mock_ctx, "user-111", "reco-222")

    assert result["recommendation_id"] == "reco-222"
    assert result["status"] == "completed"
    assert result["count"] == 1


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
