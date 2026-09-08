# INFORME DE INTELIGENCIA — Google Workspace APIs
## 24 de julio de 2026 | Preparado por Jade para Jarvis

### Resumen ejecutivo

Las Workspace APIs (Gmail, Calendar, Drive, Sheets, Docs, Admin SDK, Chat, Meet, People) son gratuitas dentro de cuotas amplias, están activamente mantenidas (SDKs Node/Python con releases semanales) y desde el **1 de mayo de 2026** entraron en un nuevo modelo de cuotas "por unidades" con overage de pago que llegará más adelante en 2026. La novedad estructural más grande del año es que Google lanzó **servidores MCP oficiales y gestionados por Google** para Gmail/Drive/Calendar/People/Chat — esto crea una tercera opción además de "API directa" y "Apps Script": conectar agentes IA (Claude, Antigravity) directo a Workspace sin escribir el wrapper OAuth. Para automatización server-to-server sin usuario presente, Service Account + Domain-Wide Delegation sigue siendo el patrón correcto; para apps donde el usuario final autoriza, OAuth2 estándar.

### Mapa de APIs disponibles

| API | Qué hace | Caso de uso típico |
|---|---|---|
| **Gmail API** | Leer/enviar/organizar correo: threads, messages, labels, drafts, filtros, watch (push notifications) | Automatizar envío transaccional, clasificar/etiquetar correo entrante, sincronizar leads a CRM |
| **Calendar API** | CRUD de eventos y calendarios, invitados, recurrencia, disponibilidad (freebusy), Events API para import/export de reuniones | Agendar citas automáticamente, sincronizar disponibilidad, recordatorios |
| **Drive API** | Subir/descargar/buscar archivos, gestionar permisos y carpetas, shared drives, changes feed | Backend que guarda/organiza archivos de usuarios, sincronización de documentos |
| **Sheets API** | Leer/escribir celdas, fórmulas, formato, gráficos, hojas múltiples | Dashboards, reportes automáticos, ingestión de datos desde apps externas |
| **Docs API** | Leer/escribir documentos de texto estructurados (párrafos, tablas, estilos) | Generación automática de contratos, propuestas, reportes con formato |
| **Admin SDK (Directory API + otros)** | Gestión de usuarios, grupos, dispositivos, orgunits del dominio; Reports API para auditoría; límites y cuotas del propio Admin Console | Provisioning/deprovisioning de usuarios, auditoría de seguridad, compliance |
| **Chat API** | Crear/gestionar "spaces" (salas), enviar/leer mensajes, cards, membership, eventos de espacio | Bots de Chat, notificaciones a canales de equipo, integraciones tipo Slack |
| **Meet API** | Gestionar conference records, participantes, artifacts (grabaciones MP4 en Drive, transcripciones en Docs), suscripción a eventos vía Pub/Sub | Analítica de reuniones, extracción automática de transcripciones/actas |
| **People API (reemplaza Contacts API)** | CRUD de contactos personales, "other contacts", directorio del dominio (listDirectoryPeople/searchDirectoryPeople) | Sincronizar contactos con CRM, autocompletar directorio interno |
| Slides API, Tasks API, Vault API, Groups Settings API, Cloud Search API | Presentaciones, tareas, eDiscovery/legal hold (licencia Vault obligatoria desde nov-2025), config de grupos, búsqueda empresarial | Nicho — evaluar solo si el proyecto lo requiere específicamente |

### Autenticación: OAuth2 vs Service Account

**OAuth2 (flujo de usuario / consentimiento):**
- Cada usuario autoriza la app explícitamente (pantalla de consentimiento).
- Funciona tanto con cuentas Workspace como con Gmail personales.
- Úsalo cuando construyes un producto B2C/multi-tenant donde no controlas el dominio del cliente, o donde el usuario debe ver y aprobar qué se comparte.
- Ejemplo: una app SaaS que ofrece "Conectar tu Google Calendar" a clientes externos de distintas empresas.

**Service Account + Domain-Wide Delegation (server-to-server):**
- Una sola credencial de Service Account puede impersonar a cualquier usuario del dominio, autorizada una vez por un Super Admin de Workspace en el Admin Console.
- No hay prompts de consentimiento por usuario — acceso "silencioso" en background.
- Solo funciona dentro de un dominio Workspace propio (no en cuentas @gmail.com personales).
- Úsalo para herramientas internas: archivado de correo, sincronización masiva de calendarios, compliance, backend que opera sobre *todos* los usuarios de la organización de Jarvis/Juan Camilo.
- Google recomienda evitar DWD si la tarea se puede lograr con un Service Account normal o con OAuth simple, porque DWD otorga confianza a nivel de admin y amplía superficie de riesgo si la credencial se filtra.
- Ejemplo concreto para AGENCIA: si Jarvis construye un backend en Vercel que debe leer/escribir el Calendar y Gmail de cuentas internas del equipo (no de clientes externos), Service Account + DWD es el patrón correcto — sin fricción de OAuth por cada agente.

### Cuotas y límites actuales

| API | Límite | Fuente / fecha de consulta |
|---|---|---|
| **Gmail API** | 1,200,000 unidades/min por proyecto · 6,000 unidades/min por usuario. Umbral gratis: 80M unidades/día antes de posible cobro. Costos por método: `messages.send`=100u, `messages.get`=20u, `messages.list`=5u, `getProfile`=1u | developers.google.com/workspace/gmail/api/reference/quota — consultado 2026-07-24 |
| **Sheets API** | 300 lecturas/min por proyecto (60/min por usuario) · 300 escrituras/min por proyecto (60/min por usuario). Payload recomendado ≤2MB, timeout 180s | developers.google.com/workspace/sheets/api/limits — consultado 2026-07-24 |
| **Drive API (proyectos nuevos, post 1-may-2026)** | Modelo por unidades: 1,000,000 u/min por proyecto · 325,000 u/min por usuario · 400,000,000 u/día (umbral gratis) · 1TB egress/día. Costos: lectura=5u, listado=100u, descarga=200u, edición=50u. Subida diaria máx. 750GB, archivo máx. 5TB | developers.google.com/workspace/drive/api/guides/limits — consultado 2026-07-24 |
| **Drive API (proyectos legacy, pre 1-may-2026)** | 20,000 llamadas/100s por usuario y por proyecto. Escrituras: máx. ~3 req/seg sostenidas por cuenta (no se puede aumentar) | mismo — consultado 2026-07-24 |
| **Calendar API (proyectos nuevos, post 1-may-2026)** | 10,000 requests/min por proyecto · 600 requests/min por usuario | developers.google.com/workspace/calendar/api/guides/quota — consultado 2026-07-24 |
| **Admin SDK Directory API** | 2,400 queries/min por usuario por proyecto (default, configurable en Cloud Console) · límite `rateLimitExceeded` por cuenta Workspace que NO se puede aumentar | developers.google.com/workspace/admin/directory/v1/limits — consultado 2026-07-24 |

**Qué pasa si se excede:** respuesta HTTP 429 ("Too many requests") o 403 ("User rate limit exceeded"). La práctica recomendada por Google es exponential backoff (reintentos con espera creciente, típicamente hasta 32-64s) y esperar a que la ventana de 1 minuto se reinicie.

### Pricing

- **Gratis dentro de los umbrales estándar** para todas las APIs listadas — no depende de tener una licencia Workspace de pago para consumir la API en sí (aunque algunas funcionalidades del *producto* sí requieren licencia, ej. Vault desde nov-2025 requiere licencia Vault).
- **Cambio en curso 2026:** desde el 1 de mayo de 2026 Google introdujo un "modelo estandarizado de cuotas para tools de agentes y APIs" (developers.google.com/workspace/tools-safety) que reescala las cuotas por unidad (no por request plano) en Gmail, Calendar y Drive. Google estima que **menos del 1% de desarrolladores activos** necesitará superar el tier estándar.
- **Overage de pago:** más adelante en 2026 (con ≥90 días de aviso) Google habilitará una opción paga para escalar cuota más allá del umbral diario estándar — requerirá tener billing de Google Cloud habilitado en el proyecto.
- Proyectos creados antes del 1-may-2026 conservan sus cuotas anteriores por un período de gracia (mínimo 60 días) antes de migrar al nuevo modelo.

### SDKs recomendados (Node.js / Python)

- **Node.js:** paquete `googleapis` (npm) — versión actual 173.x, publicada hace ~2 meses, mantenimiento activo por Google.
- **Python:** `google-api-python-client` (PyPI/GitHub `googleapis/google-api-python-client`) — versión actual 2.187.x, con **releases semanales**. Google recomienda para *código nuevo* evaluar las "Cloud Client Libraries" específicas por producto cuando existen, pero el cliente basado en discovery sigue siendo la vía estándar y soportada para Workspace APIs.
- Ambos son oficiales, de código abierto, y siguen recibiendo actualizaciones activas en 2026 — no hay señal de deprecación.

### Workspace APIs vs Google Apps Script — cuándo usar cada uno

| Dimensión | Apps Script | Workspace APIs directo (backend Vercel/Railway) |
|---|---|---|
| **Setup / curva OAuth** | Mínimo — corre como el usuario/dueño del script, o vía triggers; no necesitas gestionar tokens OAuth manualmente | Requiere configurar proyecto en Google Cloud Console, OAuth2 o Service Account + DWD, gestión de tokens/refresh |
| **Tiempo de ejecución** | Límite duro de **6 minutos por ejecución**, igual en cuenta gratis y Workspace (no se puede pagar para extenderlo). Triggers comparten pool diario: 90 min/día (consumer) vs 6h/día (Workspace) | Sin límite de ejecución impuesto por Google — limitado solo por el runtime de tu plataforma (ej. timeout de función serverless en Vercel) |
| **Cuotas diarias** | UrlFetch: 20,000/día (consumer) vs 100,000/día (Workspace); envío de email: 100/día vs 1,500-2,000/día | Cuotas por minuto de cada API (ver tabla arriba) — generalmente más generosas para volumen sostenido, pero requieren backoff propio |
| **Latencia** | Ejecuta dentro de la infraestructura de Google, sin salto de red extra hacia tu app — bueno para automatizaciones "in-house" del propio Workspace | Salto de red extra (tu servidor → Google API), pero permite integrar con el resto de tu stack (DB, otras APIs, lógica de negocio compleja) sin reescribir en Apps Script (JavaScript limitado, sin npm) |
| **Mantenimiento** | Vive dentro de Google (Script Editor), versionado más frágil, sin CI/CD real, sin tests estándar | Vive en tu repo, con CI/CD, tests, control de versiones normal, reutilizable entre proyectos |
| **Costo** | Siempre gratis (cuota escala con tipo de cuenta, no se puede comprar cuota extra por separado) | Gratis dentro de cuota; overage de pago llegará en 2026 si excedes umbrales |
| **Mejor para** | Automatizaciones simples y rápidas *dentro* del ecosistema Workspace (ej. script en una Sheet que envía correos, trigger on-edit), prototipos, tareas de un solo usuario/dominio | Productos con lógica de negocio real, integraciones multi-servicio, necesidad de escalar, equipos que ya despliegan en Vercel/Railway y quieren todo en un solo stack |
| **Tercera vía (nueva, 2026)** | — | **Servidores MCP oficiales de Google** (Gmail, Drive, Calendar, People, Chat) — permiten que un agente IA (Claude, etc.) opere Workspace sin que tú escribas el wrapper OAuth/API; más de 50 MCP servers de Google GA/preview anunciados en Cloud Next '26 |

**Regla práctica de Jade:** si la automatización vive y muere dentro de una Sheet/Doc/Form y la usa 1-2 personas, Apps Script es más rápido de lanzar. Si es un producto o proceso de negocio que ya vive en tu backend (Vercel/Railway) y necesita testing, versionado y escalar más allá de una cuenta, usa la API directa con Service Account + DWD (para automatización interna) o OAuth2 (para clientes externos). Si el objetivo es que un agente Claude/IA actúe sobre Workspace, evalúa primero el MCP server oficial de Google antes de construir un wrapper propio.

### Novedades 2025-2026 relevantes

- **Ene 2025:** Gemini se integró sin costo adicional en los planes Business Standard, Business Plus, Enterprise Starter/Standard/Plus de Workspace (antes era add-on de pago).
- **1 nov 2025:** Licencia de Google Vault ahora es obligatoria para admins que quieran seguir usando Vault (eDiscovery/legal hold).
- **1 may 2026:** Nuevo modelo de cuotas "por unidad" (weighted quota units) para Gmail, Calendar y Drive APIs — primer paso de un modelo estandarizado que eventualmente incluirá cobros por overage con aviso de 90+ días.
- **2026 (Google Cloud Next '26):** Lanzamiento de **más de 50 servidores MCP gestionados por Google**, incluyendo los de Workspace (Gmail, Drive, Calendar, People, Chat) — permiten conectar Claude Desktop/Antigravity y otros clientes MCP directo a Workspace vía OAuth client ID/secret como "custom connector", sin necesidad de programar contra las APIs REST.
- El framework `developers.google.com/workspace/tools-safety` fue creado explícitamente para regular el acceso de "agent tools" (incluyendo MCP) a las APIs de Workspace — señal de que Google está tratando el acceso vía agentes IA como una categoría de uso diferenciada, con sus propias reglas de cuota.

### Recomendación de Jade para Jarvis

1. **Para automatización interna del equipo AGENCIA** (Gmail/Calendar/Drive de las cuentas del propio negocio, no de clientes externos): usar **Service Account + Domain-Wide Delegation** desde el backend en Vercel/Railway. Es el patrón correcto, sin fricción OAuth por agente, y evita reinventar en Apps Script lo que ya vive en el stack Node/Python del equipo.
2. **Antes de escribir wrappers propios de API para que un agente Claude actúe sobre Gmail/Calendar/Drive**, evaluar los **servidores MCP oficiales de Google** (`developers.google.com/workspace/guides/configure-mcp-servers`) — pueden ahorrar semanas de desarrollo de auth + wrapper si el caso de uso es "agente IA operando Workspace" en lugar de "producto propio con lógica de negocio".
3. **Monitorear el cambio de cuotas de mayo 2026** en cualquier proyecto GCP que se cree de ahora en adelante — los proyectos nuevos ya caen en el modelo por unidades (más generoso en volumen agregado pero distinto en cómo se cuenta). Si algún proyecto de AGENCIA fue creado antes de esa fecha, tiene ventana de gracia de al menos 60 días antes de migrar.
4. Reservar Apps Script solo para automatizaciones desechables de una sola Sheet/Doc con 1-2 usuarios; cualquier cosa que vaya a producción o se reutilice entre proyectos, construirla como API directa en el stack ya estandarizado (FastAPI/Node en Railway/Vercel).

### Fuentes consultadas

- [Enable Google Workspace APIs](https://developers.google.com/workspace/guides/enable-apis) — 2026-07-24
- [Developer products | Google Workspace](https://developers.google.com/workspace/products) — 2026-07-24
- [Usage limits | Gmail API](https://developers.google.com/workspace/gmail/api/reference/quota) — 2026-07-24
- [Usage limits | Google Sheets API](https://developers.google.com/workspace/sheets/api/limits) — 2026-07-24
- [Usage limits | Google Drive API](https://developers.google.com/workspace/drive/api/guides/limits) — 2026-07-24
- [Usage limits | Google Calendar API](https://developers.google.com/workspace/calendar/api/guides/quota) — 2026-07-24
- [Directory API: Limits and Quotas](https://developers.google.com/workspace/admin/directory/v1/limits) — 2026-07-24
- [Google Workspace standardized model for agent tools and APIs](https://developers.google.com/workspace/tools-safety) — 2026-07-24
- [Control API access with domain-wide delegation](https://support.google.com/a/answer/162106?hl=en) — 2026-07-24
- [Gmail API Service Account & Domain-Wide Delegation: The 2026 Guide — Unipile](https://www.unipile.com/gmail-api-service-account-domain-wide-delegation/) — 2026-07-24
- [googleapis — npm](https://www.npmjs.com/package/googleapis) — 2026-07-24
- [google-api-python-client — GitHub](https://github.com/googleapis/google-api-python-client) — 2026-07-24
- [Google Apps Script Quotas & Workarounds (2026) — FolderPal](https://folderpal.io/articles/google-apps-script-quotas-and-workarounds-2026-breaking-limits-on-drive-automation) — 2026-07-24
- [Quotas for Google Services | Apps Script](https://developers.google.com/apps-script/guides/services/quotas) — 2026-07-24
- [Gemini AI features now included in Google Workspace subscriptions](https://knowledge.workspace.google.com/admin/gemini/gemini-ai-features-now-included-in-google-workspace-subscriptions) — 2026-07-24
- [Google Vault release notes / licensing change](https://developers.google.com/workspace/vault/release-notes) — 2026-07-24
- [Configure the Google Workspace MCP servers](https://developers.google.com/workspace/guides/configure-mcp-servers) — 2026-07-24
- [Announcing official MCP support for Google services — Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/announcing-official-mcp-support-for-google-services) — 2026-07-24
- [Google-managed MCP servers are available for everyone — Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/google-managed-mcp-servers-are-available-for-everyone) — 2026-07-24
- [Introduction | People API](https://developers.google.com/people) — 2026-07-24
- [Google Meet REST API overview](https://developers.google.com/workspace/meet/api/guides/overview) — 2026-07-24
- [Work with artifacts | Google Meet](https://developers.google.com/workspace/meet/api/guides/artifacts) — 2026-07-24
- [Google Chat API reference](https://developers.google.com/workspace/chat/api/reference/rest) — 2026-07-24

---
*Jade — Directora Intel & Capacitaciones*
*Generado: 2026-07-24*
