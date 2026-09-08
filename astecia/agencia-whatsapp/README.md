# Agencia WhatsApp Gateway

**Agencia WhatsApp Gateway** — conecta a Juan Camilo con su equipo de agentes IA (Jarvis, Jade, Sasha, etc.) directamente desde WhatsApp.

## Agentes disponibles

| Comando | Agente | Especialidad |
|---------|--------|-------------|
| `@jarvis` | Jarvis | Gerente de Programación (por defecto) |
| `@jade` | Jade | Inteligencia, tendencias y capacitaciones |
| `@ego` | Ego | Auditor supremo |
| `@sasha` | Sasha | Programación y seguridad |
| `@brook` | Brook | Frontend y dashboards |
| `@erik` | Erik | Diseño e IA visual |
| `@cinthya` | Cinthya | Automatización de procesos |

## Uso desde WhatsApp

```
@sasha implementa el login con JWT para el proyecto teclado de señas
@jade dame un briefing de tendencias en apps de accesibilidad
@ego audita el avance del proyecto
@cinthya automatiza el reporte semanal para Juan Camilo
```

Sin `@mención` → Jarvis responde por defecto.

## Setup rápido

### 1. Clonar e instalar
```bash
pip install -r requirements.txt
cp .env.example .env
# Editar .env con tus credenciales
```

### 2. Configurar Twilio
1. Crear cuenta en [twilio.com](https://twilio.com)
2. Ir a **Messaging → Try it out → Send a WhatsApp message**
3. Activar el sandbox: enviar el código de unión desde tu WhatsApp
4. Copiar `Account SID` y `Auth Token` al `.env`

### 3. Exponer el servidor localmente (desarrollo)
```bash
# Terminal 1: iniciar servidor
uvicorn main:app --reload --port 8000

# Terminal 2: exponer con ngrok
ngrok http 8000
```
Copiar la URL de ngrok (ej: `https://abc123.ngrok.io`) y pegarla en Twilio:
**Sandbox → When a message comes in → `https://abc123.ngrok.io/webhook`**

### 4. Deploy en Railway (producción)
```bash
# Instalar Railway CLI
npm install -g @railway/cli
railway login
railway init
railway up
```
Copiar la URL de Railway en Twilio Sandbox.

### 5. Configurar tu número en .env
```env
JUAN_CAMILO_PHONE=whatsapp:+57XXXXXXXXXX
```

## Estructura del proyecto

```
agencia-whatsapp/
├── main.py          # FastAPI + webhook Twilio
├── router.py        # Detecta @agente y enruta a Claude API
├── history.py       # Historial de conversación por agente
├── agents/
│   ├── __init__.py
│   └── prompts.py   # System prompts de cada agente
├── requirements.txt
├── .env.example
└── README.md
```

## Seguridad

- Solo el número registrado en `JUAN_CAMILO_PHONE` puede enviar órdenes
- Validación de firma Twilio en cada webhook
- Sin secretos en el código — todo en variables de entorno
