# 🚀 ASTECIA Integration

**ASTECIA Integration** — cerebro comercial personal de Juan Camilo Gil: automatiza email, calendario, tareas, documentos y WhatsApp con IA (Claude).

## 📋 Descripción

ASTECIA es un agente de IA que integra múltiples fuentes de datos para asistir en gestión comercial:

- **Gmail**: Leer, buscar, responder emails
- **Google Calendar**: Ver eventos, proponer reuniones
- **Google Drive**: Acceder a documentos y cotizaciones
- **Google Tasks**: Crear tareas y recordatorios
- **WhatsApp Web**: Leer y responder mensajes
- **Archivos Locales**: Plantillas, catálogos, políticas

## 🏗️ Estructura del Proyecto

```
astecia-integration/
├── server.js                  # Servidor Express + API ASTECIA
├── .env.example              # Template de variables de entorno
├── package.json              # Dependencias
├── agents/
│   ├── tools/
│   │   ├── gmail.js          # Tool: read Gmail
│   │   ├── calendar.js       # Tool: read Calendar
│   │   ├── drive.js          # Tool: read Drive
│   │   ├── tasks.js          # Tool: manage Tasks
│   │   ├── whatsapp.js       # Tool: WhatsApp Web
│   │   └── localFiles.js     # Tool: read local files
│   └── astecia.js            # Main agent (Sprint 2)
└── config/
    └── googleAuth.js         # Google OAuth setup
```

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/your-org/astecia-integration.git
cd astecia-integration
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your credentials
```

### 3. Get Google Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project: `ASTECIA-INTEGRATION`
3. Enable APIs:
   - Gmail API
   - Google Calendar API
   - Google Drive API
   - Google Tasks API
4. Create OAuth 2.0 Client ID (Desktop application)
5. Generate refresh token using provided script
6. Add to `.env`

### 4. Get Claude API Key

1. Sign up at [Anthropic Console](https://console.anthropic.com)
2. Create API key
3. Add `CLAUDE_API_KEY` to `.env`

### 5. Run Server

```bash
npm start
# or
node server.js
```

Server will start on `http://localhost:3000`

## 📡 API Endpoints

### Health Check
```bash
GET /health
```

Response:
```json
{
  "status": "online",
  "service": "ASTECIA Integration Server",
  "timestamp": "2026-04-17T20:17:00Z",
  "tools_configured": 0
}
```

### ASTECIA Agent
```bash
POST /astecia
Content-Type: application/json

{
  "message": "¿Cuáles son mis emails pendientes?",
  "history": []
}
```

Response:
```json
{
  "response": "Leyendo tus emails...",
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 150,
    "output_tokens": 200
  }
}
```

## 📅 Development Timeline

| Fase | Fechas | Tareas | Status |
|------|--------|--------|--------|
| **Sprint 0** | 17 Abril | Setup repo, deps, basic server | ✅ |
| **Sprint 1** | 18 Abril | Gmail, Calendar, Drive, Tasks | ⏳ |
| **Sprint 2** | 19 Abril | WhatsApp, Local Files | ⏳ |
| **Sprint 3** | 20 Abril | Deploy a producción | ⏳ |
| **Testing** | 21-24 Abril | QA, refinamientos | ⏳ |
| **Go-Live** | 25 Abril | 🎉 En producción | ⏳ |

## 🛠️ Stack Técnico

- **Runtime**: Node.js
- **Server**: Express.js
- **IA**: Claude Sonnet 4.6 (Anthropic API)
- **APIs**: Google Workspace (Gmail, Calendar, Drive, Tasks)
- **WhatsApp**: whatsapp-web.js (o Composio)
- **Auth**: OAuth 2.0 (Google)
- **Deploy**: Railway o Render (TBD)

## 🔐 Security Notes

- Never commit `.env` file
- Rotate Google credentials regularly
- Use refresh tokens, not access tokens in code
- WhatsApp sessions are local (not shared)
- All API keys must be environment variables
- Enable HTTPS in production

## 📚 Tools Implementation Status

| Tool | Status | Sprint | Notes |
|------|--------|--------|-------|
| `read_gmail` | TODO | Sprint 1 | List, search, read emails |
| `read_calendar` | TODO | Sprint 1 | List events, check availability |
| `read_drive` | TODO | Sprint 1 | Access files and folders |
| `manage_tasks` | TODO | Sprint 1 | Create, update, delete tasks |
| `whatsapp_send` | TODO | Sprint 2 | Send messages to contacts |
| `whatsapp_read` | TODO | Sprint 2 | Listen for incoming messages |
| `read_local_files` | TODO | Sprint 2 | Parse JSON, txt, CSV |

## 🔧 Common Issues & Troubleshooting

### Google OAuth Error
```
Error: Invalid refresh token
```
**Solution**: Regenerate token in Google Cloud Console. Ensure scopes include all APIs.

### WhatsApp Session Not Found
```
Error: Session not authenticated
```
**Solution**: Delete `.wwebjs_auth/` folder and run again to scan QR code.

### Claude API Key Invalid
```
Error: 401 Unauthorized
```
**Solution**: Check `CLAUDE_API_KEY` format. Should start with `sk-ant-`.

## 👥 Team

- **Owner**: Juan Camilo Gil (Gerente Comercial)
- **Developer**: Sasha (Programadora Senior & Seguridad)
- **Architect**: Alejo (Solutions Architect)
- **Mentor**: Jade (Intel & Capacitaciones)
- **Supervisor**: Jarvis (CEO)

## 📞 Support

- **Slack**: #astecia-dev
- **Daily Standup**: 9 AM con Jarvis
- **Issues**: Report to Sasha or Jarvis immediately

## 📄 License

Internal project - Agencia.

---

**Status**: 🔴 In Development (Sprint 0)  
**Last Updated**: 2026-04-17  
**Target Go-Live**: 2026-04-25
