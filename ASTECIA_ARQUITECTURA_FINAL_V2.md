# ASTECIA — Arquitectura Final Simplificada

**Versión:** v2 (Post-Jade Research)  
**Fecha:** 2026-04-17  
**Owner:** Jarvis (CEO) + Sasha (Desarrollo)  
**Status:** 🟢 Listo para codificar

---

## 🎯 Visión

ASTECIA tiene acceso a **TODOS tus sistemas** sin complejidad:
- ✅ Gmail (lee, busca, responde)
- ✅ WhatsApp Web (lee, responde automáticamente)
- ✅ Google Calendar (ve tu agenda)
- ✅ Google Keep / Tasks (notas inteligentes)
- ✅ Google Drive (busca documentos)
- ✅ Archivos locales (cotizaciones, formatos)

**Stack:** Claude API + MCPs + Node.js (30 líneas de código)

---

## 📐 Arquitectura

```
┌────────────────────────────────────────────────────────┐
│                    ASTECIA AGENT                       │
│              (Claude Sonnet 4.6 en Plataforma)        │
│                                                        │
│  "¿Cuál es la agenda para Cargill?"                  │
│  "Responde el email de Omnilife"                      │
│  "¿Qué cotizaciones tengo para VJ1240?"               │
└────────┬───────────────────────────────────────────────┘
         │
         ├─ Claude Agent SDK
         │  ├─ Model: claude-sonnet-4-6
         │  └─ Tools: [Gmail, Calendar, Drive, Tasks, WhatsApp, LocalFS]
         │
         ├──────────────────────────────────────────────┐
         │        MCP Servers (Model Context Protocol)   │
         │                                               │
         ├─ Google Workspace MCP                        │
         │  ├─ Gmail (lectura/búsqueda/respuesta)       │
         │  ├─ Calendar (ver eventos, crear)            │
         │  ├─ Drive (leer documentos, buscar)          │
         │  └─ Tasks (notas, crear, modificar)          │
         │                                               │
         ├─ WhatsApp MCP (Composio)                     │
         │  ├─ Lectura de mensajes                      │
         │  └─ Envío automático de respuestas           │
         │                                               │
         └─ Local File System                           │
            └─ Cotizaciones.json, formatos, etc.        │
         │                                               │
         └──────────────────────────────────────────────┘
         │
         ▼
    ┌─────────────────────────────────────────────────┐
    │   Google OAuth 2.0                              │
    │   Gmail, Calendar, Drive, Tasks, Keep           │
    │                                                 │
    │   WhatsApp Business API / Web.js                │
    │   Mensajería automática                         │
    │                                                 │
    │   Node.js fs module                             │
    │   Archivo local reader                          │
    └─────────────────────────────────────────────────┘
```

---

## 🛠️ Stack Técnico

### Backend
```
Node.js 18+
├─ @anthropic-ai/sdk (Claude Agent SDK)
├─ google-workspace-mcp (Gmail, Calendar, Drive, Tasks)
├─ composio-mcp (WhatsApp integration)
├─ whatsapp-web.js (alternativa: WhatsApp Web)
└─ fs module (local file reader)
```

### Infraestructura
```
Servidor: Railway o Render (5 USD/mes)
Database: Opcional (solo si necesitas logs)
Autenticación: Google OAuth 2.0 + WhatsApp API
```

### Deployment
```
Git → GitHub → Railway/Render (auto-deploy)
Tiempo setup: 20 minutos
```

---

## 📋 Detalles por Integración

### 1️⃣ **GMAIL**

**Qué puede hacer ASTECIA:**
- Leer últimos 10 emails
- Buscar por remitente, asunto, fecha
- Responder automáticamente
- Extraer adjuntos

**Código base:**
```javascript
const gmailTool = {
  name: 'read_gmail',
  description: 'Leer y buscar emails',
  handler: async (action, query) => {
    // action = "read" | "search" | "reply"
    // Usa Google OAuth
    const emails = await gmail.list({ q: query });
    return emails;
  }
};
```

**Setup:** 15 minutos (OAuth token de Google Console)

---

### 2️⃣ **WHATSAPP WEB**

**Opción A (RECOMENDADA): Composio MCP + WhatsApp Business API**
- ✅ Oficial (Meta autoriza)
- ✅ Producción-ready
- ✅ Sin riesgo de bloqueo
- ⚠️ Requiere verificación en Meta
- ⏱️ Setup: 30-45 minutos

**Opción B (RÁPIDO): whatsapp-web.js**
- ✅ Funciona YA
- ✅ No requiere verificación Meta
- ⚠️ Riesgo: Meta puede bloquear cuentas no autorizadas
- ⏱️ Setup: 20 minutos

**Recomendación:** Opción A para producción, Opción B para MVP

**Código base (Opción B):**
```javascript
const { Client } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');

const client = new Client();

client.on('qr', (qr) => {
  qrcode.generate(qr, { small: true });
});

client.on('message', async (message) => {
  // ASTECIA procesa y responde
  const response = await astecia.respond(message.body);
  message.reply(response);
});

client.initialize();
```

**Setup:** 20 minutos

---

### 3️⃣ **GOOGLE CALENDAR**

**Qué puede hacer:**
- Ver eventos de hoy/semana/mes
- Crear eventos automáticamente
- Buscar disponibilidad
- Enviar recordatorios

**Código base:**
```javascript
const calendarTool = {
  name: 'read_calendar',
  description: 'Ver eventos del calendario',
  handler: async (timeRange = 'today') => {
    // timeRange = "today" | "week" | "month"
    const events = await calendar.list({ 
      timeMin: startTime,
      timeMax: endTime 
    });
    return events;
  }
};
```

**Setup:** 15 minutos (mismo OAuth que Gmail)

---

### 4️⃣ **GOOGLE KEEP / TASKS**

**Problema:** Keep NO tiene API oficial

**Solución:** Usar Google Tasks API (funcionalidad similar)
- Crear notas como tareas
- Leer listas
- Marcar como completado

**Alternativa:** Keep manual + Tasks API para automatización

**Setup:** 15 minutos

---

### 5️⃣ **GOOGLE DRIVE**

**Qué puede hacer:**
- Buscar documentos por nombre
- Leer archivos (PDF, Docs, Sheets)
- Descargar automáticamente
- Extraer texto

**Setup:** 15 minutos (mismo OAuth)

---

### 6️⃣ **ARCHIVOS LOCALES**

**Qué puede hacer:**
- Leer cotizaciones.json
- Acceder a formatos (propuestas, contratos)
- Buscar archivos por nombre

**Código base:**
```javascript
const localFilesTool = {
  name: 'read_local_file',
  description: 'Leer archivos locales',
  handler: (filePath) => {
    const content = fs.readFileSync(filePath, 'utf8');
    if (filePath.endsWith('.json')) {
      return JSON.parse(content);
    }
    return content;
  }
};
```

**Setup:** 5 minutos

---

## 🚀 Plan de Implementación (SASHA)

### **SEMANA 1**

#### **Lunes (3 horas)**
- [ ] Crear Node.js project + package.json
- [ ] Configurar Google OAuth (15 min)
  - IR a: https://console.cloud.google.com
  - Crear aplicación
  - Habilitar: Gmail API, Calendar API, Drive API, Tasks API
  - Generar credenciales JSON
- [ ] Integrar Google Workspace MCP (45 min)
- [ ] Integrar WhatsApp (Opción A o B) (45 min)
- [ ] Local file reader (15 min)
- [ ] Testing básico (30 min)

#### **Martes (2 horas)**
- [ ] Conectar MCPs con Claude Agent SDK
- [ ] Testing end-to-end (leer email, responder, ver agenda)
- [ ] Manejo de errores
- [ ] Logging

#### **Miércoles (1 hora)**
- [ ] Deploy en Railway/Render
- [ ] Configurar auto-deploy con GitHub
- [ ] Testing en producción

#### **Jueves (1 hora)**
- [ ] Ajustes y optimizaciones
- [ ] Performance tuning

#### **Viernes**
- [ ] Buffer / emergencias

**Total: 7 horas de desarrollo**

---

## 💾 Estructura del Proyecto

```
astecia-integration/
├── package.json
├── .env (Google credentials, API keys)
├── .env.example
├── server.js (entry point)
├── agents/
│   ├── astecia.js (main agent)
│   └── tools/
│       ├── gmail.js
│       ├── calendar.js
│       ├── drive.js
│       ├── tasks.js
│       ├── whatsapp.js
│       └── localFiles.js
├── config/
│   ├── googleAuth.js
│   └── whatsappAuth.js
├── utils/
│   └── logger.js
└── README.md
```

---

## 🔐 Seguridad

**Credenciales:**
```
.env (local, nunca versionado)
├─ GOOGLE_CLIENT_ID
├─ GOOGLE_CLIENT_SECRET
├─ GOOGLE_REFRESH_TOKEN
├─ WHATSAPP_API_KEY (si usas Composio)
└─ CLAUDE_API_KEY
```

**RLS (Row-Level Security):** No aplica (no hay BD)

**Acceso de usuario:** ASTECIA ve TODO lo que tú ves en tu cuenta

---

## 📊 Matriz de Funcionalidades

| Plataforma | Leer | Buscar | Crear | Modificar | Eliminar | Setup | Status |
|-----------|------|--------|--------|-----------|----------|-------|--------|
| **Gmail** | ✅ | ✅ | ✅ | ⚠️ | ⚠️ | 15m | Ready |
| **Calendar** | ✅ | ✅ | ✅ | ✅ | ✅ | 15m | Ready |
| **Drive** | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ | 15m | Ready |
| **Tasks/Keep** | ✅ | ✅ | ✅ | ✅ | ✅ | 15m | Ready |
| **WhatsApp** | ✅ | ⚠️ | ✅ | ⚠️ | ⚠️ | 25m | Ready |
| **Local Files** | ✅ | ✅ | ✅ | ✅ | ✅ | 5m | Ready |

---

## 🎓 Ejemplo: ASTECIA en Acción

**ASTECIA está en Claude Platform. Usuario pregunta:**

```
"¿Cuál es mi próxima reunión con Cargill?"
```

**ASTECIA hace:**
1. Llama a `read_calendar` 
2. Busca evento "Cargill" en próximos 7 días
3. Lee la descripción del evento (Gmail integrado)
4. Responde: "Mañana 2pm en Villagorgona con Santiago Pérez. Tema: Propuesta VJ1240"

**ASTECIA luego pregunta:**
```
"¿Redacto email resumen antes de ir?"
```

**Usuario dice:** "Sí"

**ASTECIA hace:**
1. Lee últimos 5 emails de Santiago Pérez
2. Extrae contexto (ROI, timeline, objeciones)
3. Redacta email (con humanización)
4. Pregunta: "¿Envío ahora o lo reviso antes?"

---

## ✅ Checklist de Go-Live

- [ ] Google OAuth configurado y testeado
- [ ] Gmail MCP funcionando (leer, buscar, responder)
- [ ] Calendar MCP funcionando
- [ ] Drive MCP funcionando
- [ ] Tasks MCP funcionando
- [ ] WhatsApp MCP funcionando
- [ ] Local file reader funcionando
- [ ] ASTECIA puede usar todos los tools
- [ ] Logging y error handling
- [ ] Deployed en Railway/Render
- [ ] Testing end-to-end en producción
- [ ] Juan Camilo valida que funciona

---

## 🎯 Success Criteria

✅ ASTECIA lee tu Gmail automáticamente  
✅ ASTECIA responde WhatsApp en contexto  
✅ ASTECIA ve tu calendario y propone mejores tiempos  
✅ ASTECIA accede a tus cotizaciones y formatos  
✅ ASTECIA mantiene el tono humano (Sonnet 4.6)  
✅ Todo funciona solo con Claude API  
✅ Implementación en 1 semana  

---

## 📞 Asignación

**Propietario:** Sasha (Programadora Senior)  
**Deadline:** Viernes 25 de Abril (1 semana)  
**Budget:** 7 horas desarrollo + 2 horas testing  
**Prioridad:** P0 (Critical)  

**Supervisor:** Jarvis  
**Capacitación:** Jade (lunes 21 AM)

---

**Status:** 🟢 Listo para que Sasha comience  
**Próximo paso:** Sasha abre GitHub repo + comienza Lunes  
**Reunión Sasha+Jarvis:** Lunes 10 AM (kickoff)

---

**Owner:** Jarvis (CEO)  
**Contribuidores:** Jade (Intel), Sasha (Dev)  
**Fecha:** 2026-04-17  
**Versión:** 2.0 (Final, Production-Ready)
