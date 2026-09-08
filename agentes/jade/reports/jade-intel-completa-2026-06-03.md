# Intel Completa — Martes 3 Junio 2026
**Jade — Directora de Intel & Capacitaciones**
*Foco del día: Comunidades + Papers + Seguridad*

---

## 🔴 CRÍTICO — Actuar INMEDIATAMENTE

### 1. ANTHROPIC BILLING CHANGE — 12 DÍAS (Deadline: 15 junio)
**Impacto directo en la Agencia**

El 15 de junio 2026, Anthropic mueve TODA la ejecución de Agent SDK a un pool separado de créditos:
- `claude -p`, Claude Code, Claude Code GitHub Actions, Agent SDK → salen del plan Pro/Max/Team
- Nuevo pool mensual: **$20 Pro | $100 Max 5x | $200 Max 20x**
- Los créditos se consumen a tarifas API estándar. **NO hacen rollover**.
- Cuando el crédito se agota → las llamadas Agent SDK FALLAN hasta el próximo ciclo

**Por qué es crítico para la Agencia:**
- Claude Code (nuestra herramienta principal) mueve a este pool
- El subsidio anterior: un plan Pro tenía acceso a $300-600 equivalente en API. Ahora son $20.
- Si el equipo usa Claude Code intensivamente en Sprint 1 MAPER Hub, los $20 pueden agotarse en días
- **Acción Jarvis**: Revisar qué plan se usa, evaluar upgrade a Max 20x ($200/mes) antes del 15 junio
- **Acción Sasha/Brook**: Calibrar uso de Claude Code, priorizar sessions largas sobre muchas sessions cortas (prompt caching)

Fuente: [Anthropic Ends Subscription Subsidy for Agents June 15](https://www.techtimes.com/articles/317625/20260602/anthropic-ends-subscription-subsidy-agents-june-15-credit-pool-replaces-flat-rate-access.htm)

---

### 2. TRUSTAFALL + SYMJACK — RCE EN CLAUDE CODE (Confirmado)
**Vulnerabilidades que afectan directamente nuestras herramientas**

Adversa AI divulgó dos vulnerabilidades en mayo-junio 2026:

- **SymJack**: Symlink-hijack RCE afectando 6 AI coding agents
- **TrustFall**: One-click RCE que alcanza **Claude Code**, Cursor, Gemini CLI, y GitHub Copilot

**Impacto**: Un actor malicioso puede lograr ejecución de código en la máquina del desarrollador si abre un repositorio o procesa un archivo malicioso mientras Claude Code está activo.

**Acción @sasha**: Investigar el patch status de TrustFall en Claude Code. Verificar versión instalada del CLI. Evaluar si hay workaround disponible mientras se espera patch oficial.

Fuente: [Top Agentic AI Security Resources — June 2026](https://adversa.ai/blog/top-agentic-ai-security-resources-june-2026/)

---

### 3. MCP SECURITY CRISIS — 40+ CVEs ACTIVOS
**Afecta nuestra infraestructura de agentes**

Estado actual de seguridad MCP (Model Context Protocol) a junio 2026:
- **40+ CVEs** divulgados contra implementaciones MCP (Python, TypeScript, Java, Rust SDKs)
- **36.7%** de 7,000+ servidores MCP analizados vulnerables a SSRF
- **492 servidores MCP** expuestos en internet con **zero authentication**
- ClawHub (registry de skills) — primer registry en ser sistemáticamente envenenado a escala

**Vulnerabilidad crítica de diseño MCP**:
OX Security y Hacker News reportan una debilidad "by design" en la arquitectura MCP que puede habilitar RCE y tiene efectos cascada en el AI supply chain — acceso directo a bases de datos internas, API keys, y chat histories.

**Acción @sasha**: 
1. Auditar todos los MCP servers configurados en la Agencia (`.claude/settings.json`)
2. Verificar que ningún MCP server esté expuesto sin autenticación
3. Revisar que no usemos skills de ClawHub sin validar su origen
4. El proyecto MAPER Hub debe incluir MCP security en el audit de Cyber Neo

Fuente: [MCP Security 40+ CVEs](https://dev.to/piiiico/mcp-security-vulnerabilities-in-2026-40-cves-and-counting-4pco) | [OX Security Critical MCP](https://www.ox.security/blog/the-mother-of-all-ai-supply-chains-critical-systemic-vulnerability-at-the-core-of-the-mcp/)

---

## 🟡 IMPORTANTE — Próximas 2 semanas

### 4. OWASP TOP 10 PARA APLICACIONES AGÉNTICAS 2026 — PUBLICADO
El framework oficial ya está disponible. Crítico para el diseño de MAPER Hub y todos los proyectos con agentes.

Top 10 para 2026 (relevante para la Agencia):
1. **Agent Goal Hijacking** — injection cambia objetivos del agente
2. **Tool Misuse & Unintended Execution** — herramientas ejecutadas fuera de scope
3. **Identity & Privilege Abuse** — escalación de privilegios entre agentes
4. **Missing/Weak Guardrails** — sin límites en comportamiento del agente
5. **Sensitive Data Disclosure** — PII/secrets expuestos a través de agentes
6. **Data Poisoning** — datos de entrenamiento/contexto manipulados
7. **Resource Exhaustion** — token flooding, loop infinitos
8. **Supply Chain Vulnerabilities** — skills/tools maliciosos en registries
9. **Insecure Inter-Agent Communication** — no hay autenticación A2A
10. **Advanced Prompt Injection** — cross-agent injection

**Acción @sasha**: MAPER Hub Sprint 1 debe incluir revisión contra estos 10 puntos. Alejo debe usar este framework como checklist en ADR de seguridad.

Fuente: [OWASP Top 10 Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)

---

### 5. OPTIMIZACIÓN DE COSTOS CLAUDE API — 95% DE AHORRO POSIBLE
**Crítico para Sprint 1 MAPER Hub y todos los proyectos**

Con el nuevo billing del 15 junio, optimización de costos es prioridad 1.

**Los 4 levers que funcionan (validados en 30 audits)**:
1. **Prompt Caching** → hasta 90% de ahorro en input tokens
2. **Batch API** → 50% off en input + output (para tareas no-tiempo-real)
3. **Model tier routing** → Haiku para tareas simples, Opus para razonamiento complejo
4. **Context window pruning** → los agentes queman tokens 10-100x más rápido que chatbots

**Combinación óptima**: Prompt Caching + Batch API = hasta 95% de ahorro

**IMPORTANTE - tokenizer nuevo**:
Opus 4.7+ usa tokenizer nuevo que consume **35% MÁS tokens** para el mismo texto vs modelos anteriores. Los presupuestos deben recalibrarse.

**Costos actuales (mayo 2026)**:
- Haiku 4.5: $1/M input — $5/M output
- Sonnet 4.6: $3/M input — $15/M output  
- Opus 4.8: $5/M input — $25/M output

**Acción @sasha**: Implementar prompt caching en TODOS los system prompts de agentes. Implementar model routing (Haiku para clasificación, Sonnet para código, Opus solo para decisiones críticas).

Fuente: [Claude API Cost Optimization 2026](https://leanopstech.com/blog/agentic-ai-cost-runaway-token-budget-2026/) | [Prompt Caching Guide](https://www.finout.io/blog/anthropic-api-pricing)

---

### 6. PAPER: CORAL — MULTI-AGENT SELF-EVOLUTION
**Arquitectura relevante para la Agencia**

Paper publicado en arxiv (junio 2026): **CORAL: Towards Autonomous Multi-Agent Evolution for Open-Ended Discovery**

- Sistemas multi-agente con memoria persistente compartida + ejecución asíncrona + intervenciones heartbeat
- Resultados: **3-10x mejores tasas de mejora** vs baselines de búsqueda evolutiva fija
- Los agentes se auto-evolucionan sin intervención humana en tareas matemáticas, algorítmicas y de sistemas

**Por qué importa para la Agencia**: Nuestra arquitectura actual (Jarvis → Sasha/Brook/Erik/etc.) es jerárquica y síncrona. CORAL sugiere que la memoria persistente compartida entre agentes + ejecución asíncrona puede multiplicar la capacidad 3-10x.

**Acción @jarvis/@alejo**: Evaluar adoptar memoria compartida entre agentes en la Agencia (actualmente cada agente tiene memoria separada). Este es un ADR para la reunión del sábado.

Fuente: [CORAL Paper](https://arxiv.org/list/cs.MA/recent)

---

### 7. n8n 2.0 — CAPACIDADES AGÉNTICAS NATIVAS
**Acción directa para @cinthya**

n8n 2.0 (lanzado enero 2026) incluye:
- **AI Agent Nodes** con soporte MCP nativo
- **Memoria persistente** entre ejecuciones de agentes
- **Sandboxed code execution** (seguridad mejorada)
- **Monitoring de reasoning y tool execution** en tiempo real
- **Full data sovereignty** — self-hosted con persistencia real

LangGraph superó a CrewAI en estrellas GitHub en early 2026 por adopción enterprise.
CrewAI: 45,900+ stars, 12M ejecuciones diarias en producción, soporte A2A nativo.

**Acción @cinthya**: Actualizar a n8n 2.0 y adoptar AI Agent Nodes con persistent memory para los workflows de la Agencia. Presentar propuesta de migración a Jarvis antes del sábado.

Fuente: [n8n 2026 AI Agents](https://n8n.io/ai-agents/) | [n8n Review 2026](https://dev.to/nova_gg/n8n-review-2026-i-used-it-for-8-months-to-build-ai-agents-honest-verdict-kif)

---

## 🟢 INTERESANTE — Próximos 30 días

### 8. OPENCLAW — 210K ESTRELLAS, FRAMEWORK BREAKOUT 2026
- Creado por el fundador de PSPDFKit, pasó de 9k a 210k+ estrellas en semanas
- **Feature única**: puede escribir sus propios nuevos skills (auto-extensión de capacidades)
- Casos de uso: developer workflow automation, web scraping, browser automation, scheduling proactivo
- *Nota de seguridad*: 4 CVEs críticos divulgados (CVE-2026-44112, CVSS 9.6). Evaluar con cuidado.

Fuente: [Top AI GitHub Repos 2026](https://fungies.io/top-github-repositories-ai-agent-frameworks-2026/)

### 9. COMPETENCIA LATAM — PATAGON AI
- Startup de AI agents para ventas/marketing en Colombia, Brasil, México, Chile, Argentina
- Raise: **$1.1M** (OneVC + 17Sigma)
- **Análisis**: Mismo espacio que la Agencia pero enfocado en marketing automation. Diferenciador nuestro: agentes técnicos complejos + vertical industrial (MAPER, manufactura).

Fuente: [10 Rising AI Startups LATAM 2026](https://www.latamrepublic.com/top-10-emerging-ai-startups-in-latin-america-pre-series-a/)

### 10. MERCADO LATAM — SEÑAL POSITIVA
- AI startups = **45% de emerging tech**, **60% del seed funding** en LATAM ($3.8B dataset)
- Google for Startups Accelerator AI First — programa activo para LATAM
- Conpes Colombia + programas de no-repayable funds para innovación IA disponibles

Fuente: [LATAM AI Investment](https://www.thomsonreuters.com/en-us/posts/technology/latam-ai-investment/)

---

## 🎯 ACCIONES INMEDIATAS

```
@jarvis:
  - URGENTE (antes del 15 jun): Revisar plan Claude actual y evaluar upgrade a Max 20x
  - Reunión sábado: Incluir ADR sobre memoria compartida entre agentes (CORAL paper)
  - Incluir billing change en risk register MAPER Hub

@sasha:
  - HOY: Investigar TrustFall patch status en Claude Code CLI (versión instalada)
  - HOY: Auditar MCP servers en .claude/settings.json — verificar ninguno está sin auth
  - Sprint 1 MAPER Hub: Implementar prompt caching en system prompts de agentes
  - Sprint 1 MAPER Hub: Model routing (Haiku/Sonnet/Opus) para controlar costos post-15jun

@cinthya:
  - Esta semana: Actualizar a n8n 2.0, habilitar persistent agent memory
  - Propuesta de migración AI Agent Nodes para Jarvis antes del sábado

@alejo:
  - ADR de seguridad para MAPER Hub debe incluir OWASP Top 10 Agentic 2026
  - Evaluar CORAL architecture para memoria compartida entre agentes Agencia

@cyber_neo:
  - MAPER Hub audit debe incluir MCP security checklist
  - Revisar CVE-2026-44338 (PraisonAI), CVE-2026-44112 (OpenClaw) si usamos estos frameworks
```

---

## Estadísticas del día

| Métrica | Valor |
|---------|-------|
| Fuentes consultadas | 12 búsquedas web |
| CVEs identificados | 8 (3 críticos) |
| Oportunidades comerciales | 2 (Patagon AI radar, LATAM market signal) |
| Papers relevantes | 2 (CORAL, DyTopo) |
| Acciones generadas | 11 |
| Días para deadline crítico | 12 (billing change 15 jun) |

---

*Jade — Intel Diaria 2026-06-03 | Siguiente brief: Miércoles 4 jun (pipeline comercial + competencia)*
