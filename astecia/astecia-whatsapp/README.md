# ASTECIA WhatsApp — Agente Comercial Exclusivo

**ASTECIA WhatsApp** — asistente comercial estratégico 24/7 vía WhatsApp que combina a Leo (vendedor), Yang (investigadora) y Jarvis (estratega) en un agente Claude Haiku.

## Arquitectura

```
WhatsApp Business API
         ↓
    [Webhook FastAPI]
         ↓
   ASTECIA Agent
   (Claude Haiku)
         ↓
   Respuesta WhatsApp
```

## Requisitos Previos

1. **Anthropic API Key** — obtén en https://console.anthropic.com
2. **Meta WhatsApp Business API** — configurado en https://developers.facebook.com/
3. **Railway** — proyecto creado y CLI instalado
4. **Git** — para hacer push del código

## Configuración Paso a Paso

### Paso 1: Obtener Credenciales

#### Anthropic API Key
1. Ve a https://console.anthropic.com/keys
2. Crea nueva key
3. Copia el valor (empieza con `sk-ant-`)

#### WhatsApp Business API
1. Ve a https://developers.facebook.com/
2. Crea una app o usa existente
3. Configura WhatsApp Business API
4. Obtén:
   - **WHATSAPP_TOKEN**: Access token para API
   - **WHATSAPP_PHONE_ID**: ID de tu número de teléfono
   - **WHATSAPP_VERIFY_TOKEN**: Token de verificación webhook (ej: `astecia_secret_2026`)

### Paso 2: Deploy en Railway

#### Opción A: Via Dashboard Railway

1. **Sube el código a GitHub** (si aún no lo hiciste)
   ```bash
   cd astecia-whatsapp
   git add .
   git commit -m "feat: ASTECIA WhatsApp integration"
   git push origin main
   ```

2. **En Railway Dashboard**
   - Ve a tu proyecto `astecia-whatsapp`
   - Click **New** → **GitHub Repo**
   - Selecciona este repositorio
   - Railway detecta `Dockerfile` automáticamente

3. **Configura Variables de Entorno**
   - En Railway Dashboard → tu servicio → **Variables**
   - Añade:
     ```
     ANTHROPIC_API_KEY = sk-ant-...
     WHATSAPP_TOKEN = EAA...
     WHATSAPP_PHONE_ID = 123456789
     WHATSAPP_VERIFY_TOKEN = astecia_secret_2026
     ```

4. **Deploy**
   - Click **Deploy**
   - Espera a que termine (2-3 minutos)
   - Copia la URL del servicio (ej: `https://astecia-whatsapp.railway.app`)

#### Opción B: Via Railway CLI (más rápido)

1. **Instala Railway CLI** (si no tienes)
   ```bash
   npm install -g @railway/cli
   ```

2. **Login a Railway**
   ```bash
   railway login
   ```

3. **Inicializa el proyecto**
   ```bash
   cd astecia-whatsapp
   railway init
   # Selecciona el proyecto existente "astecia-whatsapp"
   ```

4. **Añade variables de entorno**
   ```bash
   railway variables set ANTHROPIC_API_KEY sk-ant-...
   railway variables set WHATSAPP_TOKEN EAA...
   railway variables set WHATSAPP_PHONE_ID 123456789
   railway variables set WHATSAPP_VERIFY_TOKEN astecia_secret_2026
   ```

5. **Deploy**
   ```bash
   railway up
   ```
   Railway compila y despliega automáticamente. Obtén la URL:
   ```bash
   railway logs
   # Busca "Application running on: https://..."
   ```

### Paso 3: Configura el Webhook en Meta

1. **Ve a Facebook App Settings**
   - https://developers.facebook.com/apps/
   - Tu app → WhatsApp → Configuration

2. **Callback URL**
   - URL: `https://astecia-whatsapp.railway.app/webhook`
   - Verify Token: `astecia_secret_2026` (el mismo que en variables)

3. **Click "Verify and Save"**
   - Meta enviará GET a tu webhook para verificar
   - Si ves error 403, revisa que Verify Token coincida

4. **Suscribirse a Webhooks**
   - En mismo lugar, busca "Subscribe to this field"
   - Selecciona: `messages` y `message_template_status_update`
   - Click Subscribe

## Testing

### Enviar Mensaje de Prueba

1. **Via WhatsApp**
   - Abre WhatsApp
   - Envía un mensaje a tu número de teléfono registrado en Meta
   - Ejemplo: "Hola ASTECIA, ¿vale la pena perseguir Cargill?"

2. **Ver Logs en Railway**
   ```bash
   railway logs -f
   ```
   Deberías ver:
   ```
   INFO - Mensaje de 573222340376: Hola ASTECIA...
   INFO - Respuesta ASTECIA: ...
   INFO - Mensaje enviado a 573222340376: wamid_...
   ```

3. **Verificar Health Check**
   ```bash
   curl https://astecia-whatsapp.railway.app/health
   ```
   Respuesta esperada:
   ```json
   {
     "status": "healthy",
     "astecia": "online",
     "whatsapp": "connected"
   }
   ```

## Cómo Usar ASTECIA

Una vez desplegado, puedes escribir a WhatsApp y ASTECIA responde en segundos:

### Ejemplos de Uso Real

```
Tú: "¿Vale la pena perseguir Prokpil?"
ASTECIA: "No. Feeling 30%, ciclo largo, margen bajo. Mejor enfócate en Cargill y O Tafur."

Tú: "¿Quién es el decision maker real en Papeles del Cauca?"
ASTECIA: "Director de Operaciones (gerente de planta). KPI: reducir costos 15%. Es licitación, cierra en 45 días."

Tú: "Redacta email de follow-up para Omnilife"
ASTECIA: "Asunto: Demo Técnica - Próximos Pasos
Estimado [nombre], agradecemos tu tiempo en la reunión. Adjuntamos el ROI en tinta que conversamos..."

Tú: "¿Cuál es mi mejor movimiento con Tecnosur?"
ASTECIA: "Llamarle hoy. Competencia bajó precio 12%, pero ustedes tienen mejor soporte. Argumentario: 6 meses sin downtime."
```

## Monitoreo

### Verificar que está corriendo

```bash
# Logs en tiempo real
railway logs -f

# Status del servicio
curl https://astecia-whatsapp.railway.app/health

# Historial de deployments
railway history
```

### Restart Manual (si necesario)

```bash
railway restart
```

## Troubleshooting

### "Error 403 en webhook verification"
- Verifica que `WHATSAPP_VERIFY_TOKEN` en Railway = token en Meta
- Reinicia el servicio: `railway restart`

### "No recibe mensajes de WhatsApp"
- Verifica webhook en Meta → Configuration está correcto
- Revisa logs: `railway logs | grep "Webhook"`
- Asegúrate que WHATSAPP_TOKEN es válido

### "ASTECIA no responde"
- Verifica que ANTHROPIC_API_KEY está configurada
- Revisa logs: `railway logs | grep "Error procesando"`
- Verifica que la API Key tiene créditos

### "Respuestas lentas"
- Haiku es muy rápido, normalmente < 2 segundos
- Si toma más, puede ser por congestión de WhatsApp
- Revisa status de Meta: https://status.cloud.meta.com/

## Estructura de Archivos

```
astecia-whatsapp/
├── main.py                 # Código principal FastAPI + ASTECIA
├── requirements.txt        # Dependencias Python
├── Dockerfile             # Para Railway
├── railway.json          # Configuración Railway
├── .env.example          # Template de variables
└── README.md             # Este archivo
```

## Variables de Entorno en Railway

| Variable | Valor | Dónde obtener |
|----------|-------|---------------|
| ANTHROPIC_API_KEY | sk-ant-... | console.anthropic.com |
| WHATSAPP_TOKEN | EAA... | developers.facebook.com |
| WHATSAPP_PHONE_ID | 123456789 | Meta App Settings |
| WHATSAPP_VERIFY_TOKEN | astecia_secret_2026 | Tú defines (cualquier string) |
| PORT | 8000 | Railway asigna automáticamente |

## Costos

- **Railway**: $5 base/mes + uso (aprox. $10-20/mes con este servicio)
- **WhatsApp Business API**: Gratis primeros 1000 mensajes/mes, luego ~$0.0079 por mensaje
- **Anthropic Claude Haiku**: ~$0.008 por 1M input tokens + $0.024 por 1M output tokens
- **Total estimado**: $30-50/mes para uso frecuente

## Roadmap

- [ ] Soporte para archivos (documentos, imágenes)
- [ ] Integración con CRM MAPER (actualizar POTs automáticamente)
- [ ] Análisis de conversación (trackear objeciones, argumentos usados)
- [ ] Escalación a Leo/Yang/Jarvis para análisis profundo
- [ ] Respuestas con audio via WhatsApp
- [ ] Dashboard de métricas

## Soporte

Para problemas, contacta a Cinthya (agente de automatización) o Jarvis (CEO).

---

**Última actualización**: 14-Abr-2026  
**Status**: Producción ✅  
**Uptime**: 24/7 en Railway  
**Owner**: Juan Camilo Gil  
**Tech Owner**: Cinthya (Automatización)
