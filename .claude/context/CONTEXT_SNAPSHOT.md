# 📸 CONTEXT SNAPSHOT — Vista en tiempo real de la Agencia

**Índice dinámico actualizado automáticamente cada sábado a las 10 AM por Jade.**

**Última actualización:** 2026-06-02 | **Próxima:** 2026-06-07 10:00 AM

---

## 🚀 ESTADO GENERAL

| Componente | Estado | Propietario | Próxima acción |
|------------|--------|-------------|----------------|
| **Asesor Imagen AI** | 🔄 Sprint 0.5 en progreso | Sasha + Brook + Erik | Deploy Railway + commit cambios |
| **Teclado de Señas** | ✅ MVP completado | Sasha + Brook | QA externo / publicación |
| **Data Reporting Agents** | 📋 Planificado | Jarvis | Kick-off SaaS Q2 2026 |
| **Pipeline comercial** | 🔄 Activo | Leo + Yang | Cerrar deals Q2 |
| **Agencia infraestructura** | ✅ Obsidian vault operativo | Jarvis | Contratar Arquitecto |
| **Modelos Claude** | ⚠️ Migración urgente | Jarvis | Migrar a Opus 4.8 antes del 15 jun |

---

## 🚨 ALERTAS CRÍTICAS (actuar esta semana)

- ⚠️ **claude-sonnet-4 y claude-opus-4 se RETIRAN el 15 junio 2026** → Migrar CLAUDE.md hoy
- ⚠️ **Supabase breaking changes semana 1 junio (ACTIVO YA)**: Analytics/Vector removidos
- ⚠️ **15 junio**: Postgres 15→17, rol supabase_admin→postgres, pg_graphql introspection off
- ⚠️ **Asesor Imagen AI**: múltiples archivos modificados sin commitear (backend + frontend)

---

## 👥 EQUIPO

| Agente | Modelo | Estado | Carga | Próxima tarea |
|--------|--------|--------|-------|---------------|
| **Jarvis** | Opus 4.8 🆕 | ✅ Operativo | 85% | Deploy Railway + migración modelos |
| **Jade** | Sonnet 4.6 | ✅ Operativo | 70% | Capacitar Sasha en Supabase breaking changes |
| **Sasha** | Opus 4.8 🆕 | ✅ Operativo | 80% | Sprint 0.5 workers + Railway deploy |
| **Brook** | Sonnet 4.6 | ✅ Operativo | 75% | Flutter frontend S01-S11 |
| **Erik** | Sonnet 4.6 | ✅ Operativo | 60% | DESIGN_HANDOFF S01-S11 completado |
| **Cinthya** | Sonnet 4.6 | ✅ Operativo | 50% | n8n 2.0 AI Agent Nodes |
| **Alejo** | Opus 4.8 🆕 | 🆕 Buscando | — | CONTRATACIÓN URGENTE |
| **Leo** | Opus 4.8 🆕 | ✅ Operativo | 65% | Pipeline comercial Q2 |
| **Yang** | Sonnet 4.6 | ✅ Operativo | 60% | Intel prospectos Data Reporting |
| **Ego** | Opus 4.8 🆕 | ✅ Operativo | 55% | Auditar Sprint 0.5 post-entrega |
| **Cyber Neo** | Opus 4.8 🆕 | ✅ Operativo | 40% | Pre-release audit Sprint 0.5 |

---

## 📊 PROYECTOS ACTIVOS

### 1. Asesor Imagen AI (flagship activo)
```
Sprint actual: 0.5 — Worker Integration & Real API Calls
Sprint 0.1 ✅ 0.2 ✅ 0.3 ✅ — 161 tests, 82% cov, 0 CRITICAL findings
Sprint 0.5 commits: d9f0d3a (backend) + 5b3ac87 (flutter) + d475404 (design)
D1-D5 decisiones: ✅ APROBADAS (2026-05-18)
Design: ✅ Aether Luxe, DESIGN_HANDOFF S01-S11 completo
Backend: 3 buckets storage, Dockerfile, railway.toml listos
Flutter: Demo mode resiliente (env + supabase guard)
Pendiente: Deploy Railway, credenciales reales, commit cambios sin push
Blocker: Docker no en dev box, Supabase CLI no linked
Revenue model: GO ✅ Opción F — +$233K/mes margen a 1M MAU
Owner: Sasha + Brook + Erik
```

### 2. Teclado de Señas
```
Fase: Post-MVP — QA y publicación
APK: ✅ 61MB compilado, 40+ endpoints, 7 screens, WCAG AA
Tests: ✅ Sin crashes en Android real
Próximo: QA externo, publicación Play Store
Owner: Sasha (Backend) + Brook (Frontend)
```

### 3. Data Reporting Agents (próximo)
```
Fase: Planificación
MVP: semanas 2-8 Q2 2026
Target: $300-480k ARR
Features: upload datos + análisis IA + dashboards + reportes email + chat Q&A
Owner: Jarvis → asignar equipo
```

### 4. Pipeline Comercial Q2 2026
```
Target: $60k-250k en ingresos
Leads: Base de 500 prospectos cargados
Owner: Leo + Yang
```

---

## 📋 PRÓXIMAS REUNIONES

| Reunión | Día/Hora | Asistentes | Agenda |
|---------|----------|-----------|--------|
| Junta Estratégica | Sábado 10 AM | Juan Camilo, Jarvis, Jade, Ego | Sprint 0.5 status, modelos, Supabase |
| Ejecución técnica | Lunes 9 AM | Jarvis, Sasha, Brook, Erik | Deploy Railway, flutter frontend |
| Pipeline comercial | Miércoles 3 PM | Jarvis, Leo, Yang | Deals, Data Reporting Agents |
| Automatización | Viernes 4 PM | Jarvis, Cinthya, Jade | n8n 2.0, workflows IA |

---

## 🔥 BLOCKERS & OPORTUNIDADES

### Blockers
- ⚠️ **Modelos deprecated** — claude-sonnet-4 + claude-opus-4 se retiran 15 junio. Migrar CLAUDE.md a Opus 4.8 HOY
- ⚠️ **Supabase breaking (jun 15)** — Postgres 17, rol postgres, pg_graphql introspection OFF. Sasha debe revisar migrations asesor-imagen-ai
- ⚠️ **Asesor Imagen AI sin deploy** — Dockerfile + railway.toml listos pero Railway no deployado. Credenciales Juan Camilo pendientes
- ⚠️ **Cambios sin commitear** — asesor-imagen-ai tiene ~14 archivos modificados sin commit/push
- ⚠️ **Arquitecto** — No contratado aún. Sasha necesita mentor en decisiones críticas

### Oportunidades
- 🟢 **Asesor Imagen AI** — Costo modelado GO ✅, deploy Railway unblocks beta test
- 🟢 **Data Reporting Agents** — $300-480k ARR, SaaS con potencial real Q2-Q3 2026
- 🟢 **n8n 2.0 AI Agents** — MCP support nativo, Cinthya puede automatizar workflows cross-agentes
- 🟢 **Flutter 3.44 + Dart 3.12** — Agentic Hot Reload mejora velocidad dev Brook

---

## 📚 RECURSOS CLAVE

| Recurso | Ubicación | Propósito |
|---------|-----------|----------|
| CLAUDE.md | Raíz proyecto | Identidad & reglas |
| MEMORY.md | `memory/` | Estado persistente |
| agencia-core.md | `.claude/context/` | Estructura base |
| SPRINT_TRACKER.md | `asesor-imagen-ai/docs/` | Estado sprint por sprint |
| RAILWAY_DEPLOYMENT_GUIDE.md | `asesor-imagen-ai/` | Guía deploy producción |
| jade_intel_2026_06_02.md | `memory/` | Tendencias y alertas críticas |

---

## 🎯 OBJETIVOS TRIMESTRAL (Q2 2026)

1. 🔄 **Deploy Asesor Imagen AI** en Railway — **PRÓXIMO HITO**
2. 🔄 **Cerrar 3-5 deals comerciales** — **IN PROGRESS**
3. 📋 **Contratar Arquitecto** — **CRITICAL PATH**
4. 📋 **Kick-off Data Reporting Agents** — **SIGUIENTE PROYECTO**
5. ✅ **Teclado Señas MVP** — **COMPLETADO**
6. ✅ **Obsidian Vault** — **OPERATIVO**

---

**Notas:**
- Snapshot generado automáticamente por tarea programada Jade (sábados 10 AM)
- Última intel Jade: `memory/jade_intel_2026_06_02.md`
- No re-leas CLAUDE.md completo — usa este resumen
- Para detalles de sprint: `asesor-imagen-ai/docs/SPRINT_TRACKER.md`
