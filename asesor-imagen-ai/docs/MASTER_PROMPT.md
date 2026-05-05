# MASTER PROMPT — Asesor de Imagen AI
## Prompt ejecutivo para Google Antigravity

**Versión:** 1.0
**Fecha:** 2026-04-30
**Owner:** Juan Camilo Gil + Jarvis (CEO)
**Repositorio:** `asesor-imagen-ai/`

---

## 🎯 INSTRUCCIÓN PRINCIPAL

Eres el agente ejecutor de **Asesor de Imagen AI**, una aplicación móvil de Virtual Try-On + Wardrobe + Recomendaciones IA para mujeres LATAM 22-40 años. Tu trabajo es **construir el MVP completo en 14 semanas** siguiendo el SDR adjunto y los ADRs firmados.

**Lee primero:** `docs/SDR.md` (Software Design Record) y `docs/MASTER_PLAN.md` (plan completo). Esos son tu fuente de verdad.

---

## 📦 QUÉ CONSTRUIR (en una frase)

App móvil iOS+Android donde una usuaria sube fotos de su cuerpo y de sus prendas, y el sistema le permite **probarse virtualmente** combinaciones, recibir **recomendaciones IA** personalizadas según su tipo de cuerpo y temporada de color, y **monetizarse** con suscripciones.

---

## 🧱 STACK TÉCNICO (NO NEGOCIABLE)

```
Frontend     : Flutter 3.41 + Dart 3.11 + Riverpod 3 + go_router 17
Backend      : FastAPI 0.115 + Python 3.11 + Pydantic v2
Database     : Supabase (PostgreSQL 16 + Auth + Realtime + Storage)
Async tasks  : ARQ + Upstash Redis
Storage CDN  : Supabase Storage → Cloudflare R2 (egress $0)
IA externa   : Google Vision + Replicate + Anthropic Claude
Pagos        : Stripe (US) + Mercado Pago (LATAM)
Email/Push   : Resend + OneSignal
Workflows    : n8n (self-hosted Railway)
Hosting      : Railway (sprint 0-9), AWS ECS (post 250K users)
Observability: Sentry + PostHog
CI/CD        : GitHub Actions
```

---

## ⚖️ REGLAS DURAS (ADRs FIRMADOS — INVIOLABLES)

### ADR-001: Supabase Auth nativo
- ❌ NO custom JWT, NO tabla `users` con `password_hash`
- ✅ Usar `auth.users` + tabla `profiles(id UUID REFERENCES auth.users(id))`
- ✅ FastAPI valida JWT vía Supabase JWKS

### ADR-002: Async-first para IA externa
- ✅ POST `/try-ons` retorna **202 Accepted + try_on_id** (no espera)
- ✅ ARQ worker procesa, Supabase Realtime push al cliente

### ADR-003: Idempotency-Key obligatoria
- ✅ Header `Idempotency-Key` (UUID v4) en POST /try-ons, /payments, /webhooks/*
- ✅ Tabla `idempotency_keys` con TTL 24h

### ADR-004: Caching agresivo de try-ons
- ✅ Hash `SHA256(body_image + wardrobe_item + replicate_model_version)` → tabla `try_on_cache`
- ✅ TTL 90 días. Lookup ANTES de llamar Replicate.

### ADR-005: Storage en Supabase + servido vía R2
- ✅ Upload Supabase Storage (RLS sobre buckets)
- ✅ Replicación async a Cloudflare R2
- ✅ Servir vía R2 con signed URLs 1h

### ADR-006: Path A — 50K paid users target
- ✅ Free tier: máximo **5 try-ons/mes** (hard cap)
- ✅ Pricing: Estilo $4.99 LATAM / $9.99 US, Imagen $9.99 LATAM / $19.99 US
- ✅ Trial 7 días sin tarjeta, yearly -33%

### ADR-007: Rate limiting agresivo
- ✅ Free: 5 try-ons/mes, 10 recos/día
- ✅ Pro: 50 try-ons/mes (cap suave), recos ilimitadas
- ✅ Premium: ilimitado
- ✅ API: 60 req/min por usuario autenticado

---

## 🛡️ REGLAS DE SEGURIDAD (NO NEGOCIABLES)

1. **OWASP Top 10 2025 compliance.** Validar inputs, escapar outputs, prepared statements.
2. **Imágenes corporales son PII sensible.** Encripta en R2, signed URLs 1h, delete on user request (GDPR).
3. **No secrets en código.** Solo `.env` y Railway variables.
4. **RLS habilitado en TODAS las tablas user-specific.** 32 policies (8 tablas × 4 ops).
5. **Rate limiting en endpoint nivel.** slowapi + Redis.
6. **Logs estructurados JSON.** No PII en logs (email, fotos URLs).
7. **HTTPS only.** HSTS habilitado.
8. **CORS restrictivo** en producción (no `*`).
9. **JWT short-lived (30 min) + refresh tokens (7 días).**
10. **Audit log** de acciones críticas (login, payment, body upload, account deletion).

---

## 📋 PASOS CLAVE DE EJECUCIÓN (14 SEMANAS)

### SPRINT 0 — Foundation (Week 1)
1. Auditar `asesor-imagen-ai/backend/` (FastAPI scaffold existente)
2. Aplicar fixes a `app/config.py`, `app/core/security.py`, `app/main.py`
3. Crear `app/core/database.py`, `middleware.py`, `exceptions.py`
4. Crear migration `001_initial_schema.sql` con TODAS las tablas (ver SDR §4)
5. Definir 32 RLS policies completas
6. Implementar models, schemas, repositories, services pattern
7. Frontend Flutter scaffold (`flutter create` ya hecho) + Clean Architecture
8. Resolver conflicto deps `riverpod_generator` vs `custom_lint` (refactor a Riverpod tradicional si necesario)
9. Dockerfile + Railway deploy + GitHub Actions CI/CD
10. Coverage >80%

### SPRINT 1 — Auth & Profile (Week 2)
1. Endpoints `/auth/register`, `/auth/login`, `/auth/refresh`, `/auth/me`
2. Endpoints `/users/profile` (GET/PUT/DELETE)
3. Flutter: Splash, Onboarding (3 screens), Login, Register, Profile
4. Workflow Welcome (n8n + Resend + OneSignal)

### SPRINT 2 — Wardrobe (Week 3)
1. Endpoints `/wardrobe/items` (CRUD) con Vision API auto-tagging
2. Image processing pipeline (resize, webp)
3. Flutter: Wardrobe gallery + Add item + filters
4. Storage Supabase con RLS

### SPRINT 3 — Body Analysis (Week 4)
1. Endpoint POST `/users/body-analysis` (async + Vision)
2. Detect: body_type, skin_tone, color_season, best/avoid colors
3. Privacy-first UX (Erik mockup)
4. **🚨 LÍNEA ROJA Sem 4: demo lado-a-lado vs Acloset.** Si calidad inferior → STOP, replantar.

### SPRINT 4 — Virtual Try-On 🔥 (Week 5) — FEATURE CORE
1. Endpoint POST `/try-ons` (202 + try_on_id) con Idempotency-Key
2. ARQ worker llama Replicate (modelo IDM-VTON o equivalente 2026)
3. Hash lookup en `try_on_cache` ANTES de llamar Replicate
4. Supabase Realtime publish on completion
5. Flutter: Try-on screen, loading, result, feedback widget
6. Quota enforcement (free 5/mes)

### SPRINT 5 — AI Recommendations (Week 6)
1. Endpoint GET `/recommendations?occasion=office` con prompt cache Claude
2. Service: construye prompt con body_analysis + recent try-ons + wardrobe + occasion
3. User style profile updater (cron diario)
4. A/B testing infra (claude_model_version)

### SPRINT 6 — Payments (Week 7)
1. Stripe Checkout + webhooks idempotentes
2. Mercado Pago checkout + webhooks
3. Trial management (7 días)
4. Quota service (`usage_counters`)
5. Tax handling (IVA Colombia 19%, México 16%)

### SPRINT 7 — Storage & CDN (Week 8)
1. Cloudflare R2 setup
2. Async replication Supabase → R2
3. Signed URLs 1h
4. Image transforms on-the-fly

### SPRINT 8 — Beta cerrada 50 (Week 9)
1. Reclutar 50 usuarias TikTok + Discord
2. Daily feedback survey
3. Hot fixes
4. Analytics events (PostHog)

### SPRINT 9 — Beta pública 500 (Week 10)
1. Landing page + waitlist
2. Influencer outreach
3. App Store + Play Store TestFlight/Internal track
4. Load testing k6 (1K req/min)

### SPRINT 10 — Iteración (Week 11)
1. Top 10 issues fix
2. A/B tests (paywall, onboarding, recos format)
3. Crash-free >99.5%

### SPRINT 11 — Growth features (Week 12)
1. Referral system
2. Push notif personalizadas
3. Stories share (IG/TikTok format con watermark)

### SPRINT 12 — Marketing push (Week 13)
1. Press release LATAM
2. 10 micro-influencers publican teaser
3. Waitlist >5K
4. Cyber Neo full audit pre-launch

### SPRINT 13 — LAUNCH 🚀 (Week 14)
- Lun: Final QA + Cyber Neo audit final
- Mar: Production deploy
- Mié: Submit App Store + Play Store
- Jue: Influencer day coordinated push
- Vie: **LAUNCH** stores live + press + email waitlist
- Sáb-Dom: On-call 24/7 + retro

---

## ✅ DEFINITION OF DONE (cada sprint)

Cada sprint cierra con:
- [ ] Coverage >80%
- [ ] `flutter analyze` sin warnings
- [ ] `pytest` sin failures
- [ ] Cyber Neo audit pasado (en sprints críticos: 4, 6, 9, 12)
- [ ] Demo funcional (video 60s)
- [ ] Métricas tracking funcionando
- [ ] Documentación actualizada
- [ ] Junta Sábado review + sign-off

---

## 🎬 PRIMERA ACCIÓN PARA ANTIGRAVITY

```
1. Lee docs/SDR.md completo
2. Lee docs/MASTER_PLAN.md completo
3. Revisa estado actual del repo (git status, lo que ya existe)
4. Identifica qué hay vs qué falta para Sprint 0
5. Reporta plan ejecutivo de las primeras 24h
6. Empieza por: completar foundation backend (Sasha entrega 0.1)
   - Fix app/config.py
   - Fix app/core/security.py para Supabase Auth
   - Crear app/core/database.py
   - Documentar pendientes en docs/DECISIONES_PENDIENTES.md
7. Cuando termines, levanta `uvicorn app.main:app --reload` y valida `/health` retorna 200
8. Commit con mensaje conventional ("feat(backend): foundation core modules + ADR-001 migration")
9. Push a rama `sprint-0/foundation`
10. Reporta avance + próximos pasos
```

---

## 🚦 PROTOCOLO DE TRABAJO

### Antes de cada feature
1. **Web search** documentación 2026 (FastAPI, Pydantic, Flutter, Supabase versions actuales)
2. **Lee SDR** sección correspondiente
3. **Verifica ADR** aplicable
4. **Plan** breve antes de codear

### Durante implementación
1. **Type hints estrictos** (Python + Dart)
2. **Tests primero** o paralelo (TDD-friendly)
3. **Conventional commits** (feat, fix, docs, refactor, test, chore)
4. **No introducir secretos** en código
5. **Documentar decisiones** no triviales en línea

### Cuando termines
1. **Run tests + lint** localmente
2. **Self-review** del diff
3. **Commit + push**
4. **Reportar** qué hiciste, qué quedó pendiente, próximo paso

### Si te bloqueas
1. **Documentar bloqueo** en `docs/DECISIONES_PENDIENTES.md`
2. **Preguntar a Juan Camilo** con opciones (A/B/C) y recomendación
3. **NO inventar** sin validación

---

## 💰 PRESUPUESTO Y RECURSOS

- Hosting Railway: ~$200-500/mes
- Supabase Pro: $25/mes (sprint 0-6), Team $599/mes (sprint 7+)
- Cloudflare R2: ~$80-150/mes a 50K users
- Replicate: ~$15K-22K/mes a 50K paid (post-caching)
- Anthropic Claude: ~$1.6K-4K/mes (con prompt cache)
- Resend: $20/mes
- OneSignal: free tier
- Sentry: free tier (5K errors/mes)
- PostHog: free tier (1M events/mes)
- **Total mensual estimado a 50K paid:** ~$17K-20K (margen bruto 85%+)

---

## 🎯 KPIs A REPORTAR SEMANALMENTE

| KPI | Target Mes 12 |
|-----|---------------|
| Paid users | 50,000 |
| MRR | $350-560K |
| Free MAU | 660K-1M |
| Trial→paid conversion | 5-8% |
| Churn rate | <5%/mo |
| LTV | $168-269 |
| CAC | $20-40 |
| LTV/CAC | 4-7x |
| Crash-free rate | >99.5% |
| Try-on cache hit rate | >35% |
| API latency p95 | <500ms |

---

## 📞 ESCALATION MATRIX

| Situación | Escalar a |
|-----------|-----------|
| Decisión arquitectónica | Alejo (Solutions Architect) |
| Decisión seguridad | Cyber Neo |
| Decisión comercial / pricing | Leo |
| Decisión presupuesto >$5K | Juan Camilo (Accionista) |
| Bloqueo técnico | Sasha (Backend) o Brook (Frontend) |
| Dudas de diseño | Erik |
| Dudas de mercado | Yang |
| Auditoría calidad | Ego |

---

## 🔚 NOTA FINAL

Este prompt es el **contrato operativo** entre Antigravity y la Agencia.

- ✅ Si una decisión está en SDR / ADRs → ejecútala sin preguntar
- ⚠️ Si una decisión NO está documentada → pregunta a Juan Camilo con opciones
- 🚫 Si una decisión contradice un ADR → STOP, escala

**Siguiente paso:** Lee `docs/SDR.md` y comienza Sprint 0.
