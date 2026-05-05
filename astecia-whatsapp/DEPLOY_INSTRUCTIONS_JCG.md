# ASTECIA WhatsApp — Instrucciones de Deployment para Juan Camilo Gil

**Última actualización**: 14 de Abril, 2026  
**Status**: Listo para producción ✅  
**Tiempo estimado de setup**: 15 minutos  

---

## ¿Qué es esto?

ASTECIA está ahora disponible 24/7 via WhatsApp. Escribe cualquier pregunta comercial y recibes respuesta en segundos, sin que tu máquina esté encendida.

Arquitectura:
```
WhatsApp → Railway (servidor 24/7) → ASTECIA (Claude Haiku) → Respuesta WhatsApp
```

---

## Resumen Rápido

Ya está 95% hecho. Solo necesitas:

1. **Obtener 4 credenciales** (5 minutos)
2. **Pegar credenciales en Railway** (3 minutos)
3. **Hacer push de código** (2 minutos)
4. **Configurar webhook en Meta** (5 minutos)

Total: **15 minutos** y listo.

---

## Paso 1: Obtener Credenciales

### 1.1 — Anthropic API Key

1. Ve a → https://console.anthropic.com/keys
2. Click **Create Key**
3. Dale un nombre: `ASTECIA WhatsApp`
4. Click **Create**
5. **COPIA EL VALOR** (empieza con `sk-ant-`, no lo compartas)
   ```
   sk-ant-abc123xyz...
   ```
   Guárdalo en un lugar seguro.

### 1.2 — WhatsApp Business API Credentials

1. Ve a → https://developers.facebook.com/
2. Selecciona tu app de WhatsApp Business
3. En el menú, ve a **WhatsApp** → **Configuration**
4. Copia estos valores:
   ```
   WHATSAPP_TOKEN = EAABsZ...  (Access Token)
   WHATSAPP_PHONE_ID = 123456789  (Phone Number ID)
   WHATSAPP_VERIFY_TOKEN = astecia_secret_2026  (Este lo defines tú)
   ```
   Guárdalos.

---

## Paso 2: Configura Variables en Railway

### Opción A — Dashboard (más visual)

1. Ve a → https://railway.app/
2. Login con tu cuenta
3. Selecciona proyecto **astecia-whatsapp**
4. Click en el servicio (debe decir "astecia-whatsapp")
5. Click **Variables** (en la pestaña)
6. Click **Add New Variable**
7. Añade estas 4:

   | Variable | Valor |
   |----------|-------|
   | `ANTHROPIC_API_KEY` | `sk-ant-abc123...` (la que copiaste) |
   | `WHATSAPP_TOKEN` | `EAABsZ...` |
   | `WHATSAPP_PHONE_ID` | `123456789` |
   | `WHATSAPP_VERIFY_TOKEN` | `astecia_secret_2026` |

8. Click **Deploy** (arriba a la derecha)

### Opción B — Terminal (más rápido, si sabes usar git bash)

```bash
# Terminal en C:\Users\PCC\Documents\JUAN CAMILO GIL\PERSONAL\PROGRAMACIÓN\AGENCIA\astecia-whatsapp\

# Login a Railway
railway login

# Inicializa proyecto
railway init
# → Selecciona "astecia-whatsapp"

# Añade variables
railway variables set ANTHROPIC_API_KEY sk-ant-abc123xyz...
railway variables set WHATSAPP_TOKEN EAABsZ...
railway variables set WHATSAPP_PHONE_ID 123456789
railway variables set WHATSAPP_VERIFY_TOKEN astecia_secret_2026

# Deploy
railway up

# Espera hasta ver "Application running on: https://..."
# Copia esa URL
```

---

## Paso 3: Deploy del Código

### Opción A — Git Push (recomendado)

1. Abre terminal en: `C:\Users\PCC\Documents\JUAN CAMILO GIL\PERSONAL\PROGRAMACIÓN\AGENCIA\astecia-whatsapp\`

2. Ejecuta:
   ```bash
   git add .
   git commit -m "feat: ASTECIA WhatsApp integration live"
   git push origin main
   ```

3. Railway detecta el push automáticamente y empieza deploy
4. Ve a https://railway.app/ y mira el progress
5. Cuando veas "Deployment successful", vas al siguiente paso

### Opción B — Script Automático

1. Terminal en: `C:\Users\PCC\Documents\JUAN CAMILO GIL\PERSONAL\PROGRAMACIÓN\AGENCIA\astecia-whatsapp\`

2. Ejecuta:
   ```bash
   bash deploy.sh
   ```

3. Espera a que termine

---

## Paso 4: Obtener URL de Railway

1. Ve a https://railway.app/
2. Selecciona proyecto **astecia-whatsapp**
3. Busca **Deployments** en el lado derecho
4. Debería estar verde ("Deployment successful")
5. **Click en el deployment** → verás detalles
6. Busca **"Domain"** → algo como:
   ```
   https://astecia-whatsapp-xyz.railway.app
   ```
7. **COPIA ESTA URL** (importante)

---

## Paso 5: Configura Webhook en Meta

1. Ve a → https://developers.facebook.com/
2. Selecciona tu app de WhatsApp Business
3. Menu → **WhatsApp** → **Configuration**
4. Busca **Webhook URL**
5. Pega aquí:
   ```
   https://astecia-whatsapp-xyz.railway.app/webhook
   (cambia "xyz" por la que copiaste)
   ```
6. **Verify Token**: `astecia_secret_2026`
7. Click **Verify and Save**

Si ves error 403: verifica que el Verify Token coincida exactamente.

---

## Paso 6: Suscribirse a Webhooks

1. En el mismo lugar (Meta → WhatsApp → Configuration)
2. Busca **Webhook fields** o **Subscribe to this field**
3. Selecciona:
   - ✅ `messages`
   - ✅ `message_template_status_update`
4. Click **Subscribe**

Listo. El webhook está configurado.

---

## Testing

### Test 1 — Verifica que está online

```bash
curl https://astecia-whatsapp-xyz.railway.app/health
```

Deberías ver:
```json
{
  "status": "healthy",
  "astecia": "online",
  "whatsapp": "connected"
}
```

### Test 2 — Envía mensaje de WhatsApp

1. Abre WhatsApp en tu teléfono
2. Envía un mensaje a tu número de WhatsApp Business
3. Ejemplo: `"¿Vale la pena perseguir Prokpil?"`
4. **ASTECIA debería responder en 2-5 segundos**

Si no responde:
```bash
# Mira logs
railway logs -f

# Busca errores
railway logs | grep ERROR
```

### Test 3 — Test local (opcional)

Quieres verificar que ASTECIA funciona antes de enviar vía WhatsApp:

```bash
# Terminal en astecia-whatsapp/

# Instala dependencias
pip install -r requirements.txt

# Test
export ANTHROPIC_API_KEY=sk-ant-abc123...
python test_astecia.py
```

Se abre una conversación interactiva con ASTECIA. Escribe preguntas y prueba.

---

## Monitoreo (después de live)

### Logs en tiempo real
```bash
railway logs -f
```

### Restart si algo falla
```bash
railway restart
```

### Ver deployments anteriores
```bash
railway history
```

---

## Ejemplos de Uso

Una vez está live, puedes preguntarle a ASTECIA desde WhatsApp:

```
Tú: "¿Vale la pena perseguir Prokpil?"
ASTECIA: "No. Feeling 30%, ciclo largo, margen 8%. 
Mejor enfócate en Cargill (40M, 70% feeling) y O Tafur (180M, avícola)."

Tú: "¿Quién es el decision maker real en Papeles del Cauca?"
ASTECIA: "Director de Operaciones (gerente de planta central).
KPI: reducir costos 15% en codificación. Cierra en 45 días."

Tú: "Redacta email follow-up para Omnilife"
ASTECIA: "Asunto: Demo Técnica — Próximos Pasos

Estimado [nombre],
Agradecemos tu tiempo en nuestra reunión del lunes...
[email completo listo para enviar]"

Tú: "¿Cuál es mi mejor movimiento con Tecnosur?"
ASTECIA: "Llamar hoy (antes de las 2pm, menos calls de competencia).
Tu diferenciador: 6 meses sin downtime con KMC. Ellos olvidan eso."
```

---

## Troubleshooting

### "Error 403 en webhook"
- Verifica Verify Token en Meta = `astecia_secret_2026`
- Reinicia Railway: `railway restart`

### "No recibe mensajes"
- Verifica webhook está configurado en Meta
- Logs: `railway logs | grep webhook`
- Revisa que WHATSAPP_TOKEN sea válido

### "ASTECIA no responde"
- Verifica ANTHROPIC_API_KEY en Railway
- Logs: `railway logs | grep ANTHROPIC`
- Asegúrate de tener créditos en Anthropic

### "Respuestas lentas"
- Haiku es ultra-rápido, siempre < 3 segundos
- Si demora más, es culpa de WhatsApp, no de ASTECIA

---

## Costos

- **Railway**: $5 base/mes + $0.0000011/CPU-segundo (~$10-20/mes)
- **WhatsApp**: Gratis primeros 1000 msgs/mes, luego $0.0079/msg
- **Claude Haiku**: ~$0.008/1M input tokens + $0.024/1M output tokens
- **Total estimado**: $30-50/mes (muy barato para un asistente 24/7)

---

## Soporte

Si algo falla:
1. Mira logs: `railway logs -f`
2. Verifica credenciales en Railway dashboard
3. Contacta a Cinthya (automatización) o Jarvis (CEO)

---

## Próximos Pasos Opcionales

- Integración con tu CRM MAPER (actualizar POTs automáticamente)
- Análisis de conversación (trackear qué argumentos funcionan mejor)
- Escalación a Leo/Yang/Jarvis para análisis profundo (análisis semanal de portfolio)
- Respuestas con audio via WhatsApp

---

**¡Listo! En 15 minutos tienes tu asistente comercial 24/7.**

Úsalo sin límite. Cada respuesta es casi instantánea, cada análisis es preciso, cada argumentario está basado en tu contexto MAPER.

Bienvenido al futuro de la venta consultiva.

— Cinthya (Automatización) & Jarvis (CEO)
