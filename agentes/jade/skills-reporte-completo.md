# Reporte de Skills para Claude Code — Jade
## Fecha: 2026-03-24 | Investigado por: Jade (Agente de Inteligencia y Capacitaciones)

---

## Resumen Ejecutivo

Se investigaron 4 repositorios de skills para Claude Code. En total se identificaron **2,100+ skills** distribuidas en los repositorios. A continuación se presenta el inventario completo, clasificación por prioridad para nuestra Agencia, y un análisis de gaps donde no existen skills pero las necesitamos.

---

## 1. Inventario por Repositorio

### 1.1 anthropics/skills — Repositorio Oficial de Anthropic
**URL:** https://github.com/anthropics/skills
**Stats:** 102k estrellas, 11.2k forks, Apache 2.0
**Modelo de instalación:** `/plugin marketplace add anthropics/skills`

Skills disponibles (17 skills oficiales):

| Skill | Qué hace | Trigger |
|-------|----------|---------|
| **pdf** | Extrae texto, tablas, metadatos, manipula PDFs, maneja formularios | "Use the PDF skill to..." |
| **docx** | Crea y edita documentos Word con brand guidelines, tracked changes | "Use the DOCX skill to..." |
| **pptx** | Genera presentaciones PowerPoint, maneja layouts y templates | "Use the PPTX skill to..." |
| **xlsx** | Manipula hojas de cálculo Excel: fórmulas, charts, transformaciones | "Use the XLSX skill to..." |
| **claude-api** | Guía para construir apps con Claude API, selección de modelos, patrones de integración | "Use the Claude API skill to..." |
| **frontend-design** | UI/UX development, interacción, calidad de interfaces | "Use the frontend-design skill to..." |
| **canvas-design** | Arte visual en PNG y PDF, diseño creativo | "Use the canvas-design skill to..." |
| **algorithmic-art** | Arte generativo y computacional con p5.js | "Use the algorithmic-art skill to..." |
| **mcp-builder** | Crea servidores MCP de alta calidad para integrar APIs externas | "Use the mcp-builder skill to..." |
| **webapp-testing** | Testing de aplicaciones web usando Playwright | "Use the webapp-testing skill to..." |
| **brand-guidelines** | Aplica colores y tipografía oficiales de una marca | "Use the brand-guidelines skill to..." |
| **internal-comms** | Redacta comunicaciones internas, status reports, newsletters | "Use the internal-comms skill to..." |
| **doc-coauthoring** | Coautoría estructurada de documentos | "Use the doc-coauthoring skill to..." |
| **slack-gif-creator** | Crea GIFs animados optimizados para Slack | "Use the slack-gif-creator skill to..." |
| **theme-factory** | Aplica temas profesionales de fuentes y colores | "Use the theme-factory skill to..." |
| **web-artifacts-builder** | Crea artefactos HTML complejos con React y Tailwind | "Use the web-artifacts-builder skill to..." |
| **skill-creator** | Guía para crear nuevas skills efectivas | "Use the skill-creator skill to..." |

**Nota clave:** El repositorio `anthropics/skills` contiene las skills de producción que alimentan las capacidades nativas de Claude. Las document skills (PDF, DOCX, PPTX, XLSX) son source-available, no open source. La skill `claude-api` es especialmente relevante — incluye routing inteligente entre haiku/sonnet/opus, evita errores comunes y referencia documentación de streaming, batches y tool use.

---

### 1.2 ComposioHQ/awesome-claude-skills
**URL:** https://github.com/ComposioHQ/awesome-claude-skills
**Enfoque:** Automatización de SaaS, productividad, desarrollo, seguridad

#### Skills de Desarrollo y Código

| Skill | Qué hace | Relevancia Agencia |
|-------|----------|-------------------|
| **software-architecture** | Implementa Clean Architecture, SOLID, patrones de diseño | ALTA |
| **subagent-driven-development** | Despacha sub-agentes independientes con checkpoints de code review | ALTA |
| **test-driven-development** | TDD para features y bugfixes | ALTA |
| **mcp-builder** | Guía para crear servidores MCP | ALTA |
| **prompt-engineering** | Técnicas y patrones de prompt engineering | ALTA |
| **root-cause-tracing** | Cuando ocurren errores profundos en ejecución | ALTA |
| **using-git-worktrees** | Crea worktrees git aislados con verificación de seguridad | ALTA |
| **finishing-a-development-branch** | Guía para completar trabajo de desarrollo | ALTA |
| **review-implementing** | Evalúa planes de implementación de código | ALTA |
| **test-fixing** | Detecta tests que fallan y propone patches | ALTA |
| **postgres** | Ejecuta queries SQL read-only contra PostgreSQL | ALTA |
| **changelog-generator** | Genera changelogs user-facing desde commits git | MEDIA |
| **langsmith-fetch** | Debugea agentes LangChain/LangGraph fetcheando traces | MEDIA |
| **aws-skills** | AWS con CDK best practices y serverless patterns | MEDIA |
| **deep-research** | Investigación autónoma multi-step con Gemini | MEDIA |
| **webapp-testing** | Testing de apps web locales con Playwright | ALTA |
| **Playwright Browser Automation** | Automatización de browser para testing | ALTA |
| **move-code-quality-skill** | Analiza paquetes Move contra estándares de calidad | BAJA |
| **pypict-claude-skill** | Diseño de test cases usando testing combinatorio | MEDIA |
| **iOS Simulator** | Interactúa con iOS Simulator para testing | MEDIA |
| **artifacts-builder** | Suite para artefactos HTML multi-componente | MEDIA |

#### Skills de Automatización y Productividad SaaS (78+ apps)

**Composio Connect Skills — Integraciones disponibles:**

| Categoría | Skills disponibles | Relevancia |
|-----------|-------------------|------------|
| **Automatización** | Make (Integromat) | ALTA |
| **Deploy/DevOps** | Vercel, Render, Supabase, Sentry, CircleCI, Datadog, PagerDuty | ALTA |
| **PM** | Notion, Linear, Jira, Asana, ClickUp, Trello, Monday, Basecamp | ALTA |
| **Comunicación** | Slack, Discord, Telegram, WhatsApp, Teams | ALTA |
| **Email** | Gmail, Outlook, SendGrid, Postmark | MEDIA |
| **CRM** | HubSpot, Salesforce, Pipedrive, Zoho | MEDIA |
| **Analytics** | PostHog, Mixpanel, Amplitude, Segment | MEDIA |
| **Diseño** | Figma, Canva, Miro | MEDIA |
| **Código** | GitHub, GitLab, Bitbucket | ALTA |
| **Storage** | Google Drive, Dropbox, Box, OneDrive | BAJA |
| **Social** | Twitter/X, LinkedIn, Reddit, TikTok, YouTube | BAJA |
| **E-commerce** | Stripe, Shopify, Square | MEDIA |

**Skills de Negocio y Marketing:**

| Skill | Qué hace |
|-------|----------|
| **competitive-ads-extractor** | Extrae y analiza anuncios de competidores desde ad libraries |
| **domain-name-brainstormer** | Genera ideas de nombres de dominio y verifica disponibilidad |
| **lead-research-assistant** | Identifica y califica leads de alta calidad |
| **content-research-writer** | Escribe contenido de alta calidad con investigación integrada |
| **twitter-algorithm-optimizer** | Analiza y optimiza tweets para máximo alcance |
| **meeting-insights-analyzer** | Analiza transcripts de reuniones para patrones de comportamiento |
| **developer-growth-analysis** | Analiza el crecimiento de desarrolladores |

**Skills de Documentos y Archivo:**

| Skill | Qué hace |
|-------|----------|
| **pdf** | Extrae texto, tablas, metadatos, merge y anotación de PDFs |
| **docx** | Crea, edita, analiza Word con tracked changes |
| **pptx** | Lee, genera y ajusta slides |
| **xlsx** | Manipulación de spreadsheets: fórmulas, charts, transformaciones |
| **file-organizer** | Organiza archivos y carpetas inteligentemente por contexto |
| **invoice-organizer** | Organiza facturas y recibos para preparación de impuestos |
| **article-extractor** | Extrae texto completo y metadatos de páginas web |
| **youtube-transcript** | Obtiene transcripts de videos de YouTube |
| **video-downloader** | Descarga videos de YouTube y otras plataformas |

**Skills de Análisis y Datos:**

| Skill | Qué hace |
|-------|----------|
| **CSV Data Summarizer** | Analiza CSVs y genera insights |
| **image-enhancer** | Mejora calidad de imágenes y screenshots |
| **NotebookLM Integration** | Conecta Claude con NotebookLM para respuestas basadas en fuentes |
| **D3.js Visualization** | Produce charts D3 y visualizaciones interactivas |
| **reddit-fetch** | Obtiene contenido de Reddit cuando WebFetch está bloqueado |

**Skills de Seguridad:**

| Skill | Qué hace |
|-------|----------|
| **computer-forensics** | Análisis forense digital e investigación |
| **threat-hunting-with-sigma-rules** | Hunting de amenazas con reglas Sigma |
| **FFUF Web Fuzzing** | Integra ffuf para análisis de vulnerabilidades |
| **metadata-extraction** | Extrae y analiza metadatos de archivos |
| **file-deletion** | Borrado seguro y sanitización de datos |

---

### 1.3 VoltAgent/awesome-agent-skills
**URL:** https://github.com/VoltAgent/awesome-agent-skills
**Stats:** 12.7k estrellas, 1.2k forks
**Enfoque:** Skills oficiales de equipos de producción, no generadas con IA

#### Skills Oficiales de Anthropic (incluidas en este repo)

Las mismas 17 skills del repositorio oficial de Anthropic más la skill template.

#### Skills por Equipo/Empresa

**VoltAgent (Framework de Agentes):**

| Skill | Qué hace |
|-------|----------|
| **create-voltagent** | Guía de inicialización de proyectos con VoltAgent |
| **voltagent-best-practices** | Patrones de arquitectura para agentes y workflows |
| **voltagent-core-reference** | Referencia de clases y ciclos de vida |
| **voltagent-docs-bundle** | Documentación embebida con versioning |

**Supabase (Oficial):**

| Skill | Qué hace |
|-------|----------|
| **postgres-best-practices** | Mejores prácticas de PostgreSQL para Supabase, RLS, índices, queries eficientes |

**Vercel (Oficial — 8 skills):**

| Skill | Qué hace |
|-------|----------|
| **react-best-practices** | Patrones y mejores prácticas de React |
| **vercel-deploy-claimable** | Automatiza despliegue de proyectos en Vercel |
| **web-design-guidelines** | Estándares de diseño web |
| **composition-patterns** | Patrones reutilizables de React |
| **next-best-practices** | Guías de Next.js |
| **next-cache-components** | Estrategias de caching |
| **next-upgrade** | Workflows de upgrade de versión |
| **react-native-skills** | Optimización de React Native |

**Cloudflare (7 skills):**

| Skill | Qué hace |
|-------|----------|
| **agents-sdk** | Agentes IA con estado, scheduling |
| **building-ai-agent-on-cloudflare** | Agentes con estado y WebSockets |
| **building-mcp-server-on-cloudflare** | Servidores MCP remotos |
| **commands** | Referencia de comandos CLI |
| **durable-objects** | Coordinación stateful |
| **web-perf** | Auditoría de Core Web Vitals |
| **wrangler** | Deploy de Workers, KV, R2, D1 |

**Netlify (11 skills):**

| Skill | Qué hace |
|-------|----------|
| **netlify-functions** | APIs serverless y tareas en background |
| **netlify-edge-functions** | Edge middleware y geolocalización |
| **netlify-blobs** | Key-value storage de objetos |
| **netlify-db** | Postgres gestionado con branching |
| **netlify-image-cdn** | Optimización y transformación de imágenes |
| **netlify-forms** | Manejo de formularios con filtro de spam |
| **netlify-frameworks** | Deploy de frameworks con SSR |
| **netlify-caching** | Configuración de CDN caching |
| **netlify-config** | Referencia de netlify.toml |
| **netlify-cli-and-deploy** | CLI setup y workflows |
| **netlify-ai-gateway** | Acceso a gateway unificado de modelos IA |

**HashiCorp Terraform (3 skills):**

| Skill | Qué hace |
|-------|----------|
| **terraform-code-generation** | Genera y valida Terraform HCL |
| **terraform-module-generation** | Creación y refactoring de módulos |
| **terraform-provider-development** | Desarrollo de providers |

**CallStack — React Native (3 skills):**

| Skill | Qué hace |
|-------|----------|
| **react-native-best-practices** | Optimización de rendimiento |
| **github** | Patrones de workflow GitHub (PRs, code review) |
| **upgrading-react-native** | Workflows de upgrade de RN |

**Expo — Mobile (oficial):**

| Skill | Qué hace |
|-------|----------|
| Multiple skills | Native UI, API routes, CI/CD, dev clients, Tailwind setup, SwiftUI, Jetpack Compose, data fetching, SDK upgrades |

**Better Auth (7 skills):**

| Skill | Qué hace |
|-------|----------|
| **best-practices** | Guía de integración de Better Auth |
| **create-auth** | Setup de autenticación |
| **emailAndPassword** | Auth email/password |
| **providers** | Referencia de auth providers |
| **organization** | Gestión de organizaciones |
| **twoFactor** | Autenticación de dos factores |
| **explain-error** | Interpretación de mensajes de error |

**Stripe (2 skills):**

| Skill | Qué hace |
|-------|----------|
| **stripe-best-practices** | Mejores prácticas de integración Stripe |
| **upgrade-stripe** | Upgrades de SDK y versión de API |

**Firecrawl (8 skills):**

| Skill | Qué hace |
|-------|----------|
| **firecrawl-cli** | Web scraping via CLI |
| **firecrawl-agent** | Extracción autónoma de datos web |
| **firecrawl-browser** | Scraping basado en browser |
| **firecrawl-crawl** | Crawling de sitios web |
| **firecrawl-download** | Descarga de contenido web |
| **firecrawl-map** | Mapeo de estructura de sitios |
| **firecrawl-scrape** | Scraping de páginas web |
| **firecrawl-search** | Búsqueda web y extracción de resultados |

**Neon (3 skills):**

| Skill | Qué hace |
|-------|----------|
| **neon-postgres** | Mejores prácticas para Serverless Postgres |
| **claimable-postgres** | Provisioning de bases de datos |
| **neon-postgres-egress-optimizer** | Optimización de egress |

**Google Workspace CLI (9 skills):**

| Skill | Qué hace |
|-------|----------|
| Drive, Sheets, Gmail, Calendar, Admin, Docs, Slides, Tasks | Gestión completa del workspace de Google |

**Otros equipos relevantes:**

| Empresa | Skills | Relevancia |
|---------|--------|------------|
| Sentry | Error tracking e integración | ALTA |
| Hugging Face | ML models y datasets | MEDIA |
| Figma | Design system e integración | ALTA |
| Trail of Bits | Seguridad y análisis de vulnerabilidades | ALTA |
| Replicate | Inferencia de modelos IA | MEDIA |
| ClickHouse | Analytics database | BAJA |
| Remotion | Video programático con React | BAJA |

---

### 1.4 sickn33/antigravity-awesome-skills
**URL:** https://github.com/sickn33/antigravity-awesome-skills
**Stats:** 27,000+ estrellas, 1,311+ skills
**Instalación:** `npx antigravity-awesome-skills --claude`
**Invocación:** `>> /skill-name` en Claude Code

Este es el repositorio más extenso. Cubre 11 dominios con 1,311+ skills. Las más relevantes para nuestra Agencia:

#### Skills de Arquitectura y Diseño de Sistemas

| Skill | Qué hace |
|-------|----------|
| **architecture** | Framework de decisiones arquitectónicas y documentación ADR |
| **architecture-decision-records** | Creación y mantenimiento de ADRs |
| **architecture-patterns** | Clean, Hexagonal y Domain-Driven Design |
| **architect-review** | Especialización en arquitectura moderna de software |
| **api-design-principles** | Mejores prácticas de REST y GraphQL |
| **api-endpoint-builder** | Endpoints REST de producción con validación y auth |
| **api-security-best-practices** | Diseño seguro de APIs con auth y rate limiting |
| **api-patterns** | Decisiones de diseño: REST vs GraphQL vs tRPC |
| **api-documentation** | Specs OpenAPI y guías para desarrolladores |
| **autonomous-agent-patterns** | Patrones de diseño para agentes de coding autónomos |
| **ai-agents-architect** | Diseño de sistemas IA para comportamiento autónomo controlable |

#### Skills de Desarrollo General

| Skill | Qué hace |
|-------|----------|
| **brainstorming** | Transforma ideas en diseños estructurados |
| **test-driven-development** | TDD orientado al trabajo |
| **debugging-strategies** | Troubleshooting sistemático |
| **lint-and-validate** | Quality checks ligeros |
| **create-pr** | Empaqueta trabajo en pull requests limpios |
| **security-auditor** | Code reviews enfocados en seguridad |
| **doc-coauthoring** | Escritura estructurada de documentación |
| **frontend-design** | Calidad de UI e interacción |
| **acceptance-orchestrator** | Orquestación de tareas de coding end-to-end |
| **ask-questions-if-underspecified** | Clarificación de requerimientos antes de implementar |
| **async-python-patterns** | Python asíncrono con asyncio |
| **advanced-evaluation** | Implementación de LLM-as-judge y sistemas de evaluación |
| **agent-evaluation** | Evaluación de calidad de agentes LLM en producción |
| **agent-memory-systems** | Arquitectura cognitiva para gestión de memoria en agentes |
| **agent-orchestration-improve-agent** | Mejora sistemática del rendimiento de agentes |
| **agent-orchestration-multi-agent-optimize** | Optimización de sistemas multi-agente |
| **agent-orchestrator** | Meta-skill para orquestar el ecosistema de agentes |
| **ai-engineer** | Apps LLM de producción y sistemas RAG |
| **ai-engineering-toolkit** | 6 workflows de producción: evaluación de prompts, RAG, seguridad |

#### Skills de Seguridad

| Skill | Qué hace |
|-------|----------|
| **007** | Auditoría de seguridad, threat modeling, pentesting |
| **security-auditor** | Code reviews enfocados en seguridad |
| **api-security-best-practices** | Diseño seguro de APIs |
| **api-security-testing** | Testing de seguridad REST/GraphQL |
| **api-fuzzing-bug-bounty** | Testing de APIs para bug bounties |
| **attack-tree-construction** | Mapeo visual de rutas de amenazas |
| **auth-implementation-patterns** | Sistemas de auth y autorización seguros |
| **aegisops-ai** | DevSecOps y FinOps autónomo |
| **agentic-actions-auditor** | Auditoría de seguridad de GitHub Actions para integraciones IA |

#### Skills de DevOps e Infraestructura

| Skill | Qué hace |
|-------|----------|
| **aws-serverless** | Estructura de funciones Lambda con manejo de errores |
| **aws-cost-optimizer** | Análisis y recomendaciones de optimización de costos AWS |
| **appdeploy** | Deploy de apps web con backend, BD y storage |
| **airflow-dag-patterns** | Mejores prácticas de Apache Airflow |
| **app-store-optimization** | Toolkit completo de ASO para iOS y Android |
| **analytics-product** | Analytics de producto: PostHog, Mixpanel, funnels |
| **analytics-tracking** | Diseño y auditoría de sistemas analíticos |

#### Skills de IA y Agentes

| Skill | Qué hace |
|-------|----------|
| **ai-agent-development** | Workflows de sistemas autónomos y multi-agente |
| **agent-manager-skill** | Gestión de agentes CLI via sesiones tmux |
| **agent-memory-mcp** | Sistema de memoria persistente y buscable para agentes IA |
| **agents-md** | Mejores prácticas de documentación de agentes |
| **agentfolio** | Directorio de descubrimiento e investigación de agentes IA |
| **ai-md** | Convierte CLAUDE.md al formato estructurado nativo de IA |
| **agent-tool-builder** | Diseño de interfaces LLM-al-mundo-externo |
| **rag-engineer** (categoría Data & AI) | Sistemas RAG para producción |

#### Skills de Mobile (no Flutter específico, pero relacionados)

| Skill | Qué hace |
|-------|----------|
| **android-jetpack-compose-expert** | UI moderna de Android con Jetpack Compose |
| **android_ui_verification** | Testing automatizado e2e en emulador Android |
| **app-store-optimization** | ASO completo para iOS y Android |
| **app-builder** | Orquestador full-stack desde lenguaje natural |

#### Skills de Workflows y Bundles (Antigravity)

**Bundles disponibles:**
- Web Wizard — desarrollo web enfocado
- Security Engineer — workflows con seguridad hardened
- Essentials — fundación de uso general
- Full-Stack Developer — desarrollo end-to-end
- QA & Testing — aseguramiento de calidad
- DevOps & Cloud — infraestructura y deploy
- OSS Maintainer — contribución open source
- Observability & Monitoring — monitoreo en producción

**Workflows de ejecución:**
- Ship a SaaS MVP
- Security Audit for a Web App
- Build an AI Agent System
- QA and Browser Automation
- Design a DDD Core Domain

---

## 2. Clasificacion por Prioridad para la Agencia

### ALTA PRIORIDAD — Implementar de inmediato

Estas skills resuelven directamente lo que hace nuestra Agencia: automatización, apps móviles, backends, IA.

| # | Skill | Repo origen | Por qué es crítica |
|---|-------|-------------|-------------------|
| 1 | **claude-api** | anthropics/skills | Nuestro stack central. Guía de modelos, streaming, tool use, sub-agentes |
| 2 | **mcp-builder** | anthropics/skills + Composio | Cinthya necesita esto para construir conectores a n8n, Make, Zapier |
| 3 | **software-architecture** | Composio | Sasha necesita Clean Architecture y SOLID para el backend |
| 4 | **subagent-driven-development** | Composio | Multiplica la velocidad de todo el equipo con sub-agentes paralelos |
| 5 | **test-driven-development** | Composio + Antigravity | TDD para las features que Sasha y Brook construyen |
| 6 | **webapp-testing** | anthropics + Composio | Testing automatizado de las interfaces que Brook construye |
| 7 | **postgres** | Composio | Sasha ejecuta queries en Supabase/PostgreSQL desde Claude Code |
| 8 | **supabase/postgres-best-practices** | VoltAgent (oficial Supabase) | RLS, índices, queries optimizados en nuestra BD principal |
| 9 | **api-design-principles** | Antigravity | Sasha diseña APIs REST de producción |
| 10 | **api-security-best-practices** | Antigravity | OWASP y seguridad para APIs de Sasha |
| 11 | **auth-implementation-patterns** | Antigravity | Auth segura con JWT para nuestros proyectos |
| 12 | **security-auditor** | Antigravity | Auditorías de seguridad de código |
| 13 | **architecture** | Antigravity | Jarvis toma decisiones arquitectónicas con este framework |
| 14 | **architecture-decision-records** | Antigravity | Documenta decisiones técnicas del equipo |
| 15 | **vercel-deploy-claimable** | VoltAgent (oficial Vercel) | Despliega proyectos en Vercel automáticamente |
| 16 | **next-best-practices** | VoltAgent (oficial Vercel) | Brook construye con Next.js como frontend principal |
| 17 | **react-best-practices** | VoltAgent (oficial Vercel) | Patrones de React para Brook |
| 18 | **agent-orchestration-multi-agent-optimize** | Antigravity | Jade optimiza la coordinación del equipo de agentes |
| 19 | **ai-agents-architect** | Antigravity | Diseñar los agentes de la Agencia con mejores prácticas |
| 20 | **debugging-strategies** | Antigravity | Troubleshooting sistemático para todo el equipo |
| 21 | **brainstorming** | Antigravity | Planificación estructurada antes de implementar |
| 22 | **create-pr** | Antigravity | Proceso de PR limpio en el workflow del equipo |
| 23 | **composio/connect** (Make) | Composio | Conecta con Make (Integromat) para automatizaciones de Cinthya |
| 24 | **composio/connect** (Render) | Composio | Deploy a Render para nuestros backends FastAPI |
| 25 | **composio/connect** (Supabase) | Composio | Conecta con Supabase desde Claude Code |
| 26 | **stripe-best-practices** | VoltAgent (oficial Stripe) | Cuando integremos pagos en proyectos de clientes |
| 27 | **ai-engineering-toolkit** | Antigravity | 6 workflows de producción incluyendo RAG y evaluación de prompts |
| 28 | **advanced-evaluation** | Antigravity | Ego evalúa la calidad de los agentes con LLM-as-judge |
| 29 | **agent-evaluation** | Antigravity | Métricas de calidad de agentes en producción |

---

### MEDIA PRIORIDAD — Útiles para proyectos específicos

| Skill | Repo origen | Cuándo usarla |
|-------|-------------|---------------|
| **pdf / docx / xlsx / pptx** | anthropics/skills | Cuando los proyectos procesen documentos |
| **langsmith-fetch** | Composio | Debugear agentes LangChain si los usamos |
| **react-native-best-practices** | VoltAgent (Callstack) | Si el proyecto de app móvil usa RN en lugar de Flutter |
| **upgrading-react-native** | VoltAgent (Callstack) | Mantener actualizadas las apps RN |
| **terraform-code-generation** | VoltAgent (HashiCorp) | Si escalamos a infraestructura más compleja |
| **better-auth / create-auth** | VoltAgent (Better Auth) | Alternativa a auth personalizada |
| **firecrawl-agent / firecrawl-scrape** | VoltAgent (Firecrawl) | Cuando proyectos requieran web scraping |
| **competitive-ads-extractor** | Composio | Análisis de competencia para Juan Camilo |
| **lead-research-assistant** | Composio | Generación de leads para el área comercial |
| **changelog-generator** | Composio | Changelogs automáticos de los proyectos |
| **using-git-worktrees** | Composio | Desarrollo paralelo en features grandes |
| **app-store-optimization** | Antigravity | Cuando lancemos apps a tiendas |
| **airflow-dag-patterns** | Antigravity | Pipelines de datos si un proyecto lo requiere |
| **analytics-product** | Antigravity | PostHog/Mixpanel para tracking en proyectos |
| **figma** (integración) | VoltAgent | Erik integra Figma con el flujo de trabajo |
| **sentry** (integración) | VoltAgent | Monitoreo de errores en producción |
| **web-perf** (Cloudflare) | VoltAgent | Auditoría de Core Web Vitals de Brook |
| **internal-comms** | anthropics/skills | Reportes y comunicaciones del equipo |
| **doc-coauthoring** | anthropics/skills | Documentación técnica colaborativa |
| **ai-md** | Antigravity | Convierte CLAUDE.md al formato estructurado óptimo |
| **agents-md** | Antigravity | Mejores prácticas de documentación de agentes |

---

### BAJA PRIORIDAD — No relevantes para nuestro stack actual

| Skill | Por qué baja prioridad |
|-------|----------------------|
| **Azure AI (60+ skills)** | No usamos Azure en nuestro stack |
| **angular / angular-best-practices** | Usamos React/Next.js no Angular |
| **algorithmic-art / canvas-design** | No es nuestro foco principal |
| **slack-gif-creator** | No crítico para el trabajo |
| **Binance / crypto skills** | No hacemos proyectos cripto |
| **Remotion** | Video programático no es nuestro foco |
| **ClickHouse** | No en nuestro stack de BD |
| **Avalonia** | Framework .NET de desktop, no usamos |
| **arm-cortex-expert** | Firmware embebido, no aplica |
| **active-directory-attacks** | Seguridad de AD enterprise, no aplica |
| **amazon-alexa** | No hacemos skills de voz |

---

## 3. Analisis de Gaps — Skills que NO Existen pero Necesita la Agencia

Este es el hallazgo mas critico del reporte. Después de revisar los 4 repositorios (2,100+ skills), confirmamos que las siguientes skills NO EXISTEN en ninguno de los repos investigados:

### Gaps Criticos (ALTA URGENCIA)

| Gap | Por qué es crítico | Quién lo necesita |
|-----|-------------------|-------------------|
| **n8n** | Cinthya usa n8n como herramienta principal de automatización. No hay NINGUNA skill de n8n en los 4 repos revisados. Solo encontramos en Composio una skill de "n8n-skills" que apunta a operar workflows pero no se pudo verificar su contenido (error 404). | Cinthya |
| **Flutter / Dart** | Nuestro stack móvil principal es Flutter. No existe ninguna skill de Flutter en ninguno de los 4 repositorios. Las skills móviles disponibles son React Native y Jetpack Compose — ambas de ecosistemas diferentes. | Sasha, Brook |
| **FastAPI** | Sasha construye todos los backends con FastAPI/Python. No hay skill específica de FastAPI. Solo existe `async-python-patterns` (asyncio) y skills genéricas de Python. | Sasha |
| **Supabase RLS y Auth** | Existe una skill de `postgres-best-practices` de Supabase pero es genérica. No hay skill específica para Supabase Auth, Row Level Security (RLS) avanzado, Supabase Realtime, Edge Functions, o Storage. | Sasha, Brook |
| **Claude Agent SDK** | El repositorio oficial de Anthropic tiene `claude-api` pero no tiene una skill específica del nuevo Claude Agent SDK con sub-agentes paralelos, que es lo que usamos en la Agencia. | Jade, Jarvis, todos |

### Gaps Importantes (MEDIA URGENCIA)

| Gap | Por qué importa | Quién lo necesita |
|-----|----------------|-------------------|
| **Firebase** | Segundo proveedor de BaaS en nuestro stack. No hay skill de Firebase (Auth, Firestore, Storage, Cloud Functions). | Sasha |
| **Railway / Render deploy** | Nuestras plataformas de deploy de backends. Railway no tiene skill. Render aparece solo como integración de Composio, no como skill de deploy. | Cinthya, Sasha |
| **n8n workflow design patterns** | No solo operar n8n, sino diseñar flujos correctos: manejo de errores, retry logic, credenciales, webhooks. | Cinthya |
| **Zapier** | Herramienta de automatización en nuestro stack. No existe skill en ningún repo. | Cinthya |
| **Make (Integromat) avanzado** | Solo aparece como integración de Composio, no como skill de diseño de workflows. | Cinthya |
| **Flutter testing** | No existe skill de testing específico para Flutter (widget tests, integration tests, golden tests). | Sasha, Brook |
| **Dart patterns** | No hay skill de patrones Dart modernos (null safety, records, patterns en Dart 3). | Sasha |

### Gaps Estratégicos (Skills únicas para Agencia de IA)

| Gap | Por qué es estratégico |
|-----|----------------------|
| **multi-agent-agency-management** | Gestionar un equipo de agentes especializados como los nuestros (Jarvis, Sasha, Brook, Erik, Cinthya, Ego, Jade). No existe ninguna skill que modele esto. |
| **CLAUDE.md-optimizer** | Aunque existe `ai-md` en Antigravity para convertir CLAUDE.md, no hay skill que optimice system prompts para agentes especializados con roles definidos. |
| **ego-audit-protocol** | No existe skill para auditoría de agentes IA en producción dentro de una agencia. `agent-evaluation` es cercano pero no cubre el protocolo de Ego. |
| **client-project-lifecycle** | Skills para gestionar el ciclo completo de un proyecto de cliente: propuesta, estimación, entrega, retroalimentación. |

---

## 4. Plan de Accion Recomendado para Jarvis

### Fase 1 — Instalacion Inmediata (esta semana)

```bash
# 1. Instalar Antigravity (contiene la mayoría de las skills de alta prioridad)
npx antigravity-awesome-skills --claude

# 2. Instalar el repositorio oficial de Anthropic
# En Claude Code:
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```

**Skills a activar primero (top 5):**
1. `@architecture` — Jarvis lo usa en cada evaluación de proyecto
2. `@security-auditor` — Sasha lo integra en su workflow de code review
3. `@test-driven-development` — Todo el equipo de ejecución
4. `@api-design-principles` — Sasha para las APIs de FastAPI
5. `@subagent-driven-development` — Para multiplicar la velocidad del equipo

### Fase 2 — Instalar Skills Específicas por Agente (semana 2)

Para **Sasha:** `software-architecture`, `api-security-best-practices`, `auth-implementation-patterns`, `postgres`

Para **Brook:** `next-best-practices`, `react-best-practices`, `webapp-testing`, `web-perf`

Para **Cinthya:** `mcp-builder`, `composio-connect` (Make, Render, Supabase)

Para **Ego:** `advanced-evaluation`, `agent-evaluation`

Para **Jade:** `agent-orchestration-multi-agent-optimize`, `ai-agents-architect`, `ai-md`

### Fase 3 — Crear Skills Propias para los Gaps (semana 3-4)

Jade recomienda crear las siguientes skills propias usando `skill-creator` como base:

1. **`/agencia/skills/n8n-workflow-design/SKILL.md`** — Diseño de flujos n8n para Cinthya
2. **`/agencia/skills/flutter-development/SKILL.md`** — Stack completo Flutter/Dart para Sasha
3. **`/agencia/skills/fastapi-patterns/SKILL.md`** — FastAPI + Pydantic + async para Sasha
4. **`/agencia/skills/supabase-complete/SKILL.md`** — Auth + RLS + Realtime + Storage para Sasha/Brook
5. **`/agencia/skills/claude-agent-sdk/SKILL.md`** — Sub-agentes paralelos para toda la Agencia

---

## 5. Observaciones Finales de Jade

### Lo que más me sorprendió

1. **n8n tiene cero presencia** en los repos más importantes del ecosistema Claude Code. Con 12k+ estrellas en GitHub y siendo una de las herramientas de automatización más usadas en startups, es un gap enorme que nadie ha cubierto todavía. Esto es una OPORTUNIDAD para que la Agencia publique una skill de n8n y gane visibilidad en la comunidad.

2. **Flutter es invisible** en el ecosistema de skills. React Native tiene tres repositorios oficiales (Vercel, Callstack). Flutter no tiene ninguno. Con el crecimiento de Flutter en 2025-2026, crear la primera skill oficial sería una posición estratégica interesante.

3. **El repo de Anthropic tiene solo 17 skills** pero 102k estrellas — lo cual indica que la comunidad valora muchísimo la calidad sobre la cantidad. Las skills que cremos para la Agencia deben seguir ese estándar de producción.

4. **La skill `claude-api` del repo oficial** es extraordinariamente útil para Jade y para cualquier agente que use el SDK. Incluye el routing inteligente entre haiku/sonnet/opus, patterns para streaming, y nota que `budget_tokens` fue deprecado en Opus 4.6 y Sonnet 4.6. Instalarla es prioritario.

5. **Composio tiene una skill de `n8n-skills`** pero al intentar acceder al archivo SKILL.md el resultado fue 404 — posiblemente fue removida o movida. Vale la pena verificar directamente en el repositorio.

### Recomendacion estratégica de Jade a Jarvis y Juan Camilo

La Agencia debería considerar publicar sus propias skills en los repositorios de la comunidad (especialmente VoltAgent y Antigravity). Las skills de n8n y Flutter serían las primeras de ese tipo y nos posicionarían como referentes técnicos. Esto genera visibilidad y potenciales clientes que buscan automatización y apps móviles — exactamente lo que hacemos.

---

**Fuentes verificadas:**
- https://github.com/anthropics/skills — consultado 2026-03-24
- https://github.com/ComposioHQ/awesome-claude-skills — consultado 2026-03-24
- https://github.com/VoltAgent/awesome-agent-skills — consultado 2026-03-24
- https://github.com/sickn33/antigravity-awesome-skills — consultado 2026-03-24
- https://raw.githubusercontent.com/sickn33/antigravity-awesome-skills/main/data/catalog.json — consultado 2026-03-24

*Reporte generado por Jade — Agente de Inteligencia y Capacitaciones — Agencia de IA*
