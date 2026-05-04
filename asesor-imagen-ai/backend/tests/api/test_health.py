"""
Tests for the /health endpoint.

Sprint 0 validation: ensure the app starts and responds correctly.
"""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.anyio
async def test_health_returns_200():
    """Health endpoint should return 200 with status ok."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "ok"
    assert data["data"]["version"] == "0.1.0"


@pytest.mark.anyio
async def test_health_has_security_headers():
    """Health endpoint response should include OWASP security headers."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/health")

    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"
    assert response.headers.get("X-Request-ID") is not None


@pytest.mark.anyio
async def test_health_has_correct_content_type():
    """Health endpoint should return JSON."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/health")

    assert "application/json" in response.headers.get("content-type", "")


@pytest.mark.anyio
async def test_nonexistent_endpoint_returns_404():
    """Requesting a non-existent endpoint should return 404 with error body."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/api/v1/nonexistent")

    assert response.status_code == 404
    data = response.json()
    # FastAPI returns {"detail": "Not Found"} for unmatched routes
    assert "detail" in data or "error" in data


@pytest.mark.anyio
async def test_openapi_docs_available_in_dev():
    """OpenAPI docs should be available in development mode."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/docs")

    # In development mode, docs should be available (200 or redirect)
    assert response.status_code == 200
