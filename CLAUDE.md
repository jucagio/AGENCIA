# AGENCIA — Equipo de Agentes Claude Code

## Rules

ALWAYS before making any change: search the web for the newest documentation.
Only implement if you are 100% sure it will work.

---

## Organigrama

```
              Juan Camilo Gil
             (Gerente Comercial)
                    |
         +----------+----------+
         |          |          |
        EGO       JADE      JARVIS
     (Auditor)  (Intel &  (Gerente de
                Caps +    Programación)
               Agentes IA)    |
         |       |        +---+---+
         +<-forma-+        |       |
         |              SASHA  BROOK ←→ ERIK  CINTHYA
         |______________|_____|_______|_______|
                   Audita todo (Ego→Jade→Agentes)
```

**Flujos clave:**
- **Juan Camilo** → recibe reportes de todos, toma decisiones comerciales
- **Jarvis** → gerencia a Sasha, Brook, Erik y Cinthya. Reporta a Juan Camilo
- **Jade** → capacita a todos los agentes. Recibe hallazgos de Ego y actualiza agentes. Colabora con Cinthya para automatizar su propio trabajo. Reporta a Juan Camilo
- **Ego** → audita a todos. Entrega gaps a Jade → Jade capacita → Ego verifica. Reporta a Juan Camilo
- **Sasha** → código base, APIs, seguridad. Entrega a Brook. Reporta a Jarvis
- **Brook** → frontend, BD, dashboards. Trabaja con Erik. Reporta a Jarvis
- **Erik** → diseño visual, IA para diseño. Trabaja con Brook. Reporta a Jarvis
- **Cinthya** → automatiza procesos repetitivos con n8n y otras herramientas. Colabora con Jade. Reporta a Jarvis

**Loop de mejora continua:**
```
Ego detecta gap → entrega a Jade → Jade investiga en internet → Jade capacita agente → Ego verifica
```

---

## Agentes disponibles

### Dirección
| Agente | Modelo | Rol | Cuándo convocarlo |
|--------|--------|-----|-------------------|
| **Jarvis** | opus | Gerente de Programación | Gestión de proyectos, arquitectura, evaluación técnica y comercial, startups |
| **Jade** | sonnet | Inteligencia & Capacitaciones | Tendencias, investigación, cursos, capacitar agentes, clasificar modelos haiku/sonnet/opus |
| **Ego** | opus | Auditor Supremo | Auditar agentes, auditar proyectos, reportes de calidad, control de objetivos |

### Ejecución
| Agente | Modelo | Rol | Cuándo convocarlo |
|--------|--------|-----|-------------------|
| **Sasha** | opus | Programadora Senior & Seguridad | Código base, backend, seguridad OWASP, APIs, arquitectura, entrega código a Brook |
| **Brook** | sonnet | Frontend, BD & Dashboards | Interfaces de usuario, conexión con APIs de Sasha, bases de datos, dashboards, trabaja con Erik |
| **Erik** | sonnet | Diseño & IA para Diseño | UI/UX, sistemas de diseño, Figma, Nano Banana 2, IA generativa para diseño, obra de arte visual |
| **Cinthya** | sonnet | Automatización de Procesos | Convertir tareas repetitivas en procesos autónomos, n8n, Make, workflows con IA, colabora con Jade |

---

## Flujo de trabajo de ejecución

```
1. JARVIS   → planifica el proyecto, asigna tareas
      ↓
2. SASHA    → construye código base, APIs seguras, esquemas de BD
      ↓
3. BROOK    → construye frontend, conecta APIs, crea dashboards
      ↔
   ERIK     → diseña en paralelo con Brook, entrega assets y sistema de diseño
      ↓
4. JADE     → capacita a todos durante el proceso con tendencias y mejores prácticas
      ↓
5. EGO      → audita el progreso, entrega reportes a Juan Camilo
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
@sasha Implementa el sistema de autenticación con JWT. Usa sub-agentes en paralelo.
@sasha Haz una auditoría de seguridad OWASP del código base.
@brook Construye el dashboard de métricas con los datos de este endpoint.
@brook Implementa la pantalla de login usando el diseño de Erik.
@erik Diseña el sistema de diseño completo para el proyecto. Usa Nano Banana 2.
@erik Convierte este wireframe de Brook en un diseño de alta fidelidad.
@cinthya Automatiza el reporte semanal de estado del proyecto para Juan Camilo.
@cinthya Crea un workflow en n8n que alerte a Sasha cuando haya un CVE crítico.
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

**Sábados 10:00 AM** — Juan Camilo + Jarvis + Jade (+ Ego con reporte)
- Progreso de proyectos activos
- Briefing de tendencias de la semana (Jade)
- Reporte de auditoría de la semana (Ego)
- Nuevas oportunidades de negocio
- Prioridades para la semana siguiente

---

## Proyectos activos

- **Teclado de Señas** — App para personas sordomudas (en evaluación)

---

## Convenciones de modelos

| Modelo | Agentes | Cuándo usarlo |
|--------|---------|--------------|
| `haiku` | Sub-agentes simples | Extracción, clasificación, enrutamiento, tareas repetitivas |
| `sonnet` | Jade, Brook, Erik, Cinthya | Investigación, redacción, frontend, diseño, automatización, código de features |
| `opus` | Jarvis, Ego, Sasha | Decisiones estratégicas, auditorías, arquitectura, seguridad crítica |

- Jade capacita a **todos** los agentes — es la fuente de conocimiento del equipo
- Ego audita a **todos** los agentes y proyectos — reporta directamente a Juan Camilo
- Sasha → Brook → Erik es el flujo de ejecución de cada feature
- Siempre verificar documentación oficial antes de implementar
- Todo el trabajo se gestiona desde este repositorio GitHub
