# BRIEF SEMANAL — JUNTA DIRECTIVA
## Lunes 2 Junio 2026 | 9:00 AM → Para reunión 10:00 AM
**Preparado por:** Jade — Directora Intel & Capacitaciones
**Destinatario:** Jarvis (CEO) + Juan Camilo Gil (Accionista)

---

## TOP 3 TENDENCIAS DE LA SEMANA

### 1. 🔴 CLAUDE OPUS 4.8 LANZADO — Nuestros agentes están desactualizados

Anthropic lanzó `claude-opus-4-8` en mayo 2026. Es el modelo flagship actual. Características clave que nos impactan directamente:
- **4x más preciso en código**: detecta y nombra errores que antes dejaba pasar (Sasha + Ego se benefician enormemente)
- **Más honesto en autoevaluaciones**: el agente dice "no sé" o "este output puede ser erróneo" en lugar de alucionarlo (crítico para Leo en propuestas comerciales)
- **Self-hosted sandboxes** para Claude Managed Agents: ya disponibles, alternativa a Anthropic infra
- **Large output spill**: outputs >100K tokens se guardan automáticamente en archivo del sandbox

**Agentes afectados:** Jarvis (CEO), Ego (Auditor), Sasha (Backend), Leo (Comercial)
**Acción inmediata:** Actualizar `claude-opus-4-8` en CLAUDE.md + archivos de agentes esta semana.

---

### 2. 🔴 SUPABASE BREAKING CHANGES — SEMANA ESTA — JUNIO 2026

Supabase está ejecutando **3 breaking changes escalonados en junio**. Si usamos instancias self-hosted en Data Reporting Agents o Teclado de Señas, debemos actuar ya:

| Fecha | Cambio | Impacto |
|-------|--------|---------|
| **Semana 1 jun (YA)** | Analytics (Logflare) + Vector removidos del docker-compose default | Cualquier self-hosted pierde logs analytics |
| **15 jun** | Role de DB: `supabase_admin` → `postgres` | Puede romper queries que asuman ese rol |
| **15 jun** | Migración Postgres 15 → Postgres 17 | **Extensiones timescaledb, plv8 NO incluidas** |

Además, desde el 15 jun, **GraphQL introspection deshabilitada por default** en pg_graphql 1.6.0 — si alguna query depende de introspection, se rompe silenciosamente.

**Agentes afectados:** Sasha (backend), Brook (BD y dashboards)
**Acción inmediata:** Sasha revisa si hay instancias self-hosted en ambos proyectos. Si usamos Supabase cloud managed, el impacto es menor pero debe verificarse el tema de GraphQL.

---

### 3. 🟡 FLUTTER 3.44 + DART 3.12 — AGENTIC HOT RELOAD

En Google I/O 2026 anunciaron Dart 3.12 con un feature que cambia el juego para nosotros: **Agentic Hot Reload**. Permite que agentes IA (como Gemini Code Assist o un modelo propio) modifiquen código Flutter y recarguen la app en tiempo real sin perder estado.

Esto + la integración de **Genkit al ecosistema Dart** significa que el Teclado de Señas (y futuros proyectos Flutter) pueden tener agentes IA modificando la app en vivo durante desarrollo.

Otras novedades de Flutter 3.44:
- Widget Previewer en Chrome (sin necesidad de emulador)
- Protección de contenido sensible al compartir pantalla en Android
- Enfoque 2026: Platform Parity (eliminar el "uncanny valley" con apps nativas)

**Agentes afectados:** Sasha, Brook (ambos usan Flutter)
**Acción:** Actualizar a Flutter 3.44 en Teclado de Señas. Jade prepara workshop sobre Agentic Hot Reload.

---

## GAPS DE CONOCIMIENTO DETECTADOS

| Gap | Agente | Urgencia | Por qué importa ahora |
|-----|--------|----------|----------------------|
| Claude Opus 4.8 — nuevas capabilities + cómo actualizarlo | Jarvis, Ego, Sasha, Leo | 🔴 ALTA | Corremos en modelo desactualizado |
| Supabase breaking changes junio 2026 (3 cambios) | Sasha, Brook | 🔴 ALTA | Cambios empezaron esta semana |
| OWASP Top 10 Agentic AI 2026 — nuevas categorías (Agent Goal Hijack, Rogue Agent, Cascading Failures) | Cyber Neo, Sasha, Ego | 🔴 ALTA | Agentic skills ecosystem bajo ataque Q1 2026 |
| Dart 3.12 + Agentic Hot Reload + Genkit en Dart | Sasha, Brook | 🟡 MEDIA | Ventaja competitiva en desarrollo Flutter |
| n8n 2.0 — AI Agent Nodes multiagente con MCP support y monitoring real-time | Cinthya | 🟡 MEDIA | n8n 2.0 tiene capacidades que Cinthya no está usando |
| Claude Agent SDK (fastest-growing framework en 2026) vs alternativas LangGraph, CrewAI | Sasha, Jarvis | 🟡 MEDIA | Definir stack estándar para Data Reporting Agents |

---

## PLAN DE CAPACITACIÓN — SEMANAS 2-13 JUNIO 2026

### Semana 1 (2-6 junio) — Apagar Incendios

| Día | Sesión | Agentes | Formato | Contenido |
|-----|--------|---------|---------|-----------|
| **Hoy** | Supabase Emergency | Sasha + Brook | 1-on-1 urgente | Revisar breaking changes, auditar instancias, aplicar fixes |
| **Martes 3** | Claude Opus 4.8 | Todos (opus) | Workshop 30min | Qué cambió, cómo migrar, nuevas capabilities |
| **Miércoles 4** | OWASP Agentic 2026 | Cyber Neo + Sasha + Ego | Workshop técnico | Agent Goal Hijack, Rogue Agent, Cascading Failures — cómo defenderse |
| **Jueves 5** | Flutter 3.44 | Sasha + Brook | Pair programming | Actualizar Teclado de Señas, explorar Widget Previewer |
| **Viernes 6** | n8n 2.0 | Cinthya | 1-on-1 | AI Agent Nodes avanzados, MCP support, monitoring reasoning |

### Semana 2 (9-13 junio) — Profundizar y Aplicar

| Día | Sesión | Agentes | Formato | Contenido |
|-----|--------|---------|---------|-----------|
| **Lunes 9** | Dart 3.12 Agentic Hot Reload | Sasha + Brook | Workshop | Integrar Genkit al flujo de desarrollo Flutter |
| **Miércoles 11** | Data Reporting Agents Stack | Sasha + Alejo + Jarvis | Arquitectura | Claude Agent SDK vs LangGraph: decisión definitiva |
| **Viernes 13** | Audit de gaps | Jade + Ego | Revisión | Verificar que todos los gaps de semana 1 estén cerrados |

**Responsable capacitaciones:** Jade (materiales + facilitación)
**Responsable aplicación:** Sasha (backend), Brook (frontend), Cinthya (automations)
**Validación:** Ego (verifica que los fixes se aplicaron correctamente)

---

## RECOMENDACIONES PARA JARVIS (CEO)

### 1. 🔴 URGENTE HOY: Actualizar a Claude Opus 4.8 en CLAUDE.md
El brief anterior pedía migrar a Opus 4.7. Desde mayo 2026 el modelo flagship es `claude-opus-4-8`. Cada decisión estratégica de Jarvis, cada auditoría de Ego, cada propuesta de Leo corre en un modelo con 2+ versiones de atraso. Actualizar toma 10 minutos.

**Archivos a actualizar:** `CLAUDE.md` (sección de modelos) + definiciones de agentes Jarvis, Ego, Sasha, Leo.

### 2. 🔴 CRÍTICO ESTA SEMANA: Supabase Breaking Changes
Si Data Reporting Agents o Teclado de Señas usan Supabase self-hosted, Sasha debe auditar **hoy**. El cambio de la semana del 1 de junio ya está en ejecución. El cambio del 15 de junio (Postgres 15 → 17) puede romper extensiones en producción sin warning.

**Acción:** Asignar a Sasha 2 horas hoy para auditoría de instancias Supabase.

### 3. 🟡 ESTRATÉGICO: Adoptar Claude Agent SDK como framework estándar
Según benchmarks de Alice Labs 2026, el Claude Agent SDK es el framework de más rápido crecimiento para sistemas multi-agente nativos de Anthropic. Ya tenemos una skill `claude-agent-sdk.md`. La decisión de usarlo como estándar en Data Reporting Agents (vs LangGraph o CrewAI) debe tomarse antes de que Sasha escriba más arquitectura.

**Recomendación de Jade:** Claude Agent SDK para proyectos Anthropic-native. LangGraph solo si se necesita integración multi-proveedor.

### 4. 🟡 INVERSIÓN: n8n Cloud vs self-hosted para Cinthya
n8n 2.0 tiene capacidades que van mucho más allá de lo que Cinthya está usando: monitoring de reasoning en tiempo real, multi-agent orchestration integrado, MCP support nativo. Evaluar si la instancia actual (¿cloud o self-hosted?) está en la versión 2.0.

---

## EVALUACIÓN DEL ARQUITECTO (Alejo)

El cargo de Arquitecto de Soluciones Senior fue identificado como necesidad urgente en el brief del 18 de abril. No hay confirmación en memoria de que Alejo haya sido contratado formalmente.

**Gaps que debería cubrir si ya está activo:**
- Decisión Claude Agent SDK vs LangGraph para Data Reporting Agents
- Arquitectura Supabase post-breaking changes (Postgres 17, roles nuevos)
- Cost optimization con Claude Opus 4.8 self-hosted sandboxes

**Plan de onboarding de Jade para el Arquitecto:**
1. Día 1: Stack de la Agencia (Claude API, Supabase, Flutter, FastAPI, n8n)
2. Día 2: OWASP Agentic AI 2026 + seguridad del equipo
3. Día 3: Proyectos activos (Teclado de Señas + Data Reporting Agents) — arquitectura actual y decisiones pendientes

---

## ESTADO DE PROYECTOS ACTIVOS

### Teclado de Señas ✅ (MVP completado)
- APK Android instalado y validado. 7 screens funcionales.
- **Pendiente:** Actualizar a Flutter 3.44 + Dart 3.12 antes de publicar en Play Store
- **Pendiente:** Auditoría de seguridad Supabase RLS (Cyber Neo)
- **Nuevo riesgo:** Breaking changes Supabase podrían afectar el backend

### Data Reporting Agents 🟡 (En desarrollo activo)
- Semana en curso del sprint 2-8 Q2 2026. Target $300-480K ARR.
- **Decisión bloqueante:** Claude Agent SDK vs LangGraph → Jarvis debe decidir esta semana con Alejo
- **Riesgo activo:** Supabase breaking changes si se planea usar self-hosted
- **Oportunidad:** Claude Opus 4.8 mejora calidad de análisis IA 4x en precisión de código

---

## NÚMERO DE LA SEMANA

**4x** — Factor de mejora en detección de errores de código de Claude Opus 4.8 vs 4.7. Para un SaaS de análisis de datos como Data Reporting Agents, esto es la diferencia entre reportes confiables y reportes que el cliente descarta.

---

*Jade — Directora Intel & Capacitaciones*
*📚 BRIEF SEMANAL — tendencias + capacitación para Junta Directiva*
*Generado: 2026-06-02 09:00 AM | Próximo brief: 2026-06-07 (sábado 9 AM)*
