# MCPs Superpoderes — Skill transversal para todos los agentes

## Descripcion
Los 4 MCPs que expanden las capacidades de Claude Code con herramientas externas: transcripcion de video, scraping web, noticias en tiempo real, y automatizacion de navegador. Configurar una vez, disponibles para todos los agentes.

## Instrucciones

Cuando el usuario pida analizar videos, extraer datos web, investigar noticias recientes, o automatizar un navegador, usar los MCPs correspondientes segun la tarea.

---

## MCP 1 — Supadata (Transcripcion de Video)

**Que hace:** Transcribe videos completos de YouTube y obtiene metricas (vistas, likes, comentarios) sin abrir el navegador.

**Setup:**
1. Registrarse en supadata.ai y obtener API key
2. Agregar a `.mcp.json` en la raiz del proyecto:

```json
{
  "mcpServers": {
    "supadata": {
      "command": "npx",
      "args": ["-y", "@supadata/mcp-server"],
      "env": {
        "SUPADATA_API_KEY": "tu-api-key-aqui"
      }
    }
  }
}
```

3. Reiniciar Claude Code y verificar con `/mcp`

**Agentes que lo usan:** Jade (analisis de contenido), Erik (inspiracion de diseno)

**Casos de uso:**
- Analizar estrategia de contenido de competidores
- Extraer informacion de tutoriales y conferencias
- Generar resumen de un curso sin verlo completo
- Comparar metricas de videos propios vs competidores

---

## MCP 2 — Apify (Web Scraping)

**Que hace:** Despliega robots que visitan cualquier pagina y extraen informacion estructurada. Cientos de scrapers pre-construidos para Instagram, TikTok, Amazon, LinkedIn, etc.

**Setup:**
1. Crear cuenta en apify.com
2. Ir a Settings > Integrations > API tokens → copiar token
3. Agregar a `.mcp.json`:

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": ["-y", "@apify/mcp-server"],
      "env": {
        "APIFY_TOKEN": "tu-token-aqui"
      }
    }
  }
}
```

**NOTA:** Apify ya esta disponible en el setup actual de la Agencia. Solo configurar el token si no esta activo.

**Agentes que lo usan:** Jade (investigacion), Cinthya (pipelines de datos), Brook (data para dashboards)

**Casos de uso:**
- Scraping de redes sociales (posts, seguidores, engagement)
- Monitoreo de precios de competidores
- Extraccion de leads y datos de contacto
- Vigilancia de menciones de marca
- Datos para dashboards de clientes

---

## MCP 3 — Last 30 Days (Noticias y Tendencias)

**Que hace:** Skill de investigacion que trae noticias de los ultimos 30 dias sobre cualquier tema usando busqueda web organizada.

**Setup (sin API key requerida):**
```bash
claude install-skill https://github.com/mvanhorn/last30days-skill
```

**Agentes que lo usan:** Jade (briefings semanales), Jarvis (evaluacion de mercado)

**Casos de uso:**
- Briefing semanal de tendencias en IA para reunion del sabado
- Investigar noticias antes de evaluar un proyecto nuevo
- Monitorear competidores y sector de un cliente
- Identificar oportunidades de negocio emergentes
- Preparar contexto para decisiones estrategicas

---

## MCP 4 — Playwright CLI (Automatizacion de Navegador)

**Que hace:** Da a Claude su propio navegador Chromium para interactuar con sitios web: screenshots, formularios, tests, navegacion autonoma.

**Setup:**
```bash
# 1. Instalar globalmente
npm install -g @anthropic-ai/claude-code-playwright

# 2. Instalar Chromium
npx playwright install chromium

# 3. Agregar a .mcp.json (sin env variables):
```

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/claude-code-playwright"]
    }
  }
}
```

**VENTAJA vs Chrome MCP:** Consume menos tokens que la integracion con Chrome.

**Agentes que lo usan:** Brook (testing), Cinthya (automatizacion), Erik (screenshots para diseno)

**Casos de uso:**
- Screenshots de landing pages en diferentes dispositivos
- Testing automatizado de formularios y flujos de usuario
- Automatizacion de workflows repetitivos en sitios web
- Auditoria visual de sitios de competidores
- Llenado automatico de formularios en procesos internos

---

## Configuracion completa .mcp.json

Archivo de referencia con los 4 MCPs configurados:

```json
{
  "mcpServers": {
    "supadata": {
      "command": "npx",
      "args": ["-y", "@supadata/mcp-server"],
      "env": {
        "SUPADATA_API_KEY": "REEMPLAZAR"
      }
    },
    "apify": {
      "command": "npx",
      "args": ["-y", "@apify/mcp-server"],
      "env": {
        "APIFY_TOKEN": "REEMPLAZAR"
      }
    },
    "last30days": {
      "command": "claude",
      "args": ["install-skill", "https://github.com/mvanhorn/last30days-skill"]
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/claude-code-playwright"]
    }
  }
}
```

## Tabla de MCPs por agente

| Agente | Supadata | Apify | Last 30 Days | Playwright |
|--------|----------|-------|--------------|------------|
| Jade | ✅ analisis de videos | ✅ investigacion | ✅ briefings | - |
| Jarvis | - | ✅ evaluacion mercado | ✅ tendencias | - |
| Sasha | - | - | - | ✅ testing |
| Brook | - | ✅ datos para dashboards | - | ✅ testing UI |
| Erik | ✅ inspiracion contenido | - | - | ✅ screenshots |
| Cinthya | - | ✅ pipelines datos | - | ✅ automatizacion |

## Tips de uso

- Proporcionar URLs exactas en vez de peticiones vagas
- Usar Plan Mode (Shift+Tab) para tareas multi-MCP complejas
- Especificar explicitamente que MCP usar: "usa Playwright para tomar un screenshot de..."
- Playwright consume menos tokens que la alternativa Chrome MCP
