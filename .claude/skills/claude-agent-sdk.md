# Claude Agent SDK — Skill para Claude Code

## Descripcion
Skill para disenar, implementar y optimizar sistemas multi-agente con Claude Code y el Claude Agent SDK. Cubre sub-agentes paralelos, orquestacion, routing de modelos haiku/sonnet/opus, y patrones de produccion. Optimizada para toda la Agencia.

## Instrucciones

Cuando el usuario pida ayuda con agentes de Claude, sub-agentes o el Agent SDK, sigue estas directrices:

### Arquitectura de Agentes en Claude Code

**Estructura de archivos para agentes:**
```
.claude/
  agents/
    jarvis.md          # System prompt del agente
    sasha.md
    brook.md
    erik.md
    cinthya.md
    jade.md
    ego.md
  skills/
    n8n-expert.md      # Skills compartidas
    flutter-expert.md
    fastapi-expert.md
  settings.local.json  # Configuracion local
CLAUDE.md              # Instrucciones globales del proyecto
```

**System prompt de un agente (formato .md):**
```markdown
# Nombre del Agente — Rol

## Identidad
Descripcion clara del rol, responsabilidades y personalidad.

## Reglas
- Regla 1
- Regla 2

## Workflow
Pasos que sigue para completar tareas.

## Herramientas
Skills y tools que usa.

## Coordinacion
Con quien trabaja y como.
```

### Routing Inteligente de Modelos

| Modelo | Costo relativo | Cuándo usar |
|--------|---------------|-------------|
| **haiku** | 1x | Clasificacion, extraccion de datos, formateo, tareas repetitivas, routing |
| **sonnet** | 5x | Coding de features, investigacion, redaccion, analisis, frontend, diseno |
| **opus** | 25x | Arquitectura, decisiones criticas, seguridad, auditorias, debugging complejo |

**Patron de routing:**
```
Input del usuario
  ↓
[haiku] Clasifica la tarea: simple / media / compleja
  ↓
simple → [haiku] ejecuta
media  → [sonnet] ejecuta
compleja → [opus] ejecuta
```

**En Claude Code, el modelo se configura por agente:**
- En `.claude/agents/nombre.md` no se especifica el modelo directamente
- El modelo se selecciona al invocar: `@agente` usa el modelo configurado en la terminal/sesion
- Para optimizar costos: usar Claude Code con sonnet por defecto, elevar a opus solo para tareas criticas

### Sub-agentes Paralelos

**Cuando usar sub-agentes:**
- Tareas independientes que pueden ejecutarse en paralelo
- Cada sub-agente trabaja en un scope aislado (archivo, feature, test)
- El agente principal coordina y verifica resultados

**Patron de invocacion (en prompts):**
```
Implementa las siguientes tareas usando sub-agentes en paralelo:
1. Sub-agente 1: [tarea A en archivo X]
2. Sub-agente 2: [tarea B en archivo Y]
3. Sub-agente 3: [tarea C en archivo Z]

Cada sub-agente debe:
- Trabajar solo en su scope asignado
- No modificar archivos de otros sub-agentes
- Reportar resultado al finalizar
```

**Mejores practicas para sub-agentes:**
1. Definir scope claro para cada sub-agente (archivos especificos)
2. Evitar que dos sub-agentes modifiquen el mismo archivo
3. El agente principal verifica la integracion despues
4. Usar para: tests, endpoints independientes, componentes UI, documentacion

### Claude API — Patrones de Integracion

**Llamada basica (Python):**
```python
import anthropic

client = anthropic.Anthropic()  # Lee ANTHROPIC_API_KEY del env

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Analiza este codigo..."}
    ]
)
print(message.content[0].text)
```

**Con system prompt y tool use:**
```python
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    system="Eres un experto en seguridad OWASP. Analiza codigo y reporta vulnerabilidades.",
    tools=[
        {
            "name": "report_vulnerability",
            "description": "Reporta una vulnerabilidad encontrada en el codigo",
            "input_schema": {
                "type": "object",
                "properties": {
                    "severity": {"type": "string", "enum": ["critical", "high", "medium", "low"]},
                    "type": {"type": "string", "description": "Tipo OWASP (ej: SQL Injection)"},
                    "location": {"type": "string", "description": "Archivo y linea"},
                    "description": {"type": "string"},
                    "fix": {"type": "string", "description": "Como corregirlo"}
                },
                "required": ["severity", "type", "location", "description", "fix"]
            }
        }
    ],
    messages=[
        {"role": "user", "content": f"Analiza este codigo:\n```python\n{code}\n```"}
    ]
)
```

**Streaming:**
```python
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    messages=[{"role": "user", "content": "Escribe un analisis detallado..."}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

**Batch API (para procesamiento masivo):**
```python
# Crear batch
batch = client.batches.create(
    requests=[
        {
            "custom_id": f"task-{i}",
            "params": {
                "model": "claude-haiku-3-5-20241022",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": prompt}]
            }
        }
        for i, prompt in enumerate(prompts)
    ]
)

# Verificar estado
batch_status = client.batches.retrieve(batch.id)
# Cuando batch_status.processing_status == "ended", descargar resultados
```

### IMPORTANTE: Cambios en la API (2025-2026)

1. **`budget_tokens` esta DEPRECADO** en Opus 4.6 y Sonnet 4.6. Usar `max_tokens` unicamente.
2. **Extended thinking**: Para tareas que requieren razonamiento profundo, usar el parametro `thinking` con los modelos que lo soporten.
3. **Modelo naming**: Los modelos mas recientes usan el formato `claude-{tier}-{version}-{date}`.

### Patrones de Orquestacion Multi-Agente

**Patron 1 — Pipeline secuencial:**
```
[Agente A] → output → [Agente B] → output → [Agente C]
Ejemplo: Sasha (API) → Brook (frontend) → Erik (diseño)
```

**Patron 2 — Fan-out / Fan-in (paralelo):**
```
                → [Sub-agente 1] →
[Orquestador] → [Sub-agente 2] → [Orquestador verifica]
                → [Sub-agente 3] →
Ejemplo: Jarvis asigna 3 features independientes en paralelo
```

**Patron 3 — Router (clasificacion + despacho):**
```
[Input] → [Router haiku] → simple → [haiku ejecuta]
                         → medio  → [sonnet ejecuta]
                         → complejo → [opus ejecuta]
Ejemplo: Jade clasifica tareas antes de asignar modelo
```

**Patron 4 — Supervisor con feedback loop:**
```
[Agente ejecuta] → [Supervisor revisa] → aprobado → [siguiente paso]
                                       → rechazado → [agente corrige]
Ejemplo: Ego audita el trabajo de Sasha, si hay gaps, Jade capacita
```

### CLAUDE.md — Mejores Practicas

El archivo `CLAUDE.md` es el system prompt global del proyecto. Estructura recomendada:

```markdown
# Proyecto — Descripcion corta

## Rules
Reglas que SIEMPRE se aplican (anti-alucinacion, verificacion, etc.)

## Equipo
Organigrama y roles de agentes.

## Stack Tecnologico
Tecnologias, versiones, convenciones.

## Flujo de Trabajo
Como se ejecutan las tareas paso a paso.

## Convenciones de Codigo
Naming, estructura, patrones.

## Proyectos Activos
Lista de proyectos en curso con estado.
```

**Tips para CLAUDE.md efectivo:**
1. Mantenerlo conciso pero completo. Los agentes lo leen en cada sesion.
2. Las `## Rules` al inicio tienen maxima prioridad.
3. Usar tablas para informacion estructurada (agentes, modelos, herramientas).
4. Actualizar frecuentemente con nuevos proyectos y decisiones.
5. No duplicar informacion que esta en los archivos de agente individuales.

### Evaluacion de Agentes (para Ego)

**Metricas clave:**
1. **Precision**: El agente completa correctamente la tarea asignada?
2. **Eficiencia**: Cuantos tokens/tiempo usa vs. lo esperado?
3. **Seguridad**: Sigue las reglas anti-alucinacion y de seguridad?
4. **Coordinacion**: Se comunica correctamente con otros agentes?
5. **Autonomia**: Resuelve sin ayuda o escala apropiadamente?

**Framework LLM-as-Judge:**
```
Evalua la respuesta del agente [nombre] en la tarea [descripcion].

Criterios (1-5):
- Correctitud: La solucion funciona y es correcta?
- Completitud: Cubrio todos los requerimientos?
- Calidad de codigo: Sigue las convenciones del proyecto?
- Seguridad: No introdujo vulnerabilidades?
- Documentacion: Explico lo que hizo y por que?

Puntuacion total: [suma/25]
Recomendacion: [aprobado / necesita revision / rechazado]
```

### Mejores Practicas Generales

1. **Un agente, una responsabilidad.** No sobrecargar agentes con multiples dominios.
2. **Documentar decisiones.** Cada decision arquitectonica debe quedar en un ADR o en CLAUDE.md.
3. **Sub-agentes para velocidad.** Siempre que haya tareas independientes, paralelizar.
4. **Routing de modelos para costos.** Haiku para lo simple, sonnet para lo medio, opus para lo critico.
5. **Feedback loops.** Ego → Jade → Agente mejora. No dejar que los errores se repitan.
6. **Prompts especificos.** Mientras mas especifico el prompt, mejor el resultado. Evitar instrucciones vagas.
7. **Verificar documentacion.** Antes de implementar, buscar la documentacion mas reciente.
8. **No confiar ciegamente.** Siempre revisar el output de los agentes, especialmente en seguridad.
