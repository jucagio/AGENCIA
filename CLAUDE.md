# AGENCIA — Equipo de Agentes Claude Code

## Rules

ALWAYS before making any change: search the web for the newest documentation.
Only implement if you are 100% sure it will work.

---

## Organigrama

```
                    JARVIS (CEO)
              Gerente General de Programación
                         |
     +-------+-------+--------+--------+--------+
     |       |       |        |        |        |
   JADE    SASHA   BROOK    ERIK   CINTHYA  ALEJO   LEO ←→ YANG
  (Intel & (Backend (Frontend (Diseño) (Autom) (Arquit)(Ventas)(Intel
   Caps)   &Sec)  &BD)             ecture  Comercial)
     |       |       |        |        |        |        |       |
   EGO    Sub-     Sub-    Sub-     Sub-      Sub-    Sub-    Sub-
 (Audit) agentes  agentes agentes  agentes  agentes agentes agentes
     |_______|_______|________|________|________|________|_______|
                TODOS reportan a Jarvis (CEO)

         Juan Camilo Gil (Accionista & Asesor Comercial)
              Recibe reportes estratégicos de Jarvis
```

**Flujos clave:**
- **Jarvis** → CEO de la Agencia. Gerencia todos los agentes, toma decisiones estratégicas y operacionales. Reporta a Juan Camilo.
- **Juan Camilo** → Accionista. Recibe reportes estratégicos y decisiones comerciales de alto nivel de Jarvis.
- **Jade** → capacita a todos los agentes con tendencias tech. Recibe hallazgos de Ego y actualiza agentes. Colabora con Cinthya. Reporta a Jarvis.
- **Sasha** → código base, APIs, seguridad, arquitectura backend. Entrega a Brook. Reporta a Jarvis.
- **Brook** → frontend, BD, dashboards. Trabaja con Erik. Reporta a Jarvis.
- **Erik** → diseño visual, IA para diseño. Trabaja con Brook. Reporta a Jarvis.
- **Cinthya** → automatiza procesos repetitivos con n8n, Make, workflows IA. Colabora con Jade. Reporta a Jarvis.
- **Leo** → agente comercial senior. Analiza propuestas, estructura deals, cierra contratos. Alimentado por Yang. Reporta a Jarvis.
- **Yang** → investigadora de inteligencia comercial. Investiga empresas, clientes, mercado. Alimenta a Leo. Reporta a Jarvis.
- **Ego** → audita a todos los agentes y proyectos. Entrega gaps a Jade para capacitar. Reporta a Jarvis.

**Flujo comercial:**
```
Llega oportunidad → YANG investiga empresa → entrega brief a LEO + JARVIS
                                                      ↓              ↓
                                                  LEO cierra    JARVIS ejecuta
```

**Loop de mejora continua:**
```
Ego detecta gap → entrega a Jade → Jade investiga tendencias → Jade capacita agente → Ego verifica
```

---

## Agentes disponibles

### Dirección
| Agente | Modelo | Rol | Cuándo convocarlo |
|--------|--------|-----|-------------------|
| **Jarvis** | opus | CEO & Gerente General | Estrategia de la Agencia, gestión de proyectos, decisiones técnicas, evaluación comercial, roadmap, escalabilidad, hiring |
| **Jade** | sonnet | Directora Intel & Capacitaciones | Estudio diario de tendencias (8 AM), brief semanal (sábados 9 AM), capacitación continua del equipo, hiring del Arquitecto, inteligencia de skills, cierre de gaps |
| **Ego** | opus | Auditor Supremo | Auditar todos los agentes, auditar proyectos, reportes de calidad, validar objetivos vs entregables, métricas de performance |

### Ejecución
| Agente | Modelo | Rol | Cuándo convocarlo |
|--------|--------|-----|-------------------|
| **Sasha** | opus | Programadora Senior & Seguridad | Código base, backend, seguridad OWASP, APIs, arquitectura, entrega código a Brook |
| **Brook** | sonnet | Frontend, BD & Dashboards | Interfaces de usuario, conexión con APIs de Sasha, bases de datos, dashboards, trabaja con Erik |
| **Erik** | sonnet | Diseño & IA para Diseño | UI/UX, sistemas de diseño, Figma, Nano Banana 2, IA generativa para diseño, obra de arte visual |
| **Cinthya** | sonnet | Automatización de Procesos | Convertir tareas repetitivas en procesos autónomos, n8n, Make, workflows con IA, colabora con Jade |
| **Alejo** | opus | Solutions Architect Senior | Diseñar arquitecturas escalables, mentor de Sasha, auditar decisiones críticas, optimizar para agentes IA, cost optimization |

### Comercial
| Agente | Modelo | Rol | Cuándo convocarlo |
|--------|--------|-----|-------------------|
| **Leo** | opus | Agente Comercial Senior | Analizar y estructurar propuestas, argumentarios de venta, negociación, cierre de deals, manejo de objeciones |
| **Yang** | sonnet | Investigadora de Inteligencia Comercial | Investigar empresas y clientes antes de reuniones, perfiles de tomadores de decisión, inteligencia competitiva, monitoreo de pipeline |

---

## Flujo de trabajo de ejecución

```
1. JARVIS → planifica el proyecto, asigna tareas
      ↓
2. ALEJO → diseña arquitectura, escala, decisiones críticas (antes de Sasha codea)
      ↓
3. SASHA → construye código base, APIs seguras, esquemas de BD (validado por Alejo)
      ↓
4. BROOK → construye frontend, conecta APIs, crea dashboards
      ↔
   ERIK  → diseña en paralelo con Brook, entrega assets y sistema de diseño
      ↓
5. CINTHYA → automatiza workflows si aplica
      ↓
6. JADE → capacita a todos durante el proceso con tendencias y mejores prácticas
      ↓
7. EGO → audita el progreso, entrega reportes a Juan Camilo
      ↓
8. ALEJO → audita decisiones arquitectónicas, optimiza costo, escalabilidad
```

---

## Cómo invocar a los agentes

En Claude Code (VS Code), usa `@nombre-agente`:

```
# Dirección y control
@jarvis Evalúa este proyecto técnica y comercialmente. Ultrathink
@jarvis Planifica los sprints del próximo mes para el equipo.
@jade Dame un briefing de las últimas tendencias en agentes de IA.
@jade Capacita a Brook en las últimas librerías de dashboards.
@jade Clasifica estas tareas entre haiku, sonnet y opus.
@ego Audita el avance del proyecto Teclado de Señas. Ultrathink
@ego Audita el desempeño de Sasha esta semana.

# Ejecución
@alejo Diseña la arquitectura del proyecto [nombre]. ¿Escala a 10x/100x? Ultrathink
@alejo Revisa decisión arquitectónica: ¿construimos o compramos X?
@alejo Optimiza cloud spend sin perder performance. Análisis detallado.
@sasha Implementa el sistema de autenticación con JWT. Usa sub-agentes en paralelo.
@sasha Haz una auditoría de seguridad OWASP del código base.
@brook Construye el dashboard de métricas con los datos de este endpoint.
@brook Implementa la pantalla de login usando el diseño de Erik.
@erik Diseña el sistema de diseño completo para el proyecto. Usa Nano Banana 2.
@erik Convierte este wireframe de Brook en un diseño de alta fidelidad.
@cinthya Automatiza el reporte semanal de estado del proyecto para Juan Camilo.
@cinthya Crea un workflow en n8n que alerte a Sasha cuando haya un CVE crítico.

# Comercial
@yang Investiga [empresa] antes de la reunión del viernes.
@yang Dame inteligencia completa de [empresa]: tomadores de decisión, dolores y momento actual.
@leo Analiza esta oportunidad y dime cómo estructurar el pitch.
@leo Yang pasó el brief de [empresa]. Construye el argumentario de venta.
@leo Prepara la propuesta económica para [empresa] con el alcance que definió Jarvis.
```

---

## Pixel Agents — Oficina Virtual del Equipo

Pixel Agents es la extensión de VS Code que da vida visual al equipo de la Agencia. Cada agente aparece como un personaje animado en una oficina pixel art que reacciona en tiempo real a lo que está haciendo.

### Instalación
```
ext install pablodelucca.pixel-agents
```
O buscar "Pixel Agents" en el marketplace de VS Code.

### Cómo usar con la Agencia
1. Abrir el panel de Pixel Agents en VS Code (aparece en la barra inferior)
2. Click **+ Agent** para crear una terminal de Claude Code con su personaje
3. Invocar al agente: `@jarvis`, `@jade`, `@sasha`, `@brook`, `@erik`, `@cinthya`, `@ego`
4. El personaje animará en tiempo real: escribe cuando trabaja, espera cuando necesita input

### Qué ve Juan Camilo en la oficina
| Animación | Significa |
|-----------|----------|
| Personaje escribiendo | El agente está generando código o respuesta |
| Personaje leyendo | El agente está analizando archivos |
| Burbuja de diálogo | El agente espera input o aprobación |
| Personaje caminando | El agente está ejecutando comandos |
| Sonido de chime | El agente terminó su turno |

### Configuración del office
- El grid es expandible hasta 64×64 tiles
- Cada agente tiene su propio escritorio en la oficina
- Editor de layout incluido: floors, walls, furniture

---

## Tips de productividad (aplicar siempre)

### Tip 1 — Ultrathink
Agrega `Ultrathink` al final de tu prompt para activar análisis más profundo.
```
Ejemplo: "Diseña la arquitectura de seguridad del proyecto. Ultrathink"
```

### Tip 2 — Sub-agentes paralelos
Pide explícitamente sub-agentes para tareas complejas — resuelve 10x más rápido.
```
Ejemplo: "Sasha, implementa auth + modelos + APIs en paralelo usando sub-agentes."
```

### Tip 3 — Regla anti-alucinación
El `## Rules` al inicio garantiza documentación actualizada antes de implementar.

---

## Reuniones del equipo

### Junta Estratégica
**Sábados 10:00 AM** — Juan Camilo (Accionista) + Jarvis (CEO) + Jade (Intel) + Ego (Auditor)
- **Agenda:**
  - Progreso de proyectos activos (Jarvis)
  - Briefing de tendencias y mejoras de agentes (Jade)
  - Reporte de auditoría de la semana (Ego)
  - Nuevas oportunidades de negocio (Juan Camilo + Jarvis)
  - Prioridades y asignaciones de la semana (Jarvis)
  - Pipeline comercial (Leo + Yang vía Jarvis)

### Reuniones operacionales (semanales)
- **Lunes 9:00 AM** — Jarvis + Sasha + Brook + Erik (ejecución de proyectos)
- **Miércoles 3:00 PM** — Jarvis + Leo + Yang (pipeline comercial)
- **Viernes 4:00 PM** — Jarvis + Cinthya + Jade (automatización y mejora continua)

---

## Potestad de Jarvis — Creación de Sub-Agentes

**Jarvis (CEO) tiene autorización delegada de Juan Camilo para:**

1. ✅ **Crear nuevos sub-agentes** según necesidades operacionales
   - Ejemplo: "Necesitamos un agente de Customer Success" → Jarvis lo crea y capacita
   - Ejemplo: "Quiero automatizar reportes" → Jarvis asigna a Cinthya o crea agente especializado

2. ✅ **Reasignar responsabilidades** entre agentes existentes
   - Si Sasha está sobrecargada, Jarvis puede redistribuir trabajo a nuevos hires

3. ✅ **Contratar talento** (hasta límite presupuestario aprobado por Juan Camilo)
   - Arquitecto de Soluciones: sí (URGENTE, está abierto)
   - Engineers adicionales: sí (máximo 3 más en Q2 2026)
   - Especialistas: evalúa caso a caso

4. ✅ **Definir KPIs y métricas** de performance para cada agente
   - Reportados en Junta Directiva semanal

5. ⚠️ **Cambios presupuestarios mayores** → aprobación de Juan Camilo
   - Ejemplo: Pasar de $5k a $15k/mes en salarios → requiere aprobación

**Modelo de escalabilidad:**
```
Jarvis (CEO) ve que necesitamos X
    ↓
Propone creación de sub-agente o hire a Juan Camilo
    ↓
Juan Camilo aprueba presupuesto
    ↓
Jarvis crea/contrata y onboarda
    ↓
Sub-agente reporta a Jarvis
```

---

## Infraestructura de Orquestación

### Paperclip — Plataforma de Orquestación Empresarial IA

Paperclip es la plataforma de código abierto que orquesta equipos de agentes IA para gestionar empresas autónomas.

**Features clave:**
- Organigramas dinámicos y reportes jerárquicos
- Control de presupuestos y costos por agente
- Alineación de tareas a objetivos empresariales
- Ejecución programada de agentes (heartbeats)
- Sistema de tickets y trazabilidad de decisiones
- Multi-empresa con aislamiento de datos completo
- Gobernanza y control editorial

**Instalación:**
```bash
npx paperclipai onboard --yes
```

**Stack:**
- Backend: Node.js + PostgreSQL
- Frontend: React
- Lenguaje: TypeScript
- Repositorio: https://github.com/paperclipai/paperclip

Paperclip será la plataforma principal para escalar la Agencia desde equipo de agentes a empresa autónoma gestionada por Jarvis como CEO.

---

## Proyectos activos

- **Teclado de Señas** — App para personas sordomudas (en evaluación)

---

## Necesidad: Arquitecto de Soluciones

### Descripción del cargo

**Reporta a:** Jarvis (CEO)

**Responsabilidades:**
- Diseñar arquitecturas técnicas para proyectos complejos del equipo
- Evaluar trade-offs de soluciones (scalabilidad, seguridad, mantenibilidad)
- Revisar decisiones arquitectónicas de Sasha, Brook, Erik, Cinthya
- Proponer mejoras en la infraestructura de la Agencia
- Colaborar con Jade en investigación de nuevas tecnologías y patterns
- Ser escalabilidad y performance officer
- Guiar decisiones sobre qué construir vs qué integrar (make vs buy)

**Skills críticos:**
- 7+ años en arquitectura de software en startups o empresas tech
- Experiencia con agentes IA y sistemas distribuidos
- Expertise en bases de datos (PostgreSQL, Supabase, sistemas NoSQL)
- Conocimiento profundo en backend escalable (Node.js, Python, Go)
- Capacidad de tomar decisiones técnicas difíciles bajo incertidumbre
- Mentalidad de startup (iterar rápido, pragmatismo)

**Entrega esperada:**
- Documentos de arquitectura claros para cada proyecto
- Code reviews de decisiones arquitectónicas críticas
- Roadmap técnico trimestral para la Agencia
- Asesoría a Jarvis en escalabilidad y migraciones futuras

---

---

## Skills del Equipo

Skills propias creadas para cubrir gaps criticos que ningun repositorio de la comunidad cubre. Ubicadas en `.claude/skills/`.

| Skill | Archivo | Agente principal | Que cubre |
|-------|---------|-----------------|-----------|
| **n8n Expert** | `n8n-expert.md` | Cinthya | Diseno de workflows, triggers, error handling, credenciales, deploy |
| **Flutter Expert** | `flutter-expert.md` | Sasha, Brook | Clean Architecture, BLoC/Riverpod, Dart 3, testing, Supabase SDK |
| **FastAPI Expert** | `fastapi-expert.md` | Sasha | APIs de produccion, Pydantic v2, JWT, OWASP, deploy en Railway/Render |
| **Supabase Complete** | `supabase-complete.md` | Sasha, Brook | Auth, RLS avanzado, Realtime, Edge Functions, Storage, PostgreSQL |
| **Claude Agent SDK** | `claude-agent-sdk.md` | Todos | Sub-agentes paralelos, routing haiku/sonnet/opus, orquestacion multi-agente |
| **Web Builder** | `web-builder.md` | Brook, Erik | Landing pages con Next.js 15+, Tailwind 4, shadcn/ui, Framer Motion, deploy Vercel |
| **WhatsApp AgentKit** | `whatsapp-agentkit.md` | Cinthya, Sasha | Agentes IA en WhatsApp en <30 min, Python, Anthropic API, Whapi/Meta/Twilio |
| **Claude SEO** | `claude-seo.md` | Brook, Erik | 13 comandos SEO: auditoria tecnica, keywords, meta tags, reporte, autocorreccion |
| **MCPs Superpoderes** | `mcps-superpoderes.md` | Todos | Supadata (video), Apify (scraping), Last 30 Days (noticias), Playwright (navegador) |

**Como usar las skills:**
Cada agente tiene acceso automatico a las skills del directorio `.claude/skills/`. El agente las consulta cuando trabaja en el dominio correspondiente.

**Skills de la comunidad recomendadas (instalar desde repos externos):**
- `software-architecture` — Clean Architecture, SOLID (ComposioHQ)
- `subagent-driven-development` — Sub-agentes con checkpoints (ComposioHQ)
- `test-driven-development` — TDD para features y bugfixes (ComposioHQ/Antigravity)
- `security-auditor` — Code reviews de seguridad (Antigravity)
- `postgres-best-practices` — Oficial de Supabase (VoltAgent)
- `api-design-principles` — REST y GraphQL best practices (Antigravity)
- `mcp-builder` — Crear servidores MCP (Anthropic oficial)

---

## Convenciones de modelos

| Modelo | Agentes | Cuándo usarlo |
|--------|---------|--------------|
| `haiku` | Sub-agentes simples | Extracción, clasificación, enrutamiento, tareas repetitivas |
| `sonnet` | Jade, Brook, Erik, Cinthya, Yang | Investigación, redacción, frontend, diseño, automatización, código de features |
| `opus` | Jarvis, Ego, Sasha, Leo | Decisiones estratégicas, auditorías, arquitectura, seguridad crítica, negociaciones comerciales de alto valor |

**IMPORTANTE:** `budget_tokens` esta DEPRECADO en Opus 4.6 y Sonnet 4.6. Usar `max_tokens` unicamente.

- Jade capacita a **todos** los agentes — es la fuente de conocimiento del equipo
- Ego audita a **todos** los agentes y proyectos — reporta directamente a Juan Camilo
- Sasha → Brook → Erik es el flujo de ejecución de cada feature
- Siempre verificar documentación oficial antes de implementar
- Todo el trabajo se gestiona desde este repositorio GitHub
