# 🔴 ASTECIA — KICKOFF INMEDIATO SASHA

**Status:** 🚨 PROYECTO INICIADO YA  
**Asignado a:** Sasha (Programadora Senior)  
**Supervisor:** Jarvis (CEO)  
**Capacitación:** Jade (HOY/AHORA)  
**Timeline:** Hoy → Viernes (5 días intensos)  
**Target:** Go-Live Viernes 25 Abril 2026

---

## 📋 TAREAS HOY (4/17/2026)

### **INMEDIATO (AHORA - 2 horas)**

**SASHA:**
- [ ] Crear GitHub repo: `astecia-integration`
- [ ] Inicializar Node.js project (`npm init -y`)
- [ ] Instalar dependencias base:
  ```bash
  npm install @anthropic-ai/sdk
  npm install google-auth-library google-api-nodejs-client
  npm install whatsapp-web.js qrcode-terminal
  npm install dotenv
  npm install express
  ```
- [ ] Crear `.env.example` (sin credenciales)
- [ ] Crear `server.js` básico (200 líneas)
- [ ] Push a GitHub

**JADE:**
- [ ] Capacitar a Sasha en MCPs + Google OAuth (30 min)
- [ ] Enviar enlaces de documentación oficial
- [ ] Setup checklist

**JARVIS:**
- [ ] Asignar créditos de cloud (Railway/Render)
- [ ] Monitorear progreso (daily standup)

---

### **HOY (6-8 PM)**

**SASHA - Google OAuth Setup (90 min)**
- [ ] Ir a https://console.cloud.google.com
- [ ] Crear proyecto "ASTECIA-INTEGRATION"
- [ ] Habilitar APIs:
  - Gmail API
  - Google Calendar API
  - Google Drive API
  - Google Tasks API
- [ ] Crear credenciales (OAuth 2.0 Client ID)
- [ ] Generar refresh token (script de prueba)
- [ ] Guardar en `.env` (no commitar)
- [ ] Crear `config/googleAuth.js` (30 líneas)

**JADE:**
- [ ] Responder preguntas de Sasha en tiempo real (Slack/Discord)

---

### **MAÑANA 18 ABRIL (8 AM - 6 PM)**

**SASHA - Sprint 1: Gmail + Calendar (8 horas)**

```
8-10 AM:   Gmail reader (2h)
          tools/gmail.js
          - list emails
          - search
          - read content

10-12 PM:  Calendar reader (2h)
          tools/calendar.js
          - list events
          - search by title
          - read details

12-1 PM:   LUNCH

1-3 PM:    Drive + Tasks (2h)
          tools/drive.js
          tools/tasks.js

3-6 PM:    Testing + debugging (3h)
          - Test cada tool individualmente
          - Logs
          - Error handling
```

**Entregable:** Todos los tools de Google funcionando en local

---

### **19 ABRIL (8 AM - 6 PM)**

**SASHA - Sprint 2: WhatsApp + Local Files (8 horas)**

```
8-11 AM:   WhatsApp integration (3h)
          - Decidir: Composio vs whatsapp-web.js
          - Setup + debugging
          - QR scanning si es web.js

11-12 PM:  Local file reader (1h)
          tools/localFiles.js
          - fs module wrapper
          - JSON parser
          - Error handling

12-1 PM:   LUNCH

1-4 PM:    Connect to Claude Agent SDK (3h)
          - agents/astecia.js
          - Registrar todos los tools
          - Test basic prompts

4-6 PM:    End-to-end testing (2h)
          - Leer email → responder en WhatsApp
          - Ver calendario → proponer tiempo
          - Buscar cotización → acceso local
```

**Entregable:** ASTECIA con acceso a TODOS los sistemas

---

### **20 ABRIL (8 AM - 12 PM)**

**SASHA - Sprint 3: Deploy + Production (4 horas)**

```
8-9 AM:    Deploy en Railway/Render
          - Crear cuenta + vinc GitHub
          - Configurar env vars en cloud
          - Deploy

9-11 AM:   Testing en producción (2h)
          - Leer email de verdad
          - Responder WhatsApp de verdad
          - Ver tu agenda real

11-12 PM:  Documentación + README.md
          - Setup para otros developers
          - Troubleshooting
```

**Entregable:** ASTECIA en producción, listo para usar

---

### **21-24 ABRIL**

**Buffer + Refinamientos**
- [ ] Optimizaciones de performance
- [ ] Manejo de edge cases
- [ ] Mejoras según feedback

---

## 🎯 DELIVERABLES POR DÍA

| Día | Deliverable | Status |
|-----|-------------|--------|
| **Hoy (4/17)** | GitHub repo + dependencias + basic server | ⏳ |
| **Mañana (4/18)** | Gmail, Calendar, Drive, Tasks funcionando | ⏳ |
| **19 Abril** | WhatsApp + Local files + ASTECIA integrado | ⏳ |
| **20 Abril** | Deploy en producción | ⏳ |
| **21-24 Abril** | Testing real + refinamientos | ⏳ |
| **25 Abril** | 🚀 GO-LIVE | ✅ |

---

## 💾 CÓDIGO BASE (Copiar-Pegar)

### **server.js**
```javascript
const express = require('express');
const { Anthropic } = require('@anthropic-ai/sdk');
const { createGmailTool } = require('./agents/tools/gmail');
const { createCalendarTool } = require('./agents/tools/calendar');
const { createDriveTool } = require('./agents/tools/drive');
const { createTasksTool } = require('./agents/tools/tasks');
const { createWhatsAppTool } = require('./agents/tools/whatsapp');
const { createLocalFilesTool } = require('./agents/tools/localFiles');

require('dotenv').config();

const app = express();
app.use(express.json());

const client = new Anthropic();

const tools = [
  createGmailTool(),
  createCalendarTool(),
  createDriveTool(),
  createTasksTool(),
  createWhatsAppTool(),
  createLocalFilesTool(),
];

// ASTECIA Agent
async function astecia(userMessage) {
  const response = await client.messages.create({
    model: 'claude-sonnet-4-6',
    max_tokens: 2048,
    system: `Eres ASTECIA, el cerebro comercial personal de Juan Camilo Gil.
    
    Tienes acceso a:
    - Gmail (leer, buscar, responder)
    - Google Calendar (ver eventos)
    - Google Drive (leer documentos)
    - Google Tasks (notas)
    - WhatsApp Web (leer/responder)
    - Archivos locales (cotizaciones, formatos)
    
    Usa estas herramientas automáticamente cuando sea necesario.
    Mantén tono humano, directo, sin relleno.`,
    messages: [
      {
        role: 'user',
        content: userMessage,
      },
    ],
    tools: tools,
  });

  return response.content[0].text;
}

app.post('/astecia', async (req, res) => {
  const { message } = req.body;
  const response = await astecia(message);
  res.json({ response });
});

app.listen(3000, () => {
  console.log('ASTECIA running on http://localhost:3000');
});
```

### **tools/gmail.js**
```javascript
const { google } = require('googleapis');
const fs = require('fs');

function createGmailTool() {
  return {
    name: 'read_gmail',
    description: 'Leer y buscar emails en Gmail',
    input_schema: {
      type: 'object',
      properties: {
        action: {
          type: 'string',
          enum: ['list', 'search', 'read'],
          description: 'Acción: listar, buscar o leer email',
        },
        query: {
          type: 'string',
          description: 'Consulta de búsqueda (ej: "from:cargill.com")',
        },
        messageId: {
          type: 'string',
          description: 'ID del mensaje para leer completo',
        },
      },
      required: ['action'],
    },
    handler: async (input) => {
      // Usar credenciales de Google OAuth
      const auth = getGoogleAuth();
      const gmail = google.gmail({ version: 'v1', auth });

      if (input.action === 'list') {
        const res = await gmail.users.messages.list({
          userId: 'me',
          maxResults: 10,
        });
        return res.data.messages || [];
      }

      if (input.action === 'search') {
        const res = await gmail.users.messages.list({
          userId: 'me',
          q: input.query,
          maxResults: 5,
        });
        return res.data.messages || [];
      }

      if (input.action === 'read') {
        const res = await gmail.users.messages.get({
          userId: 'me',
          id: input.messageId,
          format: 'full',
        });
        return res.data.payload.parts[0].data || res.data.snippet;
      }
    },
  };
}

function getGoogleAuth() {
  // Implementar con credenciales de .env
  // Usar google-auth-library para OAuth2
}

module.exports = { createGmailTool };
```

**Resto de tools:** Patrón similar (calendar, drive, tasks, whatsapp, localFiles)

---

## 🔑 CREDENCIALES REQUERIDAS

**Para HOY (crear en Google Console):**
```
GOOGLE_CLIENT_ID=xxxx
GOOGLE_CLIENT_SECRET=xxxx
GOOGLE_REFRESH_TOKEN=xxxx
CLAUDE_API_KEY=sk-ant-xxxxx
```

**Para WhatsApp (Viernes):**
```
WHATSAPP_SESSION_NAME=astecia-session
(O Composio API key si usas Composio)
```

---

## 📞 COMUNICACIÓN

**Daily Standup:** 9 AM con Jarvis (15 min)
- ¿Qué hice ayer?
- ¿Qué hago hoy?
- ¿Bloqueadores?

**Slack Channel:** #astecia-dev (Sasha, Jarvis, Jade)
- Preguntas al instante
- Compartir avances

---

## ✅ SUCCESS CRITERIA

✅ Hoy: GitHub + deps + server basic  
✅ Mañana: Google tools funcionando  
✅ 19 Abril: WhatsApp + ASTECIA integrado  
✅ 20 Abril: En producción  
✅ 25 Abril: GO-LIVE  

---

## 🚨 SI HAY BLOQUEADORES

**Sasha reporta inmediatamente a Jarvis.**

Posibles bloqueadores:
- Google OAuth no autentica → Jade capaci
ta
- WhatsApp.js no conecta → Jade investiga Composio
- Deploy falla → Jarvis asigna Railway support
- ASTECIA no responde → Debug en paralelo

**No hay "lo vemos el lunes"** — Solucionamos HOY.

---

**Jarvis:** Monitor progress, remove blockers  
**Sasha:** Code, code, code 🚀  
**Jade:** Capacita, investiga, desbloquea  

**Comencemos. AHORA.**

---

**Owner:** Jarvis (CEO)  
**Asignado a:** Sasha  
**Status:** 🔴 PROYECTO ACTIVO  
**Vence:** Viernes 25 Abril 2026  
**Fecha creación:** 2026-04-17 (AHORA)
