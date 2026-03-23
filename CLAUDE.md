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
    +---------+---------+
    |         |         |
   EGO      JADE     JARVIS
(Auditor)  (Intel &  (Gerente de
           Caps +    Programación)
          Agentes IA)
    |_________|_________|
         Audita todo
```

## Agentes disponibles

| Agente | Modelo | Especialidad | Cuándo convocarlo |
|--------|--------|-------------|-------------------|
| **Ego** | opus | Auditor Supremo | Auditar agentes, auditar proyectos, verificar calidad, reportes de estado, clasificación de modelos, control de objetivos |
| **Jarvis** | opus | Gerente de Programación | Gestión de proyectos, arquitectura, evaluación técnica y comercial, automatización, apps, startups |
| **Jade** | sonnet | Inteligencia, Capacitaciones y Experta en Agentes de IA | Tendencias, redes sociales, análisis de mercado, investigación para Ego, clasificación haiku/sonnet/opus, cursos, onboarding |

---

## Cómo invocar a los agentes

En Claude Code (VS Code), usa `@nombre-agente`:

```
@ego Audita el agente Jarvis y dame un reporte de su estado.
@ego Audita el proyecto Teclado de Señas. Ultrathink
@ego ¿Estamos usando los modelos correctos en todos los agentes?

@jarvis Evalúa este proyecto técnica y comercialmente. Ultrathink
@jarvis Necesito planificar los sprints del próximo mes.

@jade Dame un briefing de las últimas tendencias en agentes de IA.
@jade Clasifica estas tareas entre haiku, sonnet y opus.
@jade Investiga qué criterios nuevos debe tener Ego para auditar agentes.
@jade Diseña un currículo de TDD de 4 semanas para el equipo.
```

---

## Tips de productividad (aplicar siempre)

### Tip 1 — Ultrathink
Agrega `Ultrathink` al final de tu prompt para activar análisis más profundo.

```
Ejemplo: "Evalúa este proyecto y dame un roadmap. Ultrathink"
```

### Tip 2 — Sub-agentes paralelos
Pide explícitamente el uso de sub-agentes para tareas complejas — resuelve 10x más rápido.

```
Ejemplo: "Analiza el proyecto. Usa sub-agentes para explorar múltiples partes en paralelo."
```

### Tip 3 — Regla anti-alucinación (ya aplicada en Rules)
El `## Rules` al inicio garantiza que Claude busque documentación actualizada antes de implementar, eliminando el 95% de las alucinaciones.

---

## Reuniones del equipo

**Sábados 10:00 AM** — Juan Camilo (Gerente Comercial) + Jarvis + Jade
- Progreso de proyectos activos
- Briefing de tendencias de la semana (Jade)
- Nuevas oportunidades de negocio
- Evaluación de proyectos propuestos
- Prioridades para la semana siguiente

---

## Proyectos activos

- **Teclado de Señas** — App para personas sordomudas (en evaluación)

---

## Convenciones de modelos

| Modelo | Agente | Cuándo usarlo |
|--------|--------|--------------|
| `haiku` | Sub-agentes simples | Extracción, clasificación, enrutamiento, tareas repetitivas |
| `sonnet` | Jade | Investigación, redacción, cursos, análisis de mercado, código |
| `opus` | Jarvis, Ego | Decisiones estratégicas, auditorías, arquitectura, Ultrathink |

- Los agentes lanzan sub-agentes paralelos para tareas complejas
- Siempre verificar documentación oficial antes de implementar
- Ego audita a todos los agentes y proyectos — reporta a Juan Camilo
- Jade alimenta a Ego con investigación de criterios de auditoría actualizada
- Commits con mensajes descriptivos en español o inglés
- Todo el trabajo se gestiona desde este repositorio GitHub
