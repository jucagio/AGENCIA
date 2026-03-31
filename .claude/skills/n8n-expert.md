# n8n Expert — Skill para Claude Code

## Descripcion
Skill experta en n8n para disenar, implementar y depurar workflows de automatizacion. Cubre desde la arquitectura de flujos hasta patrones avanzados de error handling, credenciales y webhooks. Optimizada para el agente Cinthya de la Agencia.

## Instrucciones

Cuando el usuario pida ayuda con n8n, sigue estas directrices:

### Arquitectura de Workflows

1. **Estructura de nodos**: Siempre disenar flujos de izquierda a derecha, con un trigger claro al inicio.
2. **Naming convention**: Nombrar cada nodo con su funcion especifica (ej: "Fetch Orders from Supabase", no "HTTP Request 1").
3. **Modularidad**: Dividir flujos complejos en sub-workflows reutilizables usando el nodo "Execute Workflow".
4. **Documentacion inline**: Usar nodos Sticky Note para documentar secciones del flujo.

### Triggers Disponibles (n8n v1.x+)

| Tipo | Nodo | Caso de uso |
|------|------|-------------|
| **Webhook** | Webhook / Webhook Response | APIs externas, formularios, eventos en tiempo real |
| **Schedule** | Schedule Trigger | Tareas periodicas (cron) |
| **Event** | n8n Trigger | Workflow completado, error en otro workflow |
| **App** | Trigger de cada integracion | Gmail, Slack, GitHub, Supabase, etc. |
| **Manual** | Manual Trigger | Testing y ejecucion bajo demanda |
| **Chat** | Chat Trigger | Chatbots y interfaces conversacionales |

### Patrones de Error Handling

```
Patron 1 — Try/Catch con Error Trigger:
  [Trigger] → [Try: Nodos principales] → [Output]
                    ↓ (on error)
              [Error Trigger] → [Notificar Slack] → [Log en Supabase]

Patron 2 — Retry Logic:
  [HTTP Request] (configurar: retry on fail = true, max retries = 3, wait between = 1000ms)

Patron 3 — Validacion previa:
  [Trigger] → [IF: datos validos?] → SI → [Procesar]
                                    → NO → [Notificar error] → [Stop]
```

### Credenciales y Seguridad

- NUNCA hardcodear credenciales en expresiones. Usar siempre el sistema de credenciales de n8n.
- Para APIs: crear credenciales tipo "Header Auth" o "OAuth2" segun el servicio.
- Para Supabase: usar credencial tipo "Supabase API" con la service_role key (backend) o anon key (frontend).
- Para webhooks entrantes: siempre agregar autenticacion (Header Auth o Basic Auth).
- Variables de entorno: usar `$env` para configuracion que cambia entre ambientes.

### Integraciones Clave para la Agencia

**Supabase:**
- Nodo: Supabase (nativo en n8n)
- Operaciones: Get All, Get, Create, Update, Delete, Upsert
- Para queries complejas: usar nodo HTTP Request con la API REST de Supabase
- RLS: recordar que las credenciales service_role bypasean RLS

**Slack / Discord / Telegram:**
- Preferir nodos nativos sobre HTTP Request
- Para mensajes ricos: usar Block Kit (Slack) o Embeds (Discord)
- Rate limits: Slack = 1 msg/sec por canal, Telegram = 30 msg/sec

**GitHub:**
- Trigger: GitHub Trigger para push, PR, issues
- Operaciones: crear issues, comentar PRs, crear releases
- Usar personal access token con scopes minimos

**Claude API (Anthropic):**
- Nodo: HTTP Request al endpoint `https://api.anthropic.com/v1/messages`
- Headers: `x-api-key`, `anthropic-version: 2023-06-01`, `content-type: application/json`
- Modelos disponibles: claude-sonnet-4-20250514, claude-haiku-235-20250512, claude-opus-4-20250514
- Para tareas simples (clasificacion, extraccion): usar haiku
- Para tareas complejas (analisis, redaccion): usar sonnet
- Para decisiones criticas: usar opus
- Max tokens: usar `max_tokens` (NO budget_tokens, esta deprecado)

### Patrones de Workflow Comunes

**1. Webhook a Supabase con validacion:**
```
[Webhook] → [IF: tiene campos requeridos] → [Supabase: Insert] → [Webhook Response: 200]
                                           → [Webhook Response: 400 Bad Request]
```

**2. Reporte programado:**
```
[Schedule: cada lunes 9am] → [Supabase: Get metricas] → [Code: calcular resumen]
  → [Slack: enviar reporte] → [Gmail: enviar copia a Juan Camilo]
```

**3. Pipeline de procesamiento:**
```
[Trigger] → [Split In Batches: 10] → [HTTP Request: API externa]
  → [Merge] → [Supabase: Upsert resultados] → [Slack: notificar completado]
```

**4. Chatbot con IA:**
```
[Chat Trigger] → [Code: preparar prompt] → [HTTP Request: Claude API]
  → [Code: parsear respuesta] → [Chat Response]
```

**5. Monitor de errores:**
```
[Error Trigger (de otro workflow)] → [Code: formatear error]
  → [Supabase: log error] → [Slack: alerta al canal #errores]
```

### Nodo Code (JavaScript)

El nodo Code en n8n ejecuta JavaScript. Patrones importantes:

```javascript
// Acceder a datos de nodos anteriores
const items = $input.all();
const firstItem = $input.first();

// Acceder a datos de un nodo especifico
const webhookData = $('Webhook').first().json;

// Retornar datos (siempre array de objetos con propiedad json)
return items.map(item => ({
  json: {
    processed: true,
    original: item.json,
    timestamp: new Date().toISOString()
  }
}));

// Variables de entorno
const apiKey = $env.API_KEY;

// Hacer HTTP requests dentro del Code node
const response = await fetch('https://api.example.com/data', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ key: 'value' })
});
const data = await response.json();
return [{ json: data }];
```

### Debugging

1. **Execution log**: Revisar en n8n > Executions el log detallado de cada ejecucion.
2. **Pin data**: Fijar datos de prueba en nodos para testear sin ejecutar todo el flujo.
3. **Test workflow**: Crear un workflow de prueba que simule datos antes de conectar al real.
4. **Console log**: En nodo Code, usar `console.log()` y revisar en los logs del servidor n8n.

### Deploy y Operaciones

- **Self-hosted (recomendado)**: Docker en Railway o Render
  ```
  docker run -d --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n n8nio/n8n
  ```
- **n8n Cloud**: Para proyectos de clientes que no quieren mantener infraestructura
- **Backups**: Exportar workflows como JSON periodicamente. Guardar en el repositorio Git.
- **Versionado**: Cada workflow exportado incluye su version. Mantener un changelog.

### Mejores Practicas

1. Siempre testear con datos reales antes de activar un workflow.
2. Configurar timeout en nodos HTTP (default 60s, ajustar segun el servicio).
3. Usar el nodo "Wait" para rate limiting en lugar de loops rapidos.
4. Para flujos criticos: agregar nodo de notificacion al final (exito) y en error handling (fallo).
5. Documentar CADA workflow con un Sticky Note al inicio que explique: proposito, trigger, dependencias, contacto.
6. No crear mega-workflows. Si un flujo tiene mas de 20 nodos, dividirlo en sub-workflows.
7. Usar tags para organizar workflows: por proyecto, por equipo, por estado (dev/staging/prod).
