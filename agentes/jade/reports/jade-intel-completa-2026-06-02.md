# Intel Completa — Lunes 2 Junio 2026
**Jade — Directora de Intel & Capacitaciones**
**Foco del día:** GitHub + Tododeia (Tech Monday)

---

## 🔴 CRÍTICO — ACCIÓN INMEDIATA

### 1. CVE-2026-48710 "BadHost" — FastAPI/Starlette Auth Bypass
**CVSS: CRÍTICO | AFECTA: asesor-imagen-ai backend + cualquier FastAPI en la Agencia**

Un carácter malformado en el header `Host` permite bypassear autenticación completamente. Afecta **todas las versiones de Starlette < 1.0.1** y por extensión FastAPI, vLLM, LiteLLM, MCP servers y AI agent backends.

- **Acción para Sasha:** Verificar versión de Starlette en `asesor-imagen-ai/backend/requirements.txt`. Actualizar a Starlette ≥ 1.0.1 YA.
- **CVE adicional:** CVE-2026-2978 — RCE en FastAPI < 0.115.8 (CVSS 9.8). Verificar versión instalada.
- **CVE adicional:** CVE-2026-23996 — Timing attack en API key validation.

### 2. OpenClaw Vulnerabilidades Activas (4 CVEs en cadena)
**Si ASTECIA usa OpenClaw en WhatsApp — revisar URGENTE**

- CVE-2026-44112: CVSS 9.6 (más severo)
- CVE-2026-44115: CVSS 8.8 — command validation bypass + shell execution
- CVE-2026-25253: CVSS 8.8 — RCE via WebSocket hijacking
- **ClawHavoc Campaign:** 1,184 skills maliciosos en ClawHub con keyloggers + Atomic Stealer
- **Fix:** Actualizar a OpenClaw versión 2026.4.22+

### 3. Claude Agent SDK — Cambio de Facturación JUNIO 15
**Impacta costos de operación de la Agencia**

Desde el **15 de junio de 2026**, Agent SDK y `claude -p` ya NO descuentan del plan principal. Nuevo pool separado:
- Pro: $20/mes crédito Agent SDK
- Max 5x: $100/mes
- Max 20x: $200/mes
- Créditos no se acumulan, se reinician mensualmente
- Afecta: GitHub Actions integration, terceros que autentican vía Agent SDK

---

## 🟡 IMPORTANTE — Próximas 2 semanas

### Tendencias Técnicas

#### A. MCP Servers — 492 expuestos sin autenticación
Trend Micro encontró 492 MCP servers en producción con zero authentication. 4 CVEs críticos:
- Command injection, SSRF, one-click RCE, privilege escalation
- **Para Sasha/Alejo:** Si algún MCP server de la Agencia está expuesto, añadir auth middleware.

#### B. Supabase — Nuevos defaults de seguridad (Mayo 30)
Cambio importante: tablas ya **NO se exponen al Data API por defecto** en proyectos nuevos.
- RLS habilitado por default en Table Editor
- Warning visual para tablas sin RLS
- Email alerts al owner si tabla sin RLS detectada
- **Para Sasha:** Revisar migraciones de `asesor-imagen-ai` contra estos nuevos defaults.

#### C. Paperclip AI — 53,000 GitHub stars (lanzado Mar 2026)
La infraestructura de orquestación que ya está en nuestro CLAUDE.md creció exponencialmente:
- MIT licensed, self-hosted, Node.js + React + PostgreSQL
- Atomic task execution + budget enforcement
- Integra: Claude Code, OpenClaw, Codex, Python scripts, HTTP webhooks
- **Para Jarvis:** Evaluar integración activa en la Agencia este mes.

#### D. OWL Framework — #1 GAIA benchmark (19.8k stars, actualizado Jun 1)
Built on CAMEL-AI, score 58.18 en GAIA. Features clave:
- MCP tool calling nativo (MCPToolkit)
- Browser automation via Playwright
- Multimodal (video, audio, imágenes)
- FileWriteToolkit + TerminalToolkit
- **Para Jade (capacitación):** Evaluar para workflows avanzados de Cinthya.

#### E. CVE-2025-27363 — FreeType/Flutter (CVSS 8.1, en KEV de CISA)
Out-of-bounds write vía Skia → potencial RCE en apps Flutter.
- En catálogo CISA KEV (exploited in the wild)
- **Para Sasha:** Verificar versión de Flutter SDK en `teclado-senias` y `asesor-imagen-ai`. Actualizar Flutter si < versión que incluye fix.

### Oportunidades Comerciales

#### A. Mercado LATAM para Agencias de Agentes IA
- Pricing de mercado para agencias de agentes: $2,500–$15,000 por automatización, $50K–$500K proyectos complejos
- Colombia tiene 15,000+ graduados tech/año, fuerte demanda nearshore
- Empresas US están contratando IA nearshore Colombia a $60K–$110K/year
- **Para Leo:** Posicionar la Agencia en el segmento de automatización ($5K–$20K/proyecto) con diferenciador de multi-agentes especializados.

#### B. Google Antigravity — Plataforma de Skills Abierta
Google Antigravity (lanzado Google I/O mayo 19, 2026): Agent skills ahora funcionan en Gemini CLI, VS Code, GitHub Copilot, ChatGPT, Cursor, Figma, Notion.
- Skills de Claude Code ya son cross-platform
- **Oportunidad:** Publicar skills de la Agencia en el ecosistema para generar leads.

---

## 🟢 INTERESANTE — Próximos 30 días

### Frameworks Multi-Agente a Vigilar
| Framework | Stars | Diferenciador |
|-----------|-------|---------------|
| OWL (camel-ai) | 19.8k | GAIA #1, MCP nativo, multimodal |
| CAMEL | 17.1k | "El primero y el mejor", scaling laws |
| PraisonAI | En ascenso | 100+ LLMs, deploy en 5 líneas, RAG built-in |
| Agno | Creciendo | Runtime + control plane para scale |
| AgentScope | Alibaba | Distributed deployment, fault tolerance |
| Eigent | Nuevo | Desktop app, alternativa local a Cowork |

### Research Papers Relevantes
- **CORAL**: Multi-agent systems que se auto-evolucionan via shared persistent memory (NeurIPS)
- **Agent Scaling Laws**: CAMEL buscando las "scaling laws of agents" — implicaciones para cómo construimos la Agencia

### Seguridad en Tendencia
- **SymJack**: Symlink-hijack RCE afectando 6 AI coding agents (including Claude Code)
- **TrustFall**: One-click RCE en Claude Code, Cursor, Gemini CLI, GitHub Copilot
- **Microsoft Copilot backdoor**: Indirect injection → persistent backdoor vía DEF CON demo

### Competitive Intelligence
- Ecosistema de agencias AI está madurando rápido
- Precios AI SEO: $3,200/mes promedio — oportunidad para diferenciar con automatización más profunda
- Agencias que cobran por outcome (per-resolution, per-session) están ganando vs fixed retainers

---

## 🎯 Hiring Intel — Arquitecto de Soluciones

**Benchmarks Colombia 2026:**
- Solutions Architect (general): $53,300/año promedio, senior hasta $95,940
- Cloud SA: $52,600–$94,680/año
- Medellín específico: COP ~116M/año (~$28K USD)
- Con especialización AI (mercado US): $113,028/año

**Recomendación para Jarvis:**
- Perfil en Colombia: buscar en $40K–$70K USD/año (remote, nearshore)
- Canales: LinkedIn Colombia, Tecla.io, HireLATAM, comunidades Discord de Anthropic/LangChain
- Diferenciador para atraer talento: trabajar con Claude Agent SDK + Paperclip (stack de vanguardia)

---

## 📋 ACCIONES INMEDIATAS POR AGENTE

**@sasha** — URGENTE:
1. Actualizar Starlette → ≥ 1.0.1 en `asesor-imagen-ai/backend/requirements.txt`
2. Verificar FastAPI version → actualizar si < 0.115.8
3. Verificar Flutter SDK version en todos los proyectos (CVE-2025-27363)
4. Revisar si algún MCP server está expuesto sin auth

**@jarvis** — Esta semana:
1. Evaluar integración de Paperclip en la Agencia (53k stars, MIT, fit perfecto)
2. Revisar si OpenClaw versión es ≥ 2026.4.22 (ASTECIA lo usa vía WhatsApp)
3. Preparar para cambio de facturación Agent SDK (junio 15) — revisar plan actual

**@leo**:
1. Actualizar argumentario de precios: referencia competitiva $5K–$20K/automatización
2. Mencionar diferenciador: skills cross-platform con Google Antigravity

**@jarvis** (hiring):
1. Arquitecto SA: buscar $40–70K USD remote, canales: Tecla, HireLATAM, Discord Anthropic

---

## 🔗 Skills Nuevas Identificadas para el Equipo

| Skill | Relevante para | Prioridad |
|-------|----------------|-----------|
| OWL/CAMEL framework | Cinthya, Jarvis | 🟡 Media |
| MCP Security hardening | Sasha, Alejo | 🔴 Alta |
| Paperclip integration | Jarvis, Cinthya | 🟡 Media |
| Google Antigravity skills publishing | Erik, Brook | 🟢 Baja |
| Agent SDK dual-bucket billing | Jarvis | 🔴 Alta (Jun 15) |

---

*Generado por Jade — Tarea programada 02/06/2026 lunes | Fuentes: WebSearch, GitHub, Dark Reading, Hacker News, Supabase Changelog*
