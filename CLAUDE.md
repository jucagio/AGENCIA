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
         |                SASHA  BROOK ←→ ERIK
         |________________|_______|_______|
                    Audita todo
```

**Flujos clave:**
- **Juan Camilo** → recibe reportes de todos, toma decisiones comerciales
- **Jarvis** → gerencia a Sasha, Brook y Erik. Reporta a Juan Camilo
- **Jade** → forma y capacita a todos los agentes (Ego, Jarvis, Sasha, Brook, Erik). Reporta a Juan Camilo
- **Ego** → audita a todos los agentes y proyectos en curso. Reporta a Juan Camilo
- **Sasha** → crea código base y APIs, entrega a Brook. Reporta a Jarvis
- **Brook** → construye frontend y dashboards sobre el código de Sasha, trabaja con Erik. Reporta a Jarvis
- **Erik** → diseña la experiencia visual, trabaja en paralelo con Brook. Reporta a Jarvis

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
```

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
| `sonnet` | Jade, Brook, Erik | Investigación, redacción, frontend, diseño, código de features |
| `opus` | Jarvis, Ego, Sasha | Decisiones estratégicas, auditorías, arquitectura, seguridad crítica |

- Jade capacita a **todos** los agentes — es la fuente de conocimiento del equipo
- Ego audita a **todos** los agentes y proyectos — reporta directamente a Juan Camilo
- Sasha → Brook → Erik es el flujo de ejecución de cada feature
- Siempre verificar documentación oficial antes de implementar
- Todo el trabajo se gestiona desde este repositorio GitHub
