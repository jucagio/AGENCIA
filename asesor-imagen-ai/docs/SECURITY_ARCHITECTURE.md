# Security Architecture Review

**Author:** Alejo (Solutions Architect) — input para Cyber Neo Sprint 0.4 audit
**Date:** 2026-05-19
**Status:** ENTREGADO — coordinación con Cyber Neo
**Audience:** Cyber Neo (auditor), Sasha (implementador), Jarvis (CEO)
**Related:** Cyber Neo findings Sprint 0.3, ADR-001 (JWKS), ADR-002 (signed URLs), ADR-003 (idempotency), ADR-005 (RLS), `ADR_007_RATE_LIMITING.md`, `DECISION_AUDIT_D1_D5.md`

---

## 0. TL;DR

**Tres dominios críticos auditados:**

| Dominio | Status | Findings nuevos | Owner |
|---------|--------|-----------------|-------|
| **Worker isolation (ARQ jobs)** | 🟢 Diseño correcto | 2 mejoras (logging + DLQ) | Sasha |
| **Image storage (signed URLs)** | 🟢 Cubierto ADR-002 | 1 mejora (D5 shares 30d) | Sasha |
| **Payment flow (Stripe/MP)** | 🟢 Auditable | 2 mejoras (idempotency dedup + retry) | Sasha |

**Veredicto:** Arquitectura es **secure-by-design**. No hay vulnerabilidades arquitectónicas críticas pendientes. Cyber Neo Sprint 0.4 audit debe focar en implementación (no diseño).

---

## 1. Worker Isolation — ARQ Jobs

### 1.1 Pregunta crítica: ¿Puede job X leakear data del job Y?

**Modelo de amenaza:**
- Attacker A inyecta payload malicioso en su own try-on que causa worker process leak memoria
- Cuando worker procesa job de victim B, ve fragmentos de la sesión de A
- Resultado: A obtiene URLs / metadatos de B

**Defensa actual:**

#### Layer 1: Process-level isolation (ARQ workers)
- Cada worker ARQ es un proceso Python independiente
- Workers NO comparten memoria entre jobs (GIL + process boundary)
- Worker procesa 1 job a la vez (no concurrent jobs en mismo proceso)
- **Validación:** Sprint 0.4 setting `max_jobs=1` en ARQ config explícito

#### Layer 2: Job context inmutable
```python
# app/workers/tryon_worker.py
async def process_tryon(ctx: WorkerContext, job: dict):
    # ✅ user_id viene del job payload, NO de globals
    user_id = job['user_id']
    tryon_id = job['tryon_id']

    # ✅ Queries SIEMPRE filtran por user_id (RLS también enforced)
    tryon = await db.fetch_one(
        "SELECT * FROM try_ons WHERE id = $1 AND user_id = $2",
        tryon_id, user_id
    )

    # ✅ Storage paths siempre prefixed con user_id
    output_path = f"tryons/{user_id}/{tryon_id}.webp"
    # NUNCA: f"tryons/{tryon_id}.webp" ← path traversal risk
```

#### Layer 3: Database RLS (ADR-005)
- Aunque worker usa service_role key (bypass RLS), todas las queries deben filtrar manualmente por user_id
- Lint rule (TODO Sasha): pre-commit hook detecta `SELECT * FROM try_ons` sin `WHERE user_id` y bloquea commit

#### Layer 4: Subprocess sandboxing (futuro)
- Replicate calls happen via HTTPS → external service, no local subprocess
- Si futuro necesita local AI (ej: ONNX en-prem), wrap en Docker container con seccomp profile
- NO aplicable ahora (todo es API external)

### 1.2 Findings & Mejoras

| # | Finding | Severidad | Acción |
|---|---------|-----------|--------|
| W1 | Worker logs incluyen user_id en plaintext (potential PII en aggregated logs) | 🟢 Low | Hash user_id en logs estructurados (SHA256 con salt diario) |
| W2 | Dead-letter queue NO existe — jobs failed 3 veces se pierden silenciosamente | 🟡 Med | Crear `dlq_tryon` cola + Sentry alert + admin endpoint para retry manual |
| W3 | `max_jobs` no especificado explícito en ARQ config | 🟢 Low | `worker_settings = WorkerSettings(max_jobs=1)` para garantizar 1-at-a-time |
| W4 | Service role key en env exposes total DB access si leak | 🟡 Med | Rotación trimestral (Cinthya workflow) + restricted SQL role para workers (solo INSERT/UPDATE en `try_ons`, NO DELETE) |

---

## 2. Image Storage Security — Signed URLs

### 2.1 Modelo de amenaza

**Pregunta:** ¿Quién puede acceder a `/tryons/<user_id>/<tryon_id>.webp`?

**Atacantes considerados:**
- A1: Otro usuario autenticado intenta GET de imagen de B
- A2: Web crawler / scraper sin autenticación
- A3: User compartió signed URL en redes; otros adivinan/enumeran signed URLs
- A4: Signed URL expirada se reutiliza
- A5: Hot-linking masivo desde sitio terceros agota egress R2

### 2.2 Defensa actual (ADR-002 + ADR-005 + D5)

#### Defensa A1 (cross-user access)
- **RLS en `try_ons`:** policy `SELECT WHERE user_id = auth.uid()` enforced en DB
- Signed URL generation: backend verifica ownership ANTES de firmar
```python
async def get_tryon_signed_url(tryon_id, requesting_user_id):
    tryon = await db.fetch_one(
        "SELECT * FROM try_ons WHERE id = $1 AND user_id = $2",
        tryon_id, requesting_user_id
    )
    if tryon is None:
        raise NotFoundError()  # NO 403 — no revela existencia
    return storage.sign(tryon.result_path, expires_in=86400)
```

#### Defensa A2 (anonymous crawler)
- R2 bucket: ACL **private** by default
- Solo signed URLs funcionan
- No paths predecibles (UUID v4 random, no auto-increment)

#### Defensa A3 (URL enumeration)
- Signed URLs incluyen HMAC con secret rotativo
- Path no enumerable (UUID v4 has 122 bits entropy)
- Aunque attacker tenga URL válida, expira en 24h (normal) o 30d (shares D5)

#### Defensa A4 (expired URL reuse)
- HMAC incluye `expires_at` timestamp
- R2 rechaza signed URL con timestamp pasado (server-side validation)
- NO confiamos en client-side validation

#### Defensa A5 (hot-linking abuse)
- Cloudflare Cache Rules: cache signed URL responses 30d
- Reduce 80% requests directos a R2
- Cloudflare WAF: rate limit per-IP en `/tryons/*` (100 req/min/IP)
- Si hot-linking detectado: rotate bucket access keys + invalidate signed URLs

### 2.3 D5 Sharing — Signed URLs 30d

D5 requiere shares duraderos (Instagram Stories 24h + posibilidad de re-share). Diseño en `DECISION_AUDIT_D1_D5.md` §5:

**Diferencias vs ADR-002 base:**
- Signed URL expira **30 días** (vs 24h normal)
- Imagen es **versión watermarked** en path separado (`shares/`)
- Bucket `aifc-shares-prod` separado para easier WAF rules

**Riesgo nuevo:** Hot-linking de shares en sitios terceros (alguien embebe `<img src="https://aifc-shares.../...webp">` en blog).

**Mitigación:**
- Cloudflare cache: 30d TTL en `aifc-shares.*` (CDN absorbe carga)
- Referer header check opcional (NO confiable, pero ayuda detectar abuso)
- Si bandwidth spike: rotar keys + regenerar shares (rompe enlaces pero protege costo)

### 2.4 Findings & Mejoras

| # | Finding | Severidad | Acción |
|---|---------|-----------|--------|
| S1 | Signed URL secret rotativo cada cuánto? | 🟡 Med | Definir rotación trimestral (90d) — durante rotación, mantener 2 keys válidos 7d para no romper URLs activos |
| S2 | Watermark se aplica server-side ✅ pero variant cached en R2 sin TTL | 🟢 Low | Lifecycle policy: shares 90d → archive tier |
| S3 | Logs de signed URL generation incluyen full URL (cont. signature) | 🟡 Med | Loggear solo `tryon_id` + `expires_at`, NO la URL completa firmada |
| S4 | Cloudflare Pro no incluye Argus (bot detection) | 🟢 Low | Aceptar — Turnstile + rate limit suficiente <250K MAU |

---

## 3. Payment Flow Security — Stripe + MercadoPago

### 3.1 Modelo de amenaza

**Atacantes considerados:**
- P1: Attacker intercepta webhook Stripe/MP y replays con payload modificado
- P2: Double-billing por webhook retry (Stripe reenvía si no devolvemos 2xx)
- P3: User intenta subscription bypass enviando webhook fake
- P4: Card data leak en logs / database (PCI compliance violation)
- P5: Refund abuse (user obtiene refund + mantiene access)
- P6: SQL injection vía webhook payload

### 3.2 Defensa actual

#### Defensa P1 (webhook signature)
**Stripe:**
```python
# app/api/v1/webhooks/stripe.py (entrega 0.3)
@router.post("/stripe")
async def stripe_webhook(request: Request, db: DB):
    payload = await request.body()
    signature = request.headers.get('stripe-signature')

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,  # bytes (fix Sprint 0.3 security patch)
            sig_header=signature,
            secret=settings.STRIPE_WEBHOOK_SECRET,
            tolerance=300,  # 5 min
        )
    except stripe.SignatureVerificationError:
        raise HTTPException(400, "Invalid signature")
    # ... process event
```

**MercadoPago:**
- HMAC-SHA256 sobre `data.id` + `request_id` con secret compartido
- Validación en `app/api/v1/webhooks/mercadopago.py` (fix Sprint 0.3)

#### Defensa P2 (idempotency — webhook retry)
**Problema:** Stripe reenvía webhook 3 veces si timeout. Sin idempotency, podríamos crear subscription duplicada o creditar 3x.

**Solución (ya en ADR-003 + Sprint 0.3):**
```python
# app/api/v1/webhooks/stripe.py
event_id = event['id']  # ej: 'evt_1ABC...'

# Check si ya procesamos este event
existing = await db.fetch_one(
    "SELECT id FROM webhook_events WHERE provider = 'stripe' AND event_id = $1",
    event_id
)
if existing:
    return {"status": "already_processed"}  # 200 OK, no reprocesa

# Procesar + persistir event_id atómicamente
async with db.transaction():
    await process_event(event)
    await db.execute(
        "INSERT INTO webhook_events (provider, event_id, processed_at) VALUES ('stripe', $1, now())",
        event_id
    )
```

**Pendiente Sprint 0.4 (D8 Ego finding):** Crear tabla `webhook_events` con UNIQUE constraint en `(provider, event_id)`.

#### Defensa P3 (fake webhook)
- HMAC validation (P1) bloquea esto
- Adicionalmente: rate limit `100/min/IP` en `/webhooks/*` (ADR-007)

#### Defensa P4 (PCI compliance)
**🟢 CUMPLE — no tocamos PAN nunca.**

- Stripe Checkout / MP Checkout = redirect a su iframe
- Card data va directo de browser a Stripe/MP (NUNCA a nuestro backend)
- Solo recibimos `customer_id`, `subscription_id`, `payment_method_id` (tokens NO PCI-sensitive)
- Database NO almacena card data, NUNCA
- Logs NO loggean card data (no se puede — no la recibimos)

**PCI SAQ-A applicable** (lowest tier — outsourced card handling).

#### Defensa P5 (refund abuse)
- Webhook `customer.subscription.deleted` → revoca access inmediato
- Refund parcial: webhook `charge.refunded` → marca user como `subscription_state = 'CANCELED'`
- Grace period 30d (per D4) → access NO inmediato si refund, pero se mantiene FREE tier post-refund

#### Defensa P6 (SQL injection)
- Stripe/MP payloads son JSON parsed por SDK oficial — fields tipados
- Backend usa asyncpg parametrized queries (no string concatenation)
- Validación Pydantic en endpoints: `EventV1Stripe(BaseModel)` strict mode
- Audit Cyber Neo Sprint 0.3 confirmó zero SQL injection vectors

### 3.3 Idempotency Keys (POST /payments/checkout)

Cuando user inicia checkout, frontend genera `Idempotency-Key: <UUID>` en request. Backend cachea response 24h. Si user clic 2 veces rápido, NO se crean 2 subscriptions.

**Implementación (ya en ADR-003 + middleware Sprint 0.3):**
```python
# Cliente:
POST /api/v1/subscriptions/checkout
Idempotency-Key: 7f3d-4b2a-...
{"tier": "ACTIVE_ESTILO"}

# Si se reenvía mismo key → mismo response (200 cached)
```

**Pendiente Sprint 0.4 (A04-MED1):** UNIQUE constraint en `idempotency_keys` table.

### 3.4 Findings & Mejoras

| # | Finding | Severidad | Acción |
|---|---------|-----------|--------|
| P1 | Webhook events dedup table aún no migrada (D8 Ego finding) | 🟡 Med | Sprint 0.4: migration `webhook_events(provider, event_id) UNIQUE` |
| P2 | Idempotency UNIQUE constraint pendiente (A04-MED1) | 🟡 Med | Sprint 0.4: migration `idempotency_keys(key) UNIQUE` |
| P3 | Stripe API key NO segregado por env (test vs prod) en CI | 🟢 Low | GitHub Actions secrets separados `STRIPE_KEY_TEST` vs `STRIPE_KEY_PROD` |
| P4 | Refund webhook NO testeado end-to-end (solo subscription.created) | 🟡 Med | Sprint 1: add test cases `charge.refunded`, `subscription.deleted`, `payment_failed` |
| P5 | MP webhook retry policy desconocido (vs Stripe documentado 3 retries) | 🟢 Low | Yang/Sasha: investigar MP docs, ajustar timeout backend |

---

## 4. Defensa en Profundidad — Layers Summary

```
Internet
   ↓
[Cloudflare WAF + Rate Limit + Turnstile]   ← Layer 1: Edge defense
   ↓
[Railway / AWS ALB + TLS termination]        ← Layer 2: Transport
   ↓
[FastAPI middleware: JWKS auth + slowapi]    ← Layer 3: Authentication + Rate limit
   ↓
[Pydantic validation + SSRF check]           ← Layer 4: Input validation
   ↓
[Service layer: tier-aware logic]            ← Layer 5: Business logic + authorization
   ↓
[Postgres RLS + parametrized queries]        ← Layer 6: Data access
   ↓
[Supabase / R2: signed URLs + bucket ACL]    ← Layer 7: Storage
```

**Cada layer es independiente.** Compromise en 1 layer NO compromete el resto.

---

## 5. Compliance Status

| Framework | Status | Notas |
|-----------|--------|-------|
| **PCI DSS** | ✅ SAQ-A | Outsourced card handling (Stripe + MP) |
| **GDPR** | 🟡 Partial | Necesitamos: data deletion endpoint + cookie consent banner + DPIA |
| **CCPA** | 🟡 Partial | Mismo que GDPR — falta data deletion + opt-out sale (no aplicable, no vendemos data) |
| **OWASP Top 10 2025** | 🟢 Auditado | Cyber Neo Sprint 0.3 PASS condicional (0 CRITICAL, 2 HIGH en remediation) |
| **SOC 2 Type I** | ❌ Future | Necesario para enterprise contracts; postponer a banda 100K+ MAU |

**Gap GDPR (prioridad alta antes de launch EU):**
- [ ] Endpoint `DELETE /api/v1/users/me` — hard delete user data + cascade (Sasha Sprint 2)
- [ ] Endpoint `GET /api/v1/users/me/export` — JSON export de toda la data del user (Sasha Sprint 2)
- [ ] Banner cookie consent (Brook Sprint 1)
- [ ] DPIA documento (Jarvis + lawyer)
- [ ] DPO designado (Jarvis para MVP)

---

## 6. Coordinación Cyber Neo Sprint 0.4

**Briefing para Cyber Neo (handoff):**

### 6.1 Foco del audit Sprint 0.4

1. **Rate limiting implementation** (ADR-007)
   - Validar slowapi keys NO se pueden bypass via header injection
   - Confirmar Upstash storage usa TLS
   - Test: 10 IPs paralelas atacando /auth/login → verifica que TODAS se bloquean (no solo la primera)

2. **Docker secrets management** (Sprint 0.4 Dockerfile)
   - Validar que secrets NO están en image layers (`docker history` no muestra ENV con secrets)
   - Confirmar uso de Railway secrets manager (NO `.env` committeado)
   - Multi-stage build limpia node_modules/.git de runtime image

3. **CI/CD pipeline hardening**
   - GitHub Actions: secrets segregados por env
   - Pull requests externos NO obtienen acceso a secrets
   - Dependency scanning activo (Dependabot + Snyk)

4. **Webhook events dedup** (D8 + A04-MED1)
   - Validar migration applied
   - Test: replay attack mismo event_id → 200 OK con "already_processed"

### 6.2 Input para Cyber Neo desde este doc

- Findings W1-W4 (Worker), S1-S4 (Storage), P1-P5 (Payment) — incorporar en checklist Sprint 0.4
- Defense layers §4 — usar como reference architecture para reporting

### 6.3 Reporting esperado

- Cyber Neo Sprint 0.4 audit report con findings clasificados por severidad
- 0 CRITICAL = bloqueante release
- ≤2 HIGH con plan remediación = aprobado
- Reporte a Ego para validation cruzada

---

## 7. Acción Sprint 0.4 + Sprint 1

### Sprint 0.4 (Antigravity + Sasha)
- [ ] Migration `webhook_events` UNIQUE (P1, D8 Ego)
- [ ] Migration `idempotency_keys` UNIQUE (P2, A04-MED1)
- [ ] Dead-letter queue `dlq_tryon` + Sentry alert (W2)
- [ ] `max_jobs=1` explicit en ARQ config (W3)
- [ ] Restricted SQL role para workers (W4 — INSERT/UPDATE only)
- [ ] Logs hash user_id (W1, S3)
- [ ] Docker secrets validation (Cyber Neo audit)

### Sprint 1 (Sasha)
- [ ] Endpoint `DELETE /api/v1/users/me` (GDPR)
- [ ] Endpoint `GET /api/v1/users/me/export` (GDPR)
- [ ] Test cases refund webhooks (P4)
- [ ] Lint rule: pre-commit detecta SELECT sin WHERE user_id (W backstop)

### Sprint 2-3
- [ ] Rotación trimestral signed URL secret (S1)
- [ ] Lifecycle policy shares 90d → archive (S2)
- [ ] Investigar MP webhook retry policy (P5)

---

## 8. Risk Register

| ID | Riesgo | Probabilidad | Impacto | Mitigación | Owner |
|----|--------|:-----------:|:-------:|------------|-------|
| R-SEC-01 | Cross-user signed URL leak | 🟢 Low | 🔴 High | RLS + ownership check + UUID v4 paths | Sasha |
| R-SEC-02 | Webhook replay attack | 🟡 Med | 🟡 Med | HMAC + event dedup table | Sasha (0.4) |
| R-SEC-03 | Brute force /auth/login | 🟡 Med | 🟡 Med | slowapi 5/min/IP + Cloudflare Turnstile | Sasha (0.4) |
| R-SEC-04 | Replicate API key leak | 🟢 Low | 🔴 High | Railway secrets manager, rotación trimestral | Cinthya workflow |
| R-SEC-05 | DDoS via try-on spam | 🟡 Med | 🟡 Med | Rate limit + circuit breaker spend cap (ADR-007 CB1) | Sasha (0.4) |
| R-SEC-06 | GDPR data deletion no implementado | 🔴 High | 🟡 Med | Sprint 1 endpoint DELETE /users/me | Sasha (Sprint 1) |
| R-SEC-07 | Worker memory leak cross-job | 🟢 Low | 🔴 High | ARQ max_jobs=1 + process isolation | Sasha (0.4) |

---

**Reportado a Jarvis + Cyber Neo. Disponible para Q&A en Junta 2026-05-25.**
**— Alejo, Solutions Architect**
