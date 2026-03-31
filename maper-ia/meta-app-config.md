# Meta App Config — Checklist de Configuracion para MAPER.IA

Checklist completo para configurar la App de Meta que conecta la pagina de MAPERSA con n8n.

---

## Prerequisitos

- [ ] Cuenta de desarrollador en [developers.facebook.com](https://developers.facebook.com)
- [ ] Pagina de Facebook de MAPERSA (con rol de Administrador)
- [ ] App de Meta creada de tipo "Business" o en modo produccion

---

## 1 — Crear o configurar la App en Meta for Developers

- [ ] Ingresar a [developers.facebook.com/apps](https://developers.facebook.com/apps)
- [ ] Seleccionar la App existente de MAPERSA (o crear una nueva de tipo **Business**)
- [ ] En la App, ir a **Add Products** y agregar **Messenger**
- [ ] En **Messenger > Settings** (o Configuration), vincular la pagina de Facebook de MAPERSA

---

## 2 — Permisos requeridos

La App necesita los siguientes permisos para operar MAPER.IA. Estos se solicitan en **App Review** para modo produccion o se activan automaticamente en modo desarrollo para la cuenta del administrador.

| Permiso | Para que se usa | Modo desarrollo | Modo produccion |
|---------|----------------|-----------------|-----------------|
| `pages_messaging` | Enviar y recibir mensajes de Messenger | Disponible sin review | Requiere App Review |
| `pages_read_engagement` | Leer mensajes recibidos por la pagina | Disponible sin review | Requiere App Review |
| `pages_manage_metadata` | Gestionar la suscripcion al webhook | Disponible sin review | Requiere App Review |

### Verificar permisos activos

1. En Meta for Developers > App > **App Review** > **Permissions and Features**
2. Confirmar que los 3 permisos esten en estado "Approved" (produccion) o activos (desarrollo)

---

## 3 — Configurar el Verify Token

El Verify Token es un string secreto que tu defines. Meta lo enviara en el GET de verificacion del webhook para confirmar que el endpoint es tuyo.

- [ ] Definir el Verify Token: un string aleatorio y unico (ej. `maper_ia_verify_mapersa_2026`)
- [ ] Guardarlo como variable de entorno `META_VERIFY_TOKEN` en n8n
- [ ] Tener el valor a mano para el paso de registro del webhook

**Recomendacion de formato:** minimo 20 caracteres, sin espacios, puede tener guiones o guiones bajos.

---

## 4 — Registrar el webhook

### 4.1 Obtener la URL del webhook de n8n

1. Abrir el workflow MAPER.IA en n8n
2. Activar el workflow (toggle **Active**)
3. Hacer clic en el nodo **Webhook GET — Verificacion Meta**
4. Copiar la **Production URL** (no la Test URL)
   - Formato esperado: `https://tu-n8n.dominio.com/webhook/maper-ia-messenger`

### 4.2 Registrar en Meta

1. Ir a Meta for Developers > App > **Messenger** > **Settings**
2. En la seccion **Webhooks**, hacer clic en **Add Callback URL**
3. Completar:
   - **Callback URL**: la URL del webhook de n8n
   - **Verify Token**: el valor de `META_VERIFY_TOKEN`
4. Hacer clic en **Verify and Save**
5. Meta envia un GET al webhook — n8n debe responder con el `hub.challenge`
6. Si la verificacion es exitosa, Meta muestra "Webhook verified" con tilde verde

### 4.3 Suscribir campos del webhook

Despues de verificar el webhook, suscribir la pagina de MAPERSA a los campos necesarios:

- [ ] En la misma seccion de Webhooks, hacer clic en **Add Subscriptions** junto a la pagina de MAPERSA
- [ ] Marcar el campo `messages` — mensajes de texto entrantes
- [ ] Marcar el campo `messaging_postbacks` — respuestas a botones (recomendado)
- [ ] Hacer clic en **Save** o **Update**

---

## 5 — Test de eco inicial

Antes de probar con el AI Agent, hacer un test simple para confirmar que el webhook recibe mensajes.

### 5.1 Test manual desde Messenger

1. Abrir Facebook Messenger en cualquier dispositivo
2. Buscar la pagina de MAPERSA
3. Enviar el mensaje: `test`
4. En n8n > **Executions**, verificar que aparece una ejecucion nueva
5. Dentro de la ejecucion, expandir el nodo **Set — Extraer sender_id, message_text, timestamp**
6. Confirmar que `sender_id` y `message_text` tienen valores correctos

### 5.2 Payload esperado de Meta

El payload que Meta envia al webhook POST tiene esta estructura:

```json
{
  "object": "page",
  "entry": [
    {
      "id": "PAGE_ID",
      "time": 1234567890,
      "messaging": [
        {
          "sender": {
            "id": "SENDER_PSID"
          },
          "recipient": {
            "id": "PAGE_ID"
          },
          "timestamp": 1234567890,
          "message": {
            "mid": "MESSAGE_ID",
            "text": "Hola, buenas tardes"
          }
        }
      ]
    }
  ]
}
```

Los nodos del workflow extraen:
- `sender_id` = `entry[0].messaging[0].sender.id`
- `message_text` = `entry[0].messaging[0].message.text`
- `timestamp` = `entry[0].messaging[0].timestamp`

### 5.3 Eventos que NO son mensajes (se filtran automaticamente)

Meta tambien envia eventos de delivery y read. El nodo **IF — message_text existe** los filtra porque no tienen el campo `message.text`:

```json
{
  "delivery": { "watermark": 1234567890 }
}
```
```json
{
  "read": { "watermark": 1234567890 }
}
```

Estos eventos llegan por el mismo webhook pero el workflow los descarta en el IF sin procesarlos.

---

## 6 — Pasar la App a modo produccion (cuando MAPERSA este lista)

En modo desarrollo, solo los usuarios con rol en la App pueden chatear con el bot. Para que cualquier usuario de Facebook pueda escribirle a la pagina, la App debe estar en produccion.

- [ ] Ir a **App Review** en Meta for Developers
- [ ] Solicitar los 3 permisos listados en la seccion 2
- [ ] Completar el formulario de revision con casos de uso de MAPER.IA
- [ ] Adjuntar capturas de pantalla del flujo completo (mensaje → respuesta del asesor)
- [ ] Esperar aprobacion de Meta (tipicamente 1-5 dias habiles)
- [ ] Una vez aprobado, cambiar el switch de **Development** a **Live** en la App

---

## 7 — Buenas practicas de seguridad

### Verificacion de firma (recomendado para produccion)

Meta incluye el header `X-Hub-Signature-256` en cada POST para que puedas verificar que el mensaje viene realmente de Meta (no de un tercero que descubrio tu URL).

Para implementarlo en n8n, agrega un nodo Code al inicio de la Rama 2:

```javascript
const crypto = require('crypto');
const payload = JSON.stringify($input.item.json.body);
const signature = $input.item.json.headers['x-hub-signature-256'];
const expected = 'sha256=' + crypto.createHmac('sha256', $env.META_APP_SECRET).update(payload).digest('hex');

if (signature !== expected) {
  throw new Error('Firma invalida — posible solicitud maliciosa');
}

return $input.item;
```

### Rotation del Page Access Token

- El Page Access Token de larga duracion (60 dias) debe renovarse antes de que expire
- Configura un recordatorio cada 45 dias para renovarlo via el template n8n #14027
- Si el token expira, MAPER.IA deja de responder — es el primer lugar a revisar ante una falla total

### Limite de mensajes de Meta

Meta limita el envio de mensajes proactivos (fuera de la ventana de 24 horas de la ultima interaccion del usuario). Los follow-ups usan el tag `POST_PURCHASE_UPDATE` que permite cierto uso fuera de ventana, pero siempre dentro de los terminos de uso de Meta para mensajeria comercial.

---

## Checklist final antes de go-live

- [ ] Workflow activo en n8n
- [ ] URL del webhook verificada por Meta
- [ ] Campos `messages` y `messaging_postbacks` suscritos
- [ ] `META_PAGE_ACCESS_TOKEN` de larga duracion configurado
- [ ] Variables de entorno correctas en n8n
- [ ] Funciones RPC de Supabase aplicadas
- [ ] Test de eco exitoso (mensaje llega → n8n lo procesa)
- [ ] Test de respuesta completo (mensaje → IA → respuesta en Messenger)
- [ ] App en modo Live (o en desarrollo para pruebas internas)
