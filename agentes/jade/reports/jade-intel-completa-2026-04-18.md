# Intel Completa — 18 Abril 2026 (Sábado — Junta Directiva)
**Generado por:** Jade — Directora Intel & Capacitaciones
**Fecha:** 18 de abril de 2026
**Tipo:** Sábado → Brief Ejecutivo + Intel Completa

---

## RESUMEN EJECUTIVO

| Prioridad | Hallazgo | Acción | Responsable |
|-----------|----------|--------|-------------|
| 🔴 CRÍTICO | Claude Opus 4.7 lanzado el 16 abril | Migrar agentes opus esta semana | Jarvis |
| 🔴 CRÍTICO | On-demand tool loading → 60-80% menos costo Claude API | Implementar patrón esta semana | Sasha |
| 🔴 CRÍTICO | Node.js CVE-2026-21712/21637 — vulnerabilidad TLS | Actualizar Node.js hoy | Sasha |
| 🔴 CRÍTICO | Supabase RLS — patrón 170+ apps expuestas | Auditar proyectos activos | Sasha + Cyber Neo |
| 🟡 IMPORTANTE | Claude Managed Agents beta (alternativa a Paperclip) | Evaluar para Data Reporting Agents | Jarvis + Cinthya |
| 🟡 IMPORTANTE | OWASP Top 10 for Agentic Apps 2026 publicado | Actualizar checklist de seguridad | Sasha + Ego |
| 🟡 IMPORTANTE | Arquitecto: contratar a $180M-220M COP/año es competitivo | Avanzar hiring urgente | Jarvis |
| 🟢 INTERESANTE | StartCo Q3 2026 Medellín — evento networking obligatorio | Agendar para Q3 | Juan Camilo + Leo |

---

## TENDENCIAS TÉCNICAS

### 1. Claude Opus 4.7 — NUEVO (16 Abril 2026) 🔴
**ID del modelo:** `claude-opus-4-7`
**Disponible en:** API directa de Anthropic + AWS Bedrock

**Mejoras clave:**
- Software engineering de larga duración mejorado
- Vision de alta resolución mejorada
- Nuevos effort controls y task budgets
- Mejor rendimiento en tareas de coding complejas

**Impacto para la Agencia:**
Los agentes opus del equipo (Jarvis, Ego, Sasha, Leo) deben migrar a `claude-opus-4-7` esta semana. El CLAUDE.md debe actualizarse para reflejar el nuevo model ID.

**Acción:** @jarvis actualizar CLAUDE.md + todos los archivos de agentes que referencien `claude-opus-4-6`.

---

### 2. On-demand Tool Loading — Reducción de Costos 60-80% 🔴
**Fuente:** Medium + TokenOptimize.dev

**La técnica:**
Cargar solo las definiciones de tools que cada sub-agente necesita en su turno específico, en lugar de pasar todos los tools disponibles en cada llamada.

**Resultados reales documentados:**
- Overhead de tools: de 134K → 8.7K tokens (**85% reducción**)
- Combinado con prompt caching: **70-90% ahorro en input tokens total**
- En producción con múltiples agentes opus: **60-80% reducción del costo mensual**

**Impacto para la Agencia:**
Jarvis, Ego y Sasha corren simultáneamente con muchos tools. Aplicar este patrón puede cambiar radicalmente el burn rate de Claude API sin sacrificar calidad.

**Acción:** @sasha implementar on-demand tool loading como patrón estándar en todos los agentes. Prioridad: Jarvis y Ego (mayor costo actual).

---

### 3. Claude Managed Agents (Beta Pública — 8 Abril 2026) 🟡
**Header de API:** `managed-agents-2026-04-01`
**Precio:** costo del modelo + $0.08/hora de runtime
**Clientes actuales:** Notion, Rakuten, Asana

**Qué ofrece:**
- Contenedores aislados por agente (sandboxing automático)
- Tools integradas sin configuración
- Streaming SSE nativo
- No requiere infraestructura propia

**Vs Paperclip:**
Paperclip ofrece mejor governance, chat threads con IA, políticas de aprobación multi-etapa, y es open-source. Claude Managed Agents es más simple de arrancar pero con menos control.

**Recomendación:** Para el MVP de Data Reporting Agents, evaluar Claude Managed Agents para los runs autónomos. Menor tiempo de setup, menor costo de infra. Paperclip mejor para la Agencia en producción a largo plazo.

**Acción:** @cinthya hacer piloto de Claude Managed Agents con un flujo simple de Data Reporting Agents.

---

### 4. Paperclip v2026.416.0 — Updates Clave 🟡
**Estrellas GitHub:** 43,900 (uno de los repos de crecimiento más rápido de la historia de GitHub)

**Nuevas features:**
- Chat threads por issue con IA integrada
- Políticas de ejecución con flujos de aprobación multi-etapa
- Workspaces de ejecución experimentales con control de inicio/parada

**Impacto:** Exactamente lo que Jarvis necesita: governance, aprobaciones y trazabilidad de runs a escala. La decisión de usar Paperclip como plataforma principal sigue siendo correcta.

---

### 5. Google ADK Python v1.26.0 — Watch 🟢
**Estrellas:** 8,200 desde lanzamiento
**Features:** Multi-agente con estado, memoria, orquestación jerárquica, A2A nativo

**Por qué importa:**
Competencia directa al Claude Agent SDK. Si un cliente no quiere dependencia de Anthropic o pide stack multi-nube, este es el alternativo más maduro disponible.

**Recomendación:** Sasha lo estudia, la Agencia no lo adopta aún. Mantener en radar.

---

### 6. Agent Skills Beta — Confirmación ✅
**Header:** `skills-2025-10-02`

El directorio `.claude/skills/` que ya tiene la Agencia está **100% alineado con el estándar oficial de Anthropic**. La Agencia tiene ventaja sobre otras agencias que aún no adoptan este patrón.

---

### 7. API Code Execution GRATUITA con Web Search 🟡
Cuando se usa code execution combinado con web_search o web_fetch, el costo de code execution es **$0**.

**Impacto:** Jade y Yang pueden usar code execution intensivamente en sus investigaciones sin costo adicional.

---

### 8. Advisor Tool (Beta) 🟢
**Descripción:** Empareja un modelo ejecutor rápido con un modelo advisor de alta inteligencia que da guía estratégica mid-generation.

**Caso de uso ideal:** Jarvis como advisor de sub-agentes Sasha/Brook durante ejecución de features complejos. Reducción de errores + mejor calidad sin relanzar el agente completo.

---

## SEGURIDAD Y VULNERABILIDADES

### CVE-2026-21712 / 21637 — Node.js 🔴 CRÍTICO
**Severidad:** Alta | **Afecta:** Node.js 20.x, 22.x, 24.x
- **21712:** Crash del proceso via frames HTTP/2 malformados
- **21637:** Assertion error via URL malformada
- Fix de TLS callbacks incompleto en versiones anteriores

**Acción:** Actualizar Node.js a la release de seguridad de marzo 2026. Revisar `package.json` en todos los proyectos activos.

---

### Supabase RLS — Patrón de Exposición Masiva 🔴 CRÍTICO
**Patrón:** CVE-2025-48757 + variantes 2026
**Problema:** 170+ aplicaciones expusieron credenciales porque el código generado por IA no activa Row Level Security (RLS) por defecto.

**Proyectos en riesgo:** Teclado de Señas, Data Reporting Agents

**Acciones concretas:**
1. Auditar TODAS las tablas de Supabase en ambos proyectos
2. Verificar que RLS esté activo en cada tabla
3. Confirmar que `service_role` key NUNCA está expuesta al frontend
4. Revisar políticas RLS existentes

---

### CVE-2025-53773 — Prompt Injection → RCE en Agentes IA 🔴 CRÍTICO
**CVSS:** 9.6
**Afecta:** Cualquier agente IA con acceso a repositorios (PR descriptions, issues)

**Acción:** Ningún agente de la Agencia (Sasha, Jade) debe procesar PRs/issues sin sanitización. Aplicar output validation antes de ejecutar cualquier instrucción generada por LLM.

---

### Claude Code Leak via npm 🔴
**Fuente:** Hacker News (item 47609294) — Confirmado por Anthropic

El código fuente de Claude Code fue expuesto por error de packaging npm.

**Acción:** @sasha + @cyber-neo auditar dependencias npm en todos los proyectos activos. Verificar integridad de paquetes.

---

### OWASP Top 10 for Agentic Applications 2026 🟡 NUEVO ESTÁNDAR
**Publicado:** 2026 por OWASP GenAI Working Group

**Nuevas categorías cubiertas:**
1. Goal Misalignment
2. Tool Misuse
3. Delegated Trust
4. Inter-Agent Communication
5. Memory Poisoning
6. Emergent Autonomous Behavior
7. Prompt Injection (escalada — #1 amenaza)
8. Tool Poisoning via MCP
9. Credential Theft via MCP

**Acción:** @sasha revisar código de agentes contra este checklist. @ego incorporarlo en framework de auditorías. @cyber-neo agregar estos dominios a su checklist de 11 dominios.

---

### Prompt Injection — Escalada Generalizada 🟡
Incidentes subieron **340%** en 2026. MCP expande la superficie de ataque: tool poisoning y credential theft via MCP son vectores nuevos confirmados.

**Acción:** Todos los agentes que usen MCPs (Stitch, Apify, Apify RAG) deben validar que el contenido de tool results NO se ejecute como instrucciones del sistema.

---

### CVE-2026-39987 — Marimo Python RCE 🟡
**CVSS:** 9.3 | **Afecta:** Python, entornos notebook
WebSocket sin autenticación → RCE pre-auth.

**Acción:** Si el equipo usa notebooks (Jupyter/Marimo) para prototipar agentes, actualizar a versión 0.23.0+.

---

## INTELIGENCIA COMERCIAL

### Competencia en Colombia — Mapa del Campo

| Competidor | Posicionamiento | Diferenciador | Amenaza |
|------------|----------------|---------------|---------|
| **Automaxia** | "Agencia IA #1 Colombia" | Colombia + España, regional | Media — misma promesa pero sin multi-agente |
| **Wise Agents** | Presencia en 4 países (CO/MX/PE/US) | Expansión regional acelerada | Alta — el más similar a nosotros |
| **Agencia Digital AMD** | Marketing IA + e-commerce | Agentes voz y texto | Baja — foco distinto |
| **Coresis** | B2B técnico Colombia | Posicionamiento técnico | Media |
| **Bolmia** | Ventas + marketing automatizados | Nicho ventas | Baja |

**Diferenciador ÚNICO de la Agencia:** somos la única que vende **equipos coordinados de agentes especializados** (Jarvis + Sasha + Brook + Erik + Cinthya + Leo + Yang). Todos los competidores venden agentes aislados. Esta es nuestra fosa defensiva.

---

### Precios de Referencia del Mercado Colombiano 2026

| Servicio | Precio mercado | Nuestro posicionamiento |
|----------|---------------|------------------------|
| Chatbot con IA básico | $2M - $8M COP | No nuestro segmento |
| Automatización proceso end-to-end | $5M - $25M COP | Entrada low-end |
| Agente de voz con IA | $8M - $30M COP | Segmento medio |
| Sistema multi-agente coordinado | $50M+ COP | **Nuestro core** |
| Mantenimiento mensual | $1M - $5M COP | Recurringrevenue |

**Recomendación de Leo:** posicionarse desde $15M COP en adelante, con proyectos premium desde $50M+ COP para equipos multi-agente. Esto nos pone sobre todos los competidores identificados.

---

### Sectores con Mayor Demanda Activa 2026

**Top 3 para prospectar YA:**
1. **Fintech / Banca** — presupuesto grande, decisión rápida, casos de uso claros (fraud, onboarding, scoring)
2. **Retail / E-commerce** — temporada alta, necesitan automatización de atención al cliente
3. **Logística** — Colombia como hub regional, presión de optimización de costos

**Datos que respaldan:**
- 70% de empresas colombianas ya usan IA (RCN 2026)
- 89% planea destinar 1-15% de su presupuesto 2026 a IA generativa
- 54% de empresas en LatAm pasará experimentos de IA a producción en los próximos 6 meses

---

### TAM y Market Opportunity

| Métrica | Dato |
|---------|------|
| TAM IA en LatAm 2025 | USD 5.790 millones |
| TAM proyectado 2033 | USD 30.000+ millones |
| CAGR | 22% anual |
| Mercado SDR con IA 2026 | USD 5.810 millones (CAGR 32.3%) |
| Crecimiento agentic AI (Gartner) | +141% vs 2025 → $201.9B global |

**El timing es perfecto:** la demanda explota ahora mientras el mercado local todavía no tiene oferta de calidad consolidada.

---

### Funding Rounds — Hot Leads Potenciales

- **StartCo 2026 Medellín** (16-17 Abril, Plaza Mayor) — 350+ startups, $18M proyectados. Si la Agencia no estuvo, prioritario para Q3.
- **Dapper** (Cali, 2024) — IA para inteligencia regulatoria en mercados emergentes. Posible cliente para automatización de pipelines de datos.
- **Empresas post-Serie A/B en Colombia** — tienen capital fresco + urgencia de escalar con automatización.

---

### Hiring Intel — Arquitecto de Soluciones Senior con IA

| Nivel | Rango COP/año | USD/mes aprox. |
|-------|--------------|----------------|
| Promedio Colombia | $90M - $210M COP | $1.850 - $4.300 |
| Senior Solution Architect | $115M - $258M COP | $2.350 - $5.250 |
| Con especialidad IA (+25%) | $140M - $300M COP | $2.850 - $6.200 |

**Recomendación para Jarvis:**
- Rango competitivo: **$180M - $220M COP/año** ($3.700 - $4.500 USD/mes)
- Urgencia: OpenSistemas Colombia tiene vacante abierta similar — el mercado ya está competido
- Diferenciador para atraer talento: proyecto de agentes IA cutting-edge + autonomía técnica + posible equity

---

## PAPERS Y COMUNIDADES

### Papers Arxiv Relevantes

**"Towards a Science of Scaling Agent Systems"** (arXiv 2512.08296)
Evaluó 260 configuraciones, 6 benchmarks, 5 arquitecturas. Introduce principios cuantitativos de scaling. **Valida científicamente el modelo de Jarvis + sub-agentes paralelos.**

**"From Multi-Agent to Single-Agent: When Is Skill Distillation Beneficial?"** (arXiv 2604.01608)
Los sistemas multi-agente son mejores para tareas complejas, pero tienen overhead de coordinación y fragilidad de fase. **Ego debe vigilar bugs de coordinación como categoría de auditoría.**

**Estudio 4,700+ issues en multi-agent OSS** (arXiv 2601.07136)
Bugs más frecuentes: bugs (22%), infraestructura (14%), coordinación (10%). **Ego debe incorporar "bugs de coordinación" en sus auditorías formales.**

---

### Frameworks — Estado del Arte Abril 2026

| Framework | Stars | Recomendación para la Agencia |
|-----------|-------|-------------------------------|
| Claude Agent SDK | v0.1.48 | ✅ Framework nativo — seguir usando |
| CrewAI | 44,600 | Piloto para proyectos nuevos con roles definidos |
| LangGraph | v1.0.10 GA | Para flujos con ramas paralelas + approval gates |
| Langflow | 146,000 | Cinthya lo evalúa para workflows visuales de clientes |
| Google ADK | v1.26.0 | Radar — no prioritario aún |
| OpenAI Agents SDK | v0.10.2 | No alineado con stack Anthropic |

---

## ACCIONES PRIORIZADAS

### Para esta semana (CRÍTICO)

| # | Acción | Responsable | Urgencia |
|---|--------|-------------|---------|
| 1 | Migrar agentes opus a `claude-opus-4-7` | Jarvis | HOY |
| 2 | Actualizar CLAUDE.md con nuevo model ID | Jarvis | HOY |
| 3 | Auditar Supabase RLS en Teclado de Señas + Data Reporting | Sasha + Cyber Neo | Esta semana |
| 4 | Actualizar Node.js en proyectos activos | Sasha | Esta semana |
| 5 | Implementar on-demand tool loading en Jarvis + Ego | Sasha | Esta semana |
| 6 | Auditar dependencias npm (Claude Code leak) | Sasha + Cyber Neo | Esta semana |

### Próximas 2 semanas (IMPORTANTE)

| # | Acción | Responsable |
|---|--------|-------------|
| 7 | Evaluar Claude Managed Agents para Data Reporting Agents | Cinthya + Jarvis |
| 8 | Incorporar OWASP Agentic Apps 2026 en checklist de Ego | Ego + Sasha |
| 9 | Avanzar hiring Arquitecto — rango $180M-220M COP/año | Jarvis |
| 10 | Piloto de CrewAI para próximo proyecto con roles definidos | Sasha |
| 11 | Prospectar Fintech + Retail + Logística en Colombia | Leo + Yang |

### Próximos 30 días (INTERESANTE)

| # | Acción | Responsable |
|---|--------|-------------|
| 12 | Integrar AI Designer MCP en flujo Brook + Erik | Brook + Erik |
| 13 | Revisar Advisor Tool (beta) para Jarvis como advisor de sub-agentes | Jarvis |
| 14 | Agendar presencia en StartCo Q3 2026 Medellín | Juan Camilo + Leo |
| 15 | Evaluar Langflow para workflows visuales de clientes (Cinthya) | Cinthya |

---

*Generado automáticamente por Jade — Directora Intel & Capacitaciones*
*Próximo: Brief Ejecutivo → `jade-brief-junta-2026-04-18.md`*
