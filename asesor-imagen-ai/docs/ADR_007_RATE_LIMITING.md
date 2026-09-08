# ADR-007: Rate Limiting + Circuit Breakers Arquitectura

**Status:** ✅ APROBADO (promovido de borrador embebido en COST_MODEL §6 a doc formal)
**Decided by:** Alejo (Solutions Architect) + Sasha (Backend) + Jarvis (CEO)
**Date:** 2026-05-19
**Implementation Sprint:** 0.4 (Antigravity) — **BLOQUEANTE para release a producción**
**Supersedes:** Borrador embebido en `COST_MODEL_PATH_A.md` §6 (rev 1)
**Related:** ADR-006 (Path A), `COST_MODEL_PATH_A.md` rev 2, `DECISION_AUDIT_D1_D5.md` (D4 tier-aware), `SECURITY_ARCHITECTURE.md`

---

## 1. Context

Path A (ADR-006) target **50K paid + 500K-1M MAU free en mes 12**. D4 introduce free tier "1 try-on/día" (potencialmente 22 try-ons/usuario/mes efectivos). Sin rate limiting estricto + circuit breakers, **tres escenarios rompen el modelo**:

1. **Free MAU explota >25:1 ratio vs paid** → margen <60% (ver `COST_MODEL_PATH_A.md` §3.1)
2. **Viral spike (100K signups/24h vía TikTok)** → satura Replicate (rate limit 600 req/min default) + Railway
3. **Brute force en `/auth/login`** → riesgo seguridad + costos egress (ver hallazgo Cyber Neo A04-HIGH1, A07-HIGH1)

Sprint 0.3 dejó `RATE_LIMIT_PER_MINUTE` declarado pero NO aplicado. Cyber Neo lo marcó como **bloqueante Sprint 0.5**.

---

## 2. Decision

### 2.1 Stack: **slowapi + Redis (Upstash)**

| Opción evaluada | Elegida | Razón |
|---|:---:|---|
| **A. slowapi + Redis (Upstash)** | ✅ | Integra nativo con FastAPI middleware. Redis ya necesario para ARQ. Soporta distribución horizontal. |
| B. Custom middleware in-memory | ❌ | No funciona con múltiples workers Railway (estado por proceso). Inválido a 2+ replicas. |
| C. Supabase RLS-based (per-row counter) | ❌ | Latencia DB en cada request (15-30ms). No protege endpoints sin DB hit. No protege auth (brute force). |
| D. Cloudflare Rate Limiting (edge) | 🟡 Complemento | Bueno para WAF + per-IP, pero NO ve `user_id` (después del JWT decode). Usar **junto** con slowapi, no en lugar de. |

**Decisión final:** **slowapi + Upstash Redis + Cloudflare Turnstile** (defensa en profundidad).

### 2.2 Rate Limits Hard (per-endpoint, per-tier)

#### Endpoints de autenticación (per-IP)

| Endpoint | Free | Trial | Estilo | Imagen |
|----------|:---:|:---:|:---:|:---:|
| POST /auth/login | 5/min/IP | 5/min/IP | 5/min/IP | 5/min/IP |
| POST /auth/register | 3/min/IP | — | — | — |
| POST /auth/refresh | 10/min/IP (A07-HIGH1) | 10/min/IP | 10/min/IP | 10/min/IP |
| POST /auth/forgot-password | 3/min/IP + 10/día/email | — | — | — |

#### Endpoints AI (per-user_id)

| Endpoint | Free | Trial | Estilo | Imagen |
|----------|:---:|:---:|:---:|:---:|
| POST /api/v1/try-ons | **1/día + 8/mes hard cap** (D4 + cap recomendado) | 5/día | 5/día | unlimited (hard 200/mes anti-abuso) |
| POST /api/v1/body-analysis | 1/mes | 5/mes | unlimited | unlimited |
| POST /api/v1/recommendations | 5/día | 30/día | 100/día | unlimited |
| POST /api/v1/chat | 0 | 10/día | 30/día | 100/día |

#### Endpoints de lectura/polling (per-user_id)

| Endpoint | All tiers |
|----------|:---:|
| GET /api/v1/try-ons/{id} | 60/min |
| GET /api/v1/users/me/* | 60/min |
| GET /api/v1/wardrobe | 60/min |

#### Webhooks externos (per-source)

| Endpoint | Rate limit | Notas |
|----------|:---:|---|
| POST /webhooks/stripe | 100/min/IP | HMAC validation primary, rate limit secundario |
| POST /webhooks/mercadopago | 100/min/IP | HMAC validation primary |

### 2.3 Circuit Breakers

#### CB1: Daily Spend Cap Replicate

```python
# Concepto
DAILY_SPEND_CAP_REPLICATE = float(env.get('REPLICATE_DAILY_CAP_USD', '500'))

@before_request
async def check_replicate_budget():
    today_spend = await metrics_repo.get_today_replicate_spend()
    if today_spend >= DAILY_SPEND_CAP_REPLICATE:
        if request.user.subscription_state == 'FREE':
            raise HTTPException(503, "Daily AI budget reached. Upgrade to continue.",
                                headers={'Retry-After': str(seconds_until_midnight())})
        # Paid users siguen funcionando hasta hard cap (1.5x)
        if today_spend >= DAILY_SPEND_CAP_REPLICATE * 1.5:
            raise HTTPException(503, "Service temporarily degraded.")
```

**Triggers:**
- $500/día default (ajustable por env)
- Free tier 503 cuando se alcanza
- Paid tier sigue hasta 1.5x ($750)
- Alert a Slack #arquitectura cuando se cruza 80% del cap

#### CB2: Queue Overflow

```python
# Concepto en services/tryon.py
async def enqueue_tryon_job(user_id, payload):
    queue_depth = await arq_pool.queued_jobs_count('tryon_queue')
    if queue_depth > 500:
        raise HTTPException(503, "Service busy. Retry in 30s.",
                            headers={'Retry-After': '30'})
    if queue_depth > 200:
        # Degraded mode — return job_id pero advertir delay
        return {'job_id': ..., 'estimated_wait_seconds': queue_depth * 3, 'degraded': True}
```

#### CB3: Auto-Downgrade Free Tier

```python
# Workflow Cinthya n8n (daily 00:00 UTC)
async def evaluate_free_tier_health():
    mau_free = await metrics.mau_count(tier='FREE', days=30)
    mau_paid = await metrics.mau_count(tier_in=['TRIAL','ACTIVE_ESTILO','ACTIVE_IMAGEN'], days=30)

    ratio = mau_free / max(mau_paid, 1)
    if ratio > 25.0:
        # Sostenido 7 días → trigger downgrade
        days_breached = await metrics.consecutive_days_breached(ratio_threshold=25.0)
        if days_breached >= 7:
            await feature_flags.set('FREE_TIER_MONTHLY_CAP', 3)  # baja de 8 a 3/mes
            await alerts.send_to_jarvis(
                title="🔴 Free tier auto-downgrade triggered",
                detail=f"MAU ratio {ratio:.1f}:1 sostenido 7 días. Cap bajado 8→3/mes."
            )
```

#### CB4: Cloudflare Turnstile (anti-bot)

- `/auth/register` obligatorio con Turnstile (gratis, sin friction)
- `/auth/forgot-password` también
- `/try-ons` solo durante viral spikes (feature flag manual)

#### CB5: Per-IP Signup Burst

```python
# Detecta >20 signups desde la misma /24 CIDR en 5 min → bloquea /24 1h
# Implementación: Cloudflare WAF custom rule (mejor que slowapi por edge enforcement)
```

---

## 3. Implementation

### 3.1 Dependencias

```python
# pyproject.toml
slowapi = "^0.1.9"
upstash-redis = "^1.2.0"  # o redis-py 5.x con Upstash REST URL
```

### 3.2 Setup en FastAPI (Sprint 0.4)

```python
# app/core/rate_limiter.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from app.core.security import get_current_user_id_optional

def composite_key(request) -> str:
    """
    Para endpoints autenticados: user_id:tier
    Para endpoints públicos: IP
    Cae a IP si no hay JWT válido.
    """
    user_id = get_current_user_id_optional(request)
    if user_id:
        tier = request.state.user_tier  # set por auth middleware
        return f"{user_id}:{tier}"
    return get_remote_address(request)

limiter = Limiter(
    key_func=composite_key,
    storage_uri=settings.UPSTASH_REDIS_URL,
    strategy="fixed-window",  # vs "moving-window" — fixed más barato Redis
)

# app/main.py
def create_app() -> FastAPI:
    app = FastAPI(...)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    ...
    return app
```

### 3.3 Decoradores por endpoint

```python
# app/api/v1/auth.py
from app.core.rate_limiter import limiter

@router.post("/login")
@limiter.limit("5/minute", key_func=get_remote_address)  # per-IP, NO per-user
async def login(request: Request, ...):
    ...

@router.post("/refresh")
@limiter.limit("10/minute", key_func=get_remote_address)
async def refresh(request: Request, ...):
    ...
```

```python
# app/api/v1/try_ons.py
from app.core.rate_limiter import limiter

# Rate limit dinámico per-tier
def tryon_rate_limit(request: Request) -> str:
    tier = request.state.user_tier
    return {
        'FREE': '1/day',
        'TRIAL': '5/day',
        'ACTIVE_ESTILO': '5/day',
        'ACTIVE_IMAGEN': '200/month',  # hard cap anti-abuso
    }[tier]

@router.post("")
@limiter.limit(tryon_rate_limit)  # callable retorna string
async def create_tryon(request: Request, ...):
    # Adicionalmente: cap mensual hard
    monthly_count = await usage.get_monthly_tryon_count(user_id)
    monthly_cap = {'FREE': 8, 'TRIAL': 30, 'ACTIVE_ESTILO': 30, 'ACTIVE_IMAGEN': 200}[tier]
    if monthly_count >= monthly_cap:
        raise HTTPException(429, "Monthly limit reached. Upgrade for more.")
    ...
```

### 3.4 Response headers

```
HTTP/1.1 200 OK
X-RateLimit-Limit: 5
X-RateLimit-Remaining: 3
X-RateLimit-Reset: 1716163200
```

En 429:
```
HTTP/1.1 429 Too Many Requests
Retry-After: 47
X-RateLimit-Limit: 5
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1716163200
```

### 3.5 Tests (Sprint 0.4)

```python
# tests/test_rate_limiting.py
@pytest.mark.asyncio
async def test_login_rate_limit_5_per_min(client, redis):
    await redis.flushdb()
    for i in range(5):
        r = await client.post('/auth/login', json={...})
        assert r.status_code in (200, 401)  # válido o credenciales mal, NO 429
    r6 = await client.post('/auth/login', json={...})
    assert r6.status_code == 429
    assert 'Retry-After' in r6.headers

@pytest.mark.asyncio
async def test_tryon_rate_limit_free_tier_1_per_day(client_free_user, redis):
    await redis.flushdb()
    r1 = await client_free_user.post('/api/v1/try-ons', json={...})
    assert r1.status_code == 202
    r2 = await client_free_user.post('/api/v1/try-ons', json={...})
    assert r2.status_code == 429
    assert 'Monthly limit' not in r2.json()['detail']  # es daily, NO monthly

@pytest.mark.asyncio
async def test_tryon_monthly_cap_overrides_daily(client_free_user, db):
    # Simular 8 try-ons en el mes
    for i in range(8):
        await db.execute("INSERT INTO try_ons (user_id, created_at) VALUES (...)")
    r = await client_free_user.post('/api/v1/try-ons', json={...})
    assert r.status_code == 429
    assert 'Monthly limit reached' in r.json()['detail']
```

---

## 4. Observability

### 4.1 Métricas a exponer (Sentry + PostHog)

| Métrica | Owner | Alert threshold |
|---------|-------|----------------|
| `rate_limit.hits_total{endpoint, tier}` | Cinthya dashboard | >100/h por endpoint = posible attack |
| `rate_limit.exceeded_total{endpoint, tier}` | Cinthya | >50/h sostenido = ajustar limit |
| `circuit_breaker.tripped{name='replicate_daily_cap'}` | Cinthya → Slack | cualquier trip = page |
| `arq.queue_depth` | Cinthya | >200 = warn, >500 = page |

### 4.2 Logging estructurado

```python
# En slowapi handler custom
logger.warning(
    "rate_limit_exceeded",
    user_id=user_id,
    endpoint=request.url.path,
    tier=tier,
    limit_window=window,
    ip=request.client.host,
)
```

NO loggear IP completa en logs persistentes (GDPR) — hash SHA256 con salt diario.

---

## 5. Consequences

### Positivas
+ Margen blindado contra free explosion (CB3 auto-downgrade)
+ Viral spikes manejables (CB2 queue overflow + CB4 Turnstile)
+ Brute force en auth bloqueado (5/min/IP)
+ Cost cap Replicate prevenible (CB1)
+ Compliance: auditable (logs estructurados con tier, no PII)
+ Defensa en profundidad: Cloudflare WAF + slowapi + Postgres caps

### Negativas / Riesgos
- Complejidad adicional ~1 semana Sasha + Antigravity (Sprint 0.4)
- UX friction potencial si rate limits muy agresivos — **A/B test recomendado en Sprint 2**
- Dependencia Upstash (single point of failure si Upstash down) — mitigación: fallback in-memory con cap relajado (mejor caer abierto que cerrado en auth)
- Costo Upstash: ~$10-50/mes a 250K MAU (Pro tier requerido a 1M MAU, ~$280/mes)

### Compatibilidad con ADRs existentes
- ✅ ADR-001 (JWKS auth): compatible — middleware lee user_tier después de auth
- ✅ ADR-003 (idempotency): compatible — rate limit NO consume idempotency budget
- ✅ ADR-006 (Path A): refuerza — sin ADR-007 ADR-006 NO cierra

---

## 6. Migration Path (futuro)

| Escala | Stack | Cuándo |
|--------|-------|--------|
| <50K MAU | slowapi + Upstash $10/mes | MVP |
| 50K-500K MAU | slowapi + Upstash Pro $50-280/mes | Año 1 |
| 500K-1M MAU | slowapi + Upstash Enterprise $500+/mes | Año 2 |
| >1M MAU | Migrar a Envoy + Redis Cluster + rate limit service dedicado | Año 3+ (con migración AWS) |

---

## 7. Acción Sprint 0.4 (Antigravity Trigger)

- [ ] Agregar `slowapi`, `upstash-redis` a `pyproject.toml`
- [ ] Crear `app/core/rate_limiter.py` con composite_key
- [ ] Wire `limiter` en `create_app()` + exception handler
- [ ] Decorar endpoints auth (5/min, 10/min, 3/min)
- [ ] Decorar endpoints AI con `tryon_rate_limit` callable
- [ ] Implementar circuit breakers CB1-CB3 (CB4-CB5 = Cloudflare config, no código)
- [ ] Tests: `tests/test_rate_limiting.py` (cobertura ≥85%)
- [ ] Logs estructurados con tier + endpoint + IP hash
- [ ] PostHog events: `rate_limit_exceeded`, `circuit_breaker_tripped`
- [ ] Docs en `docs/RATE_LIMITING_OPERATIONAL.md` (cómo ajustar limits sin redeploy)

---

## 8. Validación con Cyber Neo

Pre-release (Sprint 0.4 audit):
- [ ] Confirmar que rate limit NO se puede bypass cambiando User-Agent / IP
- [ ] Validar que JWT replay attacks NO escapan rate limit
- [ ] Confirmar que Redis storage tiene TLS (Upstash sí by default)
- [ ] Verificar que rate_limit hash de IP usa salt rotatorio (no IP plana en Redis keys)
- [ ] Penetration test: intentar bypassear `/auth/login` 5/min/IP con proxy chain

---

**Status:** ✅ APROBADO para implementación Sprint 0.4
**Owners:** Sasha (implementación) + Antigravity (DevOps integration) + Cyber Neo (validación)
**— Alejo, Solutions Architect**
