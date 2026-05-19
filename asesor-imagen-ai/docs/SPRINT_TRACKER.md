# 📊 SPRINT TRACKER — Asesor de Imagen AI
## Single Source of Truth del estado del proyecto

**Owner:** Jarvis (CEO)
**Última actualización:** 2026-05-18
**Frecuencia de update:** Cada sesión + post-entregas
**Cómo leer:** Empieza por "🎯 STATUS HOY" → revisa "🚦 ACCIONES PRÓXIMAS"

---

## 🎯 STATUS HOY (vista de 1 minuto)

| Indicador | Valor | Señal |
|-----------|-------|-------|
| **Sprint actual** | Sprint 0.4 — DevOps & Hardening | 🟡 Prompt listo, trigger pendiente |
| **Entrega anterior** | 0.3 ✅ `8fe1b01` + security patch `6fca4a8` — 161 tests, 82% cov, B+ Ego | 🟢 Auditado y aprobado |
| **Días desde inicio** | ~24 días (de ~98 totales) | 🟢 Adelantado |
| **Bloqueos críticos** | 0 | 🟢 |
| **Decisiones pendientes Juan Camilo** | Ver sección D1–D5 en UX_SCREENS_PLAN.md | ⚠️ Pendiente |
| **Design system** | ✅ APROBADO — Aether Luxe (stitch_ai_fit_check_ui.zip) | 🟢 |
| **Próximo hito** | Sprint 0.4 entrega + Erik mockups S05–S11 | 📅 |

**Resumen 1 línea:** Sprints 0.1✅ 0.2✅ 0.3✅ — Design system Aether Luxe aprobado por Juan Camilo. **Sprint 0.4 (DevOps) + Erik (mockups restantes S05–S11) en paralelo.**

**Commits verificados:**
- `5eeb41b` — Sprint 0.1 Foundation ✅
- `ded674c` — Sprint 0.2 Data Layer + patch ✅
- `8fe1b01` — Sprint 0.3 Services & Endpoints ✅
- `6fca4a8` — Sprint 0.3 Security Patch (Cyber Neo + Ego findings) ✅

---

## 📦 ENTREGAS SPRINT 0 — CHECKLIST DETALLADO

### 🔧 Entrega 0.1 — Foundation Backend ✅ COMPLETA
**Commit:** `5eeb41b` | **Auditoría:** Cyber Neo + Ego ✅

### 🗄️ Entrega 0.2 — Data Layer ✅ COMPLETA
**Commits:** entrega inicial + patch `ded674c` | 107 tests, 85.32% cov, 13 findings resueltos

**TODO pendiente (no bloqueante):**
- [ ] Activar `.rpc("increment_usage")` en repos.py post-migration Supabase remote

---

### 🔌 Entrega 0.3 — Services & Endpoints ✅ COMPLETA
**Commits:** `8fe1b01` + security patch `6fca4a8`
**Status:** ✅ APROBADA — Ego B+, Cyber Neo PASS condicional (0 CRITICAL)

**Métricas finales:**
- 161 tests pasando, 1 skipped
- 82% coverage (target ≥80% ✅)
- Ruff: all checks passed ✅
- 0 findings CRITICAL, 2 HIGH mitigados en security patch

**Entregado:**
- [x] 7 servicios: Auth, Wardrobe, BodyAnalysis, Recommendation, TryOn, Subscription, User
- [x] 8 módulos de endpoints wired en /api/v1
- [x] 3 workers ARQ (stubs: vision, replicate, claude)
- [x] JWKS auth middleware activo (ADR-001)
- [x] Idempotency middleware activo con replay store (ADR-003)
- [x] **Security patch:** SSRF (AnyHttpUrl), Stripe HMAC bytes, MP template, password policy, webhook 500/503, idempotency solo cachea 2xx

**Hallazgos pendientes para Sprint 0.4 (de Cyber Neo):**
- [ ] A04-HIGH1: Rate limiting (RATE_LIMIT_PER_MINUTE declarado, no aplicado) → **BLOQUEANTE Sprint 0.5**
- [ ] A07-HIGH1: /auth/refresh sin rate limit + verificar Supabase refresh token rotation → **BLOQUEANTE Sprint 0.5**
- [ ] A04-MED1: Idempotency UNIQUE constraint en DB (race condition TOCTOU)
- [ ] A11-MED1: httpx.AsyncClient compartido via lifespan (actualmente por llamada)
- [ ] D8 (Ego): Webhook dedup por event.id Stripe (double-processing risk)

---

### 🚀 Entrega 0.4 — DevOps & Hardening
**Owner:** Antigravity (ejecutor) + Cyber Neo + Ego (auditores)
**Status:** 🟡 PROMPT LISTO — `docs/SPRINT_0_4_PROMPT.md`

**Tareas del sprint:**
- [ ] **Migration 006:** UNIQUE constraint en idempotency_keys (A04-MED1)
- [ ] **Rate limiting:** slowapi + Redis (A04-HIGH1 BLOQUEANTE)
  - [ ] `app/core/rate_limiter.py`
  - [ ] Auth endpoints: 5/min/IP
  - [ ] AI endpoints: 30/hour/user_id
  - [ ] Wire en create_app()
- [ ] **ARQ pool real:** `create_pool()` en lifespan + `ArqPoolDep` + enqueue real en services
- [ ] **Readiness probe:** Redis ping incluido
- [ ] **Sentry:** sentry-sdk[fastapi], `app/core/observability.py`, init en lifespan
- [ ] **PostHog:** track user_registered, try_on_created, subscription_activated
- [ ] **Docker:** Dockerfile multi-stage Python 3.12 slim
- [ ] **docker-compose.yml:** api + worker + redis
- [ ] **railway.toml** + `.env.example`
- [ ] **GitHub Actions:** `ci.yml` (test + ruff + docker build + smoke test)
- [ ] **Cleanup:** eliminar `commit_msg.txt`, verificar `.gitignore`
- [ ] **Tests:** test_rate_limiting.py, test_observability.py, readiness test actualizado
- [ ] Coverage ≥80%, ruff clean, Docker build exitoso

---

## 🟦 TRABAJOS PARALELOS (no bloquean Sprint 0)

### 🟣 Erik — Diseño ← DESBLOQUEADO por design system
- [x] Sistema de diseño base
- [x] 5 mockups core (login, register, onboarding x3)
- [x] **Design system Aether Luxe APROBADO** — tokens completos en `docs/design-system/DESIGN_SYSTEM.md`
- [x] **Referencia pantalla Virtual Try-On** — `stitch_ai_fit_check_ui.zip`
- [ ] **S04B: Loading state** Try-On (animación gradiente pulsante) ← NUEVO, faltaba en prototipo
- [ ] **S05: My Wardrobe** (galería closet, grid prendas, filtros)
- [ ] **S06: Style Insights** (análisis cuerpo + color season resultado)
- [ ] **S07: Body Analysis Upload** (flujo captura foto análisis)
- [ ] **S08: Collections** (looks guardados, masonry grid)
- [ ] **S09: Perfil / Settings**
- [ ] **S10: Paywall / Upgrade to Pro** (tabla tiers, CTAs por plan)
- [ ] **S11: Estados de error** (skeleton, 404, red, try-on fallido)
- [ ] Componentes Flutter: GradientButton, UploadZone, ClothingSlot, AIInsightCard
- [ ] Animaciones Lottie: loading try-on, success, empty states

### 🔵 Brook — Frontend Flutter ← tokens listos para implementar
- [x] Flutter scaffold + Clean Architecture + Riverpod + go_router
- [ ] **Fix 4 issues técnicos** (deps conflict, imports, build_runner) ← BLOQUEA TODO LO DEMÁS
- [ ] **Integrar Aether Luxe tokens** en ThemeData Flutter (`AppColors`, `AppTypography`, `AppSpacing`)
- [ ] **NavigationBar** (móvil 4 tabs) + **NavigationRail** (tablet)
- [ ] Login + Register screens (con GradientButton, inputs styled)
- [ ] Componentes base: GradientButton, UploadZone, ClothingSlot, AIInsightCard
- [ ] Virtual Try-On screen (S04) — post Erik mockups
- [ ] My Wardrobe screen (S05)

Referencia implementación: `docs/design-system/DESIGN_SYSTEM.md` sección 9 (equivalencias Flutter)

### 🟠 Yang — Inteligencia
- [x] INTEL_COMPETIDORES_2026.md + 3 personas + 10 micro-influencers
- [ ] Dossiers individuales de 10 influencers
- [ ] Validar viabilidad 660K-1M MAU free

### 🟤 Leo — Comercial
- [x] PRICING_STRATEGY.md + 3 tiers + GTM plan 14 semanas
- [ ] Outreach plan a 10 micro-influencers
- [ ] Sales deck + pitch partnerships LATAM

### 🟡 Cinthya — Automation
- [ ] AUTOMATION_WORKFLOWS.md (8 workflows) — re-trigger pendiente
- [ ] Implementación n8n (post Sprint 1)

### ⚪ Alejo — Architecture
- [x] 5 ADRs firmados (001-005)
- [ ] ADR-007 borrador (rate limiting agresivo) — pendiente este sprint
- [ ] COST_MODEL_PATH_A.md recalc — re-trigger pendiente

### 🔴 Cyber Neo — Seguridad
- [x] Audit Sprint 0.1 ✅
- [x] Audit Sprint 0.2 ✅ (13 findings resueltos)
- [x] Audit Sprint 0.3 ✅ (0 CRITICAL, 2 HIGH → ambos en security patch)
- [ ] Audit Sprint 0.4 (post entrega)

---

## ⚠️ ISSUES ABIERTOS

| # | Severidad | Descripción | Owner | Status |
|---|-----------|-------------|-------|--------|
| 1 | 🟡 Medio | Brook 4 issues técnicos Flutter | Brook | Pendiente |
| 2 | 🟢 Bajo | Cinthya workflows + Alejo cost model | Cinthya, Alejo | Re-trigger |
| 3 | 🟡 Medio | Erik 5 mockups restantes | Erik | Pendiente |
| 4 | 🟢 Bajo | UsageCounter.rpc() activar post migration remota | Post 0.4 | TODO repos.py |
| 5 | 🟢 Bajo | Aplicar migrations 004+005 a Supabase remote | Juan Camilo | Credenciales |
| 6 | 🟢 Bajo | Supabase refresh_token_rotation verificar en dashboard | Juan Camilo | A07-HIGH1 |

---

## 🚦 ACCIONES PRÓXIMAS (en orden)

| # | Acción | Owner | Trigger |
|---|--------|-------|---------|
| 1 | **🔴 TRIGGER Antigravity Sprint 0.4** (`docs/SPRINT_0_4_PROMPT.md`) | Juan Camilo | AHORA |
| 2 | Audit Cyber Neo + Ego sobre 0.4 | Jarvis lanza | Cuando 0.4 entregue |
| 3 | Junta Estratégica 16 mayo | Todo el equipo | Mañana |
| 4 | Aplicar migrations 004+005 a Supabase remote | Juan Camilo | Con credenciales |
| 5 | Verificar refresh_token_rotation en Supabase dashboard | Juan Camilo | Sprint 0.4 |
| 6 | Re-trigger Erik (5 mockups) | Jarvis | Rate limit resuelto |
| 7 | Re-trigger Brook (4 issues Flutter) | Jarvis | Post Erik |
| 8 | Re-trigger Cinthya + Alejo | Jarvis | Rate limit resuelto |

---

## 📅 HITOS PRÓXIMOS

| Fecha | Hito | Status |
|-------|------|--------|
| 2026-05-16 (vie) | Junta Estratégica — revisión Sprint 0 completo | 📅 Mañana |
| 2026-05-19 (lun) | Sprint 0.4 cierre + Docker en Railway | 🎯 Target |
| 2026-05-26 | Sprint 1 cierre (Auth + Profile end-to-end) | 🎯 Target |
| 2026-06-09 | Sprint 3 cierre (Body Analysis) — LÍNEA ROJA | 🚨 Crítico |
| 2026-06-23 | Sprint 4 cierre (Try-On core) — DEMO | 🎯 Target |
| 2026-07-31 | LAUNCH 🚀 | 🎯 Target |

---

## 💰 KPIs A TRACKEAR (post-launch)

| KPI | Target Mes 12 | Tracking |
|-----|--------------|----------|
| Paid users | 50,000 | Stripe + MP dashboard |
| MRR | $350-560K | Stripe + MP |
| Free MAU | 660K-1M | PostHog |
| Trial→paid | 5-8% | PostHog funnel |
| Churn rate | <5%/mo | Stripe |
| Crash-free | >99.5% | Sentry |
| Cache hit rate | >35% | Custom metric |
| API latency p95 | <500ms | Sentry Performance |

---

## 📝 CHANGELOG

### 2026-05-18 (sesión actual)
- Juan Camilo aprobó design system **Aether Luxe** (stitch_ai_fit_check_ui.zip)
- Creado `docs/design-system/DESIGN_SYSTEM.md` — tokens Flutter completos (colors, typography, spacing, shadows, radius, components)
- Creado `docs/UX_SCREENS_PLAN.md` — inventario 11 pantallas + UX flows detallados
- Erik desbloqueado con referencia completa para mockups S04–S11
- Brook desbloqueado con equivalencias Flutter de todos los componentes
- 5 decisiones de UX documentadas (D1–D5) pendientes de Juan Camilo

### 2026-05-15
- Sprint 0.3 completado: commit `8fe1b01` (161 tests, 82% cov)
- Security patch `6fca4a8`: 7 hallazgos Cyber Neo + 2 P0 Ego resueltos
  - SSRF (AnyHttpUrl en image_url wardrobe + body_analysis)
  - Stripe HMAC bytes-only, MercadoPago data.id template fix
  - Password policy min_length=10 + letra+dígito
  - Webhooks: 400/500/503 estructurado (no 200 silencioso)
  - Idempotency: solo cachea 2xx, falla gracefully en 4xx/5xx
  - body_bytes inicializado fuera del try, user_id en request logs
- Sprint 0.4 prompt preparado por Jarvis — listo para trigger

### 2026-05-14
- Antigravity entregó Sprint 0.3 sin commit
- Jarvis auditó, encontró 14 test failures, aplicó todos los fixes
- Cyber Neo: 0 CRITICAL, 2 HIGH (rate limiting + refresh token)
- Ego: B+ — apto para Sprint 0.4 con condiciones

### 2026-04-30
- Sprint 0.2 patch `ded674c` confirmado: 107 tests, 85.32% cov
- Sprint 0.3 prompt preparado

---

**Tracker actualizado a:** 2026-05-15
**Próximo update:** Post Sprint 0.4 entrega

> **Cómo usar este tracker:**
> 1. Revísalo cada vez que abras una sesión
> 2. Foco en "🎯 STATUS HOY" + "🚦 ACCIONES PRÓXIMAS"
> 3. Pídeme update cuando algo cambie
> 4. Jarvis lo actualiza al cierre de cada entrega
