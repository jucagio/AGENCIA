# MASTER PLAN — Asesor de Imagen AI
## Plan de ejecución completo: De cero a launch en 14 semanas

**Owner:** Jarvis (CEO)
**Accionista:** Juan Camilo Gil
**Última actualización:** 2026-04-30
**Status:** Sprint 0 — Week 1 en curso

---

## TABLA DE CONTENIDOS

1. [Visión y producto](#1-visión-y-producto)
2. [Stack técnico y arquitectura](#2-stack-técnico-y-arquitectura)
3. [Equipo y responsabilidades](#3-equipo-y-responsabilidades)
4. [Decisiones arquitectónicas firmadas (ADRs)](#4-decisiones-arquitectónicas-firmadas)
5. [Modelo de negocio](#5-modelo-de-negocio)
6. [Roadmap 14 semanas — paso a paso](#6-roadmap-14-semanas)
7. [Sprint 0 — Foundation (Week 1)](#sprint-0)
8. [Sprint 1 — Auth & Profile (Week 2)](#sprint-1)
9. [Sprint 2 — Wardrobe Management (Week 3)](#sprint-2)
10. [Sprint 3 — Body Analysis (Week 4)](#sprint-3)
11. [Sprint 4 — Virtual Try-On (Week 5)](#sprint-4)
12. [Sprint 5 — AI Recommendations (Week 6)](#sprint-5)
13. [Sprint 6 — Subscriptions & Payments (Week 7)](#sprint-6)
14. [Sprint 7 — Storage & CDN (Week 8)](#sprint-7)
15. [Sprint 8 — Beta Cerrada (Week 9)](#sprint-8)
16. [Sprint 9 — Beta Pública (Week 10)](#sprint-9)
17. [Sprint 10 — Iteración (Week 11)](#sprint-10)
18. [Sprint 11 — Growth Features (Week 12)](#sprint-11)
19. [Sprint 12 — Marketing Push (Week 13)](#sprint-12)
20. [Sprint 13 — LAUNCH (Week 14)](#sprint-13)
21. [Post-launch (Month 4-12)](#post-launch)
22. [Métricas y KPIs](#métricas-y-kpis)
23. [Riesgos y mitigaciones](#riesgos-y-mitigaciones)
24. [Checklist global de ejecución](#checklist-global)

---

## 1. VISIÓN Y PRODUCTO

### El producto en una frase
**App móvil que permite a mujeres LATAM ver cómo se les vería un outfit antes de usarlo, recibir recomendaciones de combinaciones IA personalizadas según su tipo de cuerpo y temporada de color, y aprovechar al máximo el closet que ya tienen.**

### Propuesta de valor (3 promesas)
1. **Verte sin probarte** — virtual try-on fotorrealista en <5 segundos
2. **Vestirte mejor sin gastar más** — IA combina lo que ya tienes
3. **Conocerte estilísticamente** — análisis de cuerpo + color season + preferencias aprendidas

### Target user (3 personas core)
1. **María Profesional 28-35** — Bogotá/CDMX/Buenos Aires, ingreso mid-high, closet 80+ prendas, no sabe combinarlas, gasta tiempo deciendo qué ponerse
2. **Sofía Estudiante 22-26** — universitaria, ingreso bajo, closet 30 prendas, quiere maximizar look sin gastar, sigue trends en TikTok
3. **Ana Mamá 34-42** — recuperando identidad post-maternidad, body diversity, busca empoderamiento estilístico

### MVP scope (14 semanas)
- ✅ Autenticación + perfil
- ✅ Body analysis con foto (Google Vision)
- ✅ Wardrobe gallery (upload prendas)
- ✅ Virtual try-on (Replicate)
- ✅ Recomendaciones IA (Claude)
- ✅ Suscripciones (Stripe + Mercado Pago)
- ✅ Notificaciones push + email
- ✅ Iniciar tier free + Estilo (PRO)
- ⏭️ Tier Imagen (Premium) → sem 18 (post-launch)

### Out of scope MVP
- E-commerce integrado (compras dentro app)
- Stylist humano (sem 18+)
- Web app (mobile-first)
- Argentina pricing en ARS (sem 18)
- B2B partnerships (post-launch)

---

## 2. STACK TÉCNICO Y ARQUITECTURA

### Frontend
- **Flutter 3.41.5** + Dart 3.11.3
- **Riverpod 3.3** (state management)
- **go_router 17.2** (navigation)
- **supabase_flutter 2.12** (auth, realtime, storage)
- **dio 5.9** (HTTP client)
- **freezed 3.2** + json_serializable (models)
- **flutter_dotenv** (env vars)
- **cached_network_image** (image caching)
- **image_picker** (camera + gallery)

### Backend
- **FastAPI 0.115+** + Python 3.11
- **Pydantic v2.10**
- **supabase-py 2.x** (Supabase client)
- **httpx** (async HTTP)
- **arq** (Redis-based async tasks)
- **python-jose** (JWT validation)
- **bcrypt** (legacy, eliminar post-ADR-001)

### Database
- **PostgreSQL 16** (vía Supabase)
- **RLS** (Row-Level Security) en todas las tablas user-specific
- **pgvector** (Sprint 1+ para embeddings)
- **Supabase Auth** (auth.users, ADR-001)
- **Supabase Realtime** (websockets para try-on updates)
- **Supabase Storage** (uploads iniciales)

### IA externa
- **Google Vision API** — body analysis (color, body type, measurements)
- **Replicate** — virtual try-on (Stable Diffusion + IDM-VTON model)
- **Anthropic Claude** — recomendaciones outfit + style profile

### Infraestructura
- **Railway** — backend + worker ARQ (Sprint 0-9)
- **AWS ECS** — migración eventual @ 250K+ users
- **Cloudflare R2** — CDN + replication storage (egress $0)
- **Upstash Redis** — cache + ARQ queue
- **Sentry** — error tracking
- **PostHog** — product analytics

### Pagos
- **Stripe** — US + global
- **Mercado Pago** — LATAM (Colombia, México, Chile)

### Comunicación
- **Resend** — emails transaccionales
- **OneSignal** — push notifications
- **n8n** (Railway self-hosted) — workflow automation

### DevOps
- **GitHub** — repo + actions
- **GitHub Actions** — CI/CD (test, lint, build, deploy)
- **Docker** — containerization
- **Terraform** (post-launch) — IaC

### Observability
- **Sentry** — errors + performance
- **PostHog** — events + funnel
- **Railway logs** — structured JSON
- **OpenTelemetry** (post-launch) — distributed tracing

### Diagrama macro
```
┌─────────────┐
│  Flutter    │ iOS + Android
│  (Mobile)   │
└──────┬──────┘
       │ HTTPS
       ▼
┌─────────────────────────────────┐
│  FastAPI Backend (Railway)      │
│  ├─ Auth middleware (Supabase)  │
│  ├─ /auth, /users, /wardrobe    │
│  ├─ /body-analysis, /try-ons    │
│  └─ /recommendations            │
└──┬─────────────────┬────────────┘
   │                 │
   │ async tasks     │ direct queries
   ▼                 ▼
┌───────────┐  ┌──────────────────┐
│ ARQ Worker│  │ Supabase         │
│ (Redis)   │  │ ├─ Auth          │
│           │  │ ├─ PostgreSQL    │
│ Calls:    │  │ ├─ Realtime      │
│ Replicate │  │ └─ Storage       │
│ Claude    │  └──────────────────┘
│ Vision    │            │
└───────────┘            │
                         │ replicates to
                         ▼
                  ┌──────────────┐
                  │ Cloudflare R2│
                  │ (CDN)        │
                  └──────────────┘
```

---

## 3. EQUIPO Y RESPONSABILIDADES

### Dirección
- **Juan Camilo Gil** — Accionista, decisiones estratégicas, presupuesto
- **Jarvis** (Opus) — CEO, gestión de equipos, decisiones operacionales

### Ejecución técnica
- **Sasha** (Opus) — Backend & Security, FastAPI, APIs, OWASP
- **Brook** (Sonnet) — Frontend Flutter, BD client side, dashboards
- **Erik** (Sonnet) — Diseño UI/UX, design system, mockups, branding
- **Cinthya** (Sonnet) — Automation n8n, workflows, drip campaigns
- **Alejo** (Opus) — Solutions Architect, ADRs, cost optimization, escalabilidad

### Comercial
- **Leo** (Opus) — Pricing, GTM, partnerships, propuestas
- **Yang** (Sonnet) — Intel comercial, competitor analysis, personas

### Auditoría y mejora
- **Ego** (Opus) — Auditor supremo de proyectos y agentes
- **Cyber Neo** (Opus) — Auditor de seguridad técnica (OWASP, CVE, secrets)
- **Jade** (Sonnet) — Capacitación continua, intel de tendencias

### Quién reporta a quién
- Todos reportan a **Jarvis**
- **Jarvis** reporta a **Juan Camilo**
- **Cyber Neo** reporta a **Ego**
- **Ego** reporta a **Jarvis**

---

## 4. DECISIONES ARQUITECTÓNICAS FIRMADAS (ADRs)

### ADR-001: Supabase Auth nativo
- ❌ NO custom JWT con tabla `users` propia
- ✅ Usar `auth.users` de Supabase + tabla `profiles`
- ✅ FastAPI valida JWT con JWKS endpoint
- **Razón:** RLS funciona out-of-the-box, MFA/OAuth/magic links gratis

### ADR-002: Async-first para IA externa
- ✅ POST /try-ons devuelve 202 Accepted + try_on_id
- ✅ ARQ worker procesa async, Supabase Realtime push
- **Razón:** Replicate tarda 5-15s. Síncrono = backend cae a 5K users concurrentes.

### ADR-003: Idempotency-Key obligatoria
- ✅ Header `Idempotency-Key` (UUID v4) en POST /try-ons, /payments, /webhooks/*
- ✅ Tabla `idempotency_keys` con TTL 24h
- **Razón:** Evita doble cobro a usuarios. Pattern Stripe.

### ADR-004: Caching agresivo de try-ons
- ✅ Hash SHA256(body_image + wardrobe_item + replicate_model_version) → tabla `try_on_cache`
- ✅ TTL 90 días
- **Razón:** -35% costo Replicate. Sin esto el margen colapsa.

### ADR-005: Storage Supabase + CDN Cloudflare R2
- ✅ Upload a Supabase Storage (RLS sobre buckets)
- ✅ Replicación async a R2 (egress GRATIS)
- ✅ Servir vía R2 con signed URLs 1h
- **Razón:** Servir 5TB de imágenes desde Railway = caro. R2 = $0 egress.

### ADR-006: Path A — 50K paid users
- ✅ Target: 50K paid puros en mes 12
- ✅ MRR proyectado: $350-560K (mix LATAM/US)
- ✅ Margen bruto: 85%+ con caching agresivo
- **Razón:** Modelo realista vs "$60K MRR a 50K users" del plan inicial.

### ADR-007 (pendiente Alejo): Rate limiting agresivo
- 🟡 Free tier: 5 try-ons/mes hard cap
- 🟡 Recommendations: 10/día free, 50/día pro, ilimitado premium
- 🟡 API rate limit: 60 req/min user authenticated
- **Razón:** Sin esto, MAU free explota costos a >1M.

---

## 5. MODELO DE NEGOCIO

### Pricing (firmado por Leo + Juan Camilo)

| Tier | LATAM | US | Trial | Yearly |
|------|-------|-----|-------|--------|
| **Free** | $0 | $0 | — | — |
| **Estilo** (PRO) | $4.99/mo | $9.99/mo | 7 días sin tarjeta | -33% |
| **Imagen** (Premium) | $9.99/mo | $19.99/mo | 7 días | -33% |

### Features por tier

**Free:**
- 5 try-ons/mes
- 10 recomendaciones/día
- 30 prendas máximo en wardrobe
- 1 body analysis/mes
- Watermark en imágenes generadas
- Share a redes sociales (viralidad)

**Estilo (PRO):**
- Try-ons ilimitados (cap suave 50/mes)
- Recomendaciones premium (Claude detallado)
- Wardrobe ilimitado
- Body analysis ilimitado
- Color season completo
- Outfit planner semanal
- Sin watermarks
- Prioridad inference (<3s)

**Imagen (Premium):**
- Todo de Estilo +
- Stylist humano on-demand (1 sesión/mes)
- AI styling sessions custom
- Wardrobe analytics avanzado (cuánto ahorraste, ROI por prenda)
- Early access features
- Soporte 24/7

### Forecast oficial

| Mes | Paid | MRR | Notas |
|-----|------|-----|-------|
| 3 | 4,500 | $25K | post-launch beta-to-paid |
| 6 | 18,000 | $115K | influencer wave 1 |
| 12 | **50,000** | **$350-560K** | mix LATAM 70% / US 30% |

### Unit economics
- ARPU blend: $7-11.20/mo
- LTV (24 meses): $168-269
- CAC target: $20-40
- LTV/CAC: 4-7x (saludable, industry >3x)
- Payback period: 3-5 meses

---

## 6. ROADMAP 14 SEMANAS

```
SEMANA   FOCO                         ESTADO
═══════════════════════════════════════════════
1   ⏳ Sprint 0 — Foundation         🔵 EN CURSO
2   📋 Sprint 1 — Auth & Profile
3   📋 Sprint 2 — Wardrobe
4   📋 Sprint 3 — Body Analysis
5   📋 Sprint 4 — Virtual Try-On 🔥
6   📋 Sprint 5 — AI Recommendations
7   📋 Sprint 6 — Subscriptions
8   📋 Sprint 7 — Storage & CDN
9   📋 Sprint 8 — Beta Cerrada (50)
10  📋 Sprint 9 — Beta Pública (500)
11  📋 Sprint 10 — Iteración
12  📋 Sprint 11 — Growth Features
13  📋 Sprint 12 — Marketing Push
14  📋 Sprint 13 — LAUNCH 🚀
═══════════════════════════════════════════════
```

---

<a name="sprint-0"></a>
## SPRINT 0 — FOUNDATION (Week 1: Apr 27 - May 3)

### Objetivos
- Cimientos técnicos sólidos (DB schema, FastAPI scaffold, Flutter scaffold)
- Sistema de diseño aplicable
- Inteligencia comercial completa
- Estrategia de pricing fijada
- ADRs arquitectónicos firmados

### Tareas detalladas

#### Backend (Sasha) — Entrega 0.1 Foundation
- [ ] Auditar repo `asesor-imagen-ai/backend/` (qué hay vs qué dice plan)
- [ ] Fix `app/config.py` — añadir `get_settings()`, normalizar JWT names
- [ ] Fix `app/core/security.py` — adaptar a Supabase Auth (ADR-001)
- [ ] Fix `app/main.py` — incluir router v1, middleware, exception handlers, lifespan
- [ ] Crear `app/core/database.py` — Supabase client init
- [ ] Crear `app/core/middleware.py` — logging JSON estructurado
- [ ] Crear `app/core/exceptions.py` — Custom exceptions
- [ ] Crear `docs/DECISIONES_PENDIENTES.md` — issues encontrados

#### Backend (Sasha) — Entrega 0.2 Data Layer
- [ ] Migration `001_initial_schema.sql`:
  - [ ] Tabla `profiles` (no `users` con password_hash — ADR-001)
  - [ ] Tabla `wardrobe_items` con metadata JSONB
  - [ ] Tabla `body_analysis` con measurements + color season
  - [ ] Tabla `try_ons` con feedback signals
  - [ ] Tabla `recommendations`
  - [ ] Tabla `recommendation_items` (no UUID array — fix Alejo R2)
  - [ ] Tabla `subscriptions`
  - [ ] Tabla `user_style_profile`
  - [ ] Tabla `audit_log`
  - [ ] Tabla `idempotency_keys` (ADR-003)
  - [ ] Tabla `try_on_cache` (ADR-004)
  - [ ] Tabla `usage_counters` (rate limiting)
- [ ] RLS policies completas (32 policies = 8 tablas × 4 ops)
- [ ] Índices para performance
- [ ] Triggers updated_at
- [ ] Cyber Neo audit RLS antes de aplicar
- [ ] Models Pydantic v2 + SQLAlchemy
- [ ] Schemas request/response
- [ ] Repositories pattern (base + concretos)
- [ ] Tests data layer

#### Backend (Sasha) — Entrega 0.3 Services & Endpoints
- [ ] Auth service (validar JWT Supabase via JWKS)
- [ ] User service (CRUD profile)
- [ ] Wardrobe service (CRUD items + tag automatic via Vision)
- [ ] Vision service (Google Vision integration)
- [ ] Try-on service (Replicate integration con ARQ async)
- [ ] Recommendation service (Claude integration)
- [ ] 24+ endpoints REST
- [ ] OpenAPI spec auto-generado
- [ ] Idempotency middleware
- [ ] Rate limiting middleware
- [ ] Tests E2E (>80% coverage)

#### Backend (Sasha) — Entrega 0.4 DevOps & Hardening
- [ ] Dockerfile multi-stage
- [ ] `railway.json` config
- [ ] `.github/workflows/test.yml` — lint + test + coverage gate
- [ ] `.github/workflows/deploy.yml` — build + deploy Railway
- [ ] Sentry integration
- [ ] Structured logging (JSON)
- [ ] Cyber Neo audit final
- [ ] Smoke test post-deploy

#### Frontend (Brook)
- [x] Flutter project scaffold (Jarvis lo creó)
- [x] Clean Architecture folder structure
- [x] pubspec.yaml con deps 2026
- [x] main.dart + app.dart bootstrap
- [x] 9 screens stubbed
- [x] Theme light/dark placeholder
- [x] Routing con go_router
- [x] Dio client + interceptors
- [ ] **PENDIENTE:** Resolver issue conflicto deps riverpod_generator + custom_lint
- [ ] **PENDIENTE:** Fix imports incorrectos `router.dart` (`../shared/` → `../../shared/`)
- [ ] **PENDIENTE:** Run build_runner para freezed (failures.dart)
- [ ] **PENDIENTE:** Refactor router a Riverpod tradicional o resolver code gen
- [ ] CI workflow `flutter.yml`
- [ ] README setup local

#### Diseño (Erik)
- [x] Design system (paleta, tipografía, spacing, components)
- [x] design-tokens.json (Brook puede importar)
- [x] Mockup 01: Splash + Onboarding (3 screens)
- [x] Mockup 02: Auth (login + register)
- [x] Mockup 03: Home/Dashboard
- [x] Mockup 04: Wardrobe gallery
- [x] Mockup 05: Add wardrobe item
- [ ] **PENDIENTE:** Mockup 06: Body analysis upload + results
- [ ] **PENDIENTE:** Mockup 07: Virtual try-on (loading + result + feedback)
- [ ] **PENDIENTE:** Mockup 08: Recommendations
- [ ] **PENDIENTE:** Mockup 09: Profile / Settings
- [ ] **PENDIENTE:** Mockup 10: Subscription paywall
- [ ] Iconografía custom o Lucide
- [ ] Animaciones Lottie/Rive base

#### Intel (Yang)
- [x] INTEL_COMPETIDORES_2026.md (Stitch Fix, Acloset, Whering, Cladwell, Smart Closet)
- [x] 5 personas detalladas
- [x] 10 gaps de mercado
- [x] Top 10 micro-influencers LATAM identificados
- [ ] **PENDIENTE:** Validar 660K-1M MAU free viability con marketing budget
- [ ] **PENDIENTE:** Dossiers individuales 10 micro-influencers (warming sem 11)

#### Comercial (Leo)
- [x] PRICING_STRATEGY.md (20 págs)
- [x] 3 tiers definidos con precios LATAM/US
- [x] Conversion funnel + targets
- [x] 3 pitch tracks
- [x] Top 5 objeciones + respuestas
- [x] GTM plan 14 semanas
- [x] 5-10 partnerships propuestas
- [x] 5 banderas rojas identificadas
- [ ] **PENDIENTE:** Outreach plan a 10 micro-influencers (warming sem 11)

#### Architecture (Alejo)
- [x] Auditoría plan maestro (7 riesgos detectados)
- [x] 5 ADRs propuestos (001-005)
- [x] Cost projection inicial
- [ ] **PENDIENTE:** Recalc cost model con Path A (margen 85%+)
- [ ] **PENDIENTE:** Stress test 1M MAU free
- [ ] **PENDIENTE:** Borrador ADR-007 (rate limiting)

#### Automation (Cinthya)
- [ ] **PENDIENTE:** AUTOMATION_WORKFLOWS.md (8 workflows)
- [ ] **PENDIENTE:** Stack integraciones recomendado
- [ ] **PENDIENTE:** Webhook architecture
- [ ] **PENDIENTE:** KPIs por workflow

#### CEO (Jarvis)
- [x] Plan maestro v2 con ADRs
- [x] Gantt sprint plan paralelizado
- [x] HANDOFF_PENDIENTES.md
- [x] ADR-006 firmado
- [x] Agenda Junta Sábado
- [x] MASTER_PLAN.md (este documento)

### Demo del Sprint 0 (Junta Sábado)
- Flutter app levantando en simulador
- Theme aplicado
- Navegación entre screens stubbed
- Backend `/health` endpoint retorna 200
- Reporte: ADRs firmados, pricing fijado, intel completa

---

<a name="sprint-1"></a>
## SPRINT 1 — AUTH & PROFILE (Week 2: May 4-10)

### Objetivos
- Usuario puede registrarse, hacer login, completar onboarding
- Profile básico funcional
- Cerrar issues técnicos pendientes Sprint 0

### Backend (Sasha)
- [ ] Endpoint POST `/auth/register` (Supabase Auth signup)
- [ ] Endpoint POST `/auth/login` (Supabase Auth signin)
- [ ] Endpoint POST `/auth/refresh`
- [ ] Endpoint GET `/auth/me`
- [ ] Endpoint GET `/users/profile`
- [ ] Endpoint PUT `/users/profile`
- [ ] Endpoint DELETE `/users/account` (soft delete + GDPR)
- [ ] Tests E2E auth flow
- [ ] Rate limiting en auth endpoints
- [ ] OWASP audit auth

### Frontend (Brook)
- [ ] Resolver issues técnicos Sprint 0
- [ ] Splash screen funcional (auth state check)
- [ ] Onboarding flow (3 pantallas con animaciones)
- [ ] Login screen (email + Google + Apple)
- [ ] Register screen + validación
- [ ] Forgot password flow
- [ ] Profile screen (view + edit)
- [ ] Auth state listener Riverpod
- [ ] Persistent session (Supabase auto-handle)

### Diseño (Erik)
- [ ] Mockup 06: Body analysis (privacy-first design)
- [ ] Iconografía base (50 íconos Lucide o custom)
- [ ] Animaciones Lottie: splash, onboarding, success states
- [ ] Empty states (no wardrobe, no try-ons)
- [ ] Error states + loading skeletons

### Automation (Cinthya)
- [ ] Implementar Workflow 1 (Welcome onboarding) en n8n
- [ ] Setup Resend con email templates
- [ ] Setup OneSignal con push notif templates
- [ ] Test welcome flow end-to-end

### Auditoría
- [ ] Cyber Neo: audit auth (JWT validation, rate limit, OWASP A07)
- [ ] Ego: audit Sprint 1 deliverables vs plan

### Definition of Done
- [ ] Usuaria puede registrarse + login + ver perfil
- [ ] Tests pasando >80% coverage
- [ ] Welcome email + push llegan al usuario
- [ ] Demo funcional al final de la semana

---

<a name="sprint-2"></a>
## SPRINT 2 — WARDROBE MANAGEMENT (Week 3: May 11-17)

### Objetivos
- Usuario puede subir fotos de prendas, taggear automáticamente con Vision, organizar wardrobe

### Backend (Sasha)
- [ ] Endpoint POST `/wardrobe/items` (upload imagen + Vision auto-tag)
- [ ] Endpoint GET `/wardrobe/items` (lista paginada con filtros)
- [ ] Endpoint GET `/wardrobe/items/{id}`
- [ ] Endpoint PUT `/wardrobe/items/{id}` (edit tags)
- [ ] Endpoint DELETE `/wardrobe/items/{id}` (soft delete)
- [ ] Service Vision: detect color, style, occasion
- [ ] Image processing pipeline (resize, webp)
- [ ] Storage Supabase upload con RLS

### Frontend (Brook)
- [ ] Wardrobe gallery screen (grid responsive)
- [ ] Add wardrobe item (camera + gallery picker)
- [ ] Auto-tagging UI (mostrar lo que Vision detectó, editar)
- [ ] Filtros (color, style, occasion)
- [ ] Search wardrobe
- [ ] Item detail screen
- [ ] Bulk actions (delete múltiples)

### Diseño (Erik)
- [ ] Mockup 07: Virtual try-on screen detallado
- [ ] Empty state wardrobe ("Sube tu primera prenda")
- [ ] Tag chips design
- [ ] Filter UI patterns

### Auditoría
- [ ] Cyber Neo: audit storage RLS (no leak entre users)

### Definition of Done
- [ ] Usuaria sube foto, Vision la tagea, aparece en wardrobe
- [ ] Wardrobe persiste entre sesiones
- [ ] Filtros funcionan
- [ ] Tests cobertura >80%

---

<a name="sprint-3"></a>
## SPRINT 3 — BODY ANALYSIS (Week 4: May 18-24)

### Objetivos
- Usuario sube foto de cuerpo, sistema analiza tipo, color season, proporciones

### Backend (Sasha)
- [ ] Endpoint POST `/users/body-analysis` (upload foto, async procesamiento)
- [ ] Endpoint GET `/users/body-analysis` (último análisis)
- [ ] Endpoint GET `/users/body-analysis/history`
- [ ] Service body analysis (Vision API + custom logic):
  - Body type (apple, pear, hourglass, rectangle, inverted_triangle)
  - Skin tone category (warm/cool/neutral)
  - Color season (spring/summer/autumn/winter)
  - Best colors (array hex)
  - Avoid colors
- [ ] Privacy: imágenes encriptadas en R2, signed URLs 1h
- [ ] Endpoint DELETE `/users/body-analysis/{id}` (GDPR)

### Frontend (Brook)
- [ ] Body analysis upload screen (privacy-first UX)
- [ ] Result screen (visualización color season, body type)
- [ ] Privacy explainer (qué hacemos con la foto)
- [ ] Re-take photo flow
- [ ] History de análisis

### Diseño (Erik)
- [ ] Mockup 08: Recommendations screen
- [ ] Body analysis result viz (color palette, body type)
- [ ] Privacy modal de clase mundial (objeción #1 LATAM)
- [ ] Loading state mientras procesa (15-20s)

### Auditoría
- [ ] Cyber Neo: audit privacy de imágenes corporales
- [ ] Compliance: GDPR/LATAM data laws para PII corporal

### Hito comercial (Leo)
- 🔥 **Línea roja:** demo lado-a-lado vs Acloset al final del Sprint 3.
  Si quality try-on < Acloset → atrasar launch, replantar.

### Definition of Done
- [ ] Usuaria sube foto cuerpo, recibe análisis completo en <30s
- [ ] Privacy UX 5-star (testing con 3 betas previas)
- [ ] Imágenes encriptadas, no leak
- [ ] Tests cobertura >80%

---

<a name="sprint-4"></a>
## SPRINT 4 — VIRTUAL TRY-ON 🔥 (Week 5: May 25-31)

### Objetivos
- **Feature core del producto.** Usuaria pica prenda + cuerpo → ve resultado fotorrealista en <5s.

### Backend (Sasha)
- [ ] Endpoint POST `/try-ons` (async, devuelve 202 + try_on_id)
- [ ] Endpoint GET `/try-ons/{id}` (status + resultado si listo)
- [ ] Endpoint GET `/try-ons` (history paginado)
- [ ] Endpoint POST `/try-ons/{id}/feedback` (fit, color, would_buy)
- [ ] Idempotency middleware (ADR-003)
- [ ] Try-on service:
  - Hash lookup en `try_on_cache` (ADR-004)
  - Si miss: enqueue ARQ task → llama Replicate → guarda resultado + cache
  - Si hit: return cached
- [ ] ARQ worker setup (Upstash Redis)
- [ ] Supabase Realtime publish on try-on completed
- [ ] Quota enforcement (free 5/mes, pro ilimitado)
- [ ] Replicate webhooks fallback (si polling falla)

### Frontend (Brook)
- [ ] Try-on screen (selecciona prenda + body)
- [ ] Loading state (animation + estimated time)
- [ ] Realtime listener (Supabase WS) para resultado
- [ ] Result screen (zoom, share, save, retry)
- [ ] Feedback widget post try-on (5-star + cualitativo)
- [ ] Quota indicator (X/5 try-ons usados este mes)
- [ ] Quota exceeded → paywall modal

### Diseño (Erik)
- [ ] Mockup 09: Profile / Settings
- [ ] Try-on animations (Lottie celebración cuando aparece resultado)
- [ ] Share design (Stories format Instagram/TikTok)
- [ ] Quota visual (progress bar)

### Automation (Cinthya)
- [ ] Workflow 3 (Free tier limit warning)
- [ ] Push "Te quedan 2 try-ons este mes"
- [ ] Email descuento 20% upgrade

### Auditoría
- [ ] Cyber Neo: audit Replicate integration + idempotency
- [ ] Alejo: validar caching hit rate proyectado

### 🚨 Hito CRÍTICO Leo
- Demo de calidad try-on en sem 4 vs Acloset:
  - Si superior → green light continuar a Sprint 5
  - Si inferior → STOP. Re-evaluar Replicate model, prompt engineering.

### Definition of Done
- [ ] Try-on en <5s (cache hit) / <15s (cache miss)
- [ ] Quality SUPERIOR a Acloset (validación blind test 5 betas)
- [ ] Quota enforcement funcionando
- [ ] Realtime push funciona
- [ ] Tests cobertura >80%

---

<a name="sprint-5"></a>
## SPRINT 5 — AI RECOMMENDATIONS (Week 6: Jun 1-7)

### Objetivos
- Claude genera outfits personalizados según: body type, color season, wardrobe, ocasión

### Backend (Sasha)
- [ ] Endpoint GET `/recommendations?occasion=office&count=5`
- [ ] Endpoint POST `/recommendations/{id}/feedback` (liked/disliked)
- [ ] Endpoint GET `/users/style-profile` (learned preferences)
- [ ] Service recommendations:
  - Construir prompt con: body_analysis + recent try-ons (liked/disliked) + wardrobe items + occasion
  - Claude API call (con prompt cache)
  - Parse JSON response (outfit suggestions)
  - Guardar en `recommendations` + `recommendation_items`
- [ ] User style profile updater (cron diario):
  - Analiza try-ons feedback
  - Actualiza preferred_styles, preferred_colors, occasion_preferences
- [ ] A/B testing infra (claude_model_version)

### Frontend (Brook)
- [ ] Recommendations screen (cards de outfits)
- [ ] Outfit detail (qué prendas, por qué Claude recomendó)
- [ ] Like/dislike buttons (training signal)
- [ ] Filtro por ocasión (office, casual, date, gym)
- [ ] "Try this outfit" → enqueues múltiples try-ons

### Diseño (Erik)
- [ ] Mockup 10: Subscription paywall (mejor versión del producto)
- [ ] Outfit card design (premium feel)
- [ ] Reasoning display ("Por qué Claude recomendó")

### Definition of Done
- [ ] Recomendaciones aparecen en <2s
- [ ] Cada outfit tiene reasoning visible
- [ ] Feedback se guarda y mejora siguientes recos
- [ ] Style profile se actualiza diariamente

---

<a name="sprint-6"></a>
## SPRINT 6 — SUBSCRIPTIONS & PAYMENTS (Week 7: Jun 8-14)

### Objetivos
- Monetización funcionando end-to-end. Usuaria upgrade → cobro → features unlock.

### Backend (Sasha)
- [ ] Stripe integration:
  - [ ] POST `/subscriptions/checkout-session` (Stripe Checkout)
  - [ ] POST `/webhooks/stripe` (idempotente)
  - [ ] GET `/subscriptions/me`
  - [ ] POST `/subscriptions/cancel`
  - [ ] POST `/subscriptions/resume`
- [ ] Mercado Pago integration (LATAM):
  - [ ] POST `/subscriptions/mp-checkout`
  - [ ] POST `/webhooks/mercadopago`
- [ ] Trial management (7 días sin tarjeta)
- [ ] Quota service (usage_counters):
  - Increment en cada try-on / recommendation
  - Reset mensual cron
- [ ] Service plan_features (qué unlock cada tier)
- [ ] Tax handling (IVA Colombia 19%, México 16%)

### Frontend (Brook)
- [ ] Paywall screen (con mockup Erik)
- [ ] Subscription management screen
- [ ] Upgrade flow (Free → Estilo)
- [ ] Cancel flow + win-back offer
- [ ] Receipt viewer
- [ ] Quota indicators globales

### Diseño (Erik)
- [ ] Pricing page mobile (Apple-grade)
- [ ] Upgrade flow micro-interactions
- [ ] Success states post-upgrade

### Automation (Cinthya)
- [ ] Workflow 4 (Trial expiration nudge)
- [ ] Workflow 5 (Failed payment / Dunning)
- [ ] Welcome PRO post-upgrade

### Auditoría
- [ ] Cyber Neo: audit payments (PCI compliance, no leak credit cards)
- [ ] Tests E2E: register → trial → upgrade → cobro → unlock features

### Definition of Done
- [ ] Usuaria puede pagar Estilo $4.99 LATAM con tarjeta
- [ ] Cobro automático mensual
- [ ] Cancel funciona
- [ ] Webhooks idempotentes
- [ ] Receipts emitidos

---

<a name="sprint-7"></a>
## SPRINT 7 — STORAGE & CDN (Week 8: Jun 15-21)

### Objetivos
- Imágenes servidas vía CDN, performance global, costos optimizados

### Backend (Sasha)
- [ ] Cloudflare R2 setup (bucket, API keys)
- [ ] Service replicación Supabase → R2 (async worker)
- [ ] Signed URLs con 1h expiration
- [ ] Image transforms on-the-fly (resize, webp)
- [ ] Migration de imágenes existentes (one-time)
- [ ] Cleanup script (orphan images)

### Frontend (Brook)
- [ ] Update image URLs a CDN R2
- [ ] cached_network_image con LRU policy
- [ ] Image quality selector (data saver mode)
- [ ] Offline mode básico (wardrobe en cache local)

### Performance
- [ ] Sasha: Database query optimization (EXPLAIN ANALYZE top 10 queries)
- [ ] Sasha: Connection pooling tuning
- [ ] Sasha: Redis caching layer para queries frecuentes
- [ ] Brook: Bundle size analysis Flutter
- [ ] Brook: Lazy loading screens

### Auditoría
- [ ] Cyber Neo: audit R2 access (no public buckets, no leak)
- [ ] Alejo: validar costos R2 vs proyección

### Definition of Done
- [ ] Imágenes cargan <500ms globalmente
- [ ] Costos storage bajados >30% vs Supabase only
- [ ] Tests carga: 100 usuarios concurrentes sin caída

---

<a name="sprint-8"></a>
## SPRINT 8 — BETA CERRADA (Week 9: Jun 22-28)

### Objetivos
- 50 usuarias reales probando, recopilar feedback, fix bugs críticos

### Comercial (Leo + Yang)
- [ ] Reclutar 50 betas (TikTok + Discord privado)
- [ ] Onboarding individual (call de 15 min con cada beta)
- [ ] Feedback survey diaria
- [ ] Bug report channel Discord
- [ ] NPS tracking semanal

### Backend (Sasha)
- [ ] Hot fixes según feedback betas
- [ ] Performance tuning
- [ ] Analytics events (PostHog) extensivos

### Frontend (Brook)
- [ ] UX polish según feedback
- [ ] Animations refinement
- [ ] Accessibility audit (WCAG AA)

### Diseño (Erik)
- [ ] Iteración mockups según feedback
- [ ] Onboarding video (60s)

### Automation (Cinthya)
- [ ] Workflow 6 (Weekly digest)
- [ ] In-app feedback form

### Definition of Done
- [ ] NPS >40 entre betas
- [ ] 0 bugs críticos abiertos
- [ ] >70% retention día 7
- [ ] >50% completaron primer try-on

---

<a name="sprint-9"></a>
## SPRINT 9 — BETA PÚBLICA (Week 10: Jun 29 - Jul 5)

### Objetivos
- 500 usuarias en beta abierta, validar product-market fit

### Comercial
- [ ] Lanzar landing page con waitlist
- [ ] Influencer outreach (3-5 micro-LATAM)
- [ ] Beta access codes (limitar 500)
- [ ] Conversion tracking (signup → activation)

### Backend (Sasha)
- [ ] Load testing (k6: 1K req/min sustained)
- [ ] Circuit breakers (Replicate down, Vision down)
- [ ] Graceful degradation
- [ ] Backup automatizado (Supabase)

### Frontend (Brook)
- [ ] App Store / Play Store assets (screenshots, descriptions)
- [ ] Submission a TestFlight + Play Console internal track

### Auditoría
- [ ] Cyber Neo: full audit pre-public
- [ ] Ego: audit deliverables vs plan

### Definition of Done
- [ ] App estable con 500 usuarias concurrentes
- [ ] Conversión waitlist → signup >30%
- [ ] Activation rate (first try-on) >60%

---

<a name="sprint-10"></a>
## SPRINT 10 — ITERACIÓN (Week 11: Jul 6-12)

### Objetivos
- Pulir todo basado en data real, preparar para launch

### Equipo completo
- [ ] Daily standup feedback review
- [ ] Top 10 issues priorizados → fix
- [ ] A/B tests:
  - [ ] Paywall copy (3 variants)
  - [ ] Onboarding length (3 vs 5 screens)
  - [ ] Recommendations format (cards vs list)
- [ ] Performance budget: app <5MB initial download
- [ ] Crash-free rate >99.5%

### Comercial (Leo)
- [ ] Pricing test (¿$4.99 vs $5.99 LATAM?)
- [ ] Trial length test (7 vs 14 días)

### Definition of Done
- [ ] Top 10 issues resueltos
- [ ] A/B tests con winner identificado
- [ ] Crash-free >99.5%

---

<a name="sprint-11"></a>
## SPRINT 11 — GROWTH FEATURES (Week 12: Jul 13-19)

### Objetivos
- Features que aceleran retención + viralidad

### Backend (Sasha)
- [ ] Referral system (códigos únicos, tracking)
- [ ] Push notif personalizadas (best time to send)
- [ ] In-app messaging (segmented)

### Frontend (Brook)
- [ ] Referral screen (compartir código, ver invitados)
- [ ] Notification preferences
- [ ] Stories share (Instagram/TikTok format con watermark)

### Diseño (Erik)
- [ ] Marketing assets (App Store, social media)
- [ ] Press kit (logo variants, screenshots, video)

### Automation (Cinthya)
- [ ] Workflow 7 (Win-back churned users)
- [ ] Workflow 8 (Referral program)

### Comercial (Leo + Yang)
- [ ] Outreach: 10 micro-influencers LATAM (warming → contracts)
- [ ] Beta-tester referral kit (códigos para amigas)

### Definition of Done
- [ ] Referral system funciona end-to-end
- [ ] Stories share con watermark
- [ ] 10 influencers con contrato firmado

---

<a name="sprint-12"></a>
## SPRINT 12 — MARKETING PUSH (Week 13: Jul 20-26)

### Objetivos
- Awareness pre-launch, build hype

### Comercial (Leo)
- [ ] Press release distribuido (medios LATAM tech + fashion)
- [ ] 10 influencers publican contenido teaser
- [ ] Landing page final con countdown
- [ ] Waitlist > 5K antes de launch
- [ ] Beta testimonials capturados (video, texto)

### Diseño (Erik)
- [ ] Banner social media campaña
- [ ] Video promocional 30s (TikTok/Reels)
- [ ] Email banner Resend

### Backend (Sasha)
- [ ] Production deploy con feature flags off
- [ ] Smoke tests automatizados
- [ ] On-call rotation definida

### Auditoría
- [ ] Cyber Neo: full audit pre-launch
- [ ] Ego: validation final entregables vs plan

### Definition of Done
- [ ] Waitlist >5K
- [ ] 10 influencers listos para amplificar
- [ ] Press release publicado en 5+ medios

---

<a name="sprint-13"></a>
## SPRINT 13 — LAUNCH 🚀 (Week 14: Jul 27 - Aug 2)

### Día por día

#### Lunes Jul 27 — Final QA
- Sasha + Cyber Neo: audit final
- Brook: smoke test app stores
- Alejo: review final infra

#### Martes Jul 28 — Production Deploy
- Sasha: deploy backend a Railway prod
- Smoke tests post-deploy
- Monitoring activo

#### Miércoles Jul 29 — App Stores Submit
- Brook: submit a App Store + Play Store
- Esperar review (24-48h)

#### Jueves Jul 30 — Influencer Day
- 10 influencers LATAM publican contenido (TikTok + Instagram)
- Coordinated push 6 PM hora LATAM

#### Viernes Jul 31 — LAUNCH 🚀
- App Store + Play Store live
- Press release amplificado
- Social media blitz
- Email a waitlist (5K+)

#### Sábado Ago 1 — Monitor
- Equipo on-call 24/7
- Dashboard métricas en vivo
- Hot fixes si necesario

#### Domingo Ago 2 — Retro
- Junta retro launch
- Lecciones aprendidas
- Plan Sprint 14+

### Métricas día de launch
- [ ] Downloads día 1: >1,000
- [ ] Signups día 1: >500
- [ ] First try-on completado: >250
- [ ] Crash-free: >99%
- [ ] Mentions sociales: >100

---

<a name="post-launch"></a>
## POST-LAUNCH (Mes 4-12)

### Mes 4 (Aug)
- Iteration sobre data real launch
- Lanzar tier Imagen ($9.99 LATAM / $19.99 US)
- Argentina entry (ARS pricing)
- 10K paid target

### Mes 5-6 (Sep-Oct)
- Influencer wave 2 (20+ micro-influencers)
- B2B outreach (Falabella, MercadoLibre Fashion)
- Stylist humano feature (Imagen tier)
- 18K paid target

### Mes 7-9 (Nov-Jan)
- Holiday season campaign
- Referral viral mechanics
- API access para influencers
- 30K paid target

### Mes 10-12 (Feb-Apr)
- Web app companion
- Wardrobe analytics deep
- Brand partnerships (try-on de marcas reales)
- **50K paid target — meta cumplida**

---

## MÉTRICAS Y KPIs

### North Star Metric
**Active Subscribers** (paid users que abrieron app últimos 30 días)

### Métricas operacionales (semanales)

#### Producto
- DAU / MAU
- Retention día 1, 7, 30
- Try-ons por usuaria
- Recomendaciones liked/disliked
- NPS score

#### Comercial
- Signups (free)
- Trial starts
- Trial → paid conversion
- Churn rate
- LTV
- CAC
- LTV/CAC ratio
- MRR / ARR

#### Técnico
- Latencia p95 endpoints
- Error rate
- Crash-free rate
- Uptime SLA (target 99.5%)
- Cache hit rate try-ons (target 35%+)
- Costo Replicate / paid user

### Dashboards
- **Tablero CEO** — North Star + financieros
- **Tablero Producto** — engagement + retention
- **Tablero Técnico** — latencia, errors, costos

---

## RIESGOS Y MITIGACIONES

### 1. Calidad try-on inferior a Acloset
- **Probabilidad:** Media
- **Impacto:** Crítico (mata el producto)
- **Mitigación:** Línea roja sem 4 → atrasar launch si necesario, prompt engineering, considerar Replicate model alternativo

### 2. MAU free explota costos
- **Probabilidad:** Alta si viralizamos
- **Impacto:** Alto (margen colapsa)
- **Mitigación:** ADR-007 rate limiting agresivo, caching ADR-004, watermark + cap try-ons gratis

### 3. Privacy concern fotos corporales
- **Probabilidad:** Alta (LATAM objeción #1)
- **Impacto:** Medio (frena adopción)
- **Mitigación:** Privacy de clase mundial, encriptación, "delete anytime", Erik diseño explícito

### 4. Conversión free→paid < 5%
- **Probabilidad:** Media
- **Impacto:** Alto (hit target)
- **Mitigación:** A/B test paywalls, value clear, free cap agresivo, dunning workflows Cinthya

### 5. Replicate downtime
- **Probabilidad:** Baja
- **Impacto:** Crítico (feature core caído)
- **Mitigación:** Circuit breaker, fallback a "queued for later", multi-provider eventual

### 6. Stripe / Mercado Pago compliance LATAM
- **Probabilidad:** Media
- **Impacto:** Medio (delays)
- **Mitigación:** Setup temprano (sem 6), legal advisor, tax handling correcto

### 7. Influencer flop
- **Probabilidad:** Media
- **Impacto:** Medio (revenue mes 1-3 abajo)
- **Mitigación:** 10 micro vs 1 macro (diversificar), contracts performance-based

### 8. Argentina ARS volatility
- **Probabilidad:** Alta
- **Impacto:** Bajo (entrada postpuesta a sem 18)
- **Mitigación:** Pricing ARS revisión trimestral, monetización vía cohorts US emigrados

---

## CHECKLIST GLOBAL

### Pre-launch (Sem 1-13)
- [ ] Sprint 0: Foundation
- [ ] Sprint 1: Auth
- [ ] Sprint 2: Wardrobe
- [ ] Sprint 3: Body Analysis
- [ ] Sprint 4: Try-On 🔥 (línea roja)
- [ ] Sprint 5: AI Recos
- [ ] Sprint 6: Payments
- [ ] Sprint 7: Storage/CDN
- [ ] Sprint 8: Beta cerrada (50)
- [ ] Sprint 9: Beta pública (500)
- [ ] Sprint 10: Iteración
- [ ] Sprint 11: Growth features
- [ ] Sprint 12: Marketing push
- [ ] Sprint 13: LAUNCH 🚀

### Documentación crítica
- [x] MASTER_PLAN.md (este doc)
- [x] ADR-001 a ADR-005 (Alejo)
- [x] ADR-006 (Path A revenue)
- [ ] ADR-007 (rate limiting — Alejo pendiente)
- [x] PRICING_STRATEGY.md (Leo)
- [x] INTEL_COMPETIDORES_2026.md (Yang)
- [x] design-system/ (Erik)
- [x] GANTT_SPRINT_PLAN.md (Jarvis)
- [x] HANDOFF_PENDIENTES.md (Jarvis)
- [ ] AUTOMATION_WORKFLOWS.md (Cinthya pendiente)
- [ ] COST_MODEL_PATH_A.md (Alejo pendiente)
- [x] JUNTA_SABADO_2026-05-02.md (agenda)

### ADRs firmados
- [x] ADR-001 Supabase Auth
- [x] ADR-002 Async-first
- [x] ADR-003 Idempotency-Key
- [x] ADR-004 Try-on caching
- [x] ADR-005 R2 CDN
- [x] ADR-006 Path A
- [ ] ADR-007 Rate limiting (pendiente)

### Auditorías
- [ ] Cyber Neo Sprint 1
- [ ] Cyber Neo Sprint 4 (try-on critical)
- [ ] Cyber Neo Sprint 6 (payments critical)
- [ ] Cyber Neo Sprint 9 (pre-public)
- [ ] Cyber Neo Sprint 12 (pre-launch full)
- [ ] Ego audits trimestrales

### Decisiones pendientes para Juan Camilo
- [ ] Confirmar presupuesto marketing (Yang propondrá)
- [ ] Hiring Arquitecto Senior (¿aún urgente?)
- [ ] Beta cerrada: 50 usuarias TikTok? Discord?
- [ ] Línea roja launch (atrasar si try-on < Acloset)
- [ ] Partnerships LATAM (Falabella, MercadoLibre)
- [ ] Equity / pool agentes

---

## SIGUIENTE ACCIÓN (HOY 2026-04-30)

### 4:10 PM — Reset Alejo + Cinthya
- Relanzar Alejo: cost model Path A
- Relanzar Cinthya: 8 workflows automation

### Resto del día / mañana
- Sasha (cuando vuelva): Entrega 0.1 Foundation
- Brook: cerrar issues técnicos
- Erik: 5 mockups restantes

### Sábado 2026-05-02 — JUNTA
- Review consolidado
- Decisiones pendientes
- Confirmar Sprint 1 assignments

---

**Plan vivo. Actualizar cada sábado en Junta.**

**Owner:** Jarvis
**Backup owner:** Juan Camilo
