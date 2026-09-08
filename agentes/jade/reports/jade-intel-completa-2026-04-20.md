# Intel Completa — Jade — Lunes 20 Abril 2026

**Preparado por:** Jade, Directora de Intel & Capacitaciones
**Foco del día:** GitHub + Tododeia (tech — lunes)
**Fecha:** 2026-04-20

---

## PRIORIDADES CRÍTICAS (hacer hoy o mañana)

### 🔴 1. claude-3-haiku RETIRADO AYER (19 abril)
- `claude-3-haiku-20240307` fue retirado el **19 abril 2026**
- **Acción:** Sasha verifica todos los proyectos. Migrar a `claude-haiku-4-5-20251001`

### 🔴 2. CVE-2026-27704 — Flutter/Dart (CRÍTICO)
- Afecta: Dart SDK < 3.11.0, Flutter SDK < 3.41.0
- Tipo: path traversal via symlinks → escritura de archivos arbitrarios fuera de PUB_CACHE
- **Acción:** Sasha actualiza Flutter a 3.41.0+ y Dart 3.11.0+ en Teclado de Señas AHORA

### 🔴 3. CVE-2026-33017 — FastAPI pattern (CVSS 9.3, explotado activamente)
- Origen: Langflow (FastAPI-based). Patrón: missing auth + code injection = RCE
- Ataques activos en las primeras 20h del advisory
- **Acción:** Sasha audita endpoints de Data Reporting Agents — ningún endpoint sin auth

---

## Tendencias Técnicas

### Nuevos Modelos Claude (actualización crítica de tabla CLAUDE.md)

| Modelo | ID | Contexto | Estado |
|--------|-----|----------|--------|
| **Opus 4.7** | `claude-opus-4-7` | **1M tokens** | NUEVO — reemplaza Opus 4.6 para Jarvis y Ego |
| **Sonnet 4.6** | `claude-sonnet-4-6` | **1M tokens** | ACTUALIZADO (antes 200k) |
| **Haiku 4.5** | `claude-haiku-4-5-20251001` | 200k tokens | Reemplaza Haiku 3 (retirado ayer) |
| ~~Haiku 3~~ | ~~claude-3-haiku-20240307~~ | — | **RETIRADO 19 ABRIL 2026** |
| ~~Sonnet 4~~ / ~~Opus 4~~ | (varios) | — | Se retiran 15 junio 2026 |

**Nota:** `budget_tokens` sigue deprecado. Usar `max_tokens` únicamente.

### Claude Managed Agents (public beta — lanzado 8 abril 2026)
- Header: `managed-agents-2026-04-01`
- Herramientas nativas: bash, read, write, edit, glob, grep, web_fetch, web_search
- **Memory stores:** el agente recuerda entre sesiones (preferencias, convenciones del proyecto, errores previos)
- Precio runtime: $0.08 USD/hora de agente
- Clientes actuales: Notion, Rakuten, Asana
- **Implicación estratégica:** Posicionarnos como implementadores certificados en LATAM — nadie lo tiene todavía

### The Advisor Tool (public beta)
- Patrón: Haiku ejecuta, Opus aconseja mid-generation
- Ahorro estimado: 60-72% en costo vs. usar Opus directo
- **Acción:** Jarvis evalúa integrar este patrón en flujos de la Agencia

### Batch API — nueva feature
- Opus 4.7, Opus 4.6 y Sonnet 4.6 soportan hasta **300k tokens de output** con header `output-300k-2026-03-24`
- Útil para Data Reporting Agents (grandes volúmenes de datos)

### GitHub Trending — Repos clave

| Repo | Estrellas | Relevancia |
|------|-----------|-----------|
| `paperclipai/paperclip` | 53,000+ | Orquestador CEO-level. Ya listado en CLAUDE.md — evaluar integración real esta semana |
| `NousResearch/hermes-agent` | +32,572 esta semana | Arquitectura evolutiva + adaptador Paperclip. Monitorear |
| `thedotmack/claude-mem` | +753 | Memoria comprimida para Claude Code. Útil para Jade |
| `browser-use/browser-use` | 87,448 totales | Infra para agentes web. Alejo revisa para Computer Use |
| `coleam00/Archon` | +612 | Constructor de harness deterministico con IA |

**Tendencia macro:** cluster "zero-human company" — OpenClaw, ClawCompany y Paperclip lideran la narrativa de empresas operadas 100% por agentes.

### Skills de la Comunidad — Recomendadas por agente

| Agente | Skill | Por qué ahora |
|--------|-------|---------------|
| Sasha | `security-auditor` (Antigravity) | OWASP LLM Top 10:2025 con nuevos vectores |
| Sasha | `fastapi-expert` (interna) | CVE-2026-33017 activo — patrón FastAPI |
| Brook | `postgres-best-practices` (Supabase oficial) | RLS desactivado por defecto sigue siendo #1 riesgo |
| Brook | `web-builder` (interna) | Next.js 15 + Tailwind 4 = stack dominante 2026 |
| Erik | `stitch-mcp` (interna) | Design-to-code más rápido del mercado |
| Cinthya | `n8n-advanced` (interna) | AI Agent nodes con RAG — tendencia dominante |

**Dato para Jarvis:** Agent Skills son ahora **módulos nativos en Claude Managed Agents**. Hay arquitectura oficial para empaquetar skills. Revisar si la estructura de `.claude/skills/` debe adaptarse.

---

## Seguridad & CVEs

### CVEs críticos del stack

| CVE | Sistema | CVSS | Estado |
|-----|---------|------|--------|
| CVE-2026-33017 | Langflow/FastAPI pattern | 9.3 | Explotado activamente desde 17 marzo |
| CVE-2026-27704 | Flutter SDK <3.41 / Dart <3.11 | Crítico | Path traversal en pub install |
| CVE-2025-48757 | Supabase RLS (via Lovable) | Alto | 170+ apps expuestas, patrón activo |
| Node.js Jan 2026 | Node.js (múltiples CVEs) | Varios | Release de seguridad con 8 CVEs |

### OWASP LLM Top 10:2025 — Nuevos vectores para Ego/Cyber Neo

- **LLM07 — System Prompt Leakage** (NUEVO) — exposición de system prompts con credentials
- **LLM08 — Vector and Embedding Weaknesses** (NUEVO) — RAG poisoning, vector DB attacks
- **LLM10 — Unbounded Consumption** — costos sin límite (aplica directamente a la Agencia)
- **Acción:** Ego integra LLM07 y LLM08 al checklist de auditoría de Cyber Neo

---

## Inteligencia Comercial

### Competitive Intelligence

Competidores colombianos directos: Agentesia.agency, Automaxia, AgenciaIA.com.co — todos venden chatbots y automatización básica. **Ninguno declara stack Claude/Anthropic ni capacidad full-stack.** Precio dumping: $30-70/hr.

**Diferenciador clave de la Agencia:** Agentes Claude + FastAPI + Flutter + n8n + Supabase en stack completo. Precio justificado 3-5x mayor.

### Benchmarking de Precios 2026

| Tipo | Rango |
|------|-------|
| Proyectos automatización IA | $15,000–60,000 USD (sweet spot para la Agencia) |
| Retainer mensual | $3,000–8,000 USD/mes |
| Agentes enterprise | $60,000–150,000 USD |

### Market Intelligence — Colombia

- **60% de empresas colombianas** ya tienen pilotos de IA (CIO Playbook 2026)
- **72% quieren IA pero no saben implementarla** → clientes potenciales directos
- Colombia: 4to país en VC en LATAM con $224M en Q1 2026
- **Mercado agentes IA LATAM:** $240M USD en 2026, creciendo 22-50% anual

### Evento CRÍTICO para Leo

**WOBI on AI & Business Transformation — 28 abril 2026, Medellín**
- 600 CEOs y C-Level de Colombia
- Expositores: Andrew Mayne (OpenAI), Terry Gutiérrez (Tesla LATAM)
- **Pitch para Leo:** "Somos la única agencia en Colombia que construye sobre Claude Managed Agents end-to-end."
- **Acción urgente:** Leo confirma asistencia. Jarvis prepara demo de Claude Managed Agents antes del 28.

### Hiring Intelligence — Arquitecto de Soluciones

| Perfil | Salario recomendado |
|--------|-------------------|
| Colombia local | COP 20-30M/mes |
| Remoto en USD | $60,000–80,000 USD/año |

Canales: Himalayas.app, Remote Rocketship, comunidades de Platzi alumni, StartCo Medellín.

---

## Papers — Hallazgos Relevantes

- **"Fail-open pipelines"** (arxiv 2604.01647): LLMs producen outputs confiados y bien estructurados que son sutilmente incorrectos y se propagan downstream. El patrón de falla más peligroso para Ego/Cyber Neo.
- **"Dynamic Attentional Context Scoping"**: aislar contexto por agente en orquestación multi-agente. Directamente aplicable a la arquitectura de la Agencia.
- **"Power Laws in Multi-Agent Systems"**: jerarquías de conocimiento no intencionadas emergen en sistemas multi-agente. Para Jarvis: roles más definidos evitan dominancia sistémica de un agente.

---

## Acciones por Agente

| Agente | Acción | Urgencia |
|--------|--------|---------|
| **Sasha** | Verificar versión Flutter — actualizar a 3.41.0 y Dart 3.11.0 (CVE-2026-27704) | 🔴 HOY |
| **Sasha** | Migrar cualquier uso de `claude-3-haiku` a `claude-haiku-4-5-20251001` | 🔴 HOY |
| **Sasha** | Auditar endpoints FastAPI sin autenticación (patrón CVE-2026-33017) | 🔴 MAÑANA |
| **Brook** | Verificar RLS activo en TODAS las tablas de Data Reporting Agents | 🟡 ESTA SEMANA |
| **Jarvis** | Migrar a `claude-opus-4-7` (mismo precio, 1M contexto, mejor agentic) | 🟡 ESTA SEMANA |
| **Jarvis** | Evaluar Paperclip como orquestador real de la Agencia | 🟡 ESTA SEMANA |
| **Jarvis** | Preparar demo Claude Managed Agents para WOBI (28 abril) | 🟡 URGENTE |
| **Leo** | Confirmar asistencia WOBI 28 abril Medellín — 600 CEOs | 🔴 ESTA SEMANA |
| **Ego** | Integrar LLM07 y LLM08 al checklist de Cyber Neo | 🟡 ESTA SEMANA |
| **Ego** | Migrar a `claude-opus-4-7` | 🟡 ESTA SEMANA |

---

## Fuentes

- Models Overview — platform.claude.com
- Claude Managed Agents — platform.claude.com
- Anthropic Release Notes — releasebot.io
- CVE-2026-33017 — The Hacker News
- CVE-2026-27704 — SentinelOne
- OWASP LLM Top 10:2025 — genai.owasp.org
- Paperclip — Towards AI / GitHub
- GitHub Trending Agents Radar — abril 2026
- SiliconANGLE — Claude Managed Agents launch
- CIO Playbook 2026 — ImpactoTIC
- WOBI Medellín 2026 — wbf.wobi.com
- Crunchbase LATAM Q1 2026

---

*Próxima actualización: martes 21 abril — foco: comunidades + papers + seguridad*
