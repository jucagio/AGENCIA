# Setup Guide — MAPER.IA en n8n (WhatsApp Business + Gemini)

Guia completa para configurar el workflow de MAPER.IA desde cero.

---

## Prerequisitos

Antes de importar el workflow, asegurate de tener:

- n8n instalado (self-hosted en Railway recomendado)
- Acceso al Meta for Developers Portal con la App de MAPERSA
- WhatsApp Business API configurada con el numero 3107735189
- Proyecto Supabase con el schema de MAPER.IA ya aplicado (ver `supabase-schema.sql`)
- API Key de Google Gemini activa

---

## Paso 1 — Importar el workflow

1. Abre n8n en el navegador
2. En la barra lateral izquierda, haz clic en **Workflows**
3. Haz clic en el boton **Import** (esquina superior derecha) o usa el menu **...** > **Import from file**
4. Selecciona el archivo `workflow-maper-ia.json`
5. El workflow se importa con los 3 grupos de nodos: Verificacion Meta, Mensajes Entrantes y Follow-ups

---

## Paso 2 — Configurar credenciales

Ve a **Settings** > **Credentials** > **Add credential** y crea las siguientes credenciales:

### Credencial 1 — Gemini

- Tipo: **Google Gemini (PaLM) Api**
- Nombre: `Gemini MAPERSA` (debe coincidir exactamente con el nombre en el workflow)
- API Key: tu clave de `aistudio.google.com`

### Credencial 2 — Supabase

- Tipo: **Supabase**
- Nombre: `Supabase MAPERSA`
- Host: `https://lzhfyasnsxdacxkyhqpj.supabase.co`
- Service Role Secret: tu `SUPABASE_SERVICE_ROLE_KEY`

---

## Paso 3 — Configurar variables de entorno en n8n

En Railway (donde esta n8n desplegado), agregar estas variables:

```env
# WhatsApp Business API
WHATSAPP_PHONE_NUMBER_ID=<ID del numero 3107735189 en Meta>
WHATSAPP_BUSINESS_ACCOUNT_ID=<WABA ID>
WHATSAPP_ACCESS_TOKEN=<System User Token permanente>
META_VERIFY_TOKEN=maper_ia_whatsapp_mapersa_2026
META_APP_SECRET=<Secret de la App de Meta>

# Supabase
SUPABASE_URL=https://lzhfyasnsxdacxkyhqpj.supabase.co
SUPABASE_SERVICE_ROLE_KEY=<tu service role key>
```

**Donde agregar en Railway:**
1. Ir al proyecto de n8n en Railway
2. Clic en el servicio > **Variables**
3. Agregar cada variable con su valor

---

## Paso 4 — Obtener credenciales de WhatsApp Business API

### Phone Number ID
1. Ir a developers.facebook.com > tu App > WhatsApp > Configuration
2. En Phone numbers, buscar el numero 3107735189
3. Copiar el Phone Number ID (numero de 15-16 digitos)

### WABA ID (Business Account ID)
1. En la misma pantalla de WhatsApp en Meta for Developers
2. Buscar "WhatsApp Business Account ID"

### System User Access Token (permanente)
1. Ir a business.facebook.com > Settings > System Users
2. Crear system user: `maper-ia-bot`, rol Employee
3. Add Assets > WhatsApp Accounts > Full Control
4. Generate Token con permisos: `whatsapp_business_messaging` + `whatsapp_business_management`
5. Este token NO expira

**Token temporal para prueba inmediata:**
- En Meta for Developers > WhatsApp > Getting Started hay un token temporal de 24h

---

## Paso 5 — Registrar el webhook en Meta

### 5.1 Activar el workflow primero

1. En n8n, abre el workflow MAPER.IA
2. Activa el toggle **Active** (esquina superior derecha)
3. Copia la URL del Webhook — aparece al hacer clic sobre el nodo `Webhook GET — Verificacion Meta`
   - Formato: `https://tu-n8n.railway.app/webhook/maper-ia-whatsapp`

### 5.2 Configurar en Meta for Developers

1. Ve a developers.facebook.com > tu App > **WhatsApp** > **Configuration**
2. En la seccion **Webhook**, clic en **Edit**
3. Completar:
   - **Callback URL**: `https://tu-n8n.railway.app/webhook/maper-ia-whatsapp`
   - **Verify Token**: `maper_ia_whatsapp_mapersa_2026`
4. Clic en **Verify and Save**
5. Meta hace un GET a tu URL — n8n responde con el `hub.challenge` — Meta muestra palomita verde

### 5.3 Suscribir campos del webhook

1. Despues de verificar, en la misma seccion de Webhook
2. Clic en **Manage** junto al campo de suscripciones
3. Marcar: `messages`
4. Guardar

---

## Paso 6 — Verificar las credenciales en los nodos

Despues de importar, algunos nodos mostraran un indicador rojo porque las credenciales no estan asignadas aun:

1. Nodos que requieren `Gemini MAPERSA`:
   - `Google Gemini — gemini-2.0-flash`
   - `Google Gemini — Follow-up Model`

2. Nodos que requieren `Supabase MAPERSA`:
   - `Supabase RPC — get_or_create_contact`
   - `Supabase RPC — get_conversation_history`
   - `Supabase RPC — save_message (usuario)`
   - `Supabase RPC — save_message (asistente)`
   - `Supabase RPC — get_pending_follow_ups`
   - `Supabase RPC — create_escalation`
   - `Supabase RPC — complete_follow_up`

3. Nodos de envio a WhatsApp (HTTP — Enviar respuesta/follow-up):
   - Usan variables de entorno directamente (no credenciales de n8n)
   - Verificar que `WHATSAPP_ACCESS_TOKEN` y `WHATSAPP_PHONE_NUMBER_ID` esten configuradas

---

## Paso 7 — Primer test

### Test de verificacion de webhook (Rama 1)

Este test ocurre automaticamente cuando Meta verifica el webhook en el Paso 5.

Para probarlo manualmente:

```bash
curl "https://tu-n8n.railway.app/webhook/maper-ia-whatsapp?hub.mode=subscribe&hub.verify_token=maper_ia_whatsapp_mapersa_2026&hub.challenge=123456"
```

Debes recibir `123456` como respuesta.

### Test de mensaje entrante (Rama 2)

1. Desde otro numero de WhatsApp, enviar un mensaje al 3107735189
2. En n8n > **Executions**, verificar que aparece una ejecucion nueva
3. Expandir el nodo **Set — Extraer sender_id, message_text, timestamp**
4. Confirmar que `sender_id` = numero de quien escribio (formato 57XXXXXXXXXX), `message_text` = texto enviado
5. El asesor MAPER.IA debe responder en menos de 20 segundos

### Test de escalamiento

1. Desde WhatsApp enviar: "quiero hablar con una persona"
2. En Supabase, verificar en la tabla `escalations` que se creo un registro nuevo

### Test de follow-ups (Rama 3)

1. Insertar un follow-up de prueba en Supabase:
   ```sql
   SELECT public.schedule_follow_up('573107735189', 'cotizacion pendiente', NOW(), 'Seguimiento cotizacion detector Safeline');
   ```
2. En n8n, ejecutar manualmente el nodo `Schedule — Cada 30min Horario Comercial`
3. Verificar que el mensaje se envio y el follow-up se marco como completado

### Si hay error en el envio (status 400/401):
- 401: el `WHATSAPP_ACCESS_TOKEN` no es valido o expiro — generar nuevo token
- 400: revisar el body del nodo de envio — especialmente que `to` tenga formato internacional (57XXXXXXXXXX)

---

## Paso 8 — Activar el workflow en produccion

1. Asegurate de que todos los nodos esten sin errores (sin indicadores rojos)
2. El workflow ya debe estar activo del Paso 5.1
3. Verifica en **Executions** que las ejecuciones de prueba fueron exitosas
4. MAPER.IA esta en produccion

---

## Solucion de problemas comunes

| Problema | Causa probable | Solucion |
|---------|----------------|---------|
| Meta no verifica el webhook | El workflow no esta activo | Activa el workflow antes de registrar el webhook |
| Meta no verifica el webhook | `META_VERIFY_TOKEN` no coincide | Verifica que el token sea `maper_ia_whatsapp_mapersa_2026` |
| El bot no responde | Token de WhatsApp expirado | Si usaste token temporal, generar System User Token permanente |
| Error en nodo Gemini | API Key invalida | Verifica la key en aistudio.google.com |
| Error en nodo Supabase | Funciones RPC no existen | Asegurate de haber ejecutado `supabase-functions.sql` en Supabase |
| Respuesta vacia del bot | Problema de contexto en el Set node | Verifica que `sender_id` y `message_text` se extraen correctamente |
| Follow-ups no se envian | La tabla `follow_ups` esta vacia | Los follow-ups se crean cuando el AI Agent detecta oportunidad de seguimiento |
| Error 400 al enviar WhatsApp | Formato del numero incorrecto | El numero debe ser formato internacional sin +: `573107735189` |
