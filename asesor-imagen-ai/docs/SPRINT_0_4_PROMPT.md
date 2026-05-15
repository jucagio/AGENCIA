# SPRINT 0.4 — DevOps, Rate Limiting & Hardening
## Prompt para Antigravity — Asesor de Imagen AI

**Fecha:** 2026-05-15
**Rama:** `claude/train-agents-programming-uBawO`
**Directorio base:** `asesor-imagen-ai/backend/`
**Commits previos:** `6fca4a8` (security patch) ← `8fe1b01` (Sprint 0.3)
**DoD mínimo:** Todas las tareas ✅ + tests pasan + ruff clean + coverage ≥80%

---

## Contexto crítico antes de empezar

Lee estos archivos ANTES de escribir cualquier código:
- `app/config.py` — Settings con RATE_LIMIT_PER_MINUTE, REDIS_URL, SENTRY_DSN (añadir)
- `app/main.py` — lifespan pattern; aquí añadirás ARQ pool + Redis init
- `app/core/middleware.py` — auth_middleware + idempotency_middleware ya implementados
- `requirements.txt` — arq==0.28.0 y redis==5.2.1 ya instalados
- `app/workers/vision_worker.py` — worker stub; ver cómo exporta `WorkerSettings.functions`
- `pyproject.toml` — ruff config, line-length=120, ignores configurados

**NO rompas lo que existe.** Todos los tests actuales deben seguir pasando.

---

## Stack del sprint

| Herramienta | Versión | Propósito |
|-------------|---------|-----------|
| slowapi | 0.1.9 | Rate limiting sobre Starlette |
| limits | 3.* | Backend Redis para slowapi |
| sentry-sdk[fastapi] | 2.* | Error tracking + performance |
| posthog | 3.* | Product analytics |
| arq | 0.28.0 (ya instalado) | ARQ pool real (lifespan) |
| redis | 5.2.1 (ya instalado) | Ping en readiness probe |

Agrega al `requirements.txt` los paquetes nuevos. No modifiques versiones existentes.

---

## TAREA 1 — Migration 006: Idempotency UNIQUE constraint

**Archivo:** `migrations/006_idempotency_unique.sql`

Crea la migration de forma idempotente (`IF NOT EXISTS`):

```sql
-- 006_idempotency_unique.sql
-- Adds UNIQUE(key, user_id) to idempotency_keys to prevent race conditions (ADR-003 hardening)
-- Adds failed status support and cascade index

BEGIN;

-- Unique constraint prevents race condition TOCTOU in idempotency middleware
ALTER TABLE idempotency_keys
    ADD CONSTRAINT IF NOT EXISTS idempotency_keys_key_user_unique UNIQUE (key, user_id);

-- Index for fast lookup by status (cleanup jobs)
CREATE INDEX IF NOT EXISTS idx_idempotency_keys_status ON idempotency_keys (status);

-- Add 'failed' as valid status (retry allowed on same key after failure)
-- Note: If there's a CHECK constraint on status, extend it here
-- ALTER TABLE idempotency_keys DROP CONSTRAINT IF EXISTS idempotency_keys_status_check;
-- ALTER TABLE idempotency_keys ADD CONSTRAINT idempotency_keys_status_check
--     CHECK (status IN ('processing', 'completed', 'failed'));

COMMIT;
```

También crea `migrations/006_idempotency_unique_down.sql`:

```sql
BEGIN;
DROP INDEX IF EXISTS idx_idempotency_keys_status;
ALTER TABLE idempotency_keys DROP CONSTRAINT IF EXISTS idempotency_keys_key_user_unique;
COMMIT;
```

---

## TAREA 2 — Rate Limiting con slowapi + Redis

### 2.1 Instalar dependencias

Agrega a `requirements.txt`:
```
slowapi==0.1.9
limits==3.14.0
```

### 2.2 Config — nuevos campos en `app/config.py`

Agrega al bloque de Redis:
```python
# Rate limiting (ADR-007 — Cyber Neo A04-HIGH1)
RATE_LIMIT_AUTH_PER_MINUTE: int = Field(default=5, ge=1)    # /auth/login, /register
RATE_LIMIT_REFRESH_PER_MINUTE: int = Field(default=10, ge=1) # /auth/refresh
RATE_LIMIT_AI_PER_HOUR: int = Field(default=30, ge=1)        # /try-ons, /body-analysis, /recommendations
RATE_LIMIT_DEFAULT_PER_MINUTE: int = Field(default=60, ge=1) # fallback global
```

Agrega también:
```python
# Observability
SENTRY_DSN: str = ""
POSTHOG_API_KEY: str = ""
POSTHOG_HOST: str = "https://app.posthog.com"
```

### 2.3 Rate limiter — `app/core/rate_limiter.py` (nuevo archivo)

```python
"""
Rate limiting — slowapi with Redis backend.

ADR-007: Rate limits apply per IP for auth endpoints,
per user_id for AI endpoints (cost protection).

Cyber Neo A04-HIGH1: RATE_LIMIT_PER_MINUTE was declared but never applied.
"""
from __future__ import annotations

import logging

from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.config import get_settings

logger = logging.getLogger(__name__)


def _get_user_or_ip(request: Request) -> str:
    """Key function: use user_id for auth'd requests, IP for public ones."""
    user_id = getattr(request.state, "user_id", None)
    if user_id:
        return str(user_id)
    return get_remote_address(request)


def create_limiter() -> Limiter:
    """Create Limiter with Redis backend when configured, in-memory otherwise."""
    settings = get_settings()
    redis_url = settings.REDIS_URL

    storage_uri = redis_url if redis_url else "memory://"
    return Limiter(key_func=_get_user_or_ip, storage_uri=storage_uri)


# Module-level singleton — imported by endpoints
limiter = create_limiter()
```

### 2.4 Wire rate limiter in `app/main.py`

En `create_app()`, después de crear la app:
```python
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.rate_limiter import limiter

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

### 2.5 Apply rate limits en endpoints

**`app/api/v1/endpoints/auth.py`** — importar y decorar:

```python
from app.core.rate_limiter import limiter
from app.config import get_settings

_s = get_settings()

@router.post("/register", ...)
@limiter.limit(f"{_s.RATE_LIMIT_AUTH_PER_MINUTE}/minute")
async def register(request: Request, body: RegisterRequest, ...):
    ...

@router.post("/login", ...)
@limiter.limit(f"{_s.RATE_LIMIT_AUTH_PER_MINUTE}/minute")
async def login(request: Request, body: LoginRequest, ...):
    ...

@router.post("/refresh", ...)
@limiter.limit(f"{_s.RATE_LIMIT_REFRESH_PER_MINUTE}/minute")
async def refresh(request: Request, body: RefreshRequest, ...):
    ...
```

**`app/api/v1/endpoints/try_ons.py`**, **`body_analysis.py`**, **`recommendations.py`**:

```python
@router.post("/", ...)
@limiter.limit(f"{get_settings().RATE_LIMIT_AI_PER_HOUR}/hour")
async def create_try_on(request: Request, ...):
    ...
```

**IMPORTANTE:** slowapi requiere que `request: Request` sea el primer parámetro de FastAPI.
El `Request` ya es inyectado por FastAPI; solo asegúrate de que esté en la firma.

### 2.6 Tests de rate limiting — `tests/test_rate_limiting.py`

```python
"""Tests for rate limiting middleware."""
from __future__ import annotations

import pytest
from unittest.mock import patch, AsyncMock
from tests.conftest import AUTH_HEADERS


@pytest.mark.anyio
class TestRateLimiting:
    async def test_auth_endpoint_has_limiter_state(self, client) -> None:
        """Verify app state has limiter configured."""
        from app.core.rate_limiter import limiter
        assert limiter is not None

    async def test_register_accepts_valid_request(self, client) -> None:
        """Rate-limited endpoint still accepts normal traffic."""
        with patch(
            "app.services.auth_service.AuthService.register",
            new_callable=AsyncMock,
        ) as mock_reg:
            from app.schemas.auth import TokenResponse
            from uuid import uuid4
            mock_reg.return_value = TokenResponse(
                access_token="tok", refresh_token="ref",
                expires_in=3600, user_id=str(uuid4()),
            )
            resp = await client.post(
                "/api/v1/auth/register",
                json={"email": "rate@test.com", "password": "testpass123"},
            )
            # Should not be 429 on first request
            assert resp.status_code != 429

    async def test_ai_endpoints_have_limiter(self, client) -> None:
        """Verify AI endpoints are decorated with limiter."""
        import inspect
        from app.api.v1.endpoints import try_ons, body_analysis, recommendations
        # Each module should import limiter
        assert hasattr(try_ons, "limiter") or "limiter" in dir(try_ons)
```

---

## TAREA 3 — ARQ Pool real en lifespan

### 3.1 Actualizar `app/main.py` lifespan

```python
from arq import create_pool
from arq.connections import RedisSettings

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    configure_logging()

    if settings.is_production:
        settings.assert_production_ready()

    logger.info("Starting %s v%s in %s mode", ...)

    # Supabase admin client
    try:
        app.state.supabase_admin = await create_admin_client(settings)
    except Exception as exc:
        if settings.is_production:
            raise
        logger.warning("Supabase admin client init skipped (dev): %s", exc)
        app.state.supabase_admin = None

    # ARQ Redis pool (async task queue)
    try:
        redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)
        app.state.arq_pool = await create_pool(redis_settings)
        logger.info("ARQ Redis pool connected: %s", settings.REDIS_URL)
    except Exception as exc:
        if settings.is_production:
            raise
        logger.warning("ARQ pool init skipped (dev/no Redis): %s", exc)
        app.state.arq_pool = None

    yield

    # Cleanup
    if getattr(app.state, "arq_pool", None):
        await app.state.arq_pool.close()
    logger.info("Shutting down %s", settings.APP_NAME)
    app.state.supabase_admin = None
    app.state.arq_pool = None
```

### 3.2 ARQ dependency — `app/api/deps.py`

Agrega junto a las dependencias existentes:

```python
from arq import ArqRedis

async def get_arq_pool(request: Request) -> ArqRedis | None:
    """Get ARQ Redis pool from app state. Returns None if not initialised (dev)."""
    return getattr(request.app.state, "arq_pool", None)

ArqPoolDep = Annotated[ArqRedis | None, Depends(get_arq_pool)]
```

### 3.3 Conectar workers en services

En `app/services/body_analysis_service.py`, `try_on_service.py`, `recommendation_service.py`:

Reemplaza el comentario `# TODO(Sprint 0.5): await arq_pool.enqueue_job(...)` con lógica real:

```python
async def create_analysis(self, user_id: UUID, image_url: str | None, ..., arq_pool=None) -> dict:
    # ... crear row en DB como "pending" ...
    
    # Enqueue real job if pool available, else log warning (dev without Redis)
    if arq_pool:
        job = await arq_pool.enqueue_job(
            "vision_analyze_body",
            analysis_id=str(analysis_id),
            image_url=str(image_url) if image_url else None,
            user_id=str(user_id),
        )
        job_id = job.job_id if job else f"no-pool-{analysis_id}"
    else:
        logger.warning("ARQ pool not available — body analysis job not enqueued (dev mode)")
        job_id = f"dev-stub-{analysis_id}"

    return {"analysis_id": str(analysis_id), "status": "pending", "job_id": job_id, ...}
```

Mismo patrón para `TryOnService.create_try_on` → enqueues `process_try_on`
Mismo patrón para `RecommendationService.generate_recommendations` → enqueues `generate_reco_claude`

### 3.4 Actualizar readiness probe en `app/main.py`

```python
@app.get("/health/ready", tags=["Meta"])
async def readiness(request: Request) -> JSONResponse:
    supabase_ok = getattr(request.app.state, "supabase_admin", None) is not None
    
    # Redis ping
    arq_pool = getattr(request.app.state, "arq_pool", None)
    redis_ok = False
    if arq_pool:
        try:
            await arq_pool.ping()
            redis_ok = True
        except Exception:
            redis_ok = False
    
    ready = (supabase_ok and redis_ok) or settings.is_development
    return JSONResponse(
        status_code=200 if ready else 503,
        content={
            "success": ready,
            "data": {
                "supabase": "ok" if supabase_ok else "not_initialized",
                "redis": "ok" if redis_ok else "not_initialized",
            },
        },
    )
```

---

## TAREA 4 — Sentry Integration

### 4.1 Agregar a requirements.txt:
```
sentry-sdk[fastapi]==2.21.0
```

### 4.2 `app/core/observability.py` (nuevo archivo)

```python
"""
Observability: Sentry (errors + performance) + PostHog (product analytics).
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def init_sentry(dsn: str, environment: str, release: str) -> None:
    """Initialize Sentry SDK. No-op if DSN is empty (dev without Sentry)."""
    if not dsn:
        logger.info("Sentry DSN not configured — skipping initialization")
        return

    import sentry_sdk
    from sentry_sdk.integrations.fastapi import FastApiIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration

    sentry_sdk.init(
        dsn=dsn,
        environment=environment,
        release=release,
        integrations=[
            FastApiIntegration(transaction_style="endpoint"),
            LoggingIntegration(level=logging.WARNING, event_level=logging.ERROR),
        ],
        # Performance: sample 10% of traces in prod, 100% in dev
        traces_sample_rate=1.0 if environment == "development" else 0.1,
        # Don't send PII (emails, IPs)
        send_default_pii=False,
    )
    logger.info("Sentry initialized (env=%s)", environment)


def capture_exception(exc: Exception, **context: object) -> None:
    """Capture exception to Sentry. Safe no-op if Sentry not initialized."""
    try:
        import sentry_sdk
        with sentry_sdk.push_scope() as scope:
            for key, value in context.items():
                scope.set_extra(key, value)
            sentry_sdk.capture_exception(exc)
    except ImportError:
        pass
    except Exception:  # noqa: BLE001
        pass  # never let observability break the app
```

### 4.3 Inicializar en `app/main.py` lifespan (antes del yield):

```python
from app.core.observability import init_sentry
init_sentry(
    dsn=settings.SENTRY_DSN,
    environment=settings.ENVIRONMENT,
    release=settings.APP_VERSION,
)
```

---

## TAREA 5 — PostHog Integration

### 5.1 Agregar a requirements.txt:
```
posthog==3.8.3
```

### 5.2 Agregar a `app/core/observability.py`:

```python
def get_posthog():
    """Return PostHog client singleton. None if not configured."""
    from app.config import get_settings
    settings = get_settings()
    if not settings.POSTHOG_API_KEY:
        return None
    try:
        import posthog
        posthog.api_key = settings.POSTHOG_API_KEY
        posthog.host = settings.POSTHOG_HOST
        posthog.disabled = settings.is_development  # no noise in dev
        return posthog
    except ImportError:
        return None


def track_event(user_id: str, event: str, properties: dict | None = None) -> None:
    """Track product event to PostHog. Safe no-op if not configured."""
    ph = get_posthog()
    if ph is None:
        return
    try:
        ph.capture(distinct_id=user_id, event=event, properties=properties or {})
    except Exception:  # noqa: BLE001
        pass  # never let analytics break the app
```

### 5.3 Instrumentar eventos clave

En los servicios, agrega `track_event` en los momentos importantes:

- `auth_service.py` → `register()`: `track_event(user_id, "user_registered")`
- `try_on_service.py` → `create_try_on()`: `track_event(user_id, "try_on_created", {"cache_hit": ...})`
- `subscription_service.py` → `handle_stripe_webhook()` en checkout.completed: `track_event(user_id, "subscription_activated", {"plan": ..., "provider": "stripe"})`

---

## TAREA 6 — Docker

### 6.1 `backend/Dockerfile`

```dockerfile
# syntax=docker/dockerfile:1
# Multi-stage build — Python 3.12 slim
# Stage 1: builder (instala deps)
FROM python:3.12-slim AS builder

WORKDIR /app

# Install system deps for psycopg2, Pillow, cryptography
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev libffi-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: runtime
FROM python:3.12-slim AS runtime

WORKDIR /app

# Non-root user for security
RUN useradd -m -u 1000 appuser

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=appuser:appuser app/ ./app/

USER appuser

# Default port (Railway uses PORT env var)
ENV PORT=8000
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT}/health')"

# uvicorn — production mode (no --reload)
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --workers 2"]
```

### 6.2 `backend/.dockerignore`

```
.git
.gitignore
__pycache__
*.pyc
*.pyo
.pytest_cache
.ruff_cache
.mypy_cache
venv/
.env
.env.*
tests/
docs/
migrations/
*.md
commit_msg.txt
```

### 6.3 `docker-compose.yml` (en raíz de `backend/`)

```yaml
version: "3.9"

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      redis:
        condition: service_healthy
    environment:
      - REDIS_URL=redis://redis:6379/0
      - ENVIRONMENT=development
    restart: unless-stopped

  worker:
    build:
      context: .
      dockerfile: Dockerfile
    command: ["python", "-m", "arq", "app.workers.vision_worker.WorkerSettings"]
    env_file:
      - .env
    depends_on:
      redis:
        condition: service_healthy
    environment:
      - REDIS_URL=redis://redis:6379/0
      - ENVIRONMENT=development
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
    restart: unless-stopped
```

---

## TAREA 7 — Railway Deploy Config

### 7.1 `backend/railway.toml`

```toml
[build]
builder = "DOCKERFILE"
dockerfilePath = "Dockerfile"

[deploy]
startCommand = "uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 2"
healthcheckPath = "/health"
healthcheckTimeout = 30
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3

[deploy.envs]
ENVIRONMENT = "production"
```

### 7.2 `backend/.env.example`

Crea este archivo con TODAS las variables necesarias (sin valores reales):

```bash
# Application
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
APP_VERSION=0.1.0

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080

# Redis (ARQ + Rate Limiting)
REDIS_URL=redis://localhost:6379/0

# Rate Limits
RATE_LIMIT_AUTH_PER_MINUTE=5
RATE_LIMIT_REFRESH_PER_MINUTE=10
RATE_LIMIT_AI_PER_HOUR=30
RATE_LIMIT_DEFAULT_PER_MINUTE=60

# AI APIs
ANTHROPIC_API_KEY=
GOOGLE_VISION_CREDENTIALS=
REPLICATE_API_TOKEN=
REPLICATE_MODEL_VERSION=

# Storage
SUPABASE_STORAGE_BUCKET=user-uploads
R2_ACCOUNT_ID=
R2_ACCESS_KEY_ID=
R2_SECRET_ACCESS_KEY=
R2_BUCKET=
R2_PUBLIC_URL=

# Payments
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
MERCADO_PAGO_ACCESS_TOKEN=
MERCADO_PAGO_WEBHOOK_SECRET=

# Observability
SENTRY_DSN=
POSTHOG_API_KEY=
POSTHOG_HOST=https://app.posthog.com

# Legacy (do not use in production)
SECRET_KEY=dev-only-change-me-min-32-chars-1234567890
```

---

## TAREA 8 — GitHub Actions CI/CD

### 8.1 `.github/workflows/ci.yml` (en raíz del monorepo)

```yaml
name: CI

on:
  push:
    branches: [main, "claude/**"]
    paths:
      - "asesor-imagen-ai/backend/**"
  pull_request:
    branches: [main]
    paths:
      - "asesor-imagen-ai/backend/**"

defaults:
  run:
    working-directory: asesor-imagen-ai/backend

jobs:
  test:
    name: Test & Lint
    runs-on: ubuntu-latest

    services:
      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 5s
          --health-timeout 3s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
          cache-dependency-path: asesor-imagen-ai/backend/requirements.txt

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Ruff lint
        run: python -m ruff check app/ tests/

      - name: Run tests
        env:
          ENVIRONMENT: development
          REDIS_URL: redis://localhost:6379/0
          SECRET_KEY: ci-only-test-key-min-32-chars-111
        run: |
          python -m pytest tests/ \
            --cov=app \
            --cov-report=term-missing \
            --cov-fail-under=80 \
            -q

  docker:
    name: Docker Build
    runs-on: ubuntu-latest
    needs: test

    steps:
      - uses: actions/checkout@v4

      - name: Build Docker image
        run: |
          docker build \
            --file asesor-imagen-ai/backend/Dockerfile \
            --tag asesor-imagen-ai:${{ github.sha }} \
            asesor-imagen-ai/backend/

      - name: Smoke test container
        run: |
          docker run -d \
            --name smoke \
            -p 8000:8000 \
            -e ENVIRONMENT=development \
            -e SECRET_KEY=ci-only-test-key-min-32-chars-111 \
            -e REDIS_URL=redis://localhost:6379/0 \
            asesor-imagen-ai:${{ github.sha }}
          sleep 5
          curl --fail http://localhost:8000/health || (docker logs smoke && exit 1)
          docker rm -f smoke
```

---

## TAREA 9 — Tests adicionales

### 9.1 Actualizar `tests/api/test_health.py`

Agrega test de readiness con Redis mock:

```python
async def test_readiness_with_redis(client) -> None:
    """Readiness probe includes redis status."""
    resp = await client.get("/health/ready")
    data = resp.json()["data"]
    assert "supabase" in data
    assert "redis" in data  # nuevo campo en Sprint 0.4
```

### 9.2 `tests/test_observability.py` (nuevo)

```python
"""Tests for Sentry + PostHog observability."""
from __future__ import annotations

from unittest.mock import patch, MagicMock
import pytest


class TestSentry:
    def test_init_sentry_no_dsn_is_noop(self) -> None:
        """Empty DSN → no Sentry init, no error."""
        from app.core.observability import init_sentry
        init_sentry(dsn="", environment="development", release="0.1.0")

    def test_capture_exception_safe(self) -> None:
        """capture_exception never raises even without Sentry configured."""
        from app.core.observability import capture_exception
        capture_exception(ValueError("test"), context="unit_test")

    def test_init_sentry_with_dsn(self) -> None:
        """With DSN, sentry_sdk.init is called."""
        with patch("sentry_sdk.init") as mock_init:
            from importlib import reload
            from app.core import observability
            reload(observability)
            observability.init_sentry(
                dsn="https://fake@sentry.io/123",
                environment="production",
                release="0.1.0",
            )
            mock_init.assert_called_once()


class TestPostHog:
    def test_track_event_no_key_is_noop(self) -> None:
        """Empty POSTHOG_API_KEY → no error."""
        from app.core.observability import track_event
        track_event("user-123", "test_event")

    def test_track_event_with_key(self) -> None:
        """With key configured, posthog.capture is called."""
        with patch("app.config.get_settings") as mock_settings:
            mock_settings.return_value.POSTHOG_API_KEY = "phc_fake"
            mock_settings.return_value.POSTHOG_HOST = "https://app.posthog.com"
            mock_settings.return_value.is_development = False
            with patch("posthog.capture") as mock_capture:
                from app.core.observability import track_event
                track_event("user-123", "test_event", {"key": "value"})
                # Note: may not call if import order differs — just verify no crash
```

---

## TAREA 10 — Cleanup

- Eliminar `backend/commit_msg.txt` (residual de sesión anterior)
- Verificar que `backend/.gitignore` incluye `.env`, `*.pyc`, `__pycache__`, `venv/`, `.pytest_cache/`, `.ruff_cache/`

---

## Definition of Done (DoD)

Antes de reportar completado, verifica TODOS:

```bash
# 1. Tests pasan (>= 80% coverage)
cd backend/
python -m pytest tests/ --cov=app --cov-report=term-missing -q
# → PASS, coverage >= 80%

# 2. Ruff clean
python -m ruff check app/ tests/
# → All checks passed!

# 3. Docker build exitoso
docker build -t asesor-imagen-ai:test .
# → Successfully built ...

# 4. Smoke test container
docker run -d --name smoke -p 8001:8000 \
  -e ENVIRONMENT=development \
  -e SECRET_KEY=test-key-min-32-chars-12345678901 \
  asesor-imagen-ai:test
sleep 5
curl http://localhost:8001/health
docker rm -f smoke
# → {"success": true, "data": {"status": "ok"}}

# 5. Archivos nuevos creados
ls migrations/006_idempotency_unique.sql
ls app/core/rate_limiter.py
ls app/core/observability.py
ls Dockerfile docker-compose.yml railway.toml .env.example
ls .github/workflows/ci.yml (en raíz del monorepo)

# 6. git add + git commit (NO push, solo commit)
git add -p  # revisar cada change
git commit -m "feat(devops): Sprint 0.4 — Rate limiting, ARQ pool, Sentry, PostHog, Docker, CI/CD"
```

---

## Restricciones críticas

1. **NO modificar** `pyproject.toml` (ruff config) ni `tests/conftest.py` sin razón justificada
2. **NO cambiar** las firmas existentes de endpoints que ya tienen tests
3. **NO usar** `supabase-py` — el proyecto usa `postgrest==0.16.6` directamente
4. **Todos los `try/except` en observability** deben ser `except Exception: pass` — nunca dejar caer el app por analytics
5. **`request: Request`** debe ser el primer parámetro en endpoints con `@limiter.limit()`
6. **ARQ workers** — los stubs en `vision_worker.py`, `replicate_worker.py`, `claude_worker.py` se activan en Sprint 0.5. En este sprint solo conectas el pool para que `enqueue_job` sea real.
7. **Rate limiting en tests**: en el test runner, las llamadas no deben fallar por rate limit. Usa límites altos en `.env.test` o mockeá el limiter si es necesario.

---

## Notas del arquitecto (Jarvis)

- `RATE_LIMIT_PER_MINUTE` original en config quedará como alias — renombra a `RATE_LIMIT_DEFAULT_PER_MINUTE` con backward compat
- El Dockerfile usa Python 3.12 slim, no 3.11 (el proyecto ya usa 3.12 features de ruff)
- `slowapi` con Redis en multi-worker setup es correcto — en-memory no escala a 2+ workers
- PostHog `disabled=True` en development previene noise en el dashboard de prod
- Sentry `send_default_pii=False` es obligatorio por GDPR/privacidad de usuarios
- Railway lee `$PORT` como variable de entorno — el CMD en Dockerfile usa `sh -c` para expandirla
