# DECISION AUDIT — D1-D5 (Implicaciones Técnicas)

**Author:** Alejo (Solutions Architect)
**Date:** 2026-05-19
**Status:** ENTREGADO — input para Sprint 1 (MON 26)
**Related:** `DECISIONES_APROBADAS.md` (938b670), ADR-006, ADR-007 (this delivery), `SCALING_STRATEGY_10X.md`, `SECURITY_ARCHITECTURE.md`
**Audience:** Sasha (backend), Brook (frontend), Cinthya (automation), Cyber Neo (security), Jarvis (CEO)

---

## 0. TL;DR Arquitectónico

| Decisión | Impacto Arquitectónico | Status | Sprint owner |
|----------|------------------------|--------|--------------|
| **D1** Dual branding | ⚪ Cero — pure config (env vars) | ✅ Resuelto | Brook (S01-S11) |
| **D2** Hybrid try-on | 🟢 Cubierto — ARQ + polling GET existentes | ✅ Resuelto | Sasha (workers) |
| **D3** Triggered body analysis | 🟡 Nuevo — UX state machine + event store | 🟡 Diseñar Sprint 1 | Brook + Sasha |
| **D4** Free tier + pricing | 🔴 Crítico — rate limiting + subscription FSM | 🟡 Sprint 0.4 (BLOQUEANTE) | Sasha + Antigravity |
| **D5** Social sharing | 🟢 Cubierto — signed URLs ya en ADR-002 | 🟡 Analytics events nuevos | Brook + Cinthya |

**Veredicto global:** ✅ **NO HAY BREAKING CHANGES ARQUITECTÓNICOS.** Las 5 decisiones encajan en la arquitectura aprobada (ADR-001 a ADR-006). Tres dominios necesitan trabajo nuevo: subscription state machine (D4), gamified escalation FSM (D3), analytics event taxonomy (D5).

---

## 1. D1 — Dual Branding ("AI Fit Check" + "Tu Asesor de Imagen Confiable")

### Implicación técnica
**NINGUNA a nivel arquitectónico.** Es 100% configuración de UI + assets.

### Implementación
```python
# backend: .env
APP_NAME=AI Fit Check
APP_TAGLINE=Tu Asesor de Imagen Confiable
APP_DOMAIN=aifitcheck.com  # produccion
```

```dart
// frontend: lib/core/config/app_config.dart
class AppConfig {
  static const appName = 'AI Fit Check';
  static const appTagline = 'Tu Asesor de Imagen Confiable';
  static const logoLight = 'assets/logos/aifc_light.svg';
  static const logoDark  = 'assets/logos/aifc_dark.svg';
}
```

### Riesgos
- **App Store rejection:** Bundle ID debe coincidir con nombre. Reservar `com.aifitcheck.app` YA (Juan Camilo) antes que un squatter.
- **i18n:** Tagline solo en español por ahora. Si entra mercado US, agregar `APP_TAGLINE_EN`.

### Acción
- [ ] Brook: integrar tokens en `MaterialApp.title` y splash screen
- [ ] Juan Camilo: reservar bundle IDs iOS/Android (URGENTE)
- [ ] Erik: validar que logo "AI Fit Check" funciona en favicon 16x16

---

## 2. D2 — Hybrid Try-On Flow (Upload Prominent + Wardrobe Optional)

### Implicación técnica
**Cubierto al 100% por la arquitectura existente.**

### Validación contra ADRs existentes

| Componente | Cobertura | Owner |
|------------|-----------|-------|
| Upload directo persona | ✅ `POST /api/v1/try-ons` con `image_url` SSRF-validado (entrega 0.3) | Sasha |
| Job queuing | ✅ ARQ + Redis (Sprint 0.4 — ARQ pool en lifespan) | Sasha |
| Polling GET endpoint | ✅ `GET /api/v1/try-ons/{id}` retorna `status: queued/processing/completed/failed` | Sasha |
| Wardrobe optional | ✅ `garment_ids: List[str] | None` en request payload | Brook + Sasha |
| Body analysis bypass | ✅ `body_analysis_id: str | None` — si `null`, worker usa defaults | Sasha |

### Diagrama de flujo (mermaid sintético)
```
Cliente → POST /try-ons {photo_url, garment_ids?, body_analysis_id?}
       ← 202 Accepted {job_id}
Cliente → GET /try-ons/{job_id} (polling cada 2-3s)
       ← {status: 'processing'}
       ← {status: 'completed', result_url, ai_insights}
Worker  → ARQ pulls job → Replicate API → Supabase Storage → DB update
```

### Decisión de polling vs WebSocket
**Polling gana en MVP.** Razones:
- WebSocket añade ~1 semana Sasha (conexión persistente + reconnect logic)
- Try-ons toman 20-30s → polling cada 3s = 7-10 requests, trivial
- WebSocket vale la pena solo cuando hay >100 actualizaciones/min/user (chat, presence)
- Re-evaluar a 250K MAU si Supabase Realtime se justifica

### Riesgos
- **Polling thundering herd:** Si app cliente queda abierta con polling activo y la app vuelve a foreground, todos los polls re-disparan. Mitigación: jitter en cliente (random 2-4s).
- **Polling agresivo agota rate limit:** Ya cubierto por ADR-007 (60/min en endpoints lectura).

### Acción
- [x] Sasha: `GET /try-ons/{id}` ya implementado (0.3) ✅
- [ ] Brook: polling con jitter 2-4s, exponential backoff en errores
- [ ] Sprint 0.4: validar ARQ pool en lifespan funciona con FEATURE_MOCK_WORKERS=false

---

## 3. D3 — Triggered Body Analysis (Day 0 → Day 7 Gamified)

### Implicación técnica
🟡 **NUEVO TRABAJO REQUERIDO.** Necesitamos un **state machine de engagement** + **event store** para tracking de días/usos.

### Estado del usuario (FSM)

```
                     [signup]
                         |
                         v
                  ┌──────────────┐
                  │ NEW_USER     │  (Day 0, no try-ons)
                  └──────┬───────┘
                         | first_tryon_completed
                         v
                  ┌──────────────┐
                  │ FIRST_TRYON  │  (Day 1+, soft body_analysis prompt)
                  └──────┬───────┘
                         | tryons_count >= 3
                         v
                  ┌──────────────┐
                  │ ENGAGED      │  (Day 3+, gamified badge "3/5")
                  └──────┬───────┘
                         | tryons_count >= 5
                         v
                  ┌──────────────┐
                  │ POWER_USER   │  (Day 7+, strong push body_analysis)
                  └──────┬───────┘
                         | body_analysis_completed
                         v
                  ┌──────────────┐
                  │ ANALYZED     │  (Has body_type + color_season)
                  └──────────────┘
```

### Schema (nuevo)

```sql
-- migration 007_engagement_state.sql
ALTER TABLE users ADD COLUMN engagement_state TEXT DEFAULT 'NEW_USER'
  CHECK (engagement_state IN ('NEW_USER','FIRST_TRYON','ENGAGED','POWER_USER','ANALYZED'));
ALTER TABLE users ADD COLUMN tryons_count INT DEFAULT 0;
ALTER TABLE users ADD COLUMN first_tryon_at TIMESTAMPTZ;
ALTER TABLE users ADD COLUMN body_analysis_prompts_shown INT DEFAULT 0;
ALTER TABLE users ADD COLUMN body_analysis_dismissed_at TIMESTAMPTZ;

CREATE INDEX idx_users_engagement ON users(engagement_state, tryons_count);
```

### Lógica de transición (backend trigger después de cada try-on)

```python
# app/services/engagement.py
async def advance_engagement_state(user: User, repo: UserRepo) -> str:
    if user.engagement_state == 'NEW_USER' and user.tryons_count >= 1:
        await repo.update(user.id, engagement_state='FIRST_TRYON', first_tryon_at=now())
    elif user.engagement_state == 'FIRST_TRYON' and user.tryons_count >= 3:
        await repo.update(user.id, engagement_state='ENGAGED')
    elif user.engagement_state == 'ENGAGED' and user.tryons_count >= 5:
        await repo.update(user.id, engagement_state='POWER_USER')
    elif user.engagement_state == 'POWER_USER' and user.body_analysis_id is not None:
        await repo.update(user.id, engagement_state='ANALYZED')
    return user.engagement_state
```

### Frontend (Brook)
Endpoint nuevo: `GET /api/v1/users/me/engagement` → retorna `{state, tryons_count, prompts: ['body_analysis_soft' | 'body_analysis_gamified' | 'body_analysis_strong' | null]}`

### Riesgos
- **Prompt fatigue:** Si user dismissea body_analysis 3+ veces, NO mostrar más durante 14 días (cooldown).
- **Dark pattern detection:** Apple/Google rechazan apps con escalación agresiva. Mantener `Saltarse por ahora` siempre visible.

### Acción
- [ ] Sasha (Sprint 1): migration 007 + endpoint `/users/me/engagement` + servicio FSM
- [ ] Brook (Sprint 1): consumir endpoint en S04 result screen → render del prompt correcto
- [ ] Erik: validar que los 3 estilos de prompt (soft/gamified/strong) están diseñados en S04 result
- [ ] Cinthya: workflow n8n que mida funnel `FIRST_TRYON → POWER_USER → ANALYZED` semanalmente

---

## 4. D4 — Free Tier + Pricing ($9.99 Estilo / $19.99 Imagen)

### ⚠️ DISCREPANCIA RESUELTA: 1/día vs 5/mes

D4 dice **"1 try-on/día (30/mes equivalent)"**. ADR-006 + COST_MODEL_PATH_A original modelaron **5/mes**. **NO ES LO MISMO**:

| Variable | 5/mes (ADR-006) | 1/día (D4) | Delta |
|----------|----------------:|----------:|------:|
| Free try-ons/usuario/mes | 5 | ~22 (asume 73% retention) | **+340%** |
| Replicate cost free / 900K MAU | $112,500 (sin cache) | $495,000 (sin cache) | **+4.4x** |
| Replicate cost free / 900K MAU + 55% cache | $50,625 | $222,750 | **+4.4x** |

**Impacto:** Path A 1M MAU con 1/día explota margen a **<30%** sin mitigación. D4 NO está alineado con ADR-006.

**Recomendación arquitectónica (escalar a Juan Camilo + Leo):**
- Reinterpretar D4 como **"1 try-on/día con cap mensual de 8/mes"** (preserva sticky daily habit, controla costos)
- O activar **circuit breaker de ADR-007**: si MAU_free/MAU_paid > 25:1, auto-bajar a 3/mes
- O bajar Replicate cost via prompt/model más barato para free tier (FASHN base $0.025 vs $0.05 premium)

**Esta discrepancia es BLOQUEANTE para forecast comercial.** Ver `COST_MODEL_PATH_A.md` §2 (actualizado en esta entrega).

### Subscription State Machine

```
            [signup]
                |
                v
         ┌──────────────┐
         │  FREE        │
         └──────┬───────┘
                | checkout success (Stripe/MP webhook)
                v
         ┌──────────────┐
         │  TRIAL       │  (7 días sin tarjeta)
         └──────┬───────┘
                | trial_ends + payment_method
                v
     ┌──────────────────────┐
     │  ACTIVE_ESTILO       │←──┐ upgrade
     │  ACTIVE_IMAGEN       │   │
     └──────┬───────────────┘   │
            | payment_failed    │ downgrade
            v                   │
         ┌──────────────┐       │
         │ PAST_DUE     │───────┤
         └──────┬───────┘       │
                | 7 days        |
                v               |
         ┌──────────────┐       |
         │ CANCELED     │───────┘
         └──────────────┘ (back to FREE after grace 30d)
```

### Schema

```sql
-- migration 008_subscription_state.sql
ALTER TABLE subscriptions ADD COLUMN state TEXT DEFAULT 'FREE'
  CHECK (state IN ('FREE','TRIAL','ACTIVE_ESTILO','ACTIVE_IMAGEN','PAST_DUE','CANCELED'));
ALTER TABLE subscriptions ADD COLUMN trial_ends_at TIMESTAMPTZ;
ALTER TABLE subscriptions ADD COLUMN current_period_end TIMESTAMPTZ;
ALTER TABLE subscriptions ADD COLUMN canceled_at TIMESTAMPTZ;
ALTER TABLE subscriptions ADD COLUMN stripe_subscription_id TEXT UNIQUE;
ALTER TABLE subscriptions ADD COLUMN mp_subscription_id TEXT UNIQUE;

CREATE INDEX idx_subscriptions_state ON subscriptions(state);
CREATE INDEX idx_subscriptions_period_end ON subscriptions(current_period_end)
  WHERE state IN ('ACTIVE_ESTILO','ACTIVE_IMAGEN','PAST_DUE');
```

### Rate limiting por tier (ver ADR-007)

| Endpoint | FREE | TRIAL | ACTIVE_ESTILO | ACTIVE_IMAGEN |
|----------|-----:|------:|--------------:|---------------:|
| POST /try-ons | 1/día (D4) | 5/día | 5/día | unlimited (hard 200/mes) |
| POST /body-analysis | 1/mes | 5/mes | unlimited | unlimited |
| POST /recommendations | 5/día | 30/día | 100/día | unlimited |

### Acción
- [ ] Sasha (Sprint 0.4): migration 008 + subscription FSM service
- [ ] Sasha (Sprint 0.4): wire rate limiting con tier-aware slowapi key (`f"{user_id}:{tier}"`)
- [ ] Juan Camilo: resolver discrepancia 1/día vs 5/mes (decision needed antes de MON 26)
- [ ] Leo: actualizar pricing model con cost-aware free tier
- [ ] Cinthya: webhook handler Stripe + MP idempotente (event.id dedup — ya en backlog A04-MED1 + D8 Ego)

---

## 5. D5 — Social Sharing (Instagram Stories + WhatsApp + Referral)

### Implicación técnica
**Cubierto al 80%.** Falta: signed URL strategy con ACL pública controlada + analytics event taxonomy + referral attribution.

### Signed URL strategy

```python
# app/services/sharing.py
async def create_shareable_url(tryon_id: str, user_id: str) -> dict:
    """
    Generate signed URL para compartir try-on en redes sociales.
    Política:
    - URL válida 30 días (NO 24h — usuarios comparten Stories que duran 24h)
    - URL incluye watermark según tier (free/estilo/imagen)
    - URL es trackeable (referral_code embebido)
    """
    tryon = await tryon_repo.get(tryon_id, user_id=user_id)  # RLS enforced
    if tryon is None:
        raise NotFoundError()

    user = await user_repo.get(user_id)
    watermark_variant = {
        'FREE': 'visible_full',
        'TRIAL': 'visible_full',
        'ACTIVE_ESTILO': 'corner_only',
        'ACTIVE_IMAGEN': 'none',
    }[user.subscription_state]

    # Generate watermarked variant if not exists (cached in R2)
    watermarked_path = f"shares/{tryon_id}_{watermark_variant}.webp"
    if not await storage.exists(watermarked_path):
        await jobs.enqueue('watermark_tryon', tryon_id=tryon_id, variant=watermark_variant)
        return {'status': 'processing', 'retry_after': 3}

    signed_url = await storage.create_signed_url(
        path=watermarked_path,
        expires_in=86400 * 30,  # 30 días
    )

    referral_code = await referrals_repo.create_or_get(user_id)

    return {
        'shareable_url': signed_url,
        'deep_link': f"https://aifitcheck.com/shared/{tryon_id}?ref={referral_code}",
        'instagram_story_url': f"instagram://story-camera?source_image={signed_url}",
        'whatsapp_url': f"whatsapp://send?text={urlencode(deep_link)}",
    }
```

### Schema referrals

```sql
-- migration 009_referrals.sql
CREATE TABLE referrals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  referral_code TEXT UNIQUE NOT NULL,
  shares_count INT DEFAULT 0,
  signups_attributed INT DEFAULT 0,
  conversions_attributed INT DEFAULT 0,
  free_tryons_credited INT DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE referral_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  referral_code TEXT REFERENCES referrals(referral_code),
  event_type TEXT CHECK (event_type IN ('click','signup','conversion')),
  visitor_ip_hash TEXT,  -- hashed IP for dedup (no PII)
  user_agent_hash TEXT,
  attributed_user_id UUID REFERENCES users(id),
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_referrals_code ON referrals(referral_code);
CREATE INDEX idx_referral_events_code ON referral_events(referral_code, created_at);

-- RLS: usuarios ven solo SUS referrals
ALTER TABLE referrals ENABLE ROW LEVEL SECURITY;
CREATE POLICY referrals_select_own ON referrals FOR SELECT
  USING (user_id = auth.uid());
```

### Analytics event taxonomy (D5)

```python
# Eventos a trackear via PostHog (Sprint 0.4)
EVENTS = {
    'share_button_clicked': {'tryon_id', 'platform_selected'},
    'share_completed': {'tryon_id', 'platform', 'watermark_variant'},
    'referral_link_visited': {'referral_code', 'platform_source'},
    'referral_signup_attributed': {'referral_code', 'new_user_id'},
    'referral_conversion_attributed': {'referral_code', 'new_user_id', 'tier'},
    'free_tryon_credit_granted': {'user_id', 'reason'},  # reason='referral_sharer' | 'referral_signup'
}
```

### Riesgos

| Riesgo | Severidad | Mitigación |
|--------|-----------|-----------|
| Hot-linking de shared URLs ataca egress | 🟡 Med | R2 cache + signed URL 30d (vs unsigned permanent) |
| Watermark removible client-side | 🟢 Low | Watermark se aplica server-side al WebP final |
| Referral abuse (mismo user crea N cuentas) | 🟡 Med | IP hash + user_agent dedup + máx 10 referrals/mes/cuenta |
| PII en deep link | 🟡 Med | referral_code es UUID, NO username/email |
| Instagram/WhatsApp deeplink rotos en iOS/Android | 🟡 Med | `share_plus` Flutter package + native intent fallback |

### Acción
- [ ] Sasha (Sprint 2): migrations 009 (referrals) + signed URL service + watermark worker
- [ ] Brook (Sprint 2): S04 result button [Share] → bottom sheet con 3 plataformas
- [ ] Cinthya (Sprint 0.4): wire PostHog con eventos D5
- [ ] Cyber Neo: validar que signed URLs NO leakean datos de otros users (auditar RLS)

---

## 6. Cross-Cutting Concerns (Resumen)

### Arquitectura sigue siendo válida ✅
Ninguna de las 5 decisiones invalida:
- ADR-001 (JWKS auth)
- ADR-002 (Supabase Storage + signed URLs)
- ADR-003 (idempotency middleware)
- ADR-004 (caching agresivo Replicate)
- ADR-005 (RLS por user_id)
- ADR-006 (Path A 50K paid)

### Trabajo nuevo requerido

| Item | Sprint | Owner | Tamaño |
|------|--------|-------|--------|
| Migration 007 (engagement_state FSM) | 1 | Sasha | S (2h) |
| Migration 008 (subscription_state FSM) | 0.4 | Sasha | M (4h) |
| Migration 009 (referrals) | 2 | Sasha | M (4h) |
| `/users/me/engagement` endpoint | 1 | Sasha | S (3h) |
| Sharing service + watermark worker | 2 | Sasha | L (1d) |
| Tier-aware rate limiting (slowapi key compuesta) | 0.4 | Sasha + Antigravity | S (2h) |
| Analytics events PostHog (D5 taxonomy) | 0.4 | Cinthya | S (3h) |
| Resolver discrepancia D4 (1/día vs 5/mes) | INMEDIATO | Juan Camilo + Leo + Alejo | Decisión |

**Total trabajo nuevo: ~3 días Sasha distribuidos entre sprints 0.4, 1, 2.**

### Bloqueante INMEDIATO 🔴

**D4 ambigüedad 1/día (D4) vs 5/mes (ADR-006).** Sin resolver, COST_MODEL diverge en 4.4x, paywall no se puede diseñar correctamente, y la presentación a Juan Camilo del sábado va con números inconsistentes.

**Recomendación de Alejo:** Adoptar **"1/día con cap 8/mes"** + circuit breaker ADR-007 si MAU_free/paid > 25:1. Esto preserva D4 "daily habit" pero ancla el modelo financiero.

---

## 7. Hand-off

| Receptor | Acción |
|----------|--------|
| **Jarvis** | Llevar discrepancia D4 a Juan Camilo + Leo antes de MON 26 |
| **Sasha** | Revisar migrations 007/008/009 en este doc — todos van a Sprint 1-2 |
| **Brook** | Endpoint `/users/me/engagement` consumible en Sprint 1 |
| **Cinthya** | Analytics events D5 + funnel engagement D3 |
| **Cyber Neo** | Validar RLS en referrals + signed URLs no leakean cross-user |
| **Erik** | Validar S04 muestra los 3 prompts D3 + S10 muestra los 3 tiers D4 + S04 result tiene CTA Share D5 |

---

**Status:** ✅ Entregado para Sprint 1
**— Alejo, Solutions Architect**
