# Día 1 — Deploy n8n en Railway: Guía Paso a Paso

Ejecuta esta guía en orden. Al final del día tendrás n8n funcionando con todas las credenciales listas para importar el workflow mañana.

---

## Checklist de entregables

- [ ] n8n deployado y accesible en URL pública
- [ ] Usuario admin creado
- [ ] `ANTHROPIC_API_KEY` configurada en Railway
- [ ] Variables de entorno de n8n configuradas
- [ ] URL y credenciales documentadas al final de esta guía

> Nota: Las credenciales de Gemini NO son necesarias para MAPER.IA. El workflow usa exclusivamente Claude (Anthropic). No pierdas tiempo configurando Google Cloud hoy.

---

## Paso 1 — Crear cuenta en Railway

1. Ve a [railway.app](https://railway.app)
2. Crea una cuenta (recomendado: con GitHub para facilitar integraciones futuras)
3. Verifica tu email si Railway lo pide
4. El plan gratuito incluye $5 USD de crédito mensual — suficiente para pruebas. Para producción, activa el plan **Hobby** ($5/mes) que da $10 de uso real

---

## Paso 2 — Crear el proyecto n8n

### 2.1 Nuevo proyecto

1. En el dashboard de Railway, haz clic en **"New Project"**
2. Selecciona **"Empty project"**
3. Dale un nombre descriptivo: `maper-ia-n8n`

### 2.2 Agregar el servicio n8n desde imagen Docker

1. Dentro del proyecto, haz clic en **"Add a Service"**
2. Selecciona **"Docker Image"**
3. En el campo de imagen, escribe exactamente:
   ```
   n8nio/n8n
   ```
4. Presiona Enter y haz clic en **Deploy**
5. Railway descargará la imagen oficial de n8n y desplegará el contenedor

> La imagen `n8nio/n8n` es la imagen oficial de n8n en Docker Hub. Siempre instala la versión más reciente estable.

---

## Paso 3 — Configurar variables de entorno en Railway

Antes de que n8n arranque correctamente, necesita estas variables. Ve a tu servicio n8n en Railway > pestaña **"Variables"** > agrega cada una:

### Variables obligatorias de n8n

| Variable | Valor | Para qué sirve |
|----------|-------|----------------|
| `N8N_BASIC_AUTH_ACTIVE` | `true` | Activa protección con usuario y contraseña |
| `N8N_BASIC_AUTH_USER` | `admin` (o el nombre que quieras) | Usuario de acceso a n8n |
| `N8N_BASIC_AUTH_PASSWORD` | Elige una contraseña segura | Contraseña del usuario admin |
| `N8N_ENCRYPTION_KEY` | Genera un string aleatorio de 32+ caracteres | Cifra las credenciales guardadas en n8n |
| `WEBHOOK_URL` | Se completa en el Paso 4, después de generar el dominio | URL base para los webhooks de n8n |
| `NODE_ENV` | `production` | Modo producción |
| `N8N_HOST` | Se completa en el Paso 4 | Hostname del deploy |
| `N8N_PORT` | `5678` | Puerto estándar de n8n |
| `N8N_PROTOCOL` | `https` | Protocolo |

### Variable de Anthropic (para el workflow de MAPER.IA)

| Variable | Valor | Para qué sirve |
|----------|-------|----------------|
| `ANTHROPIC_API_KEY` | Tu API Key de Anthropic | Permite que n8n llame a Claude |

### Cómo generar N8N_ENCRYPTION_KEY

Usa cualquiera de estas opciones:

**Opción A — Online:** Ve a [randomkeygen.com](https://randomkeygen.com) y copia cualquier clave de la sección "256-bit WEP Keys"

**Opción B — Terminal (si tienes Node.js):**
```bash
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

**Opción C — Manual:** Inventa un string largo de letras y números, mínimo 32 caracteres. Ejemplo: `maper2026railway_n8n_key_XY9Z2K`

> IMPORTANTE: Guarda esta clave en un lugar seguro. Si la pierdes y tienes credenciales guardadas en n8n, no podrás descifrarlas.

---

## Paso 4 — Generar el dominio público

1. En tu servicio n8n en Railway, ve a la pestaña **"Settings"**
2. En la sección **"Networking"**, haz clic en **"Generate Domain"**
3. Railway te dará una URL del tipo:
   ```
   maper-ia-n8n-production.up.railway.app
   ```
4. Copia esa URL

### Actualizar variables con el dominio real

Ahora vuelve a la pestaña **"Variables"** y actualiza:

| Variable | Valor con tu dominio real |
|----------|--------------------------|
| `WEBHOOK_URL` | `https://maper-ia-n8n-production.up.railway.app/` |
| `N8N_HOST` | `maper-ia-n8n-production.up.railway.app` |

> Reemplaza `maper-ia-n8n-production.up.railway.app` con tu URL real de Railway.

5. Después de agregar las variables, Railway redesplegará automáticamente el servicio

---

## Paso 5 — Verificar que n8n está funcionando

1. Ve a la URL que generaste: `https://tu-dominio.up.railway.app`
2. Debe aparecer la pantalla de login de n8n
3. Ingresa con el usuario y contraseña que configuraste en `N8N_BASIC_AUTH_USER` y `N8N_BASIC_AUTH_PASSWORD`
4. Si accedes al dashboard de n8n, el deploy fue exitoso

### Si n8n no carga

- Ve a Railway > tu servicio > pestaña **"Logs"** para ver los errores
- El error más común en este punto es `N8N_ENCRYPTION_KEY` no configurada o con espacios — Railway a veces agrega espacios al pegar valores

---

## Paso 6 — Obtener tu API Key de Anthropic

1. Ve a [console.anthropic.com](https://console.anthropic.com)
2. Inicia sesión con tu cuenta
3. En el menú lateral, haz clic en **"API Keys"**
4. Haz clic en **"Create Key"**
5. Dale un nombre: `MAPERSA-n8n`
6. Copia la clave — empieza con `sk-ant-`
7. Pégala como valor de `ANTHROPIC_API_KEY` en Railway (si no la pusiste antes, agrégala ahora)

> La API Key solo se muestra una vez al crearla. Guárdala en lugar seguro antes de cerrar la pantalla.

---

## Paso 7 — Documentar credenciales

Llena esta tabla con tus datos reales y guárdala en lugar seguro (NO en el repositorio de GitHub):

```
=== CREDENCIALES MAPER.IA — DÍA 1 ===

URL de n8n:         https://_____________________________.up.railway.app
Usuario n8n:        _____________________________
Password n8n:       _____________________________
N8N_ENCRYPTION_KEY: _____________________________

ANTHROPIC_API_KEY:  sk-ant-_____________________________

Fecha de setup:     _____ / _____ / 2026
```

---

## Qué viene mañana (Día 2)

Con n8n funcionando, el Día 2 se hace:

1. Crear las 3 credenciales en n8n (Anthropic, Supabase, Supabase Postgres)
2. Importar `workflow-maper-ia.json`
3. Configurar las variables de entorno del workflow (META_PAGE_ACCESS_TOKEN, META_VERIFY_TOKEN, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
4. Primer test de verificación del webhook

---

## Soporte

Si encuentras un error específico en algún paso, comparte:
- El paso donde falló
- El mensaje de error exacto (de los Logs de Railway o de n8n)

Cinthya lo diagnostica y entrega solución inmediata.

---

## Entrega Cinthya — Deploy n8n Railway MAPER.IA

**Descripción:** Guía operativa para deployar n8n self-hosted en Railway como infraestructura del workflow MAPER.IA

**Trigger:** Manual — Juan Camilo ejecuta el día 1 del setup

**Herramienta:** Railway (Docker) + n8n

**Dependencias:**
- Cuenta en railway.app
- API Key de Anthropic (console.anthropic.com)
- Crédito en Railway (plan Hobby recomendado para producción)

**Métricas de éxito:**
- URL pública de n8n accesible y con login funcional
- `ANTHROPIC_API_KEY` configurada en las variables de Railway
- `N8N_ENCRYPTION_KEY` configurada (requerida para guardar credenciales en Día 2)
