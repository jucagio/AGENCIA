# ⚡ EXECUTION PLAN — Working Without Antigravity (Until Available)

**From:** Jarvis (CEO)  
**To:** All teams (Erik, Brook, Sasha, Alejo, Jade, Ego)  
**Date:** 2026-05-18 (SAB)  
**Situation:** Antigravity delayed; team reorganized to execute in parallel  
**Status:** 🟢 **FULL EXECUTION STARTING TODAY**

---

## Situation

- ✅ Design system ready (Aether Luxe)
- ✅ D1-D5 decisions approved  
- ✅ Environment setup complete (mock + real paths)
- ❌ Antigravity unavailable for Sprint 0.4 (DevOps)
- ✅ **Everything else can proceed in parallel**

**Decision:** Don't wait. Teams execute now. Sprint 0.4 (rate limiting, Docker, CI/CD) deferred until Antigravity available. Everything else starts today.

---

## Execution Structure

```
TODAY (SAB 18) — 4 PARALLEL TRACKS

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  TRACK 1: DESIGN (Erik)         TRACK 2: FRONTEND (Brook)  │
│  ─────────────────────────       ────────────────────────  │
│  • S01-S11 mockups              • Fix 4 Flutter issues      │
│  • 7-day timeline               • 2-day timeline            │
│  • Figma high-fidelity          • Integrate design tokens   │
│  • Ready to hand off to Brook   • Ready for Sprint 1        │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  TRACK 3: INFRASTRUCTURE (Sasha) TRACK 4: STRATEGY (Alejo) │
│  ──────────────────────────────── ────────────────────────  │
│  • Supabase bucket setup         • Architecture review      │
│  • ARQ worker scaffolding        • Cost model analysis      │
│  • Health checks + observability • Scaling strategy         │
│  • RLS policies                  • ADR-007 (rate limiting)  │
│  • 3-day timeline                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘

WAITING (Juan Camilo): Credentials → then Sprint 0.5 (workers)
DELAYED (Antigravity): Sprint 0.4 → then production deployment
```

---

## Track 1: ERIK — Design S01-S11

**Owner:** Erik  
**Timeline:** 7 days (MAR 18 - SAT 25)  
**Deliverable:** 11 screens, Figma, components library, animations  
**No blockers** — start immediately  

### Available NOW (Days 1-2)
- S01: Splash (branding from D1)
- S02: Login 
- S03: Register
- S04: Virtual Try-On (upload flow)
- S04B: Loading state (shimmer animation, NEW)
- S06: Style Insights (body analysis results)
- S07: Body Analysis Upload
- S11: Error states

### Available AFTER D1-D5 ✅ (Days 3-6, BUT D1-D5 NOW APPROVED!)
- S05: My Wardrobe (D2 = hybrid flow)
- S08: Collections (D5 = sharing)
- S09: Profile (D1 = branding)
- S10: Paywall (D4 = pricing tiers)

### Quick Start
1. Read: `docs/NOTIFICACION_ERIK_DESBLOQUEADO.md` (2 min)
2. Review: `docs/DECISIONES_APROBADAS.md` (10 min)
3. Reference: `docs/design-system/DESIGN_SYSTEM.md` (5 min)
4. Start designing in Figma
5. Daily commit mockups to Figma (link in SPRINT_TRACKER)

### Success Criteria
- [ ] All 11 screens designed (high-fidelity)
- [ ] Components documented + linked to design system
- [ ] Animation specs (loading, transitions, success states)
- [ ] Figma file linked in project
- [ ] Ready to hand off to Brook for implementation

**Trigger:** You're unblocked. Go design. 🎨

---

## Track 2: BROOK — Flutter Fixes (48-hour sprint)

**Owner:** Brook  
**Timeline:** 2 days (SAB 18 - SUN 19, EOD)  
**Deliverable:** 4 issues fixed, `flutter analyze` clean, builds successfully  
**No blockers** — start immediately  

### 4 Issues to Fix

**Issue 1: Riverpod dependency conflict**
- Error: `go_router ^8.0` incompatible with `Riverpod ^2.0`
- Fix: Upgrade `pubspec.yaml`: `riverpod: ^2.5.0`
- Test: `flutter pub get`, `flutter pub upgrade`

**Issue 2: Import paths mixed**
- Problem: Some files use relative imports (`./config.dart`), others use package imports (`package:app/...`)
- Fix: Convert ALL to package imports
  ```dart
  // Before
  import './core/config.dart';
  
  // After
  import 'package:asesor_imagen/core/config.dart';
  ```
- Test: `flutter analyze` should report zero import issues

**Issue 3: build_runner missing .g.dart files**
- Problem: `freezed`, `json_serializable` generated files missing
- Fix: Run:
  ```bash
  flutter pub run build_runner build --delete-conflicting-outputs
  ```
- Test: All `.g.dart` files exist, no errors

**Issue 4: Theme integration (AppColors, AppTypography, AppSpacing)**
- Create: `lib/core/theme/app_theme.dart`
  ```dart
  import 'package:flutter/material.dart';
  
  class AppColors {
    // From DESIGN_SYSTEM.md
    static const primary = Color(0xFF1E88E5);  // blue
    static const primaryGradient = LinearGradient(
      colors: [Color(0xFF1E88E5), Color(0xFF6B5B95)],
      begin: Alignment.topLeft,
      end: Alignment.bottomRight,
    );
    static const secondary = Color(0xFF6B5B95);  // violet
    // ... 40+ tokens
  }
  
  class AppTypography {
    static const h1 = TextStyle(
      fontSize: 48,
      fontWeight: FontWeight.w600,
      height: 1.1,
    );
    static const h2 = TextStyle(
      fontSize: 32,
      fontWeight: FontWeight.w600,
      height: 1.2,
    );
    // ... 8 styles
  }
  
  class AppSpacing {
    static const xs = 8.0;
    static const sm = 16.0;
    static const md = 24.0;
    static const lg = 32.0;
    static const xl = 64.0;
  }
  
  class AppTheme {
    static ThemeData get light => ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: AppColors.primary,
      ),
      textTheme: TextTheme(
        headlineLarge: AppTypography.h1,
        headlineMedium: AppTypography.h2,
        // ... rest of text styles
      ),
    );
  }
  ```
- Wire into `MaterialApp`:
  ```dart
  MaterialApp(
    theme: AppTheme.light,
    // ... rest of config
  )
  ```
- Test: App runs, all screens use tokens

### Verification Checklist
```bash
# 1. Get dependencies
flutter pub get

# 2. Analyze
flutter analyze
# Expected: No issues

# 3. Build runner
flutter pub run build_runner build --delete-conflicting-outputs
# Expected: All .g.dart files generated, no errors

# 4. Run on device/emulator
flutter run
# Expected: App launches, all 7 screens navigable without crashes

# 5. Test theme
# Expected: All screens use AppColors, AppTypography, AppSpacing tokens
```

### Quick Start
1. Read: `docs/TRIGGER_BROOK_FLUTTER_FIXES.md` (5 min)
2. Apply fixes 1-4 in order
3. Run verification checklist
4. Commit with message: "Fix 4 Flutter issues: deps, imports, build_runner, theme"
5. Notify Jarvis when done

### Success Criteria
- [ ] Issue #1: Riverpod upgraded to ^2.5.0 ✅
- [ ] Issue #2: All imports converted to package: style ✅
- [ ] Issue #3: build_runner runs clean, all .g.dart files exist ✅
- [ ] Issue #4: AppTheme class created, MaterialApp wired ✅
- [ ] `flutter analyze` clean (zero issues) ✅
- [ ] `flutter run` succeeds on emulator/device ✅
- [ ] All 7 screens navigate without crashes ✅

**Trigger:** You're unblocked. Fix these today. 🔧

---

## Track 3: SASHA — Infrastructure Prep

**Owner:** Sasha  
**Timeline:** 3 days (MAR 18-20)  
**Deliverable:** ARQ setup, Supabase bucket, health checks, docs  
**No blockers** — start immediately  

### 6 Tasks

**T1: Create Supabase `/try-ons/` bucket** (30 min)
- Dashboard → Storage → Create bucket "try-ons"
- Test signed URLs (24h expiry)
- Document bucket name + access pattern

**T2: ARQ worker pool real setup** (4 hours)
- Create `app/core/queue.py` (ARQ pool initialization)
- Create `app/workers/base.py` (3 stub workers: vision, replicate, claude)
- Wire into FastAPI lifespan
- Services can now enqueue jobs (no processing yet)

**T3: Health checks + readiness probes** (1 hour)
- `/health/ready` → Database + Redis checks
- `/health/live` → App liveness
- Docker healthcheck config

**T4: Worker observability** (3 hours)
- Job logging (start, success, failure)
- Metrics endpoint: `/health/metrics`
- Structured logs for Sentry

**T5: Supabase RLS policies** (1 hour)
- Enable RLS on try_ons table
- Users see only their try-ons
- Workers (service role) can update via bypass

**T6: Documentation** (2 hours)
- `docs/WORKERS_INTEGRATION_GUIDE.md`
- How to switch from stubs → real APIs
- Debugging + monitoring guide

### Quick Start
1. Read: `docs/TRIGGER_SASHA_INFRASTRUCTURE.md` (10 min)
2. Execute tasks T1-T6 in order
3. Run tests: `pytest tests/ -k "test_arq" --cov`
4. Commit daily progress
5. Notify Jarvis when done

### Success Criteria (Definition of Done)
- [ ] Supabase bucket `/try-ons/` created + tested ✅
- [ ] ARQ pool initializes in lifespan ✅
- [ ] 3 stub workers available (vision, replicate, claude) ✅
- [ ] Services can enqueue jobs ✅
- [ ] Health checks: readiness + liveness ✅
- [ ] Metrics endpoint available ✅
- [ ] RLS policies on try_ons table ✅
- [ ] Documentation complete ✅
- [ ] Tests ≥85% coverage ✅
- [ ] Ruff clean ✅

**Trigger:** You're unblocked. Prepare infrastructure. 🔌

---

## Track 4: ALEJO — Architecture Review & Strategy

**Owner:** Alejo  
**Timeline:** Concurrent (3-5 days)  
**Deliverable:** Architecture validation, cost analysis, ADRs  
**No blockers** — start immediately  

### Tasks

**T1: Audit design decisions (D1-D5)** (1 day)
- Read: `docs/DECISIONES_APROBADAS.md`
- Analyze: Technical implications of each decision
- Output: `docs/DECISION_AUDIT_D1_D5.md`
  - D1 (dual branding): No architecture impact
  - D2 (hybrid flow): ARQ job queuing needed (✅ Sasha handling)
  - D3 (triggered analysis): Soft vs hard offers → scaling UX queries
  - D4 (free tier + paywall): Rate limiting architecture (✅ waiting Antigravity)
  - D5 (social sharing): CDN strategy for shared images

**T2: Cost model path A recalculation** (1 day)
- Update: `docs/COST_MODEL_PATH_A.md`
- New assumptions:
  - 1M MAU at launch (vs 660K)
  - $350-500K MRR target (from D4)
  - Infrastructure: Railway (vs AWS)
  - API costs: Vision, Replicate, Claude (pass-through)
- Output: Cloud spend forecast + optimization opportunities

**T3: ADR-007: Rate Limiting Architecture** (1 day)
- Decision: How to implement rate limiting (slowapi vs custom?)
- Scope: Auth endpoints (5/min), AI endpoints (30/hour)
- Trade-offs: Redis cost vs performance
- Output: `docs/ADR_007_RATE_LIMITING.md`

**T4: Scaling strategy** (1 day)
- Question: How to scale to 10x (10M MAU)?
- Implications:
  - Database: Supabase → managed PostgreSQL?
  - Job queue: ARQ + Redis → Celery + message broker?
  - Storage: Supabase → S3 + CloudFront?
  - API: FastAPI → distributed API servers?
- Output: `docs/SCALING_STRATEGY_10X.md`

**T5: Security architecture review** (1 day)
- Coordinate with Cyber Neo on OWASP coverage
- Focus: Worker isolation, image storage security, payment flow
- Output: Input for Cyber Neo Sprint 0.4 audit

### Quick Start
1. Read: `docs/DECISIONES_APROBADAS.md` + `docs/design-system/DESIGN_SYSTEM.md`
2. Execute T1-T5 in parallel or sequence (your call)
3. Write ADRs + analysis docs
4. Coordinate with Jarvis on strategic decisions
5. Notify Jarvis when complete

### Success Criteria
- [ ] Decision audit complete (D1-D5 technical implications) ✅
- [ ] Cost model updated (1M MAU, $350-500K MRR, Railway) ✅
- [ ] ADR-007 written (rate limiting decision) ✅
- [ ] Scaling strategy documented (10x path) ✅
- [ ] Security review coordinated with Cyber Neo ✅
- [ ] All docs committed + linked in SPRINT_TRACKER ✅

**Trigger:** Mentor the team. Ensure technical excellence. ✅

---

## Supporting Teams

### JADE — Continuous Capacity Building
**What:** Train team on new systems as they build
- Worker patterns (ARQ, async jobs, retries)
- Design system integration (Erik → Brook handoff)
- Rate limiting architecture (waiting for Sprint 0.4 details)

**When:** During Tracks 1-4 execution

---

### EGO — Quality Assurance
**What:** Audit as teams deliver
- Erik mockups: Design spec compliance
- Brook fixes: Compile + lint success
- Sasha infrastructure: Test coverage ≥85%
- Alejo docs: Architecture quality

**When:** Daily spot checks, formal audits post-delivery

---

### CYBER NEO — Security Readiness
**What:** Prepare for Sprint 0.4 audit
- Coordinate with Alejo on security architecture
- Plan OWASP 2025 compliance audit for Sprint 0.4
- Review worker security model (isolation, input validation)

**When:** Planning now, execution post-Sprint 0.4

---

## Timeline

### Week 1: Tracks 1-4 in Parallel

| Day | Erik (Design) | Brook (Flutter) | Sasha (Infra) | Alejo (Arch) | Status |
|-----|---------------|-----------------|---------------|--------------|--------|
| SAB 18 | S01-S04 design start | Issue #1-2 fixes | T1 bucket + T2 pool | T1-T2 audit | 🟢 ON |
| SUN 19 | S04B + S06-S07 start | Issue #3-4 fixes + test | T3-T4 health + metrics | T3 ADR-007 | 🟢 ON |
| MON 20 | S05-S08 design | COMPLETE + commit | T5-T6 RLS + docs | T4-T5 scale | 🟢 ON |
| TUE 21 | S09-S10 design | READY for next phase | COMPLETE + audit | COMPLETE | ✅ |
| WED 22 | S11 + refinement | — | — | — | ✅ |
| THU 23 | Final handoff to Brook | — | — | — | ✅ |
| SAT 25 | DELIVERED (11/11) | — | — | — | ✅ |

### Week 2: Waiting Points

| When | Blocker | Impact |
|------|---------|--------|
| When Juan Camilo provides credentials | GCV + Replicate keys | Sprint 0.5 workers unblocked |
| When Antigravity available | Sprint 0.4 (rate limiting) | Production deployment readiness |

---

## How It Fits Together

```
TODAY (SAB 18):
  ┌─────────────┬─────────────┬──────────────┬──────────────┐
  │   ERIK      │    BROOK    │    SASHA     │    ALEJO     │
  │   Design    │   Fixes     │ Infrastructure│  Architecture│
  │  11 screens │ 4 issues    │  6 tasks     │   5 docs     │
  └─────────────┴─────────────┴──────────────┴──────────────┘
         ↓           ↓              ↓             ↓
      7 days     2 days          3 days       5 days
         │           │              │             │
         ├───────────┼──────────────┤             │
         │           │              │             │
      WED 20     SUN 19          MON 20       SAT 25
     (S06 ready)  (DONE)        (DONE)       (DONE)
         │
         ↓
      THU 21: Handoff to Brook for implementation
      ↓
      Sprint 1 kickoff (MON 26): Auth + Profile build

PARALLEL WAITING:
  ⏳ Juan Camilo credentials → Sprint 0.5 (workers)
  ⏳ Antigravity available → Sprint 0.4 (DevOps) + production
```

---

## Success = Every Track Complete by Their Deadline

| Track | Owner | Deadline | Status |
|-------|-------|----------|--------|
| Design S01-S11 | Erik | SAT 25 | 🎯 |
| Flutter fixes (4/4) | Brook | SUN 19 | 🎯 |
| Infrastructure | Sasha | MON 20 | 🎯 |
| Architecture + docs | Alejo | SAT 25 | 🎯 |

**When all 4 complete:** Ready for Sprint 1 (Auth + Profile) starting MON 26.

---

## FAQ

**Q: Why no Antigravity until Sprint 0.4?**  
A: DevOps (rate limiting, Docker, CI/CD) can wait. Design, frontend, infrastructure can't. We parallelize to maximize velocity.

**Q: Can we start Sprint 0.5 without Sprint 0.4?**  
A: Technically yes (workers don't require rate limiting). Strategically no — rate limiting is a security prerequisite before production. Once Antigravity delivers Sprint 0.4 and Juan Camilo provides credentials, we kick off Sprint 0.5.

**Q: What if Juan Camilo doesn't provide credentials by WED 21?**  
A: Workers remain stubs. We proceed with Sprint 1 (Auth + Profile) using mock data. When credentials arrive, we activate workers with no code changes (flip FEATURE_MOCK_WORKERS=false).

**Q: What if Antigravity is still unavailable by SUN 19?**  
A: No impact to Sprint 0.4 execution yet. We're prepping infrastructure, design, and fixes. Antigravity needed for: rate limiting (prerequisite), Docker, CI/CD, production deployment. By EOD WED 20, we'll know timeline.

**Q: Who does code review on Erik's mockups?**  
A: Ego daily spot-check on design spec compliance. Formal approval from Jarvis when all 11 screens delivered.

**Q: Who integrates design tokens from Erik into Brook's code?**  
A: Brook does (reference `docs/design-system/DESIGN_SYSTEM.md` section 8 — Flutter equivalences).

---

## Communication Protocol

**Daily standup:** 10:00 AM (async in Slack)
- Track 1 (Erik): Screens designed today
- Track 2 (Brook): Issues fixed, blockers
- Track 3 (Sasha): Infrastructure progress
- Track 4 (Alejo): Docs completed

**Escalation:** If blocked, ping Jarvis immediately

**Junta Estratégica:** SAT 25, 10:00 AM
- Review all 4 track completions
- Approve designs, fixes, infrastructure
- Plan Sprint 1 kickoff (MON 26)

---

## Resources

**Design:**
- `docs/NOTIFICACION_ERIK_DESBLOQUEADO.md`
- `docs/design-system/DESIGN_SYSTEM.md`
- `docs/DECISIONES_APROBADAS.md`

**Frontend:**
- `docs/TRIGGER_BROOK_FLUTTER_FIXES.md`
- `docs/design-system/DESIGN_SYSTEM.md` (section 8: Flutter)

**Infrastructure:**
- `docs/TRIGGER_SASHA_INFRASTRUCTURE.md`
- `docs/ENVIRONMENT_SETUP_GUIDE.md`

**Architecture:**
- `docs/DECISIONES_APROBADAS.md`
- `docs/COST_MODEL_PATH_A.md` (for reference)

---

## Final Word

We don't wait for Antigravity. We execute all 4 tracks in parallel. By MON 20, we'll have:
- ✅ Design mockups (Erik)
- ✅ Flutter fixes (Brook)
- ✅ Infrastructure scaffolding (Sasha)
- ✅ Architecture strategy (Alejo)

Then we integrate and move to Sprint 1. Antigravity joins when available.

**Status: 🟢 FULL EXECUTION — GO.**

---

**Commits verified:**
- `8db4ee7` — .env.example ✅
- `4fbd208` — ENVIRONMENT_SETUP_GUIDE.md ✅
- `771b23a` — SPRINT_TRACKER update ✅
- `fa496e4` — READY_TO_START_SUMMARY.md ✅
- `fb7442a` — IMMEDIATE_NEXT_STEPS_FOR_JUAN_CAMILO.md ✅
- `fd13887` — TRIGGER_SASHA_INFRASTRUCTURE.md ✅

Questions? → Jarvis

Let's build. 🚀
