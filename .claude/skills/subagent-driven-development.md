---
name: subagent-driven-development
description: >
  Framework para ejecutar tareas complejas usando sub-agentes paralelos con checkpoints
  de validación. Usar cuando una tarea tenga múltiples componentes independientes que
  puedan ejecutarse en paralelo, o cuando se necesite velocidad 10x en la entrega.
  Todos los agentes deben aplicar este patrón. Especialmente útil para Sasha, Brook, Jade.
---

# Subagent-Driven Development

Ejecutar tareas complejas descomponiéndolas en sub-agentes especializados que corren **en paralelo**, con checkpoints de validación entre etapas.

## Por qué sub-agentes

| Sin sub-agentes | Con sub-agentes |
|----------------|----------------|
| Secuencial: A → B → C → D | Paralelo: A + B + C + D simultáneo |
| 1x velocidad | Hasta 10x velocidad |
| Un solo contexto sobreargado | Contextos limpios y enfocados |
| Un error bloquea todo | Los errores son aislados por agente |

---

## Patrón base

```
ORQUESTADOR (Opus)
    ├── Subagente 1 (Haiku/Sonnet) → Tarea A
    ├── Subagente 2 (Haiku/Sonnet) → Tarea B
    ├── Subagente 3 (Haiku/Sonnet) → Tarea C
    └── CHECKPOINT → validar resultados → continuar o reintentar
```

---

## Cuándo usar cada modelo en sub-agentes

| Tarea del sub-agente | Modelo |
|---------------------|--------|
| Extracción de datos, clasificación, formateo | **Haiku** |
| Investigación, redacción, código de features | **Sonnet** |
| Decisiones estratégicas, arquitectura, auditoría | **Opus** |

**Regla:** el orquestador siempre en Opus. Los sub-agentes en el modelo mínimo que resuelve la tarea.

---

## Ejemplos por agente

### Sasha — Backend en paralelo
```
@sasha Implementa el módulo de usuarios:
- Subagente 1: modelo de datos + migraciones
- Subagente 2: repositorio con Supabase
- Subagente 3: endpoints FastAPI
- Subagente 4: tests de seguridad
→ Checkpoint: integrar y verificar que todo conecta
```

### Brook — Frontend en paralelo
```
@brook Construye el dashboard:
- Subagente 1: componentes de KPIs
- Subagente 2: gráficas con Recharts
- Subagente 3: tabla con filtros y paginación
- Subagente 4: conexión a APIs de Sasha
→ Checkpoint: integrar y verificar navegación
```

### Jade — Capacitación en paralelo
```
@jade Capacita al equipo en X:
- Subagente 1: material para Sasha (foco backend)
- Subagente 2: material para Brook (foco frontend)
- Subagente 3: material para Erik (foco diseño)
→ Checkpoint: verificar que cada material es específico al rol
```

---

## Checkpoints — Puntos de validación obligatorios

Un checkpoint ocurre cuando todos los sub-agentes de una etapa terminan y antes de comenzar la siguiente.

```
ETAPA 1: Sub-agentes en paralelo
    ↓
CHECKPOINT 1:
  - ¿Todos los sub-agentes completaron su tarea?
  - ¿Los outputs son compatibles entre sí?
  - ¿Hay errores o inconsistencias?
  Si todo OK → continuar a ETAPA 2
  Si hay problemas → reintentar solo los sub-agentes fallidos
    ↓
ETAPA 2: Sub-agentes de integración
    ↓
CHECKPOINT 2: validación final
```

---

## Template de instrucción para sub-agentes

Cuando el orquestador lanza un sub-agente, siempre incluye:

```markdown
**Contexto**: [qué ya existe, qué hizo el sub-agente anterior]
**Tu tarea específica**: [una sola responsabilidad clara]
**Input que recibes**: [qué datos/archivos tienes disponibles]
**Output esperado**: [qué exactamente debes entregar]
**Restricciones**: [qué NO debes hacer]
**Criterio de éxito**: [cómo saber que terminaste correctamente]
```

---

## Anti-patrones a evitar

```
❌ Un sub-agente con múltiples responsabilidades no relacionadas
❌ Sub-agentes que dependen unos de otros (eso es secuencial, no paralelo)
❌ Orquestador que no valida el output de los sub-agentes
❌ Usar Opus para tareas que Haiku resuelve bien
❌ Sub-agentes sin contexto suficiente para trabajar de forma autónoma
```

---

## Señal para activar este patrón

Cuando alguien dice:
- "implementa X, Y y Z" → X, Y, Z son sub-agentes paralelos
- "construye A y también B" → A y B en paralelo
- "necesito esto rápido" → siempre paralelo
- La tarea tiene 3+ componentes independientes → sub-agentes

*Fuente: ComposioHQ Superpowers Skills + Claude Agent SDK*
