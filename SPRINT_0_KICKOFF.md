# 🎯 SPRINT 0 KICKOFF — Asesor de Imagen AI
## Semana 1: Abril 1-7, 2026

**Proyecto:** Asesor de Imagen AI + Virtual Try-On
**Owner:** Juan Camilo Gil
**PM:** Jarvis
**Lead Dev:** Sasha
**Status:** 🟢 LISTO PARA ARRANCAR

---

## 📋 CAMBIOS ARQUITECTÓNICOS CONFIRMADOS

### 1. IA Recomendaciones: Claude → **Gemini API**
```
ANTES: Claude Sonnet ($0.003-0.015/análisis)
AHORA: Google Gemini 2.0 Flash (similar precio, mejor visual analysis)

Ventaja: Gemini es nativo en análisis multimodal (ropa, colores, estilos)
```

**Endpoints afectados:**
- `GET /api/recommendations/{user_id}` → Gemini
- `GET /api/style-analysis/{user_id}` → Gemini vision
- `POST /api/event-matching` → Gemini classification

---

### 2. Pagos: Stripe → **PSE + Google Pay**
```
ANTES: Stripe + Mercado Pago
AHORA: PSE (PayU) + Google Pay + Apple Pay

Por qué PSE:
✅ LATAM-native (Colombia, Perú, etc.)
✅ Sin intermediarios (banca directa)
✅ Tasa de conversión más alta
✅ Comisión: 1.9% + $1,200 COP fija
```

**Flow de pagos:**
```
Usuario Premium ($4.99-8.99/mes)
    ↓
Selecciona método: PSE | Google Pay | Apple Pay
    ↓
PSE: Transferencia bancaria inmediata (PayU)
Google Pay: Tarjeta guardada + débito automático
    ↓
Webhook PayU → nuestra API (confirm payment)
    ↓
Usuario accede Premium features
```

**Tabla DB necesaria:**
```sql
subscriptions {
  id, user_id, status, payment_method,
  pse_reference, google_pay_token,
  amount_paid, payment_date, next_billing_date
}
```

---

### 3. Stack Técnico FINAL
| Layer | Technology | Version | Por qué |
|-------|-----------|---------|--------|
| Backend | FastAPI | 0.109+ | Rápido, async, integración APIs |
| Mobile | Flutter | 3.19+ | Cross-platform (iOS + Android) |
| Database | Supabase | Latest | PostgreSQL + RLS + Auth |
| Try-On | Replicate | API | Generative AI, $0.001-0.005/img |
| Recomendaciones | Gemini | 2.0 Flash | Visual analysis multimodal |
| Pagos | PayU + Google Pay | Native | PSE + tarjeta |
| Deploy | Railway | Latest | Managed, auto-scale |

---

## 🔐 CREDENCIALES CONFIRMADAS

### Ya Disponibles ✅
```
Google Vision API:        ✅ CREADO (mismo proyecto)
Replicate Token:          ✅ <REDACTED_REPLICATE>
Gemini API:               ✅ LISTO (mismo proyecto Google Cloud)
Supabase URL:             ✅ https://qzmjhxhhgdakvsnhbsze.supabase.co
Supabase API Key:         ✅ <REDACTED_SUPABASE>
Supabase Password:        ✅ <REDACTED_PASSWORD>
Google Pay:               ✅ NATIVO (Flutter integration)
Apple Pay:                ✅ NATIVO (StoreKit 2)
```

### Por Crear Esta Semana ⏳
```
PayU Sandbox Account:     ⏳ (contactar PayU, 1-2 días)
  └─ Test PSE credentials
  └─ Test tarjeta credentials
  └─ Webhook configuration
```

**⚠️ SEGURIDAD:**
- Credenciales NO en GitHub público
- .env.local (gitignored)
- Railway Secrets (para CI/CD)
- Compartir solo entre equipo core

---

## 📊 TAREAS SPRINT 0 (Semana 1)

### Sasha — Backend Lead (35h esta semana)

**Bloque 1 — Arquitectura Final (30h)**
- [ ] Revisar documento arquitectura existente
- [ ] Update RecommendationService: Claude → Gemini
- [ ] Update PaymentService: Stripe → PayU + Google Pay
- [ ] Database schema final (7 tablas, RLS policies)
- [ ] OpenAPI 3.0 spec completo (40+ endpoints)
- [ ] Security checklist (JWT, rate limiting, OWASP)

**Bloque 2 — Infraestructura (40h)**
- [ ] Verificar Supabase project
- [ ] Crear migrations (Alembic)
- [ ] Setup Railway staging
- [ ] GitHub repo privado + branch protection
- [ ] FastAPI boilerplate (Poetry)
- [ ] Docker + docker-compose
- [ ] GitHub Actions (CI/CD)

**Bloque 3 — Documentación (5h)**
- [ ] SPRINT_0_DELIVERABLES.md
- [ ] DEVELOPER_QUICKSTART.md
- [ ] PAYMENT_INTEGRATION_GUIDE.md
- [ ] GEMINI_INTEGRATION_GUIDE.md

**Entrega:** Viernes 4 de abril

---

### Brook — Frontend Prep (20h esta semana)

**Bloque 1 — Review & Preparation**
- [ ] Revisar Flutter architecture specs
- [ ] Setup Flutter project locally
- [ ] Review design system (Erik)
- [ ] Prepare for Sprint 1 (auth screens)

**Bloque 2 — GitHub Access**
- [ ] Clone repo privado (cuando Sasha lo cree)
- [ ] Setup Flutter environment
- [ ] Verificar connection a Supabase

**Stand by:** Esperar a Sasha para repo + OpenAPI spec

---

### Erik — Design Confirmation (15h esta semana)

**Bloque 1 — System Finalization**
- [ ] Revisar design system (colores pastel, tipografía)
- [ ] Confirm component library
- [ ] Verify accessibility (WCAG AA)

**Bloque 2 — Sprint 1 Prep**
- [ ] Prepare auth screens design
- [ ] Prepare body analysis screens
- [ ] Prepare wardrobe upload screens

**Stand by:** Esperar designs confirmadas para Sprint 1

---

### Cinthya — Copy & UX (10h esta semana)

**Bloque 1 — Copy Library Finalization**
- [ ] Revisar copy library (50+ frases)
- [ ] Tone & voice guidelines (empowering, no judgmental)
- [ ] Payment copy (PSE, Google Pay explanations)

**Bloque 2 — Sprint 1 Prep**
- [ ] Copy para auth flows
- [ ] Copy para body analysis
- [ ] Error messages + edge cases

---

### Jarvis — PM (10h esta semana)

**Bloque 1 — Kick-off**
- [ ] Verificar credenciales distribuidas
- [ ] Setup communication channels
- [ ] Create project board (Asana/GitHub Projects)

**Bloque 2 — Monitoring**
- [ ] Daily standup (10 min, async Slack)
- [ ] Review progress
- [ ] Remove blockers

**Bloque 3 — Sprint 1 Planning**
- [ ] Preparar Sprint 1 backlog
- [ ] Confirmar prioridades

---

## 📅 TIMELINE SPRINT 0

```
LUNES 1 DE ABRIL
├─ Kick-off oficial (todos en call 30 min)
├─ Distribuir credenciales (securely)
├─ Sasha arranca arquitectura
└─ Asignar tareas en board

MARTES-JUEVES (2-4 ABRIL)
├─ Sasha: arquitectura + infraestructura
├─ Brook: review specs + local setup
├─ Erik: design finalization
├─ Cinthya: copy library
└─ Jarvis: monitoreo diario

VIERNES 4 DE ABRIL (FIN SPRINT 0)
├─ Sasha entrega:
│  ├─ OpenAPI 3.0 spec
│  ├─ GitHub repo privado
│  ├─ Supabase migrations
│  ├─ Railway staging live
│  └─ SPRINT_0_DELIVERABLES.md
├─ Go/No-Go decision
└─ Sprint 1 kickoff ready
```

---

## 🎯 DELIVERABLES SPRINT 0

**Viernes 4 de abril, EOD:**

```
✅ SPRINT_0_DELIVERABLES.md (Sasha)
✅ OpenAPI 3.0 Specification
✅ GitHub repo privado: asesor-imagen-ai
✅ Supabase project verified + migrations
✅ Railway staging URL live
✅ FastAPI boilerplate ready
✅ Docker image building
✅ CI/CD pipeline (GitHub Actions)
✅ DEVELOPER_QUICKSTART.md
✅ PAYMENT_INTEGRATION_GUIDE.md
✅ GEMINI_INTEGRATION_GUIDE.md
✅ PayU sandbox setup (if available)
✅ Go/No-Go decision for Sprint 1
```

---

## ⚠️ RIESGOS + MITIGACIÓN

| Riesgo | Probabilidad | Mitigación |
|--------|------------|-----------|
| PayU sandbox no disponible | Media | Usar test credentials genéricas, integrar later |
| Supabase RLS policies complejas | Baja | Documentación clara, tests desde día 1 |
| GitHub Actions CI/CD issues | Baja | Usar templates estándar FastAPI |
| API rate limits (Google Vision) | Muy Baja | Free tier suficiente para MVP |

---

## 📞 COMUNICACIÓN

**Daily Standup (Async, Slack)**
- **Cuándo:** 9 AM Colombia (mensaje en Slack)
- **Qué:** Status (en progreso / bloqueado / completado)
- **Quién:** Sasha, Brook, Jarvis

**Weekly Review (Friday 5 PM)**
- **Duración:** 30 min
- **Asistentes:** Todos + Juan Camilo
- **Agenda:** Deliverables, blockers, Sprint 1 readiness

---

## 🚀 GO/NO-GO DECISION CRITERIA (Viernes 4 Abril)

**GO si:**
- ✅ OpenAPI spec completo (40+ endpoints)
- ✅ Supabase migrations exitosas
- ✅ Railway deployment funciona
- ✅ GitHub CI/CD pipeline verde
- ✅ FastAPI health check respondiendo
- ✅ Documentación 100% completa

**NO-GO si:**
- ❌ Supabase no conecta correctamente
- ❌ Rails deployment fails
- ❌ OpenAPI spec incompleto
- ❌ Security vulnerabilities encontradas

**Decision:** Jarvis + Juan Camilo + Sasha (viernes EOD)

---

## 📁 REPOSITORIO STRUCTURE (FINAL)

```
asesor-imagen-ai/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py (FastAPI app)
│   │   ├── config.py (settings, .env)
│   │   ├── database.py (Supabase connection)
│   │   ├── models/ (Pydantic schemas)
│   │   │   ├── auth.py
│   │   │   ├── body.py
│   │   │   ├── wardrobe.py
│   │   │   ├── tryons.py
│   │   │   ├── recommendations.py
│   │   │   └── subscriptions.py
│   │   ├── routes/ (40+ endpoints)
│   │   │   ├── auth.py
│   │   │   ├── body.py
│   │   │   ├── wardrobe.py
│   │   │   ├── tryons.py
│   │   │   ├── recommendations.py
│   │   │   ├── subscriptions.py
│   │   │   └── analytics.py
│   │   ├── services/ (business logic)
│   │   │   ├── auth_service.py
│   │   │   ├── body_analysis_service.py
│   │   │   ├── wardrobe_service.py
│   │   │   ├── tryon_service.py
│   │   │   ├── recommendation_service.py (GEMINI)
│   │   │   ├── payment_service.py (PSE + Google Pay)
│   │   │   └── analytics_service.py
│   │   ├── utils/
│   │   │   ├── security.py (JWT)
│   │   │   ├── validators.py
│   │   │   └── helpers.py
│   │   └── security.py (JWT, OWASP)
│   ├── migrations/ (Alembic)
│   │   ├── env.py
│   │   └── versions/
│   │       └── 001_initial_schema.py
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_body_analysis.py
│   │   ├── test_wardrobe.py
│   │   ├── test_tryons.py
│   │   ├── test_recommendations.py
│   │   └── test_payments.py
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── pyproject.toml (dependencies)
│   ├── .env.example
│   └── README.md
├── mobile/ (Flutter - Sprint 1+)
├── docs/
│   ├── SPRINT_0_DELIVERABLES.md
│   ├── DEVELOPER_QUICKSTART.md
│   ├── PAYMENT_INTEGRATION_GUIDE.md
│   ├── GEMINI_INTEGRATION_GUIDE.md
│   ├── openapi.json (3.0 spec)
│   └── DATABASE_SCHEMA.md
├── .github/
│   └── workflows/
│       ├── test.yml (pytest)
│       └── deploy.yml (Railway auto-deploy)
├── .gitignore
└── README.md (main project overview)
```

---

## ✅ CHECKLIST FINAL (ANTES DE ARRANCAR)

**Juan Camilo:**
- [ ] ¿Aprobadas arquitectura y cambios?
- [ ] ¿Credenciales distribuidas a Sasha?
- [ ] ¿PayU sandbox contact hecho?

**Sasha:**
- [ ] ¿Credenciales recibidas?
- [ ] ¿Arquitectura documento revisado?
- [ ] ¿Listo para arrancar lunes 1 de abril?

**Todos:**
- [ ] ¿Acceso a Slack/comunicación?
- [ ] ¿Entendido el plan?

---

## 📞 CONTACTO & SOPORTE

**Problemas/Blockers durante Sprint 0:**
- Mensaje directo a Sasha (Slack)
- Escalada a Jarvis si urgente
- Jarvis notifica a Juan Camilo

**Reunión de Kick-off:**
- **Día:** Lunes 1 de abril, 10 AM Colombia
- **Duración:** 30 minutos
- **Link:** [TBD]
- **Asistentes:** Todos + Juan Camilo

---

## 🎬 STATUS

```
🟢 SPRINT 0 OFICIALMENTE APROBADO Y LISTO

Inicio: Lunes 1 de abril, 2026
Fin: Viernes 4 de abril, 2026
Equipo: Sasha (lead), Brook, Erik, Cinthya, Jarvis
Budget: Incluido en $208K total MVP
```

---

**Documento preparado por:** Jarvis, Gerente de Programación
**Fecha:** 2026-03-29
**Versión:** 1.0 FINAL
**Status:** ✅ READY TO GO
