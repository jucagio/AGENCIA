# Sprint 1 — Gmail + Calendar + Drive + Tasks

**Fechas**: 18 Abril 2026 (8 AM - 6 PM)  
**Asignado a**: Sasha  
**Supervisor**: Jarvis  
**Capacitación**: Jade  

## 🎯 Objetivo

Implementar 4 tools funcionales que permitan a ASTECIA leer datos de Google Workspace:
- Gmail (list, search, read)
- Calendar (list events)
- Drive (list files)
- Tasks (list tasks)

## 📅 Timeline

```
8:00 - 10:00  → Gmail Tool (2h)
10:00 - 12:00 → Calendar Tool (2h)
12:00 - 1:00  → LUNCH
1:00 - 3:00   → Drive + Tasks Tools (2h)
3:00 - 6:00   → Testing + debugging (3h)
```

## ✅ Tareas

### Gmail Tool (Sprint 1 - Day 1)

**Archivo**: `agents/tools/gmail.js`

```javascript
exports.createGmailTool = () => ({
  name: 'read_gmail',
  description: 'Leer y buscar emails en Gmail',
  input_schema: {
    type: 'object',
    properties: {
      action: { enum: ['list', 'search', 'read'] },
      query: { type: 'string' },
      messageId: { type: 'string' },
    },
  },
  handler: async (input) => {
    // Implementar
  }
})
```

**Acciones**:
- [ ] `list` - Últimos 10 emails
- [ ] `search` - Buscar por query (from:, subject:, etc)
- [ ] `read` - Obtener contenido completo de un email

**Test cases**:
- [ ] list() → obtiene 10 emails
- [ ] search('from:cargill.com') → filtra por dominio
- [ ] read(messageId) → obtiene el contenido completo

---

### Calendar Tool (Sprint 1 - Day 1)

**Archivo**: `agents/tools/calendar.js`

```javascript
exports.createCalendarTool = () => ({
  name: 'read_calendar',
  description: 'Leer eventos de Google Calendar',
  input_schema: {
    type: 'object',
    properties: {
      action: { enum: ['list', 'search'] },
      query: { type: 'string' },
      timeMin: { type: 'string' },
      timeMax: { type: 'string' },
    },
  },
  handler: async (input) => {
    // Implementar
  }
})
```

**Acciones**:
- [ ] `list` - Eventos de esta semana
- [ ] `search` - Buscar por título del evento

**Test cases**:
- [ ] list() → obtiene próximos 7 días
- [ ] search('reunión') → filtra eventos

---

### Drive Tool (Sprint 1 - Day 1)

**Archivo**: `agents/tools/drive.js`

```javascript
exports.createDriveTool = () => ({
  name: 'read_drive',
  description: 'Leer archivos y carpetas de Google Drive',
  input_schema: {
    type: 'object',
    properties: {
      action: { enum: ['list', 'search', 'read'] },
      folderId: { type: 'string' },
      query: { type: 'string' },
      fileId: { type: 'string' },
    },
  },
  handler: async (input) => {
    // Implementar
  }
})
```

**Acciones**:
- [ ] `list` - Listar archivos en raíz
- [ ] `search` - Buscar por nombre
- [ ] `read` - Leer contenido de archivo (si es texto/JSON)

---

### Tasks Tool (Sprint 1 - Day 1)

**Archivo**: `agents/tools/tasks.js`

```javascript
exports.createTasksTool = () => ({
  name: 'manage_tasks',
  description: 'Leer y crear tareas en Google Tasks',
  input_schema: {
    type: 'object',
    properties: {
      action: { enum: ['list', 'create'] },
      title: { type: 'string' },
      due: { type: 'string' },
    },
  },
  handler: async (input) => {
    // Implementar
  }
})
```

**Acciones**:
- [ ] `list` - Obtener tareas pendientes
- [ ] `create` - Crear nueva tarea

---

## 🧪 Testing

### Unit Tests

```bash
# Test Gmail
curl -X POST http://localhost:3000/astecia \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Cuáles son mis últimos 3 emails?"}'

# Test Calendar
curl -X POST http://localhost:3000/astecia \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Qué eventos tengo esta semana?"}'

# Test Drive
curl -X POST http://localhost:3000/astecia \
  -H "Content-Type: application/json" \
  -d '{"message": "Busca archivos en Drive sobre cotizaciones"}'

# Test Tasks
curl -X POST http://localhost:3000/astecia \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Cuáles son mis tareas pendientes?"}'
```

## 📊 Deliverables

Por fin de día 18 Abril:
- [x] `agents/tools/gmail.js` - Funcional
- [x] `agents/tools/calendar.js` - Funcional
- [x] `agents/tools/drive.js` - Funcional
- [x] `agents/tools/tasks.js` - Funcional
- [x] Todos los tools integrados en `server.js`
- [x] Tests exitosos (manual)
- [x] Push a GitHub

## 🚨 Blockers

Si encuentro problemas:
1. Google OAuth error → Jade ayuda con configuración
2. API quota exceeded → Jarvis aumenta límites
3. Token inválido → Regenerar en Google Cloud Console
4. Encoding issues → Usar UTF-8 en headers

**Report inmediatamente a Jarvis si hay bloqueos.**

---

**Owner**: Sasha  
**Status**: PENDING (starts April 18 8 AM)  
**Supervisor**: Jarvis  
