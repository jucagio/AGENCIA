# GANTT MAESTRO — Asesor de Imagen AI
## MVP 14 Semanas | Paralelización Optimizada

**Owner:** Jarvis (CEO)  
**Última actualización:** 2026-04-25  
**Filosofía:** Maximizar trabajo paralelo. Bloqueos solo en dependencias técnicas reales.

---

## LEYENDA

```
🟢 = Sasha (Backend)
🔵 = Brook (Frontend Flutter)
🟣 = Erik (Diseño UI/UX)
🟡 = Cinthya (Automatización)
🔴 = Cyber Neo (Seguridad)
⚪ = Alejo (Arquitectura on-call)
🟠 = Yang (Inteligencia)
🟤 = Leo (Comercial)
⬛ = Jade (Capacitación)

█ = En ejecución
░ = Espera
▓ = Bloqueado por dependencia
✓ = Completado
```

---

## SPRINT 0 — WEEK 1: FOUNDATION (Día 1-7)

### Vista Día por Día (paralelización máxima)

```
Día:                    1    2    3    4    5    6    7
═══════════════════════════════════════════════════════
🟢 Sasha 0.1 Foundation █████░░░░░░░░░░░░░░░░░░░░░░░░░░  (en curso)
🟢 Sasha 0.2 Data Layer ░░░░░██████████░░░░░░░░░░░░░░░░
🟢 Sasha 0.3 Endpoints  ░░░░░░░░░░░░░░░██████████░░░░░░
🟢 Sasha 0.4 DevOps     ░░░░░░░░░░░░░░░░░░░░░░░░░░██████

🔴 Cyber Neo audit RLS  ░░░░░░░░░░░░██████░░░░░░░░░░░░░  ← Antes de migration
🔴 Cyber Neo audit code ░░░░░░░░░░░░░░░░░░░░░░░░░░░░██░  ← Pre-deploy

⚪ Alejo on-call        ░░█░█░░░█░░░░░█░░░░░█░░░░░░░░█░  ← Decisiones bloqueantes

🟣 Erik UI System       ████████████████░░░░░░░░░░░░░░░  ← PARALELO total
🟣 Erik Mockups core    ░░░░██████████████████████░░░░░  ← screens MVP
🟣 Erik Try-On UX       ░░░░░░░░░░░░░░░░░░░██████████░░  ← spec con Brook

🔵 Brook Flutter setup  ████████░░░░░░░░░░░░░░░░░░░░░░░  ← PARALELO Sasha
🔵 Brook Auth screens   ░░░░░░░░██████████░░░░░░░░░░░░░  ← post-Erik mockups
🔵 Brook Wardrobe UI    ░░░░░░░░░░░░░░░░░░██████████░░░  ← post-Sasha 0.3

🟠 Yang Market Research ████████████░░░░░░░░░░░░░░░░░░░  ← PARALELO total
🟠 Yang Competitor Intel░░░░░░░░░░░░██████░░░░░░░░░░░░░  ← pricing/features

🟡 Cinthya Workflows    ░░░░░░░░░░░░░░░░░░░░░░██████░░░  ← post-endpoints

⬛ Jade Capacita Sasha  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  ← Supabase Auth nativo
⬛ Jade Capacita Brook  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░██░  ← Supabase Realtime

🟤 Leo Pricing strategy ░░░░░░░░░░██████████░░░░░░░░░░░  ← con Yang intel
═══════════════════════════════════════════════════════
```

### Dependencias críticas (NO se pueden saltar)

```
Sasha 0.1 ──→ Sasha 0.2 (necesita config + core modules)
Sasha 0.2 ──→ Cyber Neo audit RLS (antes de aplicar migration)
Sasha 0.2 ──→ Sasha 0.3 (necesita schema)
Sasha 0.3 ──→ Brook Wardrobe UI (Brook necesita endpoints reales)
Sasha 0.3 ──→ Cinthya Workflows (necesita webhooks)
Sasha 0.4 ──→ Cyber Neo audit code (pre-deploy)

Erik UI System ──→ Brook Auth screens (necesita design tokens)
Erik Mockups ──→ Brook Wardrobe UI

Yang Market Research ──→ Leo Pricing strategy
```

### Trabajos PARALELIZABLES desde Día 1 (no esperan a nadie)

✅ **Erik** — Sistema de diseño + mockups (no necesita backend)  
✅ **Brook** — Flutter project setup, navegación base, state management config  
✅ **Yang** — Market research, competitor analysis (Glamoutfit, Stitch Fix, Acloset)  
✅ **Jade** — Capacitar a Sasha en Supabase Auth nativo (ADR-001)  

---

## SPRINT 1-2 — WEEK 2-3: AUTH + CORE EXPERIENCE

```
Semana:                 2         3
═════════════════════════════════════════
🟢 Auth + Profile       ████████░░░░░░░░░
🟢 Wardrobe CRUD        ░░░░░░░░████████░
🟢 Body Analysis API    ░░░░░░░░░░██████░  ← Google Vision integration

🔵 Login/Register UI    ████████░░░░░░░░░  ← post-Erik
🔵 Onboarding flow      ░░░░████████░░░░░
🔵 Wardrobe gallery     ░░░░░░░░████████░

🟣 Onboarding mockups   ████████░░░░░░░░░
🟣 Wardrobe mockups     ░░░░████████░░░░░
🟣 Body Analysis UX     ░░░░░░░░████████░

🟡 Welcome email auto   ░░░░░░░░██████░░░  ← post-auth
🟡 Webhook Stripe setup ░░░░░░░░░░░░██████

🟠 User personas        ████░░░░░░░░░░░░░  ← marketing
🟤 Landing page copy    ░░░░████████░░░░░  ← con Yang
═════════════════════════════════════════
```

---

## SPRINT 3-4 — WEEK 4-5: VIRTUAL TRY-ON

```
Semana:                 4         5
═════════════════════════════════════════
🟢 Replicate integ      ████████░░░░░░░░░
🟢 ARQ worker async     ████████░░░░░░░░░  ← ADR-002
🟢 Idempotency-Key      ░░░░████░░░░░░░░░  ← ADR-003
🟢 Try-on cache (hash)  ░░░░░░░░████████░  ← ADR-004
🟢 Try-on feedback API  ░░░░░░░░░░██████░

🔴 Cyber Neo audit      ░░░░░░░░░░░░██████  ← async + idempotency

🔵 Try-on screen        ████████████░░░░░  ← UX clave
🔵 Realtime updates     ░░░░░░░░████████░  ← Supabase WS
🔵 Feedback widget      ░░░░░░░░░░██████░

🟣 Try-on animations    ████████░░░░░░░░░  ← Lottie/Rive
🟣 Result share design  ░░░░████████░░░░░

🟡 Notif push setup     ░░░░░░░░░░░░██████
═════════════════════════════════════════
```

---

## SPRINT 5-6 — WEEK 6-7: AI RECOMMENDATIONS + STORAGE

```
Semana:                 6         7
═════════════════════════════════════════
🟢 Claude integration   ████████░░░░░░░░░  ← prompt engineering
🟢 User Style Profile   ░░░░████████░░░░░  ← learning loop
🟢 Recos endpoint       ░░░░░░░░████████░
🟢 Cloudflare R2 setup  ████████░░░░░░░░░  ← ADR-005
🟢 Image pipeline       ░░░░████████░░░░░  ← resize, webp

🔵 Recos screen         ░░░░░░██████████░
🔵 Outfit builder UI    ░░░░░░░░░░██████░

🟣 Recos card design    ████████░░░░░░░░░
🟣 Outfit composition   ░░░░████████░░░░░

🟠 Influencer outreach  ░░░░░░░░░░██████░  ← pre-launch
🟤 Beta tester recruit  ░░░░░░░░░░██████░
═════════════════════════════════════════
```

---

## SPRINT 7-8 — WEEK 8-9: PAYMENTS + SUBSCRIPTIONS

```
Semana:                 8         9
═════════════════════════════════════════
🟢 Stripe Checkout      ████████░░░░░░░░░
🟢 Webhook handlers     ░░░░████████░░░░░  ← idempotente
🟢 Usage counters       ░░░░░░░░████████░  ← quota enforcement
🟢 Mercado Pago         ░░░░░░░░░░██████░  ← LATAM

🔴 Cyber Neo audit      ░░░░░░░░░░░░██████  ← payments = crítico

🔵 Paywall UI           ████████░░░░░░░░░
🔵 Subscription mgmt    ░░░░████████░░░░░
🔵 Quota indicators     ░░░░░░░░██████░░░

🟣 Pricing page         ████████░░░░░░░░░
🟣 Upgrade flows        ░░░░████████░░░░░

🟡 Dunning emails       ░░░░░░░░██████░░░  ← failed payments
🟡 Cancel surveys       ░░░░░░░░░░██████░
═════════════════════════════════════════
```

---

## SPRINT 9-10 — WEEK 10-11: BETA + ITERATION

```
Semana:                10        11
═════════════════════════════════════════
🟢 Bug fixes + polish   ████████████████░
🟢 Performance tuning   ░░░░████████████░
🟢 Analytics events     ░░░░░░░░████████░  ← Mixpanel/PostHog

🔵 UX polish            ████████████████░
🔵 Animations           ░░░░████████████░
🔵 Accessibility        ░░░░░░░░████████░  ← WCAG AA

🟠 Beta tester feedback ████████████████░  ← daily standups
🟤 Sales pipeline       ░░░░████████████░  ← B2B partnerships

🟡 Auto reports beta    ░░░░░░░░████████░
═════════════════════════════════════════
```

---

## SPRINT 11-12 — WEEK 12-13: GROWTH + OPTIMIZATION

```
Semana:                12        13
═════════════════════════════════════════
🟢 A/B testing infra    ████████░░░░░░░░░
🟢 Referral system      ░░░░████████░░░░░
🟢 Push notifications   ░░░░░░░░████████░

🔵 Referral UI          ░░░░████████░░░░░
🔵 Notifications UI     ░░░░░░░░████████░

🟣 Marketing assets     ████████████████░  ← App Store, social

🟠 Influencer launch    ░░░░████████████░  ← pre-launch buzz
🟤 Press kit            ████████░░░░░░░░░
🟤 Launch partnerships  ░░░░░░░░████████░

🟡 Drip campaigns       ████████████░░░░░
═════════════════════════════════════════
```

---

## SPRINT 13 — WEEK 14: LAUNCH

```
Día:                    1    2    3    4    5    6    7
═══════════════════════════════════════════════════════
🟢 Final QA + hotfix    ████████░░░░░░░░░░░░░░░░░░░░░░░
🔴 Cyber Neo full audit ████████░░░░░░░░░░░░░░░░░░░░░░░  ← BLOCK
⚪ Alejo final review   ████░░░░░░░░░░░░░░░░░░░░░░░░░░░  ← BLOCK
🟢 Production deploy    ░░░░░░░░██░░░░░░░░░░░░░░░░░░░░░  ← T-day -3
🔵 App Store submission ░░░░░░░░░░██████░░░░░░░░░░░░░░░  ← review wait
🟤 PR launch            ░░░░░░░░░░░░░░░░░░██████████░░░  ← LAUNCH 🚀
🟠 Monitor + react      ░░░░░░░░░░░░░░░░░░██████████████
═══════════════════════════════════════════════════════
```

---

## RESUMEN: TRABAJOS PARALELOS DESDE DÍA 1

### Hoy (mientras Sasha hace 0.1) puedes activar:

| Agente | Tarea esta semana | No depende de |
|--------|-------------------|---------------|
| 🟣 **Erik** | Sistema de diseño completo (colores, tipografía, componentes, tokens) | Nadie |
| 🟣 **Erik** | Mockups: Login, Register, Onboarding, Home, Wardrobe gallery | Nadie |
| 🔵 **Brook** | Flutter project setup, routing, state management (Riverpod), folder structure | Nadie |
| 🔵 **Brook** | Connect a Supabase Auth client side (parallel a Sasha) | Nadie |
| 🟠 **Yang** | Competitor analysis: Stitch Fix, Acloset, Glamoutfit, Whering | Nadie |
| 🟠 **Yang** | User personas + JTBD interviews | Nadie |
| 🟤 **Leo** | Definir pricing strategy + tier features | Yang research |
| 🟡 **Cinthya** | Diseñar workflows: welcome email, abandoned wardrobe, weekly digest | Endpoints (post 0.3) |
| ⬛ **Jade** | Capacitar a Sasha en Supabase Auth nativo + RLS patterns | Nadie |

### Bloqueos reales (NO paralelizables)

```
Sasha 0.2 (migration SQL) ──BLOQUEA──→ Brook (necesita schema para typed clients)
Sasha 0.3 (endpoints) ──BLOQUEA──→ Cinthya workflows (necesita webhooks)
Erik mockups ──BLOQUEA──→ Brook screens (necesita design specs)
Cyber Neo audit ──BLOQUEA──→ Production deploy (no release sin sign-off)
```

---

## DECISIÓN PARA JUAN CAMILO

**¿Activamos paralelización máxima ahora?**

Si sí, lanzo en paralelo:
1. 🟣 **Erik** → Sistema de diseño + mockups (Día 1-7)
2. 🔵 **Brook** → Flutter scaffold + setup (Día 1-3)
3. 🟠 **Yang** → Market research + competitor intel (Día 1-5)
4. ⬛ **Jade** → Capacitar a Sasha en Supabase Auth (Día 1-2, urgente)

**Resultado al final de Sprint 0:**
- Backend listo (Sasha)
- Diseño completo del MVP (Erik)
- Frontend scaffold + auth UI (Brook)
- Inteligencia comercial completa (Yang + Leo)
- Workflows automatizados listos para conectar (Cinthya)

**Velocidad teórica:** 4-5x más rápido que ejecución secuencial.  
**Costo:** Nada extra (los agentes ya están en el equipo).

---

## CHECK-IN POINTS (Junta Estratégica)

| Día | Evento | Quién participa |
|-----|--------|------------------|
| Sábado Week 1 | Sprint 0 review + retrospectiva | Jarvis + Juan Camilo + Sasha + Alejo + Erik + Brook |
| Sábado Week 4 | Try-On milestone + demo en vivo | Todo el equipo |
| Sábado Week 8 | Payments milestone + revenue projections | Jarvis + Juan Camilo + Leo |
| Sábado Week 11 | Beta feedback + Go/No-Go decision | Todo el equipo |
| Sábado Week 14 | Post-launch retrospectiva | Todo el equipo |

---

**Plan v1.0 — Living document. Actualizar al cierre de cada sprint.**
