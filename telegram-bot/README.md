# Agencia Bot — Bot de Telegram para el Equipo de Agentes Claude

Bot de Telegram que conecta directamente con el equipo de agentes de la Agencia. Escribe `@jarvis`, `@sasha` o cualquier otro agente desde Telegram y obtienes respuesta en tiempo real con streaming, historial de conversación por agente y control de acceso para que solo tú puedas usarlo.

---

## ¿Qué hace?

- Despacha mensajes al agente correcto según el `@mention` que escribas en el chat.
- Muestra la respuesta en tiempo real mientras Claude escribe (streaming progresivo).
- Mantiene historial de conversación separado por agente, con ventana deslizante configurable.

---

## Agentes disponibles

| @mention   | Agente  | Modelo              | Rol                              |
|------------|---------|---------------------|----------------------------------|
| `@jarvis`  | Jarvis  | claude-opus-4-5     | Gerente de Programación          |
| `@jade`    | Jade    | claude-sonnet-4-5   | Inteligencia & Capacitaciones    |
| `@sasha`   | Sasha   | claude-opus-4-5     | Programadora Senior & Seguridad  |
| `@brook`   | Brook   | claude-sonnet-4-5   | Frontend, BD & Dashboards        |
| `@erik`    | Erik    | claude-sonnet-4-5   | Diseño & IA para Diseño          |
| `@cinthya` | Cinthya | claude-sonnet-4-5   | Automatización de Procesos       |
| `@ego`     | Ego     | claude-opus-4-5     | Auditor Supremo                  |

---

## Cómo usarlo

Escribe en el chat de Telegram con el bot:

```
@jarvis Planifica los sprints del próximo mes para el equipo.

@jade Dame un briefing de las últimas tendencias en agentes de IA.

@sasha Implementa el sistema de autenticación con JWT. Ultrathink

@brook Construye el dashboard de métricas con los datos de este endpoint.

@ego Audita el avance del proyecto Teclado de Señas. Ultrathink
```

El sufijo `Ultrathink` activa análisis más profundo en el modelo.

---

## Comandos

| Comando           | Qué hace                                              |
|-------------------|-------------------------------------------------------|
| `/start`          | Muestra el mensaje de bienvenida con la lista de agentes |
| `/help`           | Igual que `/start`                                    |
| `/agents`         | Lista todos los agentes disponibles                   |
| `/reset`          | Borra el historial de conversación de todos los agentes |
| `/reset @jarvis`  | Borra solo el historial del agente indicado           |

---

## Setup rápido

**Paso 1 — Clonar el repositorio**

```bash
git clone <url-del-repo>
cd agencia/telegram-bot
```

**Paso 2 — Crear el archivo de variables de entorno**

```bash
cp .env.example .env
```

Abre `.env` y completa los valores (ver sección "Variables de entorno" abajo).

**Paso 3 — Instalar dependencias (desarrollo local)**

```bash
pip install -e ".[dev]"
```

**Paso 4 — Ejecutar el bot localmente**

```bash
python -m src.main
```

**Paso 5 — O ejecutar con Docker**

```bash
docker compose up --build
```

---

## Variables de entorno

| Variable                   | Descripción                                                       | Ejemplo                        |
|----------------------------|-------------------------------------------------------------------|--------------------------------|
| `TELEGRAM_TOKEN`           | Token del bot obtenido de @BotFather en Telegram                  | `7123456789:AAFx...`           |
| `ANTHROPIC_API_KEY`        | Clave de API de Anthropic (console.anthropic.com)                 | `sk-ant-api03-...`             |
| `ALLOWED_USER_IDS`         | Lista de Telegram user IDs autorizados, separados por coma        | `123456789,987654321`          |
| `MAX_HISTORY_MESSAGES`     | Cantidad máxima de mensajes en el historial por agente            | `20`                           |
| `RATE_LIMIT_MESSAGES`      | Mensajes máximos permitidos por usuario en la ventana de tiempo   | `10`                           |
| `RATE_LIMIT_WINDOW_SECONDS`| Ventana de tiempo en segundos para el rate limiting               | `60`                           |
| `LOG_LEVEL`                | Nivel de logging (`DEBUG`, `INFO`, `WARNING`, `ERROR`)            | `INFO`                         |
| `ENVIRONMENT`              | Entorno de ejecución                                              | `development` o `production`   |

---

## Deploy en Railway

**Paso 1 — Crear proyecto en Railway**

Ingresa a [railway.app](https://railway.app), crea un nuevo proyecto y conecta tu repositorio de GitHub.

**Paso 2 — Configurar variables de entorno**

En el panel de Railway, ve a tu servicio → "Variables" y agrega todas las variables del archivo `.env`.

```
TELEGRAM_TOKEN=tu_token
ANTHROPIC_API_KEY=sk-ant-...
ALLOWED_USER_IDS=123456789
ENVIRONMENT=production
```

**Paso 3 — Configurar el comando de inicio**

Railway detecta el `Dockerfile` automáticamente. Si prefieres sin Docker, configura el start command como:

```bash
python -m src.main
```

**Paso 4 — Deploy**

```bash
git push origin main
```

Railway despliega automáticamente en cada push. Monitorea los logs desde el panel para confirmar que el bot arrancó correctamente (verás `starting_bot` y `bot_polling` en los logs).

---

## Cómo obtener tu Telegram user ID

Necesitas tu user ID numérico para configurar `ALLOWED_USER_IDS`. Sigue estos pasos:

1. Abre Telegram y busca el bot `@userinfobot`.
2. Inicia una conversación y escribe `/start`.
3. El bot responde con tu información, incluyendo tu **Id** numérico. Por ejemplo: `Id: 123456789`.
4. Copia ese número y ponlo en la variable `ALLOWED_USER_IDS` del archivo `.env`.

Si quieres agregar más de un usuario, separa los IDs con coma: `123456789,987654321`.

---

## Arquitectura

El flujo completo de un mensaje desde Telegram hasta la respuesta:

```
Usuario escribe en Telegram
         |
         v
   python-telegram-bot (polling)
         |
         v
   MessageHandler.handle_message()
         |
    +----+----+
    |         |
  Es /cmd?  Es @mention?
    |         |
    v         v
 _handle_   parse_message()
 _command()      |
              get_agent()   ← registry.py
                 |
         stream_agent_response()   ← claude_service.py
                 |
         ┌───────┴────────┐
         |                |
   session_service    Anthropic API
   (historial)        (streaming)
         |                |
         └───────┬────────┘
                 |
         placeholder.edit_text()
         (actualiza el mensaje cada 100 chars)
                 |
                 v
   Respuesta final en Telegram
```

**Componentes clave:**

- `mention_parser.py` — detecta `@agente` y separa el contenido del mensaje.
- `registry.py` — mapea nombres de agentes a modelo Claude y system prompt.
- `session_service.py` — mantiene historial de conversación por `(user_id, agent_name)` con ventana deslizante.
- `rate_limiter.py` — sliding window para evitar abuso (10 mensajes / 60 segundos por defecto).
- `claude_service.py` — llama a la API de Anthropic con streaming y edita el placeholder de Telegram en tiempo real.
