# ROADMAP 7 DÍAS — Ejecución Paralela

**Owner:** Jarvis (CEO)  
**Period:** 2026-05-18 a 2026-05-25  
**Status:** 🟡 **CRÍTICO** — Timeline al límite

---

## 🎯 OBJETIVO DEL SPRINT

Get to **Sprint 0.4 + Sprint 0.5 BOTH READY** for parallel execution, with:
- ✅ Rate limiting + DevOps spec clear (Sprint 0.4)
- ✅ Worker integration spec clear (Sprint 0.5)
- ✅ Frontend unblocked (Brook 4 issues + theme done)
- ✅ Design finished (Erik mockups S05-S11)
- ✅ Decisions made (Juan Camilo D1-D5)

---

## 📅 TIMELINE DETALLADO

### **DAY 1 — SÁB 2026-05-18 (HOY)**

#### Junta Estratégica 10:00 AM
**Asistentes:** Juan Camilo, Jarvis, Jade, Ego  
**Agenda:**
- [ ] Review Sprint 0 final metrics (161 tests, 82% cov, 0 CRITICAL)
- [ ] Approve Sprint 0.5 prompt (036829c)
- [ ] Decidir go/no-go para Sprint 0.4 trigger
- [ ] Juan Camilo: confirmar credenciales GCV + Replicate timeline
- [ ] Decisiones UX (D1-D5) — iniciar conversación comercial

**Outputs:**
- ✅ Sprint 0.4 trigger APPROVED
- ✅ Sprint 0.5 blockers identificados (credenciales)
- 🟡 D1-D5 feedback (Juan Camilo)

---

### **DAY 2 — DOM 2026-05-19**

#### Morning — Trigger Sprint 0.4 + Brook fixes
**Owners:** Jarvis, Brook, Antigravity

**Jarvis:**
- [ ] Trigger Antigravity con `docs/SPRINT_0_4_PROMPT.md`
  - Message: "Rate limiting es bloqueante para S0.5. 7 días. Cyber Neo audita post-entrega."
- [ ] Confirm Supabase bucket `/try-ons/` creation (5 min task)

**Brook:**
- [ ] START: Fix 4 issues técnicos Flutter (parallel track)
  1. [ ] Issue #1: Dependency conflict (pubspec.yaml upgrade Riverpod)
  2. [ ] Issue #2: Import paths (convert to package: imports)
  3. [ ] Issue #3: build_runner (flutter pub run build_runner build)
  4. [ ] Issue #4: Theme integration (AppTheme.dart + AppColors/Typography/Spacing)
- [ ] Milestones: by EOD check pub get + analyze clean

**Erik:**
- [ ] Hold for D1-D5 feedback from Juan Camilo
- [ ] Prepare S04B loading state design (no wait on D1-D5)

**Antigravity:**
- [ ] Review Sprint 0.4 prompt
- [ ] Plan rate limiting architecture
- [ ] Assess timeline (7 días OK?)

**Juan Camilo:**
- [ ] Respond to D1-D5 questionnaire (CRITICAL PATH)
- [ ] If missing: credenciales GCV + Replicate, send to Jarvis

#### Afternoon — Commercial alignment
**Owners:** Leo, Juan Camilo, Yang

**Leo:**
- [ ] Review pricing implications of D4 decision (free tier limits)
- [ ] Prepare talking points for Juan Camilo on D3/D5 (conversion impact)

**Juan Camilo:**
- [ ] Meeting with Leo + Yang: validate D1-D5 from commercial angle
  - D1 (app name) — branding + positioning
  - D3 (onboarding) — conversion funnel impact
  - D4 (free tier) — revenue vs growth trade-off
  - D5 (social) — viral loop potential

**Output:** [ ] D1-D5 DECIDED (hard decisions made)

---

### **DAY 3 — LUN 2026-05-20**

#### Morning — Erik unblocked + Brook continues
**Owners:** Erik, Brook, Jarvis

**Jarvis:**
- [ ] Send D1-D5 decisions to Erik (enable screen design)
- [ ] Monitor Sprint 0.4 rate limiting progress (Day 1/7)
- [ ] Follow up: credenciales GCV + Replicate received?

**Erik:**
- [ ] S04B: Design loading state (shimmer animation, 15-30 sec)
  - Reference: Aether Luxe primaryGradient (135° #0058BE→#9466FF)
  - Motion: pulsing gradient shimmer
- [ ] S05: My Wardrobe — apply D2 decision (upload vs wardrobe selection)
  - Grid layout: 2 cols mobile, 3 desktop
  - Upload zone OR wardrobe selector (based on D2)
  - Empty state illustration
- [ ] S06: Style Insights — no dependencies on D1-D5
  - Card: body type + color season results
  - Paleta personal con color swatches
- [ ] Timeline: 2 screens/day feasible? (S04B + S05 hoy)

**Brook:**
- [ ] Continue Issue #2 + #3 (imports + build_runner)
  - `flutter analyze` must be clean
  - build_runner generation must work
- [ ] Issue #4 (theme): Start AppTheme integration
  - [ ] Create lib/core/theme/app_theme.dart
  - [ ] Copy all tokens from DESIGN_SYSTEM.md
  - [ ] Wire into MaterialApp

**Output:**
- [ ] Brook: 3/4 issues fixed (analysis clean, build_runner works)
- [ ] Erik: 2 screens (S04B, S05) mockups in progress

---

### **DAY 4 — MAR 2026-05-21**

#### Morning — Rate limiting critical check
**Owner:** Jarvis, Antigravity

**Jarvis:**
- [ ] CHECK: Antigravity rate limiting half-done? (Day 2/7)
- [ ] If blocked: intervene immediately
- [ ] If on track: monitor
- [ ] Any credenciales for GCV/Replicate yet?

#### Full day — Erik mockups + Brook theme final
**Owners:** Erik, Brook

**Erik:**
- [ ] S07: Body Analysis Upload
  - Instruction text: "foto de frente, buena luz"
  - Upload zone OR use profile photo
  - Preview + confirm
  - Loading animation (reference S04B)
- [ ] S08: Collections (looks guardados)
  - Masonry grid OR uniform grid (decision)
  - Cards: imagen + fecha + AI insight snippet
  - Empty state
- [ ] S09: Profile / Settings
  - Avatar + nombre + email + plan
  - Notificaciones toggle, idioma, privacidad
  - Logout button (error color)
- [ ] S11: Error states (all screens)
  - Skeleton loading shimmer
  - 404 illustration
  - Network error
  - Try-on failed
- [ ] Timeline: 4 screens done

**Brook:**
- [ ] Issue #4 final: Theme fully integrated
  - [ ] AppTheme.lightTheme() wired in main.dart
  - [ ] All widget code references AppColors, AppTypography, AppSpacing
  - [ ] Hot reload works without theme errors
  - [ ] Verify: `flutter analyze` still clean
- [ ] START: S01 Splash/Onboarding
  - 3 slides: "Verte sin probarte" / "Vestirte mejor" / "Conocete estilísticamente"
  - Primary gradient button: "Comenzar gratis"
  - Navigation indicator (dots)

**Output:**
- [ ] Brook: All 4 issues RESOLVED. App compiles + hot reload works.
- [ ] Erik: 4 screens done (S07-S11). 6/11 mockups complete.

---

### **DAY 5 — MIÉ 2026-05-22**

#### Morning — Checkpoint
**Owner:** Jarvis

**Jarvis:**
- [ ] CHECK: Antigravity progress (Day 3/7, rate limiting must be working)
- [ ] CHECK: Erik progress (S07-S11 done, remaining?)
- [ ] CHECK: Brook progress (4 issues fixed, S01 in progress?)
- [ ] Any blockers? Escalate immediately.

#### Full day — S01-S04 implementation + final mockups
**Owners:** Brook, Erik

**Erik:**
- [ ] S10: Paywall / Upgrade to Pro
  - Header with crown icon
  - Tier comparison table: Free | Estilo | Imagen
  - Feature list with checkmarks
  - Pricing in COP/USD
  - Social proof (users activos)
- [ ] Final mockups: S01, S02, S03 (auth screens)
  - Splash + 3 slides
  - Login form
  - Register form
- [ ] DELIVERABLE: 11/11 screens complete in Figma/Stitch
- [ ] Export to DESIGN.md format for Brook integration

**Brook:**
- [ ] Implement S01: Splash + Onboarding (3 slides)
  - PageView with 3 slides
  - Dots indicator (primary gradient)
  - "Comenzar gratis" CTA navigates to Register
  - Uses AppTheme colors + typography

**Output:**
- [ ] Erik: 11/11 mockups COMPLETE (all screens done)
- [ ] Brook: S01-S02 screens implemented (S03 next)

---

### **DAY 6 — JUE 2026-05-23**

#### Morning — Rate limiting final check + Backend prep
**Owner:** Jarvis, Antigravity

**Jarvis:**
- [ ] CHECK: Sprint 0.4 near completion? (Day 5/7)
- [ ] CHECK: Credenciales GCV + Replicate **MUST** be here for S0.5 start
- [ ] If missing: escalate to Juan Camilo TODAY
- [ ] Schedule Cyber Neo audit for post-0.4 delivery

#### Full day — Authentication screens + S04 readiness
**Owner:** Brook

**Brook:**
- [ ] S02: Login screen
  - Email input + password input (show/hide toggle)
  - "Iniciar sesión" button
  - Link "¿Olvidaste tu contraseña?" (disabled for MVP)
  - "o continúa con Google" (OAuth placeholder)
  - Navigation to Register
  - Wired to Auth API (POST /api/v1/auth/login)
- [ ] S03: Register screen
  - Nombre + email + password inputs
  - Checkbox términos
  - Password policy info (min 10, letter+digit)
  - "Crear cuenta" button
  - Wired to Auth API (POST /api/v1/auth/register)
- [ ] S04 structure ready:
  - Upload zone component (UploadZone)
  - Clothing slot grid (max 5 items, ClothingSlot)
  - CTA button "Generar Outfit Ideal" (disabled until photo loaded)
  - Not waiting for result state yet (depends on S0.5 workers)

**Output:**
- [ ] Brook: S01-S04 basic flow complete
- [ ] Antigravity: Sprint 0.4 delivered + audited?
- [ ] Credentials received = Sprint 0.5 can START

---

### **DAY 7 — VIE 2026-05-24 / SAB 2026-05-25**

#### Day 7A — Final integrations + verification
**Owner:** Jarvis, all teams

**Jarvis:**
- [ ] Verify:
  - [ ] Sprint 0.4 DELIVERED (rate limiting implemented)
  - [ ] Cyber Neo audit status (blockers resolved?)
  - [ ] Sprint 0.5 ready to trigger (blockers all clear)
  - [ ] Design system 11/11 screens delivered
  - [ ] Flutter 4/4 issues fixed + theme integrated
  - [ ] Credenciales confirmed

**Antigravity:**
- [ ] Sprint 0.4 wrap-up + documentation
- [ ] READY for Sprint 0.5 trigger (pending creds)

**Erik:**
- [ ] Final review: 11 mockups aligned with brand
- [ ] Deliver Figma/DESIGN.md export to Brook

**Brook:**
- [ ] Final testing: S01-S04 functional flow
- [ ] Prepare for S05-S11 implementation (post-Erik)
- [ ] Document any remaining technical debt

#### Day 7B — Saturday Junta (2026-05-25 10:00 AM)
**Attendees:** Juan Camilo, Jarvis, Jade, Ego

**Agenda:**
- [ ] Review Sprint 0 to 0.5 readiness
- [ ] Approve Sprint 0.4 + Sprint 0.5 execution (parallel)
- [ ] Verify credenciales delivered
- [ ] Discuss timeline risk to LAUNCH 2026-07-31
- [ ] Assign priorities for Sprint 1 onwards
- [ ] Confirmation: all blockers clear

**Outputs:**
- ✅ Sprint 0.4 + 0.5 both APPROVED for parallel execution
- ✅ Timeline to launch reviewed + mitigations planned
- ✅ Next week priorities locked

---

## 🚨 CRITICAL DEPENDENCIES

```
D1-D5 decisions
  ↓
Erik mockups S05-S11
  ↓
Brook implementation S05-S11
  ↓
Sprint 0.5 (workers)
  ↓
Sprint 1 onwards
```

**If D1-D5 delayed:** -5 to -7 days in timeline  
**If Brook 4 issues not resolved:** COMPLETE BLOCKER  
**If Sprint 0.4 rate limiting fails:** S0.5 cannot start  
**If credenciales late:** S0.5 blocked indefinitely

---

## 📊 SUCCESS METRICS (DAY 7)

| Deliverable | Target | Actual | Status |
|-------------|--------|--------|--------|
| Sprint 0.4 prompt executed | 100% | ? | TBD |
| Sprint 0.5 prompt ready | 100% | ✅ 100% | ✅ |
| D1-D5 decisions made | 100% | ? | 🟡 |
| Erik mockups S05-S11 | 100% | ? | 🟡 |
| Brook 4 issues fixed | 100% | ? | 🟡 |
| Brook S01-S04 implemented | 100% | ? | 🟡 |
| Credenciales in hand | 100% | ? | 🟡 |
| Cyber Neo audit done | 100% | ? | 🟡 |

---

## 🎯 PARALLEL TRACKS (CRITICAL)

```
Track A — Backend DevOps          Track B — Frontend              Track C — Design
(Antigravity + Cyber Neo)         (Brook)                        (Erik + Juan Camilo)
───────────────────────────       ──────────────────────────     ──────────────────
Day 1-7: Sprint 0.4               Day 2-3: Fix 4 issues          Day 2: Await D1-D5
  • Rate limiting                 Day 4-7: S01-S04               Day 3-7: Mockups
  • Sentry, PostHog                                               Day 7: Deliver 11 screens
  • Docker multi-stage                                           
  • GitHub CI/CD                                                 Track D — Commercial
  • ReadinessstackProbe            Track E — Blockers              (Leo + Juan Camilo)
→ CRITICAL for S0.5 workers      (Jarvis oversight)              ───────────────────
                                  ────────────────────────       Day 2: D1-D5
                                  Credenciales (GCV, Replicate)   decisions
                                  Supabase bucket /try-ons/      Day 2-7: Revenue
                                  Rate limiting ready            model validation
```

**All tracks must complete by DAY 7 for parallel execution of Sprint 0.4 + 0.5 + concurrent design.**

---

## 🔴 IF TIMELINE SLIPS

**Escalation matrix:**

| Blocker | Owner | Mitigation |
|---------|-------|-----------|
| D1-D5 delayed >24h | Juan Camilo | Leo can provide recommendations, but Juan Camilo final decision |
| Brook 4 issues >48h | Brook | Sasha pairs on code review + strategy |
| Sprint 0.4 rate limiting delayed | Antigravity | Reduce scope (only API endpoints, workers exempt for S0.5) |
| Credenciales >48h late | Juan Camilo | Mock workers, delay S0.5 to following week |
| Erik mockups delayed | Erik | Reduce S05-S11 to 5 screens, defer rest to Sprint 1 |

**RED LINE: All tracks must be > 80% complete by DAY 7 for LAUNCH 2026-07-31 viability.**

