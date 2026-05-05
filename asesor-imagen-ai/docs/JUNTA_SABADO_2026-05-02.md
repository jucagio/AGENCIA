# Junta Estratégica — Sábado 2026-05-02, 10:00 AM
## Asesor de Imagen AI — Sprint 0 Review

**Asistentes:**
- Juan Camilo Gil (Accionista)
- Jarvis (CEO)
- Sasha (Backend)
- Alejo (Architecture)
- Erik (Diseño)
- Brook (Frontend)
- Yang (Intel)
- Leo (Comercial)
- Cinthya (Automation)
- Jade (Capacitación) — opcional
- Ego (Auditor) — opcional

**Duración:** 90 minutos
**Modalidad:** Demo + Decisiones

---

## 📋 Agenda

### Bloque 1 — Status Sprint 0 (15 min)
**Owner:** Jarvis

Reporte de avance Week 1:
- ✅ Plan maestro v2 con ADRs aplicados
- ✅ Gantt maestro paralelizado
- ⚠️ Backend (Sasha): bloqueado por rate limit, retoma 0.1
- ✅ Frontend (Brook): scaffold 80% (4 issues técnicos pendientes)
- ✅ Diseño (Erik): system + 5 mockups (faltan 5)
- ✅ Intel (Yang): competitor analysis completa
- ✅ Comercial (Leo): pricing strategy completa
- ✅ Architecture (Alejo): cost model recalculado Path A
- ✅ Automation (Cinthya): 8 workflows diseñados

**Veredicto:** Sprint 0 al ~70% sin Sasha. Recovery plan: extender 0.1 a Week 2 o lanzar 0.1 + 0.2 en paralelo cuando vuelva.

---

### Bloque 2 — Decisiones arquitectónicas firmadas (10 min)
**Owner:** Alejo + Jarvis

| ADR | Decisión | Status |
|-----|----------|--------|
| 001 | Supabase Auth nativo (no custom JWT) | ✅ Firmado |
| 002 | Async-first para llamadas a IA externa | ✅ Firmado |
| 003 | Idempotency-Key obligatoria | ✅ Firmado |
| 004 | Caching agresivo de try-ons | ✅ Firmado **(crítico para margen)** |
| 005 | Storage Supabase + Cloudflare R2 CDN | ✅ Firmado |
| 006 | Path A — 50K paid puros | ✅ Firmado por Juan Camilo |
| 007? | Rate limiting agresivo (a definir post-recalc Alejo) | 🟡 Borrador |

---

### Bloque 3 — Modelo financiero Path A (15 min)
**Owner:** Leo + Alejo

**Pricing fijado:**
| Tier | LATAM | US |
|------|-------|----|
| Free | $0 (5 try-ons/mes) | $0 |
| Estilo (Pro) | $4.99/mo | $9.99/mo |
| Imagen (Premium) | $9.99/mo | $19.99/mo |

**Forecast:**
- Mes 3: 4,500 paid → $25K MRR
- Mes 6: 18,000 paid → $115K MRR
- Mes 12: **50,000 paid → $350-560K MRR** ($4.2-6.7M ARR)

**Margen bruto esperado:** 85%+ (con caching ADR-004 + prompt cache Claude)

**Decisión Junta:** ¿Aprobamos forecast como objetivo oficial trimestral?

---

### Bloque 4 — Demo Frontend (10 min)
**Owner:** Brook + Erik

Live demo:
- Flutter app levantando en simulador
- Navegación: splash → onboarding → login (mockup)
- Theme tokens de Erik aplicados
- Limitaciones actuales (issues #1-#4 documentados)

**Decisión Junta:** ¿Aprobamos design system + folder structure como base para 13 sprints restantes?

---

### Bloque 5 — Inteligencia comercial (15 min)
**Owner:** Yang + Leo

Top hallazgos:
- 5 competidores analizados (Stitch Fix, Acloset, Whering, Cladwell, Smart Closet)
- 10 gaps de mercado detectados — el más explotable: **LATAM Spanish-native UX + body diversity**
- 3-5 personas detalladas
- 10 micro-influencers LATAM identificados (Caro Cuevas, Anto Castelló, etc.)

**Banderas rojas Leo:**
1. ⚠️ Si try-on MVP no supera Acloset al sem 4 → atraso launch
2. ⚠️ Privacy de fotos corporales → objeción #1 LATAM
3. ⚠️ Argentina ARS volátil → entrada postpuesta a sem 18
4. ⚠️ Conversión free→paid debe ser 5-8% (industry: 2-3%)
5. ⚠️ MAU free explota costos si > 1M sin caching

**Decisión Junta:** ¿Validamos las 5 banderas como riesgos a monitorear semanalmente?

---

### Bloque 6 — Próximos sprints (15 min)
**Owner:** Jarvis

**Sprint 1 (Week 2):**
- Sasha: Migration SQL + RLS (post-Cyber Neo audit) + auth endpoints
- Brook: Resolver issues #1-#4 + Login/Register screens (con mockups Erik)
- Erik: 5 mockups restantes (body, try-on, recos, profile, paywall)
- Cinthya: Implementar Workflow 1 (welcome) en n8n
- Yang: Validar 660K-1M MAU free viability con presupuesto marketing
- Leo: Outreach plan a 10 micro-influencers (warming)

**Sprint 2 (Week 3):**
- Sasha: Wardrobe CRUD + body analysis API + Google Vision
- Brook: Wardrobe gallery + add item screens
- Erik: Iconografía custom + animaciones Lottie
- Cinthya: Workflows 3, 4, 5 (limit warning, trial, dunning)
- Cyber Neo: Audit primero de seguridad

**Decisión Junta:** ¿Confirmamos asignaciones?

---

### Bloque 7 — Decisiones pendientes que necesitan Juan Camilo (10 min)

1. **Presupuesto marketing:** ¿Confirmamos $X para CAC influencer + ads? (Yang propondrá número)
2. **Equipo:** ¿Hiring del Arquitecto Senior aún urgente, o Alejo cubre con on-call?
3. **Beta cerrada (sem 8-10):** ¿50 usuarias inicial? ¿Reclutamiento por TikTok? ¿Discord privado?
4. **Línea roja launch:** Si Sasha no entrega try-on superior a Acloset al sem 4, ¿atrasamos launch? (Leo recomienda sí)
5. **Partnerships LATAM:** ¿Abrir conversaciones con Falabella / MercadoLibre Fashion antes de launch?

---

## 📦 Entregables presentables al sábado

Documentos en `asesor-imagen-ai/docs/`:
- ✅ `ADR-006-revenue-model.md`
- ✅ `INTEL_COMPETIDORES_2026.md` (Yang)
- ✅ `PRICING_STRATEGY.md` (Leo, 20 págs)
- ✅ `GANTT_SPRINT_PLAN.md` (Jarvis)
- ✅ `HANDOFF_PENDIENTES.md` (Jarvis)
- 🔵 `COST_MODEL_PATH_A.md` (Alejo, en curso)
- 🔵 `AUTOMATION_WORKFLOWS.md` (Cinthya, en curso)
- ✅ `design-system/design-system.md` + `design-tokens.json` (Erik)
- ✅ 5 mockups en `mockups/` (Erik)

Demo frontend:
- Flutter app levantando en simulador iOS/Android
- Theme aplicado
- Navegación funcional (mockup screens)

---

## ⏰ Timeline previo a Junta

| Día/Hora | Quién | Qué |
|----------|-------|-----|
| **Mier 29 - 1 PM** | Reset rate limit Brook + Erik + Yang | Continúa trabajo |
| **Mier 29 - 3:10 PM** | Reset rate limit Sasha | Empieza Entrega 0.1 |
| **Mier 29 - tarde** | Alejo + Cinthya | Entregan reportes |
| **Jue 30** | Sasha | Continúa 0.1 + empieza 0.2 |
| **Vie 1** | Brook | Cierra issues + empieza login UI con mockups Erik |
| **Vie 1** | Erik | Termina 5 mockups restantes |
| **Sáb 2 - 9 AM** | Jarvis | Final brief + pre-Junta sync |
| **Sáb 2 - 10 AM** | **JUNTA** | 🎯 |

---

**Owner del sync de mañana (3:10 PM):** Jarvis
**Owner pre-Junta brief (sáb 9 AM):** Jarvis
