# SPRINT 0.3 — Services & Endpoints
## Prompt ejecutivo para Google Antigravity

**Versión:** 1.0
**Fecha:** 2026-04-30
**Commit base:** `ded674c` (Sprint 0.2 completo, 107 tests, 85.32% coverage)
**Repositorio:** `asesor-imagen-ai/backend/`
**Owner:** Jarvis (CEO Agencia) → Antigravity (ejecutor)

---

## 🎯 OBJETIVO DE ESTE SPRINT

Construir la **capa de servicios y endpoints completa** del backend:
- Activar autenticación real (Supabase JWKS + PyJWT)
- Activar idempotency middleware completo (replay logic)
- Implementar 7 módulos de servicios
- Implementar 8 módulos de endpoints (24+ rutas)
- Implementar 3 ARQ workers (vision, replicate, claude)
- `ruff` + `mypy` limpios, coverage >=80%, todos los tests en verde

**Al finalizar:** `uvicorn app.main:app --reload` levanta y **todos los endpoints responden** correctamente (con Supabase mock en tests, real en prod).

---

## 📋 ESTADO ACTUAL (lo que ya existe — NO tocar sin razón)

```
backend/app/
├── config.py              ✅ Pydantic v2, lru_cache, Settings completo
├── main.py                ✅ lifespan, middlewares, exception handlers
├── core/
│   ├── admin_client.py    ✅ AdminClient (.with_user_check, .trusted, .schema fix)
│   ├── database.py        ✅ postgrest-py 0.16.6 client
│   ├── exceptions.py      ✅ AuthenticationError, NotFoundError, ValidationError, etc.
│   ├── middleware.py       ✅ logging, CORS, security headers. PENDIENTE: activar auth + idempotency
│   └── security.py        ⚠️  LEGACY — python-jose (CVE-2024-33664/33663). REEMPLAZAR con PyJWT
├── models/                ✅ 9 modelos Pydantic v2 (profile, wardrobe, body_analysis, try_on,
│                             recommendation, subscription, usage_counter, user_style_profile)
├── schemas/               ✅ auth.py, profile.py, wardrobe.py, body_analysis.py,
│                             try_on.py, recommendation.py, subscription.py
├── repositories/
│   ├── base.py            ✅ BaseRepository + paginación
│   └── repos.py           ✅ 9 repos concretos (Profile, Wardrobe, BodyAnalysis,
│                              Recommendation, RecommendationItem, TryOn,
│                              Subscription, UserStyleProfile, UsageCounter)
├── services/__init__.py   ❌ VACÍO — construir en este sprint
├── api/v1/
│   ├── router.py          ❌ VACÍO (shell) — activar en este sprint
│   └── endpoints/__init__.py ❌ — construir módulos aquí
└── workers/               ❌ No existe — crear en este sprint
```

---

## 🛠️ TAREAS ORDENADAS (ejecutar en secuencia)

### TAREA 1 — Reemplazar python-jose → PyJWT[crypto]

**Archivo:** `requirements.txt` o `pyproject.toml`

```
# ELIMINAR:
python-jose[cryptography]

# AGREGAR:
PyJWT[crypto]>=2.9.0
cryptography>=42.0.0
httpx>=0.27.0          # si no está ya
```

**Nuevo archivo:** `backend/app/core/supabase_auth.py`

Implementar JWKS validation con PyJWT para Supabase Auth (ADR-001):

```python
"""
Supabase Auth JWKS validator (ADR-001).

Fetches JWKS from Supabase, caches with TTL, validates ES256 tokens.
Replaces legacy python-jose (CVE-2024-33664, CVE-2024-33663).

References:
  https://supabase.com/docs/guides/auth/jwks
  https://pyjwt.readthedocs.io/en/stable/usage.html#retrieve-rsa-signing-keys-from-a-jwks-endpoint
"""

import time
import httpx
from jwt import PyJWKClient, decode as jwt_decode, PyJWTError
from app.config import get_settings
from app.core.exceptions import AuthenticationError

# Module-level JWKS client (cached internally by PyJWKClient).
_jwks_client: PyJWKClient | None = None
_jwks_last_refresh: float = 0.0

def _get_jwks_client() -> PyJWKClient:
    """Return a (re)initialized PyJWKClient, refreshing if TTL expired."""
    global _jwks_client, _jwks_last_refresh
    settings = get_settings()
    ttl = settings.SUPABASE_JWKS_CACHE_TTL_SECONDS
    now = time.monotonic()
    if _jwks_client is None or (now - _jwks_last_refresh) > ttl:
        _jwks_client = PyJWKClient(settings.supabase_jwks_url, cache_jwk_set=True, lifespan=ttl)
        _jwks_last_refresh = now
    return _jwks_client

def validate_supabase_token(token: str) -> dict:
    """
    Validate a Supabase-issued JWT against JWKS.

    Returns:
        Decoded payload dict with 'sub' (user UUID), 'role', 'aud', etc.

    Raises:
        AuthenticationError: if token is missing, expired, or invalid.
    """
    settings = get_settings()
    if not token:
        raise AuthenticationError("Authorization token missing")
    try:
        client = _get_jwks_client()
        signing_key = client.get_signing_key_from_jwt(token)
        payload = jwt_decode(
            token,
            signing_key.key,
            algorithms=["ES256", "RS256"],
            audience=settings.SUPABASE_JWT_AUDIENCE,
            options={"verify_exp": True},
        )
        if not payload.get("sub"):
            raise AuthenticationError("Invalid token: missing sub claim")
        return payload
    except PyJWTError as exc:
        raise AuthenticationError(f"Invalid or expired token: {exc}") from exc
```

**Actualizar `core/security.py`** — eliminar todo el código python-jose. Mantener únicamente `hash_password` y `verify_password` (se usan en tests legacy hasta que Supabase Auth sea el único path).

---

### TAREA 2 — Activar auth_middleware en middleware.py

El middleware ya existe como stub. Reemplazar la función `auth_middleware` con implementación real:

```python
# Rutas públicas que NO requieren JWT
PUBLIC_ROUTES: frozenset[str] = frozenset({
    "/",
    "/health",
    "/health/ready",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/api/v1/auth/register",   # POST registro → Supabase Auth
    "/api/v1/auth/login",      # POST login → Supabase Auth
    "/api/v1/auth/refresh",    # POST refresh → Supabase Auth
    "/api/v1/webhooks/stripe", # validado por Stripe-Signature header
    "/api/v1/webhooks/mercadopago",
})

async def auth_middleware(request: Request, call_next: CallNext) -> Response:
    """
    Validate Supabase JWT (ADR-001). Skip PUBLIC_ROUTES.
    Attach decoded payload to request.state.user_payload.
    Attach user UUID string to request.state.user_id.
    """
    from app.core.supabase_auth import validate_supabase_token
    from app.core.exceptions import AuthenticationError

    if request.url.path in PUBLIC_ROUTES:
        return await call_next(request)

    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"detail": "Authorization header missing or malformed"})

    token = auth_header[7:]
    try:
        payload = validate_supabase_token(token)
        request.state.user_payload = payload
        request.state.user_id = payload["sub"]
    except AuthenticationError as exc:
        return JSONResponse(status_code=401, content={"detail": str(exc)})

    return await call_next(request)
```

Importar `JSONResponse` de fastapi.responses en middleware.py.

---

### TAREA 3 — Activar idempotency_middleware completamente (ADR-003)

Reemplazar el stub de `idempotency_middleware` con lógica completa:

```
Lógica:
1. Si la ruta NO está en IDEMPOTENT_ENDPOINTS → pasar directo (call_next)
2. Leer header Idempotency-Key. Si falta → 422
3. Buscar en tabla `idempotency_keys` WHERE key = <valor> AND user_id = <user_id>
4. Si encontrado Y status = 'completed' → retornar response_body cacheado (200 o 202)
5. Si no existe → crear registro con status='processing'
6. Llamar call_next(request) → obtener response
7. Serializar response body, actualizar registro con status='completed', response_body, status_code
8. Retornar response

Usar AdminClient.trusted() para leer/escribir idempotency_keys (es infraestructura, no user data).
IDEMPOTENCY_TTL_SECONDS = 86400 (ya en config.py).
```

Schema tabla `idempotency_keys` (ya en migration 004):
```sql
CREATE TABLE idempotency_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    key TEXT NOT NULL UNIQUE,
    user_id UUID REFERENCES auth.users(id),
    request_path TEXT NOT NULL,
    request_method TEXT NOT NULL,
    response_status INTEGER,
    response_body JSONB,
    status TEXT DEFAULT 'processing',
    created_at TIMESTAMPTZ DEFAULT now(),
    expires_at TIMESTAMPTZ NOT NULL
);
```

---

### TAREA 4 — Dependency Injection (`app/api/deps.py`)

Crear archivo nuevo con las dependencias FastAPI reutilizables:

```python
"""
FastAPI dependency providers.

Usage in endpoints:
    from app.api.deps import CurrentUser, get_admin_client
    
    @router.get("/me")
    async def get_me(user: CurrentUser, admin: AdminClient = Depends(get_admin_client)):
        ...
"""
from typing import Annotated
from uuid import UUID
from fastapi import Depends, Request
from app.core.admin_client import AdminClient
from app.core.database import get_admin_client as _db_get_admin_client
from app.core.exceptions import AuthenticationError

def get_current_user_id(request: Request) -> UUID:
    """Extract user UUID from JWT payload attached by auth_middleware."""
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise AuthenticationError("User not authenticated")
    return UUID(user_id)

def get_admin_client() -> AdminClient:
    """Provide AdminClient instance via DI."""
    return _db_get_admin_client()

CurrentUser = Annotated[UUID, Depends(get_current_user_id)]
AdminDep = Annotated[AdminClient, Depends(get_admin_client)]
```

---

### TAREA 5 — Supabase Auth HTTP client (`app/services/auth_service.py`)

Implementar auth via Supabase GoTrue API REST (no supabase-py — ya reemplazado por postgrest-py):

```python
"""
Auth service — wraps Supabase GoTrue REST API.

ADR-001: usamos Supabase Auth nativo. No tabla users propia, no bcrypt en auth path.
Calls GoTrue endpoints:
  POST /auth/v1/signup
  POST /auth/v1/token?grant_type=password
  POST /auth/v1/token?grant_type=refresh_token
  GET  /auth/v1/user  (with access token)
"""
import httpx
from uuid import UUID
from app.config import get_settings
from app.core.exceptions import AuthenticationError, ValidationError as AppValidationError
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse

class AuthService:
    def __init__(self) -> None:
        self._settings = get_settings()
        self._base = f"{self._settings.SUPABASE_URL}/auth/v1"
        self._headers = {
            "apikey": self._settings.SUPABASE_ANON_KEY,
            "Content-Type": "application/json",
        }

    async def register(self, req: RegisterRequest) -> TokenResponse:
        """Register via Supabase GoTrue /signup."""
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self._base}/signup",
                json={"email": req.email, "password": req.password},
                headers=self._headers,
            )
        if resp.status_code not in (200, 201):
            data = resp.json()
            msg = data.get("msg") or data.get("message") or "Registration failed"
            raise AppValidationError(message=msg, fields={"email": msg})
        data = resp.json()
        return self._to_token_response(data)

    async def login(self, req: LoginRequest) -> TokenResponse:
        """Login via Supabase GoTrue password grant."""
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self._base}/token?grant_type=password",
                json={"email": req.email, "password": req.password},
                headers=self._headers,
            )
        if resp.status_code != 200:
            raise AuthenticationError("Invalid email or password")
        return self._to_token_response(resp.json())

    async def refresh(self, refresh_token: str) -> TokenResponse:
        """Exchange refresh_token for new access_token."""
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self._base}/token?grant_type=refresh_token",
                json={"refresh_token": refresh_token},
                headers=self._headers,
            )
        if resp.status_code != 200:
            raise AuthenticationError("Invalid or expired refresh token")
        return self._to_token_response(resp.json())

    @staticmethod
    def _to_token_response(data: dict) -> TokenResponse:
        return TokenResponse(
            access_token=data["access_token"],
            token_type="bearer",
            refresh_token=data.get("refresh_token", ""),
            expires_in=data.get("expires_in", 3600),
            user_id=data["user"]["id"],
        )
```

---

### TAREA 6 — Services restantes

Crear los siguientes servicios. Pueden usar stubs funcionales donde la IA externa (Vision, Replicate, Claude) no está aún integrada — pero deben encolarse en ARQ.

#### `app/services/user_service.py`
- `get_profile(user_id) -> Profile | None` — usa ProfileRepository
- `update_profile(user_id, update) -> Profile` — usa ProfileRepository
- `delete_account(user_id) -> None` — soft delete, llama Supabase Auth admin delete
- `get_body_analysis(user_id) -> BodyAnalysis | None`

#### `app/services/wardrobe_service.py`
- `list_items(user_id, page, size) -> list[WardrobeItem]`
- `get_item(user_id, item_id) -> WardrobeItem`
- `create_item(user_id, data, image_bytes) -> WardrobeItem`
  - Upload image a Supabase Storage vía HTTP (o stub con URL directa en tests)
  - Encolar vision_worker para auto-tagging
- `update_item(user_id, item_id, update) -> WardrobeItem`
- `delete_item(user_id, item_id) -> None` — soft delete (deleted_at)

#### `app/services/body_analysis_service.py`
- `create_analysis(user_id, image_bytes) -> dict[str, str]`
  - Verifica usage_counter (free cap ADR-007)
  - Encola `vision_worker` via ARQ → retorna `{job_id, status: "pending"}`
- `get_analysis(user_id, analysis_id) -> BodyAnalysis`

#### `app/services/try_on_service.py` ← CORE DEL NEGOCIO
- `create_try_on(user_id, wardrobe_item_id, body_analysis_id, idempotency_key) -> dict`
  - ADR-004: calcular SHA256(body_analysis_id + wardrobe_item_id + REPLICATE_MODEL_VERSION)
  - Buscar cache en `try_on_cache` → si hit, retornar resultado directo (cache_hit=True)
  - Si miss: crear try_on con status="pending", encolar `replicate_worker` vía ARQ
  - Retornar 202 con `{try_on_id, status: "pending", estimated_seconds: 30}`
- `get_try_on(user_id, try_on_id) -> TryOn`
- `list_try_ons(user_id, page, size) -> list[TryOn]`
- `submit_feedback(user_id, try_on_id, feedback) -> TryOn`

#### `app/services/recommendation_service.py`
- `generate_recommendations(user_id) -> list[RecommendationItem]`
  - Buscar body_analysis + user_style_profile del usuario
  - Construir prompt para Claude API (anthropic)
  - Llamar Claude claude-opus-4-7 → parsear JSON response
  - Guardar en recommendations + recommendation_items
  - Encolar `claude_worker` si la generación es async (ver abajo)
- `get_recommendations(user_id, page, size) -> list[Recommendation]`

#### `app/services/subscription_service.py`
- `get_current(user_id) -> Subscription | None`
- `create_stripe_checkout(user_id, tier, yearly) -> str` — retorna URL checkout
- `create_mp_preference(user_id, tier, yearly) -> str` — retorna URL redirect
- `handle_stripe_webhook(payload, signature) -> None`
- `handle_mp_webhook(payload, signature) -> None`

---

### TAREA 7 — ARQ Workers (`app/workers/`)

Crear directorio y 3 workers:

#### `app/workers/__init__.py` — vacío

#### `app/workers/vision_worker.py`
```python
"""
ARQ worker: Google Vision API auto-tagging de prendas.

Triggered by wardrobe_service.create_item() y body_analysis_service.create_analysis().
"""
from arq import func
from app.config import get_settings

async def vision_tag_wardrobe(ctx: dict, wardrobe_item_id: str, image_url: str) -> dict:
    """
    Llama Google Vision API para auto-tagging de prenda.
    Actualiza wardrobe_items con: category, primary_color, detected_style.
    
    En este sprint: stub que simula tags aleatorios para que el pipeline funcione.
    Sprint 2 integra Vision API real.
    """
    # TODO Sprint 2: google.cloud.vision_v1 call
    # Stub para validar pipeline:
    tags = {"category": "top", "primary_color": "blue", "detected_style": "casual"}
    # Update wardrobe_item via AdminClient...
    return {"wardrobe_item_id": wardrobe_item_id, "tags": tags, "status": "completed"}

async def vision_analyze_body(ctx: dict, body_analysis_id: str, image_url: str) -> dict:
    """
    Llama Google Vision API + análisis IA para body type + color season.
    Actualiza body_analysis con resultados.
    
    Stub para este sprint.
    """
    # TODO Sprint 3: Vision API + custom model
    return {"body_analysis_id": body_analysis_id, "status": "completed"}

# ARQ worker settings
class WorkerSettings:
    functions = [func(vision_tag_wardrobe, timeout=120), func(vision_analyze_body, timeout=120)]
    redis_settings = None  # set at startup from settings.REDIS_URL
```

#### `app/workers/replicate_worker.py`
```python
"""
ARQ worker: Replicate Virtual Try-On inference.

Triggered by try_on_service.create_try_on().
ADR-004: before calling Replicate, check try_on_cache.
ADR-002: on completion, push via Supabase Realtime.
"""
from arq import func

async def process_try_on(ctx: dict, try_on_id: str, content_hash: str) -> dict:
    """
    1. Double-check cache (race condition guard)
    2. Call Replicate model (stub for this sprint — returns placeholder URL)
    3. Upload result to Supabase Storage → R2
    4. Update try_ons table: status=completed, result_cdn_url
    5. Write to try_on_cache (TTL 90 days)
    
    Sprint 4 integra Replicate real.
    """
    # TODO Sprint 4: replicate.run(settings.REPLICATE_MODEL_VERSION, ...)
    result_url = f"https://placeholder.r2.dev/try_on_{try_on_id}.webp"
    # Update try_on status + cache...
    return {"try_on_id": try_on_id, "status": "completed", "result_cdn_url": result_url}

class WorkerSettings:
    functions = [func(process_try_on, timeout=300)]
    redis_settings = None
```

#### `app/workers/claude_worker.py`
```python
"""
ARQ worker: Anthropic Claude recommendations generation.

Triggered by recommendation_service.generate_recommendations().
"""
from arq import func

async def generate_reco_claude(ctx: dict, user_id: str, recommendation_id: str) -> dict:
    """
    Build prompt from user body analysis + style profile.
    Call Claude claude-opus-4-7 for structured outfit recommendations.
    Parse JSON response → save recommendation_items.
    
    Stub for this sprint: returns hardcoded demo recommendations.
    Sprint 5 integrates Claude full pipeline.
    """
    # TODO Sprint 5: anthropic.AsyncAnthropic().messages.create(...)
    return {"recommendation_id": recommendation_id, "status": "completed", "count": 5}

class WorkerSettings:
    functions = [func(generate_reco_claude, timeout=120)]
    redis_settings = None
```

---

### TAREA 8 — Endpoints (8 módulos en `app/api/v1/endpoints/`)

#### `app/api/v1/endpoints/auth.py`
```
POST /auth/register     → AuthService.register() → 201 + TokenResponse
POST /auth/login        → AuthService.login()    → 200 + TokenResponse
POST /auth/refresh      → AuthService.refresh()  → 200 + TokenResponse
GET  /auth/me           → get_current_user_id + ProfileRepo → 200 + Profile
```

#### `app/api/v1/endpoints/users.py`
```
GET    /users/profile   → UserService.get_profile()    → 200 + Profile
PUT    /users/profile   → UserService.update_profile() → 200 + Profile
DELETE /users/account   → UserService.delete_account() → 204
```

#### `app/api/v1/endpoints/wardrobe.py`
```
GET    /wardrobe/items          → WardrobeService.list_items()   → 200 + list
POST   /wardrobe/items          → WardrobeService.create_item()  → 201 + WardrobeItem
GET    /wardrobe/items/{id}     → WardrobeService.get_item()     → 200 + WardrobeItem
PUT    /wardrobe/items/{id}     → WardrobeService.update_item()  → 200 + WardrobeItem
DELETE /wardrobe/items/{id}     → WardrobeService.delete_item()  → 204
```

#### `app/api/v1/endpoints/body_analysis.py`
```
POST /body-analysis             → BodyAnalysisService.create_analysis() → 202 + {job_id, status}
GET  /body-analysis/{id}        → BodyAnalysisService.get_analysis()    → 200 + BodyAnalysis
```

#### `app/api/v1/endpoints/try_ons.py`
```
POST /try-ons                   → TryOnService.create_try_on()     → 202 + {try_on_id, status, estimated_seconds}
                                  [Idempotency-Key REQUIRED — ADR-003]
GET  /try-ons                   → TryOnService.list_try_ons()      → 200 + list
GET  /try-ons/{id}              → TryOnService.get_try_on()        → 200 + TryOn
POST /try-ons/{id}/feedback     → TryOnService.submit_feedback()   → 200 + TryOn
```

#### `app/api/v1/endpoints/recommendations.py`
```
POST /recommendations           → RecommendationService.generate() → 202 + {recommendation_id, status}
GET  /recommendations           → RecommendationService.list()     → 200 + list
GET  /recommendations/{id}      → RecommendationService.get()      → 200 + Recommendation
```

#### `app/api/v1/endpoints/subscriptions.py`
```
GET  /subscriptions/current         → SubscriptionService.get_current()        → 200 + Subscription | null
POST /subscriptions/stripe/checkout → SubscriptionService.create_stripe()      → 200 + {url}
POST /subscriptions/mp/preference   → SubscriptionService.create_mp()          → 200 + {url}
```

#### `app/api/v1/endpoints/webhooks.py`
```
POST /webhooks/stripe       → SubscriptionService.handle_stripe_webhook()  → 200 OK
                              [Validar Stripe-Signature header — HMAC-SHA256]
                              [Idempotency via Stripe event.id]
POST /webhooks/mercadopago  → SubscriptionService.handle_mp_webhook()      → 200 OK
                              [Validar x-signature header]
```

---

### TAREA 9 — Activar router en `app/api/v1/router.py`

```python
from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth, users, wardrobe, body_analysis, try_ons, recommendations, subscriptions, webhooks
)

api_v1_router = APIRouter()

api_v1_router.include_router(auth.router,            prefix="/auth",            tags=["Auth"])
api_v1_router.include_router(users.router,           prefix="/users",           tags=["Users"])
api_v1_router.include_router(wardrobe.router,        prefix="/wardrobe",        tags=["Wardrobe"])
api_v1_router.include_router(body_analysis.router,   prefix="/body-analysis",   tags=["Body Analysis"])
api_v1_router.include_router(try_ons.router,         prefix="/try-ons",         tags=["Try-On"])
api_v1_router.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
api_v1_router.include_router(subscriptions.router,   prefix="/subscriptions",   tags=["Subscriptions"])
api_v1_router.include_router(webhooks.router,        prefix="/webhooks",        tags=["Webhooks"])
```

**Verificar que `main.py` ya incluye `api_v1_router` en el prefix `/api/v1`.** Si no, agregar.

---

### TAREA 10 — Tests

Crear/ampliar tests con coverage >=80%. Usar mocks para:
- Supabase GoTrue API (httpx mock)
- AdminClient (ya mockeado en Sprint 0.2)
- ARQ enqueue (mock)
- Stripe/MP webhooks (payloads de ejemplo)

**Archivos de test a crear:**
```
backend/tests/
├── test_auth_endpoints.py       — register, login, refresh, me
├── test_users_endpoints.py      — get/update profile, delete account
├── test_wardrobe_endpoints.py   — CRUD completo, pagination
├── test_body_analysis_endpoints.py — create (202), get
├── test_try_on_endpoints.py     — create (202 + idempotency), list, get, feedback
├── test_recommendations_endpoints.py — generate, list, get
├── test_subscriptions_endpoints.py — current, stripe checkout, mp preference
├── test_webhooks.py             — stripe + mp signature validation
├── test_supabase_auth.py        — validate_supabase_token (mock JWKS)
└── test_idempotency_middleware.py — replay lógica completa
```

**Para los tests de endpoints:** usar `pytest-asyncio` + `httpx.AsyncClient` con app en modo test.

**Header de autenticación en tests:** crear fixture `auth_headers` que devuelva
`{"Authorization": "Bearer <mock_token>"}` y mockee `validate_supabase_token()` para retornar `{"sub": "test-user-uuid", "role": "authenticated"}`.

---

## ⚖️ REGLAS DURAS — NO NEGOCIABLES

1. **`ruff check .` → cero errores antes del commit**
2. **`mypy app/ --strict` → cero errores antes del commit** (usa `# type: ignore` solo si es inevitable, con comentario)
3. **`pytest --cov=app --cov-report=term-missing` → coverage >=80%**
4. **Nunca loguear tokens, passwords, image URLs (PII)**
5. **Todos los endpoints bajo `/api/v1/*` (excepto PUBLIC_ROUTES) requieren JWT válido**
6. **`POST /try-ons` DEBE retornar 422 si falta `Idempotency-Key` header**
7. **Stripe webhook: validar `Stripe-Signature` header con HMAC-SHA256 usando `STRIPE_WEBHOOK_SECRET`. Retornar 400 si falla.**
8. **No secrets hardcodeados. Todo via `get_settings()`.**
9. **Nunca usar `.table()` directo del AdminClient — usar `.with_user_check()` o `.trusted()`**
10. **Workers son stubs funcionales. Deben encolarse correctamente en ARQ y retornar estructura válida.**

---

## 📂 ARCHIVOS A CREAR/MODIFICAR (resumen)

### Crear nuevos:
```
backend/app/core/supabase_auth.py
backend/app/api/deps.py
backend/app/services/auth_service.py
backend/app/services/user_service.py
backend/app/services/wardrobe_service.py
backend/app/services/body_analysis_service.py
backend/app/services/try_on_service.py
backend/app/services/recommendation_service.py
backend/app/services/subscription_service.py
backend/app/workers/__init__.py
backend/app/workers/vision_worker.py
backend/app/workers/replicate_worker.py
backend/app/workers/claude_worker.py
backend/app/api/v1/endpoints/auth.py
backend/app/api/v1/endpoints/users.py
backend/app/api/v1/endpoints/wardrobe.py
backend/app/api/v1/endpoints/body_analysis.py
backend/app/api/v1/endpoints/try_ons.py
backend/app/api/v1/endpoints/recommendations.py
backend/app/api/v1/endpoints/subscriptions.py
backend/app/api/v1/endpoints/webhooks.py
backend/tests/test_auth_endpoints.py
backend/tests/test_users_endpoints.py
backend/tests/test_wardrobe_endpoints.py
backend/tests/test_body_analysis_endpoints.py
backend/tests/test_try_on_endpoints.py
backend/tests/test_recommendations_endpoints.py
backend/tests/test_subscriptions_endpoints.py
backend/tests/test_webhooks.py
backend/tests/test_supabase_auth.py
backend/tests/test_idempotency_middleware.py
```

### Modificar:
```
backend/app/core/middleware.py    → activar auth_middleware + idempotency_middleware completo
backend/app/core/security.py     → eliminar python-jose, mantener bcrypt helpers
backend/app/api/v1/router.py     → incluir todos los routers
backend/app/main.py              → verificar que api_v1_router está incluido
backend/requirements.txt         → PyJWT[crypto]>=2.9.0, eliminar python-jose
```

---

## ✅ DEFINICIÓN DE DONE

Sprint 0.3 está DONE cuando:

- [ ] `uvicorn app.main:app --reload` levanta SIN warnings ni errores
- [ ] `GET /health` → `{"status": "healthy"}`
- [ ] `POST /api/v1/auth/register` con body válido → 201 + TokenResponse
- [ ] `POST /api/v1/auth/login` con creds válidas → 200 + TokenResponse
- [ ] `GET /api/v1/auth/me` con token válido → 200 + Profile
- [ ] `GET /api/v1/wardrobe/items` sin token → 401
- [ ] `POST /api/v1/try-ons` sin `Idempotency-Key` → 422
- [ ] `POST /api/v1/try-ons` con todo correcto → 202 + `{try_on_id, status: "pending"}`
- [ ] `POST /api/v1/webhooks/stripe` con signature inválida → 400
- [ ] `ruff check .` → 0 errores
- [ ] `mypy app/` → 0 errores
- [ ] `pytest --cov=app` → coverage >=80%, todos los tests en verde
- [ ] git commit + git push en rama principal

---

## 🗂️ CONTEXTO IMPORTANTE

**postgrest-py vs supabase-py:** En Sprint 0.2 se reemplazó supabase-py por postgrest-py 0.16.6 (misma librería subyacente, sin dependencia pyiceberg que falla en Windows). El código ya usa `from app.core.database import get_admin_client`. **No revertir a supabase-py.**

**Auth path:** Para llamadas a Supabase GoTrue API, usar `httpx.AsyncClient` directamente con la base URL `{SUPABASE_URL}/auth/v1`. No usar supabase-py.

**AdminClient pattern (NO romper):**
- User data: `admin.with_user_check(user_id, id_column="user_id")` 
- Profiles table: `admin.with_user_check(user_id, id_column="id")`
- Infrastructure (idempotency, audit, usage): `admin.trusted()`
- NUNCA: `admin.table(...)` directo

**migration 004 status:** Aplicada en tests locales. Supabase remote: pendiente (Juan Camilo aplica con credenciales). Tests usan mocks del AdminClient.

---

## 📤 ENTREGA ESPERADA

Al terminar, reportar:
1. Hash del commit
2. Lista de archivos creados/modificados
3. Output de `pytest --cov=app --cov-report=term-missing` (últimas 30 líneas)
4. Output de `ruff check . && mypy app/` 
5. Cualquier decisión arquitectónica tomada (para que Jarvis la valide)
6. Issues encontrados o TODO items para sprints futuros

**Rama:** commit directo a main (o rama `claude/sprint-0-3-...` si Antigravity prefiere)
