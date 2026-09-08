import pytest
import datetime
import pytz
from httpx import AsyncClient, ASGITransport
import redis.asyncio as aioredis
from unittest.mock import AsyncMock, patch, MagicMock

from app.main import app
from app.core.rate_limiter import get_bogota_iso_week, get_bogota_sunday_reset_timestamp, TryOnRateLimitMiddleware

@pytest.fixture
def mock_redis():
    mock = AsyncMock(spec=aioredis.Redis)
    # Default behavior: evalsha returns allowed, current_usage
    mock.evalsha.return_value = [1, 1]
    mock.setnx.return_value = True
    return mock

def test_timezone_functions():
    # CR-2: ISO_WEEK in Bogota timezone
    week = get_bogota_iso_week()
    assert week.startswith("20")
    assert "-W" in week

    ts = get_bogota_sunday_reset_timestamp()
    assert ts > 0
    
    bogota = pytz.timezone("America/Bogota")
    dt = datetime.datetime.fromtimestamp(ts, tz=bogota)
    assert dt.weekday() == 6  # Sunday
    assert dt.hour == 23
    assert dt.minute == 59
    assert dt.second == 59

@pytest.mark.asyncio
async def test_middleware_blocks_on_lua_reject(mock_redis):
    # CR-1: Lua script rejects
    mock_redis.evalsha.return_value = [0, 3] # Blocked, usage is 3
    
    middleware = TryOnRateLimitMiddleware(app, redis_pool=mock_redis)
    
    # Create dummy request
    scope = {
        "type": "http",
        "method": "POST",
        "url": "/api/v1/try-ons",
        "path": "/api/v1/try-ons",
        "headers": [(b"idempotency-key", b"test-key")],
        "state": {}
    }
    
    # We must test using httpx with the app, but we need to mock Auth
    # Let's patch validate_supabase_token to allow us through auth_middleware
    with patch("app.core.supabase_auth.validate_supabase_token", return_value={"sub": "test-user-id"}), \
         patch("app.core.middleware.aioredis.from_url", return_value=mock_redis):
        
        # Override the middleware redis pool for TryOnRateLimitMiddleware
        # We can't easily inject mock_redis into the running app's middlewares, so we patch from_url
        with patch("app.core.rate_limiter.aioredis.from_url", return_value=mock_redis):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
                response = await ac.post("/api/v1/try-ons", headers={"Authorization": "Bearer token", "Idempotency-Key": "test"})
                # Should return 429
                assert response.status_code == 429
                assert "Weekly cap reached" in response.json()["detail"]
                assert response.headers["x-ratelimit-remaining"] == "0"

@pytest.mark.asyncio
async def test_middleware_fallback_to_postgres(mock_redis):
    # Simulate Redis Exception to trigger CR-4
    mock_redis.evalsha.side_effect = Exception("Redis down")
    
    with patch("app.core.supabase_auth.validate_supabase_token", return_value={"sub": "test-user-id"}), \
         patch("app.core.middleware.aioredis.from_url", return_value=mock_redis), \
         patch("app.core.rate_limiter.aioredis.from_url", return_value=mock_redis):
         
         # We need to mock the Postgres RPC
         mock_admin = AsyncMock()
         mock_rpc_exec = AsyncMock()
         mock_rpc_exec.execute.return_value = MagicMock(data=4) # Returns 4, meaning blocked
         mock_admin.rpc.return_value = mock_rpc_exec
         
         app.state.supabase_admin = mock_admin
         
         async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post("/api/v1/try-ons", headers={"Authorization": "Bearer token", "Idempotency-Key": "test"})
            # Fallback failed because usage is 4 (> limit of 3), returns 503 fail-closed (Q2)
            assert response.status_code == 503
            assert "Service Unavailable" in response.json()["detail"]

@pytest.mark.asyncio
async def test_idempotency_race_condition(mock_redis):
    # CR-3: SETNX lock fails
    mock_redis.setnx.return_value = False
    mock_redis.get.return_value = None # No cached response, meaning race condition
    
    with patch("app.core.supabase_auth.validate_supabase_token", return_value={"sub": "test-user-id"}), \
         patch("app.core.middleware.aioredis.from_url", return_value=mock_redis):
         
         async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post("/api/v1/try-ons", headers={"Authorization": "Bearer token", "Idempotency-Key": "race-key"})
            assert response.status_code == 409
            assert "Concurrent request processing" in response.json()["detail"]

