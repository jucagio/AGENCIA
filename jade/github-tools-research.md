# Jade — Investigacion de Herramientas GitHub para Bot de Telegram

Fecha: 2026-03-23
Investigadora: Jade (Agente de Inteligencia y Capacitaciones)
Fuente: Investigacion web y GitHub — todo verificado en sesion

---

## 1. Repositorios de referencia encontrados

### roombawulf/claudegram
- URL: https://github.com/roombawulf/claudegram
- Stars: 1 (proyecto personal, codigo limpio y referenciable)
- Licencia: MIT
- Stack: Python 3.10+, python-telegram-bot (async), Anthropic SDK, SQLite, Systemd

**Que hace:**
Bot de Telegram que integra Claude con acceso completo a un VPS. Claude puede ejecutar comandos bash, editar archivos y navegar la web directamente desde Telegram. Incluye streaming en vivo de respuestas.

**Arquitectura:**
```
Telegram <-> python-telegram-bot (async) <-> TelegramHandler
                                                    |
                                            ClaudeClient (Anthropic SDK)
                                           /         |          \
                                    Caching     Streaming    Tool Loop
                                       |             |            |
                                   SQLite      edit_message    bash/editor
```

**Componentes del proyecto:**
- `main.py` — punto de entrada, registro de handlers
- `claude_client.py` — SDK con cache, streaming y tool loop
- `telegram_handler.py` — handlers de comandos y mensajes
- `tools.py` — sesion bash persistente y editor de texto
- `database.py` — esquema SQLite y operaciones async
- `conversation.py` — historial de mensajes y auto-summarizacion
- `streaming.py` — intervalos de edicion configurables

**Patrones de codigo relevantes:**
- `STREAM_EDIT_INTERVAL_MS: 1500` — edita el mensaje cada 1.5 segundos mientras Claude genera
- `STREAM_MIN_CHARS: 50` — solo edita si hay al menos 50 caracteres nuevos (evita spam a la API)
- Auto-summarizacion del historial a 120K tokens para mantener contexto largo sin perder memoria
- Enrutamiento de modelos: Haiku para tareas simples, Sonnet para complejas
- Cache de prompts que ahorra ~90% en tokens de entrada cached

**Recomendacion para nuestra implementacion:**
El patron de `STREAM_EDIT_INTERVAL_MS` + `STREAM_MIN_CHARS` es la solucion correcta para simular streaming con `edit_message_text` sin violar el flood control de Telegram. Copiar este patron directamente para Sasha.

---

### NachoSEO/claudegram
- URL: https://github.com/NachoSEO/claudegram
- Stars: 110
- Forks: 37
- Stack: TypeScript 5.x, Node.js 18+, Grammy bot framework, Anthropic Claude Agent SDK

**Que hace:**
Puente entre Telegram y un agente Claude Code corriendo localmente en la maquina. El agente tiene acceso a bash, archivos, web browsing, Reddit (OAuth2), Medium (Freedium), YouTube/TikTok/Instagram (yt-dlp), y voz (Groq Whisper + OpenAI TTS).

**Arquitectura modular:**
```
src/
  bot/      — handlers Telegram, routing de comandos, voz, fotos, auth middleware
  claude/   — ciclo de vida del agente, persistencia de sesion, queue de requests, MCP tools
  telegram/ — streaming de mensajes, chunking, MarkdownV2, Telegraph Instant View
  integrations/
    reddit/   — cliente OAuth2 TypeScript
    medium/   — via Freedium mirror
    media/    — yt-dlp wrapper
```

**Patrones relevantes:**
- `STREAMING_MODE` toggle — permite cambiar entre streaming en vivo o esperar respuesta completa
- `DANGEROUS_MODE` — auto-aprueba todos los permisos de herramientas (util para uso personal)
- Sessions por topic de foro — cada topic de Telegram es una sesion independiente
- `/resume` y `/continue` — permite retomar sesiones anteriores sin perder contexto
- Control de chunking que preserva bloques de codigo al partir mensajes largos
- Telegraph Instant View para respuestas muy largas (no rompe el limite de 4096 chars)
- TTS de respuestas: convierte texto de Claude en notas de voz via OpenAI gpt-4o-mini-tts

**Recomendacion para nuestra implementacion:**
El modelo de sesiones por topic de foro de Telegram es perfecto para un bot multi-agente: cada agente de la Agencia (Jade, Sasha, Brook, etc.) puede tener su propio topic dentro de un grupo. El pattern de queue de requests evita condiciones de carrera cuando el usuario envia multiples mensajes rapido.

---

### mtzanidakis/praktor
- URL: https://github.com/mtzanidakis/praktor
- Stars: 19
- Stack: Go (61.3%), TypeScript (37.1%), Docker Compose
- Ultima release: v0.7.1 (Marzo 2026)
- Licencia: MIT

**Que hace:**
Orquestador multi-agente de Claude Code con I/O via Telegram, aislamiento Docker por agente, patrones swarm y UI de Mission Control en tiempo real. Es el proyecto mas sofisticado del ecosistema para multi-agentes reales.

**Arquitectura:**
```
Telegram -> praktor gateway (Go) -> Enrutador de 3 niveles
                                           |
                    +----------------------+---------------------+
                    |                      |                     |
            Agente Default          @coder Container    @researcher Container
            (clasificacion IA)      (Docker aislado)    (Docker aislado)
                    |                      |                     |
              SQLite memory          filesystem            filesystem
              (FTS5 + vector)      propio                  propio
```

**Sistema de enrutamiento de 3 niveles:**
1. Prefijo explicito `@nombre_agente` — enruta directamente
2. Clasificacion via IA — el agente default lee el mensaje y decide quien lo maneja
3. Fallback al agente default si la clasificacion falla

**Caracteristicas de orquestacion:**
- Cada agente tiene su propio `AGENT.md` (personalidad) y `USER.md` (perfil del usuario)
- Swarm patterns: fan-out (un mensaje a todos), pipeline (A->B->C), collaborative (varios coordinan)
- Memoria hibrida por agente: FTS5 (busqueda por palabras clave) + vector semantico (all-MiniLM-L6-v2)
- Hot reload de configuracion sin restart (`praktor.yaml`)
- MCP servers por agente — cada agente puede tener sus propias herramientas
- Tareas programadas: cron, interval, one-shot (hasta 3 concurrentes)
- Vault cifrado AES-256-GCM para secretos por agente
- Backup/restore via tarballs zstd-compressed

**Estructura del repo:**
```
cmd/           — CLI
internal/      — logica del gateway
agent-runner/  — runtime del contenedor de agentes
ui/            — dashboard React (Mission Control)
config/        — ejemplos de configuracion
docs/          — diagramas de arquitectura
scripts/       — utilidades de deployment
```

**Recomendacion para nuestra implementacion:**
Praktor es la referencia de arquitectura para escalar la Agencia a multi-agentes reales en Telegram. El patron de `AGENT.md` por agente es identico al `CLAUDE.md` que ya usamos. Si queremos llevar la Agencia a Telegram con enrutamiento real entre Jade, Sasha, Brook, etc., praktor es el blueprint. No hace falta reinventar la rueda — estudiar su `praktor.yaml` de configuracion.

---

### jsayubi/ccgram
- URL: https://github.com/jsayubi/ccgram
- Stars: 2
- Stack: TypeScript, Node.js 18+, tmux/PTY
- Tests: 84 (vitest)

**Que hace:**
Bot que actua como puente para aprobar permisos de Claude Code desde el telefono. Cuando Claude necesita permiso para ejecutar algo, envia botones inline a Telegram (Allow/Deny/Always). El usuario responde desde el movil y Claude continua.

**Patron de aprobacion de permisos (muy relevante):**
```
Claude solicita permiso -> hook genera promptId, escribe archivo pending
          |
          v
Telegram envia botones inline (Allow / Deny / Always Allow)
          |
          v
Usuario toca respuesta -> bot escribe archivo result
          |
          v
Hook lee resultado -> retorna decision a Claude -> Claude continua
```

**IPC via filesystem (`/tmp/claude-prompts/`):**
- Evita complejidad de sockets o bases de datos para estado temporal
- Los hooks son scripts simples que leen/escriben archivos
- Supresion inteligente: si el usuario mensajeo en los ultimos 5 minutos, no notifica (configurable via `ACTIVE_THRESHOLD_SECONDS`)

**Recomendacion para nuestra implementacion:**
El patron de IPC via archivos `/tmp/` es simple y robusto para notificaciones de permisos. Si Sasha necesita aprobar operaciones destructivas desde Telegram, este es el pattern mas limpio sin dependencias extra.

---

### RichardAtCT/claude-code-telegram
- URL: https://github.com/RichardAtCT/claude-code-telegram
- Stars: 2,200 (el mas popular del ecosistema)
- Stack: Python 3.11+, python-telegram-bot, FastAPI (webhooks opcionales), SQLite, systemd

**Que hace:**
El bot de Claude Code para Telegram mas maduro y completo. Dos modos: Agentic (conversacion natural con visualizacion de herramientas en tiempo real) y Classic (interfaz tipo terminal con 13 comandos).

**Caracteristicas de produccion:**
- Rate limiting con algoritmo token bucket
- Limites de gasto por usuario
- Autenticacion HMAC-SHA256 para webhooks de GitHub
- Modo Project Threads: cada topic de Telegram es un proyecto independiente
- 16 herramientas configurables con allowlist/denylist
- 3 niveles de verbosidad (0=silencioso, 1=normal, 2=detallado)
- Sandboxing por directorio, prevencion de path traversal, audit logging
- Transcripcion de voz: Mistral Voxtral / OpenAI Whisper

**Recomendacion para nuestra implementacion:**
Es la referencia de produccion para un bot personal serio. El algoritmo de token bucket para rate limiting es superior al simple sleep/retry. Sasha debe estudiar su implementacion de seguridad (directorio sandboxing + audit logging) antes de implementar cualquier acceso a filesystem.

---

### htdt/teleforge
- URL: https://github.com/htdt/teleforge
- Stars: 12
- Stack: JavaScript (Node.js), Grammy, MCP server via TCP

**Que hace:**
Bot minimalista para ejecutar tareas one-shot de Claude Code en VMs headless. Diseno pensado para "mandar una tarea y olvidarse" — el agente ejecuta solo sin interaccion.

**Arquitectura IPC interesante:**
```
bot.mjs (Grammy + TCP server)
    |-- recibe tarea de Telegram
    |-- spawna claude CLI como subprocess
    |-- MCP server via TCP local
    |       |-- send_message (Claude -> Telegram)
    |       |-- ask_user (pausa para input)
    |       |-- send_image (enviar imagenes)
    |-- streaming de resultados de vuelta
```

**Patron clave:** `--dangerously-skip-permissions` para ejecucion autonoma sin prompts interactivos. Util para bots de CI/CD y automatizacion desatendida.

**Recomendacion para nuestra implementacion:**
El patron de TCP local entre el bot y el MCP server es elegante para desacoplar responsabilidades sin overhead de red. Cinthya puede usar este patron para automatizaciones desatendidas donde no se necesita aprobacion humana.

---

### Plugin Oficial de Anthropic para Telegram (Claude Code Channels)
- URL: https://github.com/anthropics/claude-plugins-official/blob/main/external_plugins/telegram/README.md
- Estado: Research Preview (lanzado 20 Marzo 2026)
- Requisitos: Claude Code v2.1.80+, sesion claude.ai activa (no API key), Bun runtime
- Stack: TypeScript, Bun, MCP Server

**Que hace:**
El canal oficial de Anthropic que conecta Telegram directamente a Claude Code. El MCP server hace polling al Bot API (sin webhook publico, sin puerto abierto). Expone 3 herramientas a Claude:

**Los 3 tools del plugin oficial:**

| Tool | Parametros | Notas |
|------|-----------|-------|
| `reply` | chat_id, text, reply_to?, files? | Auto-chunking, soporta imagenes y docs hasta 50MB |
| `react` | message_id, emoji | Solo emojis de la whitelist de Telegram |
| `edit_message` | message_id, text | Solo mensajes enviados por el bot |

**Flujo de autenticacion (primera vez):**
1. DM al bot -> bot responde con codigo de 6 caracteres
2. En Claude Code: `/telegram:access pair <codigo>`
3. Cambiar politica a `allowlist` despues del pareo

**Limitaciones importantes del plugin oficial:**
- Sin historial de mensajes — no hay `fetch_messages` tool
- Sin busqueda de mensajes anteriores
- Las fotos se descargan eager al llegar (porque Telegram no permite recuperarlas despues)
- Requiere sesion de claude.ai (no compatible con solo API key)

**Estado de los archivos:**
```
~/.claude/channels/telegram/
    .env                  — TELEGRAM_BOT_TOKEN
    access.json           — politica de acceso, allowlist
    inbox/                — fotos descargadas al llegar
```

**Recomendacion para nuestra implementacion:**
Para uso inmediato y simple, el plugin oficial es suficiente. Pero para la Agencia (multi-agente, control de estado, sesiones persistentes) necesitamos la implementacion custom. Usar el plugin oficial como referencia del protocolo de autenticacion y manejo de fotos.

---

## 2. Patrones de multi-agent orchestration en Telegram

### El patron de Praktor (el mas maduro)

El sistema de 3 niveles de enrutamiento de praktor es la referencia para orquestar multiples agentes:

```
Mensaje del usuario en Telegram
          |
          v
Clasificacion automatica
          |
    +-----+-----+-----+-----+
    |     |     |     |     |
  @jade @sasha @brook @ego @default
    |     |     |     |     |
  Claude Claude Claude Claude Claude
  (su   (su   (su   (su   (su
  CLAUDE.md) CLAUDE.md) ...)
```

**Patrones de swarm disponibles:**

- **Fan-out**: un mensaje se manda a todos los agentes simultaneamente (ej: briefing semanal)
- **Pipeline**: A procesa -> pasa a B -> B procesa -> pasa a C (ej: Sasha -> Brook -> Erik)
- **Collaborative**: varios agentes coordinan en paralelo sobre el mismo problema

### El patron de NachoSEO (topics como sesiones)

Usar los Topics de Telegram (grupos con topics activados) para separar contexto por agente:
- Topic "Jade" -> sesion de Jade
- Topic "Sasha" -> sesion de Sasha
- Topic "General" -> conversacion libre, enrutamiento automatico

### El patron de OpenClaw (bot de referencia 2026)

OpenClaw (210,000+ stars en GitHub) usa Telegram como interfaz principal para equipos multi-agente. Su arquitectura clave:
- Cada agente tiene su propio bot token (cuota separada de Telegram)
- Comunicacion bot-a-bot via shared context files
- Escalation chains: si un agente no puede resolver, escala al siguiente

**Recomendacion para la Agencia:**
Implementar el enrutamiento via `@nombre_agente` como en Praktor. Es el patron mas natural para Telegram y el mas escalable. Cada agente mantiene su `CLAUDE.md` como ya lo tenemos — solo hay que agregar el router delante.

---

## 3. Streaming con Telegram Bot API — Mejores practicas

### El metodo correcto segun la version de Bot API

#### Bot API 9.5+ (disponible desde 1 Marzo 2026) — RECOMENDADO
Telegram introdujo `sendMessageDraft` en Bot API 9.3 (31 Dic 2025) y lo abrio a todos los bots en la version 9.5 (1 Mar 2026).

**Como funciona `sendMessageDraft`:**
```python
# 1. Enviar el primer draft con un draft_id unico
await bot.send_message_draft(
    chat_id=chat_id,
    draft_id="unique-draft-id",
    text="Generando respuesta..."
)

# 2. Actualizar el draft con texto incremental
async for chunk in claude_stream:
    accumulated_text += chunk
    await bot.send_message_draft(
        chat_id=chat_id,
        draft_id="unique-draft-id",
        text=accumulated_text
    )

# 3. Finalizar con sendMessage o editMessageText
await bot.send_message(chat_id=chat_id, text=accumulated_text)
```

**Ventajas sobre edit_message_text:**
- Animacion nativa en el cliente (como ChatGPT) — sin flickering
- No cuenta contra el limite de 20 ediciones/minuto
- No genera eventos 429 Too Many Requests
- Renderizado nativo de Telegram en tiempo real

**Nota importante:** python-telegram-bot v22 puede no tener soporte nativo aun. Verificar si esta en la version instalada o usar `bot.send` directo a la Bot API con requests.

#### Metodo clasico (edit_message_text) — para compatibilidad

Si `sendMessageDraft` no esta disponible en la libreria, el patron probado es:

```python
# Patron de roombawulf/claudegram
STREAM_EDIT_INTERVAL_MS = 1500  # editar cada 1.5 segundos
STREAM_MIN_CHARS = 50           # solo editar si hay 50+ chars nuevos

accumulated = ""
last_edit_len = 0
last_edit_time = time.time()

async for chunk in claude_stream:
    accumulated += chunk
    now = time.time()
    chars_since_last = len(accumulated) - last_edit_len
    time_since_last = now - last_edit_time

    if chars_since_last >= STREAM_MIN_CHARS and time_since_last >= 1.5:
        await message.edit_text(accumulated)
        last_edit_len = len(accumulated)
        last_edit_time = now

# Edicion final siempre
await message.edit_text(accumulated)
```

**Por que estos valores:**
- 1.5 segundos entre ediciones = maximo ~40 ediciones por minuto por chat
- El limite real de Telegram es ~20 ediciones/minuto por grupo, pero en chats privados es mas permisivo
- 50 chars minimos evita ediciones triviales que no agregan valor visual

---

## 4. Gestion de sesiones — Comparativa

| Opcion | Pros | Contras | Cuando usarla |
|--------|------|---------|---------------|
| **Dict en memoria** | Cero dependencias, instantaneo, codigo simple | Se pierde al reiniciar, no escala a multiples instancias | Prototipado rapido, bots sin estado critico |
| **PicklePersistence (PTB)** | Integrado en python-telegram-bot, cero infra extra, persiste en disco | Archivo binario (no legible), no apto para multiples instancias, lento para historiales grandes | Bot personal simple que solo corre en un proceso |
| **SQLite** | Sin servidor, archivo unico, queries SQL completas, async con aiosqlite | No escala horizontalmente, riesgo de lock en concurrencia alta | Proyectos personales serios — es lo que usa claudegram y claude-code-telegram |
| **Redis** | Sub-milisegundo, escala horizontal, TTL nativo, persistencia opcional | Infra adicional, costo en produccion | Bots con alta concurrencia, multiples instancias, sesiones con expiracion |
| **Supabase (PostgreSQL)** | Managed, backups automaticos, row-level security, realtime subscriptions | Latencia de red (~10-50ms vs microsegundos de Redis), costo por uso | Cuando ya se usa Supabase en el proyecto, necesitas historial de conversaciones auditable o integracion con otros servicios |

**Recomendacion para la Agencia (bot personal):**

Para un bot personal de la Agencia con 1-5 usuarios:
```
SQLite (via aiosqlite) = el punto optimo
```
- Cero infra adicional
- Async nativo
- Historial de conversaciones completo
- Schemas migrables
- Es lo que usan los mejores bots del ecosistema (claudegram, claude-code-telegram)

Si en el futuro se necesita persistir contexto de conversaciones en el mismo Supabase que ya usa la Agencia para otros proyectos, la migracion es trivial — mismos schemas, solo cambiar el driver.

**Patron hibrido recomendado para escalar:**
```
Redis (sesion activa, TTL 24h)
    +
SQLite / Supabase (historial permanente, memoria a largo plazo)
```

---

## 5. Telegram Flood Control — Lo que debes saber

### Limites oficiales (parcialmente documentados)

Telegram no documenta todos sus limites publicamente. Los confirmados son:

| Limite | Valor | Aplica a |
|--------|-------|----------|
| Mensajes por segundo (global por bot) | ~30 msg/s | Todos los metodos que generan updates |
| Mensajes por minuto a un mismo grupo | ~20 msg/min | sendMessage a grupos |
| Ediciones por minuto a un mismo grupo | ~20 ediciones/min | editMessage en grupos |
| Notificaciones en masa | ~30 msg/s total | Broadcasting a multiples usuarios |
| Broadcast recomendado | Distribuir en 8-12 horas | Para notificaciones masivas |

**Desde Bot API 8.0 (Noviembre 2025):**
- Headers en cada respuesta indicando el estado del rate limit
- Campo `adaptive_retry` dentro de respuestas 429 con sugerencia de espera
- Bots que respetan `adaptive_retry + jitter` evitan blacklist 99.7% del tiempo

### El error 429 — RetryAfter

```python
from telegram.error import RetryAfter
import asyncio

async def safe_edit(message, text):
    while True:
        try:
            await message.edit_text(text)
            break
        except RetryAfter as e:
            # e.retry_after = segundos que debes esperar
            await asyncio.sleep(e.retry_after + 1)  # +1 por jitter
        except Exception:
            break  # otros errores no son recuperables con retry
```

### AIORateLimiter (incluido en python-telegram-bot v20+)

```python
from telegram.ext import ApplicationBuilder
from telegram.ext import AIORateLimiter

application = (
    ApplicationBuilder()
    .token(TOKEN)
    .rate_limiter(AIORateLimiter())
    .build()
)
```

### Estrategia para streaming con edit_message_text

El patron correcto para NO violar flood control al hacer streaming:

1. **Intervalo minimo entre ediciones: 1.5 segundos** (patron de claudegram)
2. **Solo editar si hay contenido nuevo significativo** (minimo 50 chars)
3. **Una edicion final garantizada** al terminar la generacion
4. **Capturar RetryAfter y esperar exactamente lo que dice Telegram**
5. **Con Bot API 9.5+ usar `sendMessageDraft`** — elimina este problema por completo

### Para chats privados vs grupos

- **Chats privados**: limites mucho mas permisivos — el 1 mensaje/segundo por chat aplica principalmente a grupos
- **Grupos**: limite de 20 ediciones/minuto es el mas restrictivo para streaming
- **Para la Agencia (uso personal)**: chats privados -> se puede editar con mayor frecuencia sin problemas

---

## 6. Herramientas adicionales encontradas

### python-telegram-bot v22.7 (actual)
- URL: https://python-telegram-bot.org
- Stars: 25,000+
- Es la libreria Python estandar para bots de Telegram

**Features clave para la Agencia:**
- `ConversationHandler` para flujos multi-paso (onboarding, flujos guiados)
- `PicklePersistence` / `BasePersistence` para sesiones sin infra extra
- `AIORateLimiter` para manejo automatico de flood
- `ApplicationBuilder` con rate_limiter integrado
- `JobQueue` para tareas programadas (cron jobs desde el bot)
- Soporte completo async/await (asyncio)

**Advertencia importante:** `ConversationHandler` requiere `concurrent_updates=False` — procesa updates uno por uno. Esto es una limitacion para bots de alta concurrencia pero aceptable para un bot personal.

### Grammy (Node.js/TypeScript)
- URL: https://grammy.dev
- Alternativa TypeScript a python-telegram-bot
- Plugin `auto-retry` nativo para flood control
- Usado por NachoSEO/claudegram y htdt/teleforge
- `autoRetry()` maneja 429s automaticamente sin codigo adicional

### OpenClaw (referencia de ecosistema 2026)
- URL: https://openclaw.com (210,000+ stars)
- El proyecto de bots de IA mas grande en GitHub en 2026
- Primero en implementar `sendMessageDraft` (Bot API 9.5)
- Su arquitectura con Telegram supergroups es la referencia para equipos multi-agente

### Anthropic Claude Code Channels
- Lanzado: 20 Marzo 2026 (hace 3 dias)
- URL: https://github.com/anthropics/claude-plugins-official
- La solucion oficial de Anthropic para conectar Claude Code con Telegram y Discord
- Research preview — no production-ready aun
- No requiere API key (usa sesion claude.ai)

### PraisonAI
- URL: https://github.com/MervinPraison/PraisonAI
- Multi-agente low-code que entrega a Telegram, Discord y WhatsApp
- Alternativa de alto nivel si no se quiere construir el routing desde cero

### AgentConnect
- URL: https://akki0511.github.io/AgentConnect
- Framework Python para bots Telegram con capacidades multi-agente
- Documentacion con ejemplo de Telegram dedicado

### aiosqlite
- URL: https://github.com/omnilib/aiosqlite
- Wrapper async de SQLite para Python
- Usado por claudegram y claude-code-telegram
- Cero overhead, perfecto para bots personales

---

## 7. Recomendaciones finales para el equipo

### Para Sasha (codigo base y arquitectura):

**Stack recomendado para el bot de la Agencia:**
```
python-telegram-bot v22.7 (async)
    + Anthropic SDK (streaming nativo)
    + aiosqlite (sesiones y historial)
    + AIORateLimiter (flood control automatico)
```

**Patrones de implementacion prioritarios:**

1. **Streaming**: implementar el patron de `roombawulf/claudegram`:
   - `STREAM_EDIT_INTERVAL_MS = 1500`
   - `STREAM_MIN_CHARS = 50`
   - Si Bot API 9.5 esta disponible en PTB v22.7, migrar a `sendMessageDraft`

2. **Sesiones**: SQLite con aiosqlite
   - Una tabla `conversations` con `(chat_id, message_id, role, content, timestamp)`
   - Una tabla `sessions` con `(chat_id, agent_name, context_summary, last_active)`
   - Auto-summarizacion cuando el historial supere 100K tokens (patron de claudegram)

3. **Seguridad**:
   - `ALLOWED_USER_IDS` en `.env` — whitelist de Telegram IDs numericos
   - Path traversal prevention si Claude accede al filesystem
   - Audit log de todas las operaciones de herramientas

4. **Enrutamiento multi-agente**:
   - Prefijo `@nombre_agente` en el mensaje enruta al agente correcto
   - Cada agente carga su `CLAUDE.md` como system prompt
   - Fallback a Jarvis si no hay prefijo explicito

5. **Manejo de errores de Telegram:**
```python
from telegram.error import RetryAfter, TimedOut, NetworkError

async def safe_send(func, *args, max_retries=3, **kwargs):
    for attempt in range(max_retries):
        try:
            return await func(*args, **kwargs)
        except RetryAfter as e:
            await asyncio.sleep(e.retry_after + 1)
        except (TimedOut, NetworkError):
            await asyncio.sleep(2 ** attempt)  # backoff exponencial
    raise Exception("Max retries exceeded")
```

**Referencia principal a estudiar:** `RichardAtCT/claude-code-telegram` (2,200 stars) — el bot de produccion mas completo del ecosistema. Especialmente su implementacion de token bucket para rate limiting y directorio sandboxing.

---

### Para Brook (handlers y UI de Telegram):

**Diseño de handlers recomendado:**

```python
# Un handler por agente — patron limpio y extensible
application.add_handler(MessageHandler(
    filters.TEXT & filters.Regex(r'^@jade\s'),
    jade_handler
))
application.add_handler(MessageHandler(
    filters.TEXT & filters.Regex(r'^@sasha\s'),
    sasha_handler
))
# Handler default (sin prefijo) -> Jarvis
application.add_handler(MessageHandler(
    filters.TEXT & ~filters.COMMAND,
    jarvis_handler
))
```

**UX de Telegram para respuestas largas:**
- Usar `parse_mode=ParseMode.MARKDOWN_V2` para formateo
- Chunking automatico: partir en bloques de 4000 chars (limite de Telegram: 4096)
- Preservar bloques de codigo al chunkar — no partir en medio de ```
- Para respuestas muy largas: Telegraph Instant View (patron de NachoSEO)
- Typing indicator: `await context.bot.send_chat_action(chat_id, ChatAction.TYPING)`

**Comandos minimos para el bot de la Agencia:**
```
/start     — saludo y menu de agentes disponibles
/help      — lista de comandos
/status    — estado de sesion actual
/clear     — limpiar historial de la sesion
/resume    — retomar sesion anterior
/agents    — listar agentes disponibles y sus capacidades
```

---

### Para Cinthya (automatizacion futura):

**Oportunidades de automatizacion detectadas:**

1. **Skills Intelligence Report automatico (sabados 10 AM):**
   - Jade investiga las 5 fuentes del equipo cada semana
   - Cinthya programa el job con `JobQueue` de python-telegram-bot:
   ```python
   application.job_queue.run_repeating(
       jade_weekly_report,
       interval=timedelta(weeks=1),
       first=datetime(2026, 3, 28, 10, 0, 0)  # proximo sabado
   )
   ```

2. **Alertas de CVEs para Sasha:**
   - Cinthya monitorea NVD (nvd.nist.gov) por nuevas CVEs criticas
   - Si detecta una relevante para el stack (FastAPI, Python, Supabase), notifica a Sasha via Telegram
   - Patron de ccgram: notificacion inteligente (no notifica si Sasha estuvo activa en los ultimos 5 min)

3. **Notificaciones de progreso de proyectos:**
   - Webhooks de GitHub -> Cinthya recibe el evento -> Cinthya notifica a Jarvis en Telegram
   - Patron de `RichardAtCT/claude-code-telegram`: HMAC-SHA256 para verificar webhooks de GitHub

4. **Automatizacion del onboarding de nuevos agentes:**
   - Cuando se crea un nuevo `CLAUDE.md`, Cinthya notifica al equipo en Telegram
   - Jade recibe el nuevo CLAUDE.md y prepara el briefing de capacitacion

5. **Patron IPC de ccgram para aprobaciones:**
   - Si algun agente necesita aprobacion de Juan Camilo para una accion critica
   - Bot envia mensaje con botones inline (Aprobar / Rechazar / Ver mas)
   - Juan Camilo aprueba desde el telefono, el agente continua

**Herramienta recomendada para automatizaciones complejas:**
n8n con el nodo de Telegram Bot (no code) para flujos que no requieren Python. Para flujos que necesitan acceder a Claude, usar el SDK de Anthropic directo en Python.

---

## Fuentes consultadas

- [roombawulf/claudegram](https://github.com/roombawulf/claudegram)
- [NachoSEO/claudegram](https://github.com/NachoSEO/claudegram)
- [mtzanidakis/praktor](https://github.com/mtzanidakis/praktor)
- [jsayubi/ccgram](https://github.com/jsayubi/ccgram)
- [RichardAtCT/claude-code-telegram](https://github.com/RichardAtCT/claude-code-telegram)
- [htdt/teleforge](https://github.com/htdt/teleforge)
- [Anthropic claude-plugins-official / Telegram](https://github.com/anthropics/claude-plugins-official/blob/main/external_plugins/telegram/README.md)
- [python-telegram-bot — Avoiding flood limits (wiki)](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Avoiding-flood-limits)
- [grammY — Flood Limits](https://grammy.dev/advanced/flood)
- [Telegram Bot API — sendMessageDraft (Bot API 9.5)](https://core.telegram.org/bots/api)
- [Dev.to — Claude Code Channels: Two-way bridge Telegram-Terminal](https://dev.to/ji_ai/claude-code-channels-how-anthropic-built-a-two-way-bridge-between-telegram-and-your-terminal-2dpn)
- [DEV Community — State management Redis vs StatefulSets vs External DBs](https://dev.to/inboryn_99399f96579fcd705/state-management-patterns-for-long-running-ai-agents-redis-vs-statefulsets-vs-external-databases-39c5)
- [AI Base News — Telegram Bot API 9.5 streaming](https://www.aibase.com/news/25881)
- [openclaw/openclaw — sendMessageDraft issues](https://github.com/openclaw/openclaw/issues/32180)
- [python-telegram-bot docs v22.7](https://docs.python-telegram-bot.org/en/stable/)

---

_Documento generado por Jade — Agente de Inteligencia y Capacitaciones_
_Revision recomendada: mensual (el ecosistema de bots de Telegram + Claude evoluciona rapido)_
