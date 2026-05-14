# 📊 SPRINT TRACKER — Asesor de Imagen AI
## Single Source of Truth del estado del proyecto

**Owner:** Jarvis (CEO)
**Última actualización:** 2026-04-30 (post ded674c — Sprint 0.2 patch completado)
**Frecuencia de update:** Cada sesión + post-entregas
**Cómo leer:** Empieza por "🎯 STATUS HOY" → revisa "🚦 ACCIONES PRÓXIMAS"

---

## 🎯 STATUS HOY (vista de 1 minuto)

| Indicador | Valor | Señal |
|-----------|-------|-------|
| **Sprint actual** | Sprint 0 (Foundation) — entrega 0.3 | 🟢 Listo para trigger |
| **Entrega anterior** | 0.2 ✅ patch `ded674c` — 107 tests, 85.32% coverage | 🟢 Auditado y aprobado |
| **Días desde inicio** | ~14 días (de ~98 totales) | 🟢 Adelantado |
| **Bloqueos críticos** | 0 | 🟢 |
| **Decisiones pendientes Juan Camilo** | 0 activas | 🟢 |
| **Próximo hito** | Junta Estratégica 16 mayo (reprogramada) | 📅 |

**Resumen 1 línea:** Sprint 0.1 ✅ (`5eeb41b`) + Sprint 0.2 ✅ patch (`ded674c`, 13 findings resueltos, 107 tests, 85.32% cov). **Sprint 0.3 = Services & Endpoints → TRIGGER ANTIGRAVITY AHORA.**

**Commits verificados:**
- `5eeb41b` — Sprint 0.1 Foundation ✅
- `ded674c` — Sprint 0.2 Data Layer + patch (12 archivos, +1222/-96 líneas) ✅

---

## 📦 ENTREGAS SPRINT 0 — CHECKLIST DETALLADO

### 🔧 Entrega 0.1 — Foundation Backend ✅ COMPLETA
**Owner:** Antigravity (ejecutor) + Cyber Neo + Ego (auditores)
**Commit:** `5eeb41b`
**Status:** ✅ APROBADA

- [x] Audit `asesor-imagen-ai/backend/` actual
- [x] Fix `app/config.py` — get_settings() lru_cache + Pydantic v2
- [x] Fix `app/core/security.py` — JWKS validation Supabase Auth
- [x] Fix `app/main.py` — lifespan async + middlewares + exception handlers
- [x] Crear `app/core/database.py`
- [x] Crear `app/core/middleware.py` — StructuredLogMiddleware + IdempotencyMiddleware stub
- [x] Crear `app/core/exceptions.py`
- [x] Trabajo en repo real (no scratch)
- [x] postgrest-py 0.16.6 instalado (supabase-py reemplazado por compat. Windows)
- [x] git commit + push
- [x] Cyber Neo audit → APPROVED WITH FIXES
- [x] Ego audit → 82/100 → patch aplicado
- [x] Validación final Jarvis ✅

---

### 🗄️ Entrega 0.2 — Data Layer (Migrations + Models + Schemas) ✅ COMPLETA
**Owner:** Antigravity + Cyber Neo (RLS audit)
**Commits:** entrega inicial + patch `ded674c`
**Status:** ✅ APROBADA (13 findings resueltos, 107 tests, 85.32% coverage)

- [x] Migration `004_consolidated_schema_v2.sql` — 12 tablas (IF NOT EXISTS, idempotente)
- [x] `004_consolidated_schema_v2_down.sql` — rollback simétrico
- [x] `005_rls_policies.sql` — ~34 policies RLS
- [x] Triggers `updated_at` en todas las tablas
- [x] Índices de performance
- [x] Models Pydantic v2 en `app/models/` (9 modelos incl. UserStyleProfile)
- [x] Schemas en `app/schemas/auth.py`
- [x] BaseRepository + 9 repos concretos en `app/repositories/`
- [x] AdminClient: `.with_user_check(id_column=)`, `.trusted()`, `.schema()` fix
- [x] Stored proc `increment_usage()` (atomic counter)
- [x] **Cyber Neo + Ego audit** → todos los findings resueltos
- [x] 107 tests (incl. integration/test_repos_real_schema.py)
- [x] SCHEMA_DIAGRAM.md (Mermaid ER)

**TODO pendiente post-0.2 (no bloqueante):**
- [ ] Activar `.rpc("increment_usage")` en repos.py:UsageCounterRepository.increment (una vez migration aplicada a Supabase remote)

---

### 🔌 Entrega 0.3 — Services & Endpoints
**Owner:** Antigravity + Cyber Neo + Ego
**Status:** 🟡 TRIGGER LISTO — prompt entregado a Juan Camilo

- [ ] Services: auth, user, wardrobe, vision, try_on, recommendation
- [ ] Endpoints `/auth/*` (register, login, refresh, me)
- [ ] Endpoints `/users/*` (profile, body-analysis)
- [ ] Endpoints `/wardrobe/*` (CRUD)
- [ ] Endpoints `/try-ons/*` (POST 202 + GET + feedback)
- [ ] Endpoints `/recommendations/*`
- [ ] Endpoints `/subscriptions/*` + webhooks
- [ ] ARQ workers (vision_worker, replicate_worker, claude_worker)
- [ ] Idempotency middleware activo (no stub)
- [ ] Tests integración endpoints
- [ ] **Cyber Neo audit endpoints**

---

### 🚀 Entrega 0.4 — DevOps & Hardening
**Owner:** Antigravity + Cyber Neo (final audit)
**Status:** ⚪ Pendiente (espera 0.3)

- [ ] Dockerfile multi-stage (Python 3.11 slim)
- [ ] `railway.json` con build/start commands
- [ ] `.github/workflows/test.yml` (lint + mypy + pytest + coverage)
- [ ] `.github/workflows/deploy.yml` (build + deploy Railway)
- [ ] Sentry SDK integrado
- [ ] PostHog SDK integrado
- [ ] Rate limiting con slowapi + Upstash Redis
- [ ] Coverage final >80%
- [ ] **Cyber Neo audit FULL pre-deploy**
- [ ] Smoke test producción

---

## 🟦 TRABAJOS PARALELOS (no bloquean Sprint 0)

### 🟣 Erik — Diseño
- [x] Sistema de diseño base (colores, tipografía, tokens)
- [x] 5 mockups core (login, register, onboarding x3)
- [ ] 5 mockups restantes (body, try-on, recos, profile, paywall premium)
- [ ] Iconografía custom set
- [ ] Animaciones Lottie key (loading try-on, success, milestones)

### 🔵 Brook — Frontend Flutter
- [x] `flutter create` + scaffold
- [x] Clean Architecture folder structure
- [x] Riverpod + go_router setup
- [ ] **ISSUE #1:** Conflicto deps `riverpod_generator` vs `custom_lint`
- [ ] **ISSUE #2:** Fix imports en `router.dart`
- [ ] **ISSUE #3:** Run `build_runner` para freezed
- [ ] **ISSUE #4:** Theme tokens de Erik integrados
- [ ] Login + Register screens (post-Erik)

### 🟠 Yang — Inteligencia
- [x] `INTEL_COMPETIDORES_2026.md`
- [x] 3 personas detalladas
- [x] 10 micro-influencers identificados LATAM
- [ ] Dossiers individuales de los 10 influencers
- [ ] Validar viabilidad 660K-1M MAU free con presupuesto marketing

### 🟤 Leo — Comercial
- [x] `PRICING_STRATEGY.md` (20 págs)
- [x] 3 tiers definidos con precios
- [x] GTM plan 14 semanas
- [ ] Outreach plan a 10 micro-influencers
- [ ] Sales deck + pitch para partnerships LATAM

### 🟡 Cinthya — Automation
- [ ] `AUTOMATION_WORKFLOWS.md` (8 workflows) — re-trigger pendiente
- [ ] Implementación n8n (post Sprint 1)

### ⚪ Alejo — Architecture
- [x] 5 ADRs firmados (001-005)
- [x] Auditoría plan maestro
- [ ] `COST_MODEL_PATH_A.md` recalc — re-trigger pendiente
- [ ] ADR-007 borrador (rate limiting agresivo)

### 🔴 Cyber Neo — Seguridad
- [ ] Audit Sprint 0.1 (post Antigravity entrega real)
- [ ] Audit RLS policies Sprint 0.2
- [ ] Audit endpoints Sprint 0.3
- [ ] Audit FULL pre-deploy Sprint 0.4

---

## ⚠️ ISSUES ABIERTOS

| # | Severidad | Descripción | Owner | Status |
|---|-----------|-------------|-------|--------|
| 1 | 🟢 Bajo | Brook 4 issues técnicos Flutter pendientes | Brook | Pendiente (no bloquea 0.3) |
| 2 | 🟢 Bajo | Cinthya workflows + Alejo cost model recalc | Cinthya, Alejo | Re-trigger pendiente |
| 3 | 🟡 Medio | Erik 5 mockups restantes (body, try-on, recos, profile, paywall) | Erik | Pendiente |
| 4 | 🟢 Bajo | UsageCounter.rpc() activar post Supabase remote migration | Antigravity | TODO en repos.py:L1 |
| 5 | 🟢 Bajo | commit_msg.txt residual + untracked files | Housekeeping | Pendiente |

---

## 🚦 ACCIONES PRÓXIMAS (en orden)

| # | Acción | Owner | Trigger |
|---|--------|-------|---------|
| 1 | **🔴 TRIGGER Antigravity Sprint 0.3** (prompt listo abajo) | Juan Camilo | AHORA |
| 2 | Audit Cyber Neo + Ego sobre 0.3 | Jarvis lanza | Cuando 0.3 reporte llegue |
| 3 | Trigger Antigravity Sprint 0.4 (DevOps) | Juan Camilo | Cuando 0.3 aprobado |
| 4 | Re-trigger Erik (5 mockups restantes) | Jarvis | Cuando rate limit resuelto |
| 5 | Re-trigger Brook (4 issues Flutter) | Jarvis | Post Erik mockups |
| 6 | Re-trigger Cinthya + Alejo | Jarvis | Cuando rate limit resuelto |
| 7 | Aplicar migrations 004+005 a Supabase remote | Juan Camilo (credenciales) | Post 0.3 |
| 8 | Junta Estratégica 16 mayo (reprogramada) | Todo el equipo | 16 mayo |

---

## 📅 HITOS PRÓXIMOS

| Fecha | Hito | Status |
|-------|------|--------|
| 2026-05-09 (sáb) | Junta Estratégica Sprint 0 review | 📅 Programada |
| 2026-05-12 (mar) | Sprint 0 cierre completo | 🎯 Target |
| 2026-05-19 | Sprint 1 cierre (Auth + Profile) | 🎯 Target |
| 2026-06-02 | Sprint 3 cierre (Body Analysis) — LÍNEA ROJA | 🚨 Crítico |
| 2026-06-09 | Sprint 4 cierre (Try-On core) — DEMO Junta | 🎯 Target |
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
| LTV/CAC | >3x | Manual sheet |
| Crash-free | >99.5% | Sentry |
| Cache hit rate | >35% | Custom metric |
| API latency p95 | <500ms | Sentry Performance |

---

## 📝 CHANGELOG (entradas más recientes primero)

### 2026-04-30 (sesión actual)
- Sprint 0.2 patch `ded674c` confirmado: 107 tests, 85.32% cov, 13 findings resueltos
- Tracker actualizado al estado real
- Sprint 0.3 prompt preparado por Jarvis — listo para trigger

### 2026-05-04
- Antigravity entregó Sprint 0.1 v1 con 3 issues (scratch dir, Supabase mock, no commit)
- Juan Camilo eligió Opción B → re-trigger Antigravity con instrucciones correctas
- Tracker creado para seguimiento

### 2026-05-02 (Sábado — Junta Estratégica simulada en docs)
- ADR-006 firmado (Path A: 50K paid puros, MRR $350-560K mes 12)
- 5 decisiones para Juan Camilo documentadas en agenda Junta

### 2026-04-30
- Master Prompt + SDR + Gantt entregados a Antigravity
- Decisión: Antigravity como ejecutor de código, agentes Claude como auditores

### 2026-04-29
- Leo entregó PRICING_STRATEGY.md (20 págs) — detectó discrepancia ARPU
- Juan Camilo confirmó Path A
- Yang entregó INTEL_COMPETIDORES_2026.md
- Erik entregó design system + 5 mockups
- Brook entregó Flutter scaffold (4 issues pendientes)
- Cinthya + Alejo hit rate limit antes de entregar

### 2026-04-25
- Plan Sprint 0 v1 redactado por Jarvis
- Sasha pausó pidiendo split en 4 entregas (Opción A) — APROBADO
- Alejo auditoría: 5 ADRs firmados (001-005), 7 riesgos detectados

---

## 🔗 DOCUMENTOS REFERENCIA

| Documento | Para qué |
|-----------|----------|
| `MASTER_PROMPT.md` | Contrato operativo Antigravity |
| `SDR.md` | Software Design Record completo |
| `MASTER_PLAN.md` | Plan Sprint 0 detallado |
| `GANTT_SPRINT_PLAN.md` | Cronograma 14 semanas |
| `PRICING_STRATEGY.md` | Pricing + GTM (Leo) |
| `INTEL_COMPETIDORES_2026.md` | Competitive intel (Yang) |
| `ADR-001..006.md` | Decisiones arquitectónicas firmadas |
| `JUNTA_SABADO_2026-05-02.md` | Agenda Junta Estratégica |
| `HANDOFF_PENDIENTES.md` | Issues técnicos pendientes |

---

**Tracker actualizado a:** 2026-05-04
**Próximo update:** Cuando Antigravity reporte Sprint 0.1 v2

> **Cómo usar este tracker:**
> 1. Revísalo cada vez que abras una sesión
> 2. Foco en "🎯 STATUS HOY" + "🚦 ACCIONES PRÓXIMAS"
> 3. Pídeme update cuando algo cambie
> 4. Yo lo actualizo automáticamente al cierre de cada entrega
