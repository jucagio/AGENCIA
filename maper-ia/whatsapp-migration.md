# MAPER.IA — Migración de Messenger a WhatsApp Business API
## Día 2: Guía completa de adaptación del workflow

---

## Diagnóstico del workflow actual

El workflow actual tiene 3 ramas que funcionan sobre Messenger. Esto es lo que cambia y lo que se mantiene:

| Componente | Estado actual | Estado tras migración |
|------------|--------------|----------------------|
| Webhook GET (verificación) | `GET /maper-ia-messenger` | Cambiar path a `maper-ia-whatsapp` |
| Webhook POST (mensajes) | `POST /maper-ia-messenger` | Mismo path nuevo |
| Objeto de verificación | `hub.mode`, `hub.verify_token`, `hub.challenge` | IGUAL — WhatsApp usa el mismo protocolo |
| Payload entrante | `entry[0].messaging[0].sender.id` | Diferente — ver estructura nueva abajo |
| API de envío | `graph.facebook.com/v21.0/me/messages` | `graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages` |
| Autenticación | `access_token` como query param | `Authorization: Bearer TOKEN` en header |
| Follow-ups | Tag `POST_PURCHASE_UPDATE` para Messenger | Usar templates de WhatsApp aprobados |
| Supabase (todas las RPCs) | Sin cambios | Sin cambios |
| IA Agent (Gemini) | Sin cambios | Sin cambios |
| Escalamientos | Sin cambios | Sin cambios |

**Conclusión: el 80% del workflow se reutiliza. Solo cambian los nodos de entrada y salida de Meta.**

---

## Parte 1 — Credenciales que necesitas obtener

Tienes 4 credenciales nuevas. Las obtienes todas en el mismo lugar: Meta for Developers.

### Credencial 1: Phone Number ID

Este es el identificador del número 3107735189 dentro de Meta. No es el número de teléfono — es un ID numérico largo que Meta asigna internamente.

**Dónde obtenerlo:**
1. Ir a [developers.facebook.com](https://developers.facebook.com) e ingresar con tu cuenta de Meta Business
2. Seleccionar tu App (la que ya tienes para MAPERSA) o crear una nueva
3. En el panel izquierdo: **WhatsApp > Configuration** (o **Getting Started**)
4. En la sección **Phone numbers**, verás el número 3107735189 listado
5. El Phone Number ID aparece debajo del número — es un número de 15-16 dígitos, algo como `573103456789012`
6. Copiarlo — lo necesitas en el nodo de envío

### Credencial 2: Business Account ID (WABA ID)

El ID de tu cuenta de WhatsApp Business. Aparece en la misma pantalla.

**Dónde obtenerlo:**
1. En la misma sección de WhatsApp en Meta for Developers
2. Busca "WhatsApp Business Account ID" o "WABA ID" — también es un número largo
3. Alternativamente: [business.facebook.com](https://business.facebook.com) > Settings > Business Account Info

### Credencial 3: System User Access Token (permanente)

El Page Access Token de Messenger expiraba. Para WhatsApp en producción usamos un System User Token que no expira.

**Pasos exactos:**
1. Ir a [business.facebook.com](https://business.facebook.com)
2. Panel izquierdo: **Settings** > **System Users**
3. Clic en **Add** > nombre: `maper-ia-bot` > rol: **Employee**
4. Clic en el usuario recién creado > **Add Assets**
5. Seleccionar **WhatsApp Accounts** > seleccionar tu cuenta de WhatsApp Business > marcar **Full Control**
6. Clic en **Generate Token** del system user
7. Seleccionar tu App > marcar permisos: `whatsapp_business_messaging` + `whatsapp_business_management`
8. Copiar el token — este NO expira (a diferencia del Page Access Token)

**Si no tienes acceso a System Users:** usa el token temporal de la consola de WhatsApp (válido 24h) para probar, luego configuras el permanente.

**Token temporal para prueba inmediata:**
1. En Meta for Developers > WhatsApp > Getting Started
2. Hay un token temporal generado automáticamente con expiración de 24h
3. Úsalo para probar hoy — luego lo reemplazas con el permanente

### Credencial 4: Webhook Verify Token

Lo defines tú. Usa este valor:

```
maper_ia_whatsapp_mapersa_2026
```

O define uno propio: mínimo 20 caracteres, sin espacios. Guárdalo — lo necesitas en dos lugares: en n8n (variable de entorno) y en Meta al registrar el webhook.

---

## Parte 2 — Cambios en el workflow n8n

### Cambio 1: Path del webhook (ambos nodos)

**Nodo: "Webhook GET — Verificacion Meta"**

Cambiar el campo `path`:
```
maper-ia-messenger  →  maper-ia-whatsapp
```

**Nodo: "Webhook POST — Mensajes Entrantes"**

Cambiar el campo `path`:
```
maper-ia-messenger  →  maper-ia-whatsapp
```

La URL resultante será:
```
https://tu-n8n.railway.app/webhook/maper-ia-whatsapp
```

Esta es la URL que registras en Meta. La verificación GET usa el mismo protocolo que Messenger (`hub.mode`, `hub.verify_token`, `hub.challenge`) — no cambia nada en ese flujo.

---

### Cambio 2: Estructura del payload entrante

WhatsApp envía una estructura diferente a Messenger. Actualizar el nodo "Set — Extraer sender_id, message_text, timestamp":

**Estructura actual (Messenger):**
```json
{
  "object": "page",
  "entry": [{
    "messaging": [{
      "sender": { "id": "PSID_DEL_USUARIO" },
      "message": { "text": "Hola" },
      "timestamp": 1234567890
    }]
  }]
}
```

**Estructura nueva (WhatsApp Business API):**
```json
{
  "object": "whatsapp_business_account",
  "entry": [{
    "id": "WABA_ID",
    "changes": [{
      "value": {
        "messaging_product": "whatsapp",
        "contacts": [{
          "profile": { "name": "Carlos Pérez" },
          "wa_id": "573107735189"
        }],
        "messages": [{
          "from": "573107735189",
          "id": "wamid.xxx",
          "timestamp": "1234567890",
          "text": { "body": "Hola, buenos días" },
          "type": "text"
        }]
      },
      "field": "messages"
    }]
  }]
}
```

**Nuevas expresiones para el nodo Set:**

| Campo | Expresión actual (Messenger) | Expresión nueva (WhatsApp) |
|-------|-----------------------------|-----------------------------|
| `sender_id` | `={{ $json.body.entry[0].messaging[0].sender.id }}` | `={{ $json.body.entry[0].changes[0].value.messages[0].from }}` |
| `message_text` | `={{ $json.body.entry[0].messaging[0].message.text }}` | `={{ $json.body.entry[0].changes[0].value.messages[0].text.body }}` |
| `timestamp` | `={{ $json.body.entry[0].messaging[0].timestamp }}` | `={{ $json.body.entry[0].changes[0].value.messages[0].timestamp }}` |
| `contact_name` | `={{ $json.body.entry[0].id }}` (era page_id) | `={{ $json.body.entry[0].changes[0].value.contacts[0].profile.name }}` |

El `sender_id` en WhatsApp es el número de teléfono internacional (ej: `573107735189`). Esto es importante porque en Supabase la columna `messenger_id` ahora almacenará números de WhatsApp. Si ya tienes datos de Messenger, los contactos de WhatsApp crearán registros nuevos — es el comportamiento correcto.

---

### Cambio 3: Filtro de eventos que no son mensajes

WhatsApp también envía eventos de status (delivered, read, sent). El filtro actual busca que `message_text` no esté vacío — eso funciona, pero necesitas agregar una condición adicional porque WhatsApp envía el payload de forma diferente cuando es un status.

**En el nodo "IF — message_text existe (filtrar delivery/read)"**, agregar una segunda condición:

Condición adicional:
- Campo: `={{ $json.body.entry[0].changes[0].value.messages }}`
- Operador: `is not empty`
- Combinador: `AND` con la condición existente

Esto filtra los webhooks de status (delivery, read) que no tienen el campo `messages`.

---

### Cambio 4: Nodo de envío de respuesta

Este es el cambio más importante. La API de envío de WhatsApp es diferente a Messenger.

**Nodo: "HTTP — Enviar respuesta a Messenger"**

Renombrar a: `HTTP — Enviar respuesta a WhatsApp`

**URL actual:**
```
https://graph.facebook.com/v21.0/me/messages
```

**URL nueva:**
```
https://graph.facebook.com/v21.0/{{ $env.WHATSAPP_PHONE_NUMBER_ID }}/messages
```

**Autenticación actual (query param):**
```
?access_token={{ $env.META_PAGE_ACCESS_TOKEN }}
```

**Autenticación nueva (header):**
Eliminar el query parameter `access_token`. En su lugar, agregar header:
```
Authorization: Bearer {{ $env.WHATSAPP_ACCESS_TOKEN }}
```

**Body actual (Messenger):**
```json
{
  "recipient": { "id": "{{ sender_id }}" },
  "message": { "text": "{{ respuesta }}" },
  "messaging_type": "RESPONSE"
}
```

**Body nuevo (WhatsApp):**
```json
{
  "messaging_product": "whatsapp",
  "to": "{{ $('Set — Capturar respuesta IA').item.json.sender_id }}",
  "type": "text",
  "text": {
    "body": "{{ $('Set — Capturar respuesta IA').item.json.ai_response.replace(/\[ESCALAR[^\]]*\]/g, '').trim() }}"
  }
}
```

---

### Cambio 5: Nodo de envío de follow-ups

**Nodo: "HTTP — Enviar follow-up a Messenger"**

Los follow-ups en WhatsApp requieren templates aprobados por Meta para mensajes fuera de la ventana de 24 horas. Para empezar, usa este enfoque:

**Fase 1 (inmediata — dentro de ventana de 24h):** mismo formato que el cambio 4, sin tag.

**Fase 2 (cuando tengas template aprobado):** estructura de template:
```json
{
  "messaging_product": "whatsapp",
  "to": "{{ sender_id }}",
  "type": "template",
  "template": {
    "name": "maper_seguimiento_comercial",
    "language": { "code": "es_CO" },
    "components": [{
      "type": "body",
      "parameters": [{ "type": "text", "text": "{{ mensaje_generado }}" }]
    }]
  }
}
```

Por ahora, para que funcione desde el día 1, el nodo de follow-up usa el mismo formato de texto libre. Solo funciona dentro de la ventana de 24h desde el último mensaje del cliente — que es exactamente cuándo tiene sentido hacer follow-up comercial de todos modos.

**URL del nodo de follow-up:** misma URL nueva con Phone Number ID
**Autenticación:** mismo header Bearer

---

### Cambio 6: Supabase — campo messenger_id

Las RPCs de Supabase usan el parámetro `p_messenger_id` para identificar contactos. En WhatsApp, el `sender_id` es un número de teléfono internacional.

**No necesitas cambiar las RPCs de Supabase.** El número de WhatsApp (`573107735189`) simplemente se almacena en la columna `messenger_id` como string. El sistema funciona igual — solo el tipo de valor cambia.

Si en el futuro quieres distinguir contactos de Messenger vs WhatsApp, agrega una columna `channel` a la tabla `contacts` — pero eso no bloquea el lanzamiento.

---

## Parte 3 — Variables de entorno a agregar en n8n

En Railway (donde está n8n desplegado), agregar estas variables:

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `WHATSAPP_PHONE_NUMBER_ID` | El ID numérico del número 3107735189 | Obtenido en Meta > WhatsApp > Configuration |
| `WHATSAPP_BUSINESS_ACCOUNT_ID` | El WABA ID | Obtenido en Meta > WhatsApp > Configuration |
| `WHATSAPP_ACCESS_TOKEN` | El System User Token permanente | Generado en Meta Business Manager |
| `META_VERIFY_TOKEN` | `maper_ia_whatsapp_mapersa_2026` | Ya existía — mantener o cambiar el valor |

Puedes eliminar `META_PAGE_ACCESS_TOKEN` una vez que el sistema funcione en WhatsApp.

**Dónde agregar en Railway:**
1. Ir al proyecto de n8n en Railway
2. Clic en el servicio > **Variables**
3. Agregar cada variable con su valor

---

## Parte 4 — Registrar el webhook en Meta

Una vez que el workflow está modificado y activo en n8n:

### Paso 1: Obtener la URL del webhook
1. En n8n, abrir el workflow
2. Activar el toggle **Active** (esquina superior derecha)
3. Clic en el nodo **Webhook GET — Verificacion Meta**
4. Copiar la **Production URL**
   - Debe ser: `https://tu-n8n.railway.app/webhook/maper-ia-whatsapp`

### Paso 2: Registrar en Meta for Developers
1. Ir a Meta for Developers > tu App > **WhatsApp** > **Configuration**
2. En la sección **Webhook**, clic en **Edit**
3. Completar:
   - **Callback URL**: `https://tu-n8n.railway.app/webhook/maper-ia-whatsapp`
   - **Verify Token**: `maper_ia_whatsapp_mapersa_2026`
4. Clic en **Verify and Save**
5. Meta hace un GET a tu URL — n8n responde con el `hub.challenge` — Meta muestra palomita verde

### Paso 3: Suscribir campos del webhook
1. Después de verificar, en la misma sección de Webhook
2. Clic en **Manage** junto al campo de suscripciones
3. Marcar: `messages`
4. Guardar

---

## Parte 5 — Verificar que todo funciona (test en 5 minutos)

### Test 1: Verificación del webhook
- Si el webhook ya está registrado y la palomita es verde, este test está hecho.

### Test 2: Mensaje entrante básico
1. Desde otro número de WhatsApp, enviar un mensaje al 3107735189
2. En n8n > **Executions**, verificar que aparece una ejecución nueva
3. Expandir el nodo **Set — Extraer sender_id, message_text, timestamp**
4. Confirmar que `sender_id` = número de quien escribió, `message_text` = texto enviado

### Test 3: Respuesta completa
1. El mismo mensaje del Test 2 debe haber generado una respuesta de MAPER.IA
2. Verificar en el WhatsApp que envió el mensaje que llegó una respuesta del bot
3. En n8n, expandir el nodo **HTTP — Enviar respuesta a WhatsApp** — debe tener status 200

### Test 4: Escalamiento
1. Desde WhatsApp enviar: "quiero hablar con una persona"
2. En Supabase, verificar en la tabla `escalations` que se creó un registro nuevo

### Si hay error en el envío (status 400/401):
- 401: el `WHATSAPP_ACCESS_TOKEN` no es válido o expiró — generar nuevo token
- 400: revisar el body del nodo de envío — especialmente que `to` tenga formato internacional (57XXXXXXXXXX)

---

## Resumen ejecutivo — Qué hacer en orden

```
1. Obtener Phone Number ID  →  Meta for Developers > WhatsApp > Configuration
2. Obtener WABA ID          →  misma pantalla
3. Generar Access Token     →  Meta Business Manager > System Users > Generate Token
4. Agregar variables en Railway: WHATSAPP_PHONE_NUMBER_ID, WHATSAPP_ACCESS_TOKEN
5. En n8n — cambiar path de ambos webhooks a "maper-ia-whatsapp"
6. En n8n — actualizar nodo Set con nuevas expresiones de payload
7. En n8n — agregar condición de filtro para status events
8. En n8n — actualizar nodo HTTP de envío (URL + auth + body)
9. En n8n — actualizar nodo HTTP de follow-up (URL + auth + body)
10. Activar workflow
11. Registrar webhook en Meta > WhatsApp > Configuration
12. Suscribir campo "messages"
13. Hacer test desde WhatsApp
```

Tiempo estimado real: 45-60 minutos si tienes acceso a Meta for Developers y Railway.

---

## Nota sobre la App de Meta existente

Si la App que tienes ya tiene Messenger configurado para MAPERSA, tienes dos opciones:

**Opción A — Misma App, agregar WhatsApp (recomendada):**
- En la App existente, ir a **Add Product** > agregar **WhatsApp**
- Esto mantiene todo en una sola App
- Los webhooks de Messenger y WhatsApp son independientes — no se interfieren

**Opción B — App nueva solo para WhatsApp:**
- Crear App nueva de tipo "Business"
- Más limpio pero requiere re-configurar todo desde cero

Recomiendo la Opción A. Menos fricción, mismas credenciales de App (App ID, App Secret).
