# TRIGGER — ANTIGRAVITY SPRINT 0.4

**From:** Jarvis (CEO)  
**To:** Antigravity (Backend Engineer)  
**Date:** 2026-05-18 (SAB)  
**Sprint:** 0.4 — DevOps & Hardening  
**Duration:** 7 días (2026-05-18 a 2026-05-25)  
**Status:** 🟢 APPROVED — Ready to START NOW

---

## 📋 MISSION

Implementar **Rate Limiting + DevOps** para hardening del proyecto:
- Rate limiting (BLOQUEANTE para Sprint 0.5 workers)
- Sentry observability
- PostHog analytics
- Docker multi-stage build
- GitHub Actions CI/CD
- Railway deployment config

---

## 🎯 SCOPE (7 tareas principales)

### 1. RATE LIMITING (CRITICAL — A04-HIGH1, A07-HIGH1)
**Files:** `app/core/rate_limiter.py`, `create_app()` lifespan  
**Status:** Currently declared but not applied (config exists, no middleware)

**Implementation:**
```python
# app/core/rate_limiter.py
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import redis.asyncio as redis

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379",
    strategy="moving-window",
)

# Auth endpoints: 5 requests/min per IP (strict)
@app.post("/auth/login")
@limiter.limit("5/minute")
async def login(...): pass

# AI endpoints: 30 requests/hour per user_id (generous)
@app.post("/api/v1/body-analysis")
@limiter.limit("30/hour", key_func=get_user_id)
async def body_analysis(...): pass

# Backoff exponential on 429:
# Client: retry after X seconds (2^attempt)
# Server: return Retry-After header
```

**Tests:**
- `test_rate_limiting_auth_endpoints.py` — 5/min per IP
- `test_rate_limiting_ai_endpoints.py` — 30/hour per user
- `test_rate_limiting_429_response.py` — Verify Retry-After header

**Cyber Neo Audit:** Must verify 0 bypasses (no hardcoded exemptions)

---

### 2. SUPABASE ARQ POOL (async job queue)
**Files:** `app/core/lifespan.py`, `app/dependencies.py`  
**Status:** ARQ is declared in config, but pool not created in lifespan

**Implementation:**
```python
# app/core/lifespan.py
from arq import create_pool
from arq.connections import RedisSettings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    redis_settings = RedisSettings(host="localhost", port=6379)
    app.state.arq_pool = await create_pool(redis_settings)
    
    yield
    
    # Shutdown
    await app.state.arq_pool.close()

# app/dependencies.py
class ArqPoolDep:
    def __init__(self, request: Request):
        self.pool = request.app.state.arq_pool

# In services:
async def enqueue_job(pool, job_name, payload):
    await pool.enqueue_job(job_name, payload)
```

**Tests:** `test_arq_pool.py` — pool creates, enqueues, processes

---

### 3. SENTRY INTEGRATION
**Files:** `app/core/observability.py` (NEW), `main.py` init  
**Packages:** sentry-sdk[fastapi]

**Implementation:**
```python
# app/core/observability.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

def init_sentry():
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        integrations=[FastApiIntegration()],
        traces_sample_rate=0.1,  # 10% of transactions
        environment=settings.ENV,
    )

# main.py
from app.core.observability import init_sentry
init_sentry()
```

**Config:** Add to `.env.example`:
```
SENTRY_DSN=https://...@sentry.io/...
```

---

### 4. POSTHOG ANALYTICS
**Files:** `app/core/observability.py` (add PostHog), service telemetry  
**Packages:** posthog

**Events to track:**
- `user_registered` (SignUpRequest)
- `try_on_created` (TryOnCreateRequest)
- `subscription_activated` (SubscriptionResponse)
- `body_analysis_completed` (BodyAnalysisResponse)

**Implementation:**
```python
# app/core/observability.py
from posthog import Posthog

posthog = Posthog(
    api_key=settings.POSTHOG_API_KEY,
    host="https://app.posthog.com",
)

# In services:
posthog.capture(
    distinct_id=user_id,
    event="try_on_created",
    properties={"wardrobe_items": 3, "cache_hit": False},
)
```

---

### 5. DOCKER MULTI-STAGE BUILD
**Files:** `Dockerfile` (NEW)

**Specification:**
```dockerfile
# Stage 1: Builder
FROM python:3.12-slim as builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app/ ./app
COPY alembic/ ./alembic
COPY alembic.ini .
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Build & test:**
```bash
docker build -t asesor-imagen-ai:latest .
docker run -p 8000:8000 asesor-imagen-ai:latest
# Verify: curl http://localhost:8000/health
```

---

### 6. DOCKER-COMPOSE (api + worker + redis)
**Files:** `docker-compose.yml` (NEW)

**Specification:**
```yaml
version: "3.9"
services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://...
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
  
  worker:
    build: .
    command: python -m arq app.workers
    environment:
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
```

---

### 7. GITHUB ACTIONS CI/CD
**Files:** `.github/workflows/ci.yml` (NEW)

**Steps:**
1. Checkout
2. Install dependencies
3. Run tests (`pytest`)
4. Run linter (`ruff check`)
5. Build Docker image
6. Run smoke test (docker container health check)

**Specification:**
```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
      redis:
        image: redis:7-alpine
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest tests/ --cov=app --cov-report=xml
      - run: ruff check app/
      - run: docker build -t test:latest .
```

---

## 🎯 DELIVERABLES (End of Day 7)

### Code
- [ ] `app/core/rate_limiter.py` — slowapi + Redis integration
- [ ] `app/core/lifespan.py` — ARQ pool creation (updated)
- [ ] `app/core/observability.py` — Sentry + PostHog init
- [ ] `app/main.py` — init_sentry() called, ARQ pool in lifespan
- [ ] `Dockerfile` — multi-stage build
- [ ] `docker-compose.yml` — api + worker + redis
- [ ] `.github/workflows/ci.yml` — test + lint + build + smoke test
- [ ] `.env.example` — SENTRY_DSN, POSTHOG_API_KEY added

### Configuration
- [ ] Rate limiting config: AUTH_RATE_LIMIT=5/min, AI_RATE_LIMIT=30/hour
- [ ] Redis connection tested (local + Railway)
- [ ] Sentry project created (free tier OK)
- [ ] PostHog project created (free tier OK)
- [ ] Railway.toml created (deploy config)

### Tests
- [ ] `tests/test_rate_limiting.py` (≥3 tests)
- [ ] `tests/test_observability.py` (Sentry + PostHog mocked)
- [ ] `tests/test_readiness_probe.py` (Redis ping included)
- [ ] Coverage ≥80%, ruff clean

### Documentation
- [ ] `docs/DEVOPS_IMPLEMENTATION.md` (NEW) — setup instructions, credentials, debugging

---

## 📋 DEFINITION OF DONE

✅ **Sprint 0.4 is DONE when:**

- [ ] All 7 tasks implemented (code complete)
- [ ] Tests: ≥80% coverage, all passing
- [ ] Ruff: all checks passed, 0 errors
- [ ] Docker: build successful, smoke test passes
- [ ] Readiness probe: `/health` includes Redis ping
- [ ] Credentials: all env vars in `.env.example` (no secrets in code)
- [ ] Cyber Neo audit: PASS (no rate limit bypasses, no RCE vectors)
- [ ] Ego audit: verify fixes are correct + aligned with Architecture

---

## 🚨 BLOCKERS FOR SPRINT 0.5

**Sprint 0.5 CANNOT START without:**
1. ✅ Rate limiting implemented (in this sprint)
2. ✅ ARQ pool real (in this sprint)
3. ⏳ Credenciales GCV + Replicate (Juan Camilo)
4. ⏳ Supabase bucket `/try-ons/` (Jarvis)

---

## 📞 SUPPORT

- Jarvis: Strategy + escalation
- Cyber Neo: Post-delivery audit
- Ego: Final quality sign-off

---

## 🎬 NEXT STEP

**Start NOW.** Day 1/7 begins today.

By EOD Day 7 (2026-05-25), this sprint must be DONE and audited so Sprint 0.5 can start immediately.

**Timeline:** Rate limiting is your Day 1-2 priority. Docker/CI/CD can happen in parallel Days 2-5. Final testing Days 6-7.

Good luck. Let's ship. 🚀

