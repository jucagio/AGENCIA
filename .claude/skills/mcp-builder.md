---
name: mcp-builder
description: >
  Crear servidores MCP (Model Context Protocol) personalizados para extender las
  capacidades de Claude con herramientas, recursos y prompts propios. Usar cuando
  se necesite conectar Claude a una API interna, base de datos, o servicio externo
  sin disponible en el marketplace de MCPs. Agentes: Jarvis, Cinthya, Sasha.
---

# MCP Builder — Crear Servidores MCP Personalizados

## ¿Qué es MCP?

El **Model Context Protocol (MCP)** es un estándar abierto de Anthropic que permite a Claude conectarse con herramientas y datos externos de forma segura. Un servidor MCP expone:

- **Tools** — funciones que Claude puede llamar (buscar en BD, enviar email, crear issue)
- **Resources** — datos que Claude puede leer (archivos, URLs, bases de datos)
- **Prompts** — templates reutilizables para tareas específicas

```
Claude ↔ MCP Protocol ↔ Tu Servidor MCP ↔ Tu API/BD/Servicio
```

---

## Setup inicial — Python (SDK oficial Anthropic)

```bash
pip install mcp
```

```python
# server.py — estructura básica de un servidor MCP
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

# Crear el servidor
server = Server("mi-servidor-mcp")

# Listar las tools disponibles
@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="buscar_cliente",
            description="Busca un cliente en la base de datos por email o nombre",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Email o nombre del cliente"
                    }
                },
                "required": ["query"]
            }
        )
    ]

# Implementar la ejecución de cada tool
@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "buscar_cliente":
        query = arguments["query"]
        # Tu lógica real aquí
        results = await search_customers_in_db(query)
        return [types.TextContent(type="text", text=str(results))]

    raise ValueError(f"Tool desconocida: {name}")

# Ejecutar el servidor
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

---

## Setup inicial — TypeScript/Node.js

```bash
npm install @modelcontextprotocol/sdk
```

```typescript
// server.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  { name: "mi-servidor-mcp", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// Definir tools
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "crear_tarea",
      description: "Crea una tarea en el sistema de gestión",
      inputSchema: {
        type: "object",
        properties: {
          titulo: { type: "string", description: "Título de la tarea" },
          asignado_a: { type: "string", description: "Email del responsable" },
          prioridad: { type: "string", enum: ["alta", "media", "baja"] }
        },
        required: ["titulo"]
      }
    }
  ]
}));

// Implementar tools
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "crear_tarea") {
    const { titulo, asignado_a, prioridad } = request.params.arguments as any;
    const tarea = await crearTareaEnSistema({ titulo, asignado_a, prioridad });
    return {
      content: [{ type: "text", text: `Tarea creada: ${JSON.stringify(tarea)}` }]
    };
  }
  throw new Error(`Tool desconocida: ${request.params.name}`);
});

// Iniciar servidor
const transport = new StdioServerTransport();
await server.connect(transport);
```

---

## Registrar el MCP en Claude Code

```json
// .claude/settings.json o ~/.claude/settings.json
{
  "mcpServers": {
    "mi-servidor": {
      "command": "python",
      "args": ["ruta/al/server.py"],
      "env": {
        "DATABASE_URL": "postgresql://...",
        "API_KEY": "mi-api-key"
      }
    }
  }
}
```

---

## Patterns avanzados

### MCP con Resources (datos que Claude puede leer)

```python
@server.list_resources()
async def list_resources() -> list[types.Resource]:
    return [
        types.Resource(
            uri="agencia://proyectos/activos",
            name="Proyectos Activos",
            description="Lista de proyectos activos de la Agencia",
            mimeType="application/json"
        )
    ]

@server.read_resource()
async def read_resource(uri: str) -> str:
    if uri == "agencia://proyectos/activos":
        proyectos = await db.get_active_projects()
        return json.dumps(proyectos, ensure_ascii=False)
```

### MCP con Prompts reutilizables

```python
@server.list_prompts()
async def list_prompts() -> list[types.Prompt]:
    return [
        types.Prompt(
            name="analizar_cliente",
            description="Genera un análisis comercial de un cliente",
            arguments=[
                types.PromptArgument(
                    name="empresa",
                    description="Nombre de la empresa",
                    required=True
                )
            ]
        )
    ]

@server.get_prompt()
async def get_prompt(name: str, arguments: dict) -> types.GetPromptResult:
    if name == "analizar_cliente":
        empresa = arguments["empresa"]
        return types.GetPromptResult(
            description=f"Análisis de {empresa}",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Analiza comercialmente a {empresa}. Identifica: industria, tamaño, dolores principales y oportunidad para la Agencia."
                    )
                )
            ]
        )
```

---

## MCPs útiles para construir en la Agencia

| MCP | Qué hace | Agente que lo usa |
|-----|----------|------------------|
| **supabase-internal** | CRUD directo a las BDs de los proyectos | Sasha, Brook |
| **github-agencia** | Crear issues, PRs, revisar código | Jarvis, Sasha |
| **notion-memoria** | Leer/escribir en Notion como memoria | Jade, Yang |
| **whatsapp-notify** | Enviar notificaciones a Juan Camilo | Cinthya |
| **google-calendar** | Crear eventos de reuniones | Jarvis |

---

## Checklist antes de publicar un MCP

```
[ ] Cada tool tiene descripción clara (Claude la usa para decidir cuándo llamarla)
[ ] inputSchema es preciso con tipos y campos required
[ ] Errores manejados con mensajes útiles (no stack traces)
[ ] Variables sensibles en env vars, nunca hardcodeadas
[ ] MCP registrado en settings.json con env vars correctas
[ ] Tool probada manualmente antes de usar con Claude
[ ] README con: descripción, setup, lista de tools disponibles
```

*Fuente: Anthropic MCP Official Documentation + MCP Builder Skill*
