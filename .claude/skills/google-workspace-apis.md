---
name: google-workspace-apis
description: >
  Integración directa con las Google Workspace APIs (Gmail, Calendar, Drive, Sheets, Docs,
  Admin SDK, Chat, Meet, People) desde un backend propio (FastAPI/Node en Vercel/Railway),
  como alternativa o complemento a Google Apps Script. Cubre autenticación (OAuth2 vs
  Service Account + Domain-Wide Delegation), cuotas y límites actuales, SDKs oficiales, y
  cuándo usar los servidores MCP oficiales de Google en vez de programar un wrapper propio.
  Usar cuando el proyecto necesite leer/escribir Gmail, Calendar, Drive, Sheets o Docs de
  forma automatizada, cuando se evalúe Apps Script vs API directa, o cuando un agente Claude
  deba operar sobre Workspace.
  Agentes: Cinthya, Sasha, Jarvis.
---

# Google Workspace APIs — Integración Directa

## Mapa de APIs disponibles

| API | Qué hace | Caso de uso típico |
|---|---|---|
| **Gmail API** | Leer/enviar/organizar correo: threads, messages, labels, drafts, watch (push) | Envío transaccional, clasificar correo entrante, sync a CRM |
| **Calendar API** | CRUD de eventos y calendarios, invitados, recurrencia, freebusy | Agendar citas, sincronizar disponibilidad, recordatorios |
| **Drive API** | Subir/descargar/buscar archivos, permisos, carpetas, shared drives | Backend que organiza archivos de usuarios |
| **Sheets API** | Leer/escribir celdas, fórmulas, formato, gráficos | Dashboards, reportes automáticos, ingestión de datos |
| **Docs API** | Leer/escribir documentos estructurados | Generación automática de contratos/propuestas |
| **Admin SDK** | Gestión de usuarios/grupos/dispositivos del dominio, Reports API | Provisioning, auditoría, compliance |
| **Chat API** | Spaces, mensajes, cards, membership | Bots de Chat, notificaciones a canales |
| **Meet API** | Conference records, participantes, artifacts (grabaciones, transcripciones) | Analítica de reuniones, extracción de actas |
| **People API** | CRUD de contactos, directorio del dominio | Sincronizar contactos con CRM |

Slides, Tasks, Vault (requiere licencia desde nov-2025), Groups Settings y Cloud Search son nicho — evaluar solo si el proyecto lo requiere específicamente.

## Autenticación: elige según quién usa la API

**OAuth2 (flujo de usuario)** — el usuario final autoriza explícitamente. Úsalo cuando el producto es B2C/multi-tenant y no controlas el dominio del cliente (ej. "Conectar tu Google Calendar" en un SaaS).

**Service Account + Domain-Wide Delegation (server-to-server)** — una credencial impersona a cualquier usuario del dominio, autorizada una vez por un Super Admin en el Admin Console. Sin prompts por usuario. Solo funciona dentro de un dominio Workspace propio, no en cuentas @gmail.com personales. Úsalo para automatización interna del propio equipo/negocio (ej. un backend en Vercel que lee/escribe Calendar y Gmail de cuentas internas).

Google recomienda evitar DWD si la tarea se resuelve con un Service Account normal u OAuth simple — DWD otorga confianza a nivel de admin y amplía la superficie de riesgo si la credencial se filtra.

## Cuotas actuales (verificar vigencia si pasó mucho tiempo desde jul-2026)

| API | Límite |
|---|---|
| Gmail API | 1.2M unidades/min/proyecto · 6,000 u/min/usuario. `messages.send`=100u, `messages.get`=20u, `messages.list`=5u |
| Sheets API | 300 lecturas/min/proyecto · 300 escrituras/min/proyecto (60/min por usuario cada una) |
| Drive API (post 1-may-2026) | 1M u/min/proyecto · 325K u/min/usuario · 400M u/día gratis |
| Calendar API (post 1-may-2026) | 10,000 req/min/proyecto · 600 req/min/usuario |
| Admin SDK Directory | 2,400 queries/min/usuario/proyecto (configurable) |

Si se excede: HTTP 429/403 → aplicar exponential backoff (reintentos con espera creciente hasta 32-64s).

Desde el 1-may-2026 Gmail/Calendar/Drive migraron a un modelo de "unidades ponderadas" con overage de pago futuro (aviso ≥90 días). Proyectos creados antes de esa fecha tienen ventana de gracia de al menos 60 días.

## SDKs oficiales

- **Node.js:** `googleapis` (npm) — mantenimiento activo por Google.
- **Python:** `google-api-python-client` — releases semanales.

Ambos son la vía estándar y soportada para Workspace APIs; no hay señal de deprecación.

## Cuándo usar API directa vs Apps Script vs MCP

| Dimensión | Apps Script | API directa (backend propio) |
|---|---|---|
| Setup OAuth | Mínimo, corre como el dueño del script | Requiere proyecto en Cloud Console + OAuth2/Service Account |
| Tiempo de ejecución | Límite duro de 6 min/ejecución, no negociable | Sin límite de Google, solo el de tu plataforma |
| Mantenimiento | Vive en Script Editor, sin CI/CD real | Vive en tu repo, con tests y versionado normal |
| Mejor para | Automatización desechable de 1 Sheet/Doc, 1-2 usuarios | Producto con lógica de negocio real, integraciones multi-servicio, equipo que ya despliega en Vercel/Railway |

**Regla práctica:** si la automatización vive y muere dentro de una Sheet/Doc y la usan 1-2 personas, Apps Script es más rápido. Si es un proceso de negocio que ya vive en el backend del equipo, usa la API directa (Service Account + DWD para uso interno, OAuth2 para clientes externos).

**Tercera vía (2026):** Google lanzó servidores MCP oficiales y gestionados para Gmail/Drive/Calendar/People/Chat (`developers.google.com/workspace/guides/configure-mcp-servers`). Si el objetivo es que un agente Claude/IA opere Workspace, evalúa primero el MCP server oficial antes de programar un wrapper propio — puede ahorrar semanas de desarrollo de auth.

## Antes de implementar

1. Verifica la documentación oficial vigente en `developers.google.com/workspace/[api]` — las cuotas y el modelo de pricing están en transición durante 2026.
2. Si es automatización interna del equipo → Service Account + DWD.
3. Si es un agente IA operando Workspace → revisa MCP servers oficiales primero.
4. Si es desechable de una sola Sheet/Doc → Apps Script, no sobre-construyas.

## Fuente
Informe completo con todas las URLs y fechas de consulta: `agentes/jade/reports/jade-google-workspace-apis-2026-07-24.md`. Revisar vigencia de cuotas/pricing si esta skill se usa mucho después de esa fecha.
