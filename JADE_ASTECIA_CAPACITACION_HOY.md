# 📚 JADE — Capacitación ASTECIA (HOY 17 Abril, 6-8 PM)

**Asignado a**: Jade (Directora Intel & Capacitaciones)  
**Agente a Capacitar**: Sasha (Programadora Senior)  
**Tema**: Google OAuth + MCPs  
**Duración**: 2 horas máximo  
**Canal**: Slack #astecia-dev  

---

## 🎯 Objetivo

Capacitar a Sasha para:
1. Setup Google Cloud project
2. Crear OAuth 2.0 credentials
3. Generar refresh token
4. Integrar en `config/googleAuth.js`
5. Resolver cualquier bloqueador

---

## 📚 Materiales Requeridos

### Documentación Oficial (buscar HOY)

1. **Google OAuth 2.0 for Desktop**
   - https://developers.google.com/identity/oauth2/native-app
   - https://developers.google.com/identity/protocols/oauth2

2. **Google APIs Client Library for Node.js**
   - https://googleapis.dev/nodejs/
   - https://github.com/googleapis/google-api-nodejs-client

3. **Gmail API Reference**
   - https://developers.google.com/gmail/api/reference/rest

4. **Google Calendar API Reference**
   - https://developers.google.com/calendar/api/guides/overview

5. **Google Drive API Reference**
   - https://developers.google.com/drive/api/guides/about-sdk

6. **Google Tasks API Reference**
   - https://developers.google.com/tasks/reference/rest

### MCPs (Model Context Protocol)

- Search for: "Apify MCP", "Google API MCP", latest tools
- Document: Which MCPs can optimize ASTECIA
- Send links: Google Drive, Gmail, etc MCPs

---

## 🚀 Step-by-Step Capacitación

### 1. Google Cloud Console Setup (30 min)

**Con Sasha:**

```
1. Ir a https://console.cloud.google.com
2. Click "Create Project"
3. Nombre: "ASTECIA-INTEGRATION"
4. Esperar a que se cree
5. Click "Select Project"
```

**Habilitar APIs (6 min cada una):**

```
1. Search bar → "Gmail API"
   Click "Enable"

2. Search bar → "Google Calendar API"
   Click "Enable"

3. Search bar → "Google Drive API"
   Click "Enable"

4. Search bar → "Google Tasks API"
   Click "Enable"
```

---

### 2. OAuth 2.0 Credentials (20 min)

**Con Sasha:**

```
1. Left sidebar → "Credentials"
2. Click "Create Credentials" → "OAuth Client ID"
3. Choose: "Desktop application"
4. Click "Create"
5. Download JSON (IMPORTANTE: guardar en seguro)
6. Extract:
   - GOOGLE_CLIENT_ID
   - GOOGLE_CLIENT_SECRET
```

---

### 3. Generate Refresh Token (30 min)

**Crear script temporal** (Sasha corre):

```javascript
// script_temp_get_token.js
const { google } = require('googleapis');

const CLIENT_ID = 'your-client-id';
const CLIENT_SECRET = 'your-client-secret';
const REDIRECT_URL = 'http://localhost:3000/oauth/callback';

const oauth2Client = new google.auth.OAuth2(
  CLIENT_ID,
  CLIENT_SECRET,
  REDIRECT_URL
);

const scopes = [
  'https://www.googleapis.com/auth/gmail.readonly',
  'https://www.googleapis.com/auth/calendar.readonly',
  'https://www.googleapis.com/auth/drive.readonly',
  'https://www.googleapis.com/auth/tasks',
];

const authUrl = oauth2Client.generateAuthUrl({
  access_type: 'offline',
  scope: scopes,
  prompt: 'consent',
});

console.log('Abre este URL en tu navegador:');
console.log(authUrl);
console.log('\nDespués de autorizar, copia el código de la URL');
console.log('Pega aquí:');

// Sasha obtiene el código, lo pasa al script
// Script intercambia por refresh token
// Sasha copia refresh token a .env
```

**Paso a paso**:
1. Sasha corre script → genera URL
2. Sasha abre URL en navegador
3. Google pide permisos → Click "Allow"
4. Redirige a callback con código
5. Sasha copia código → pega en script
6. Script genera GOOGLE_REFRESH_TOKEN
7. Sasha copia a `.env`

---

### 4. Test Integration (20 min)

**Sasha corre**:

```bash
cd astecia-integration
npm test:google-auth
```

**Verificar**:
- ✅ OAuth2 client se crea
- ✅ Token refresh funciona
- ✅ Gmail API accessible
- ✅ Calendar API accessible
- ✅ Drive API accessible
- ✅ Tasks API accessible

---

## ⚠️ Troubleshooting Common Issues

### "Invalid Client ID"
→ Sasha verificó credenciales en Google Console  
→ Asegurar que están en `.env`

### "Redirect URL Mismatch"
→ En Google Console, agregar `http://localhost:3000/oauth/callback`  
→ En Settings → OAuth Consent Screen

### "Token Expired"
→ Normal después de 1 hora si no se usa  
→ `config/googleAuth.js` auto-refresca

### "Rate Limit Exceeded"
→ Jarvis aumenta quotas en Google Cloud  
→ Request `@jarvis` immediately

---

## 📋 Checklist Capacitación

### Para Jade

- [ ] Buscar documentación oficial más reciente
- [ ] Verificar MCPs disponibles (Google APIs)
- [ ] Preparar step-by-step para Sasha
- [ ] Tener respuestas a preguntas frecuentes
- [ ] Monitor Slack #astecia-dev
- [ ] Responder preguntas en tiempo real
- [ ] Verificar que `.env` está correcto
- [ ] Confirmar que `config/googleAuth.js` funciona

### Para Sasha

- [ ] Google Cloud project creado
- [ ] 4 APIs habilitadas
- [ ] OAuth credentials guardadas
- [ ] Refresh token en `.env`
- [ ] `config/googleAuth.js` testado
- [ ] Listo para Sprint 1 mañana 8 AM

---

## 🎓 MCPs to Investigate

Jade debe investigar si hay MCPs que simplifiquen:

1. **Gmail Integration**
   - Buscar: "Apify Gmail MCP", "Gmail integration"
   - Evaluar: ¿es más rápido que usar googleapis directamente?

2. **Google Calendar**
   - Buscar: "Calendar API MCP", "Anthropic Google Calendar"
   - Evaluar: ¿podemos usar MCP en lugar de SDK?

3. **Google Drive**
   - Buscar: "Drive MCP", "Document retrieval"
   - Evaluar: ¿hay MCPs de terceros?

4. **Superhuman/Email Intelligence**
   - Buscar: "Email understanding MCP", "Gmail analysis"
   - Bonus: ¿herramientas para análisis de emails?

**Reportar hallazgos a Sasha** para considerar en Sprint 1.

---

## 📞 Communication

- **Canal**: Slack #astecia-dev
- **Horario**: Today 6-8 PM
- **Emergencia**: Call Jarvis if blocker can't be resolved
- **Escalation**: @jarvis in Slack

---

## ✅ Success Criteria

✅ `.env` poblado con credenciales reales  
✅ `config/googleAuth.js` testado y funcional  
✅ Refresh token working  
✅ Sasha lista para Sprint 1 mañana  
✅ Cero bloqueadores  

---

**Capacitador**: Jade (Directora Intel & Capacitaciones)  
**Agente**: Sasha (Programadora Senior)  
**Fecha**: 17 Abril 2026, 6-8 PM  
**Status**: ✅ LISTO PARA EMPEZAR  
