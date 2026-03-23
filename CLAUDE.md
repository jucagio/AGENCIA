# AGENCIA — Proyecto de Agentes Claude Code

## Rules

ALWAYS before making any change. Search on the web for the newest documentation.
And only implement if you are 100% sure it will work.

## Agentes disponibles en esta agencia

| Agente | Especialidad | Cuándo convocarlo |
|--------|-------------|-------------------|
| **Jarbis** | Gerente técnico de software | Gestión de proyectos, decisiones de arquitectura, liderazgo de equipo, cursos VS Code |
| **Jade** | Capacitadora de equipo | Onboarding, documentación, mantener al equipo actualizado, transferencia de conocimiento |

## Tips de productividad (aplicar siempre)

### Tip 1 — Ultrathink
Agrega `Ultrathink` al final de tu prompt para activar análisis más profundo y razonamiento extendido.

```
Ejemplo: "Revisa este bug y dame una solución. Ultrathink"
```

### Tip 2 — Sub-agentes paralelos
Pide explícitamente el uso de sub-agentes para tareas complejas — resuelve 10x más rápido.

```
Ejemplo: "Analiza el proyecto. Usa sub-agentes para explorar múltiples partes en paralelo."
```

### Tip 3 — Regla anti-alucinación (ya está aplicada arriba)
El `## Rules` al inicio de este archivo garantiza que Claude busque documentación actualizada antes de implementar, eliminando el 95% de las alucinaciones.

## Cómo invocar a los agentes

En Claude Code (VS Code), usa `@nombre-agente` para convocar a un agente:

```
@jarbis Necesito planificar los sprints del próximo mes. Ultrathink
@jade Crea un plan de onboarding para el nuevo desarrollador que entra la próxima semana.
```

O desde claude.ai o terminal:
```bash
# Los agentes son sub-agentes reutilizables de la agencia
# Se invocan automáticamente según el tipo de tarea
```

## Convenciones del proyecto

- Todos los agentes usan `claude-sonnet-4-6` por defecto
- Los agentes pueden lanzar sub-agentes paralelos para tareas complejas
- Siempre verificar documentación oficial antes de implementar
- Commitear con mensajes descriptivos en español o inglés
