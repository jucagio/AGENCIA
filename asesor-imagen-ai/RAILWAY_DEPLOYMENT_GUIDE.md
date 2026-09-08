# Railway Deployment Guide — Asesor de Imagen AI
Cinthya — Automatización | 2026-05-22

Guia paso a paso para deployar el backend de Asesor de Imagen AI en Railway.
Tiempo estimado: 15-20 minutos (primera vez), 2 minutos (re-deploys).

---

## Pre-requisitos

Antes de empezar, tener listos:
- [ ] Credenciales de Supabase de Sasha (URL + anon key + service role key)
- [ ] Cuenta en Railway (ver Paso 1)
- [ ] Repositorio en GitHub con el codigo del proyecto (o usar Railway CLI)

---

## Paso 1: Crear cuenta Railway

1. Ir a https://railway.app
2. Click "Login" -> "Login with GitHub"
3. Usar la cuenta GitHub de Juan Camilo (jucagio2595@gmail.com)
4. Confirmar el email si es cuenta nueva
5. Seleccionar plan "Hobby" ($5/mes) — suficiente para el MVP

> Plan Hobby incluye: $5 de credito mensual, proyectos ilimitados, custom domains.
> El backend en idle consume ~$2-3/mes. Redis add-on ~$1/mes adicional.

---

## Paso 2: Crear proyecto Railway

**Opcion A — Desde GitHub (recomendada):**

1. Railway Dashboard -> "New Project"
2. Click "Deploy from GitHub repo"
3. Conectar cuenta GitHub si es la primera vez
4. Seleccionar el repo `AGENCIA` (o el repo donde esta asesor-imagen-ai)
5. Railway detecta el `railway.toml` automaticamente
6. Nombre del proyecto: `asesor-imagen-ai`
7. Click "Deploy Now" (por ahora fallara — falta agregar env vars)

**Opcion B — Sin GitHub (Railway CLI):**

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Desde la carpeta raiz del repo
railway init

# Nombre del proyecto cuando lo pida: asesor-imagen-ai
# Seleccionar "Empty Project"
```

---

## Paso 3: Agregar Redis (add-on de Railway)

Railway tiene Redis como add-on nativo — es la opcion mas simple.

1. Railway Dashboard -> tu proyecto `asesor-imagen-ai`
2. Click "+ New" (boton azul arriba a la derecha)
3. Seleccionar "Database" -> "Add Redis"
4. Railway crea el servicio Redis y agrega `REDIS_URL` automaticamente al entorno

> NO hay que copiar ni pegar la REDIS_URL. Railway la inyecta sola en todos
> los servicios del mismo proyecto.

**Alternativa — Upstash (si prefieres Redis externo):**
1. https://upstash.com -> crear cuenta -> "Create Database"
2. Seleccionar region us-east-1 (menor latencia si Railway esta en us-east)
3. Copiar "Redis URL (TLS)" — formato: `rediss://:password@host:port`
4. Pegarla como `REDIS_URL` en Railway (Paso 4)

---

## Paso 4: Pegar environment variables

1. Railway Dashboard -> proyecto `asesor-imagen-ai` -> servicio backend
2. Tab "Variables"
3. Click "Raw Editor" (pegar todas de una)
4. Copiar el bloque de abajo con los valores reales y pegarlo:

```
ENVIRONMENT=production
SECRET_KEY=<genera con: python -c "import secrets; print(secrets.token_hex(32))">
SUPABASE_URL=https://<tu-proyecto>.supabase.co
SUPABASE_ANON_KEY=<de Sasha — anon key>
SUPABASE_SERVICE_ROLE_KEY=<de Sasha — service role key>
SUPABASE_AVATARS_BUCKET=avatars
SUPABASE_WARDROBE_BUCKET=wardrobe
SUPABASE_TRYONS_BUCKET=tryons
ALLOWED_ORIGINS=https://asesor-imagen-ai-production.up.railway.app
FEATURE_MOCK_WORKERS=false
FEATURE_RATE_LIMIT_ENABLED=true
```

> REDIS_URL NO es necesaria si usas el add-on de Railway (Paso 3).
> Las variables de Fase 2 (REPLICATE_API_TOKEN, ANTHROPIC_API_KEY) se agregan
> cuando lleguen. Ver archivo RAILWAY_ENV_VARS.txt para la lista completa.

5. Click "Update Variables" -> Railway triggerea un nuevo deploy automaticamente

**Donde obtener cada variable:**

| Variable | Fuente |
|----------|--------|
| `SECRET_KEY` | Generar localmente (ver comando arriba) |
| `SUPABASE_URL` | Supabase Dashboard -> Project Settings -> API -> Project URL |
| `SUPABASE_ANON_KEY` | Supabase Dashboard -> Project Settings -> API -> anon/public |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase Dashboard -> Project Settings -> API -> service_role |
| `ALLOWED_ORIGINS` | URL publica de Railway (disponible despues del primer deploy) |
| `REPLICATE_API_TOKEN` | https://replicate.com -> Account -> API Tokens |
| `ANTHROPIC_API_KEY` | https://console.anthropic.com -> API Keys |

---

## Paso 5: Deploy

**Via Railway Dashboard:**
1. Railway auto-deploya cuando cambias variables o haces push a GitHub
2. Dashboard -> proyecto -> pestaña "Deployments" para ver el log en tiempo real
3. El build tarda ~3-5 minutos (descarga imagen Docker, instala deps, compila)

**Via Railway CLI:**
```bash
# Desde la carpeta raiz del repo (donde esta railway.toml)
railway up

# Para ver logs en tiempo real
railway logs
```

**Que hace Railway durante el build:**
1. Lee `railway.toml` -> usa `asesor-imagen-ai/backend/Dockerfile`
2. Build context: `asesor-imagen-ai/backend/`
3. Multi-stage build: builder (instala deps) -> runtime (imagen minimal)
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Health check: `GET /health` cada 30s, timeout 5s

---

## Paso 6: Esperar que el build termine

Senales de build exitoso en el log:
```
✓ Build succeeded
✓ Container started
INFO: Started server process
INFO: Waiting for application startup
INFO: Application startup complete
INFO: Uvicorn running on 0.0.0.0:PORT
```

Senales de error a investigar:
```
# Error de credenciales
AssertionError: SUPABASE_URL is required in production
→ Revisar que SUPABASE_URL este bien escrita en Variables

# Error de Redis
ConnectionError: Error connecting to Redis
→ Verificar que el add-on Redis este en el mismo proyecto
→ O que REDIS_URL de Upstash este bien formateada (rediss://)

# Error de SECRET_KEY
AssertionError: SECRET_KEY must be at least 32 characters
→ Regenerar con: python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Paso 7: Copiar URL publica

1. Railway Dashboard -> proyecto -> servicio backend -> tab "Settings"
2. Seccion "Domains" -> copiar la URL generada
   Formato: `https://asesor-imagen-ai-production.up.railway.app`
3. Si quieres dominio custom: "Custom Domain" -> pega tu dominio -> configura DNS

**Opcional — custom domain:**
```
CNAME asesor-imagen-ai.tudominio.com -> asesor-imagen-ai-production.up.railway.app
```

---

## Paso 8: Actualizar ALLOWED_ORIGINS con la URL real

Ahora que tienes la URL publica, actualiza la variable:

1. Railway Dashboard -> Variables
2. `ALLOWED_ORIGINS` -> editar -> pegar URL real:
   `https://asesor-imagen-ai-production.up.railway.app`
3. Si tambien usas el APK Flutter (no web), esta variable puede ser `*` temporalmente
   durante desarrollo — pero NUNCA en produccion final.
4. Railway auto-redeploya con la nueva variable

---

## Paso 9: Actualizar Flutter .env.production.json

Brook necesita esta URL para compilar el APK de produccion.

Archivo: `asesor-imagen-ai/frontend/.env.production.json`

```json
{
  "API_BASE_URL": "https://asesor-imagen-ai-production.up.railway.app",
  "API_VERSION": "v1",
  "ENVIRONMENT": "production"
}
```

Luego Brook recompila el APK:
```bash
cd asesor-imagen-ai/frontend
flutter build apk --release --dart-define-from-file=.env.production.json
```

---

## Paso 10: Verificar health check

Confirmar que el backend esta vivo:

```bash
# Liveness probe (siempre 200 si el proceso corre)
curl https://asesor-imagen-ai-production.up.railway.app/health

# Respuesta esperada:
{
  "success": true,
  "data": {
    "status": "ok",
    "service": "Asesor de Imagen AI",
    "version": "0.1.0",
    "environment": "production",
    "timestamp": "2026-05-22T..."
  }
}

# Readiness probe (verifica Redis + Supabase + ARQ)
curl https://asesor-imagen-ai-production.up.railway.app/ready

# Respuesta esperada (todos en "ok"):
{
  "success": true,
  "data": {
    "db": "ok",
    "redis": "ok",
    "queue": "ok",
    "timestamp": "2026-05-22T..."
  }
}
```

Si `/ready` retorna `503`, alguna dependencia no esta conectada. Ver logs de Railway.

---

## Estado: LISTO para Fase 2

Con el deploy verificado, el backend esta listo para recibir las API keys de Fase 2:

1. Abrir Railway Dashboard -> Variables
2. Agregar:
   ```
   REPLICATE_API_TOKEN=r8_xxxx
   ANTHROPIC_API_KEY=sk-ant-xxxx
   ```
3. Cambiar: `FEATURE_MOCK_WORKERS=false` (ya esta en false)
4. Railway redeploya automaticamente (~2 min)
5. Verificar `/ready` nuevamente

Reportar a Jarvis: Backend LIVE en `https://...up.railway.app` — READY para Fase 2.

---

## Re-deploys futuros

Cada push a la rama conectada triggerea un deploy automatico.
Para deploy manual desde CLI:
```bash
railway up
```

Para ver logs:
```bash
railway logs --tail 100
```

Para rollback a deploy anterior:
Railway Dashboard -> Deployments -> click en deploy anterior -> "Rollback"

---

## Arquitectura final en Railway

```
Railway Project: asesor-imagen-ai
├── Service: backend
│     Dockerfile: asesor-imagen-ai/backend/Dockerfile
│     startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
│     healthcheckPath: /health
│     healthcheckTimeout: 30s
│     restartPolicy: on_failure (max 3 retries)
│
└── Service: Redis (add-on)
      Railway lo gestiona automaticamente
      REDIS_URL inyectada automaticamente
```

---

Preparado por Cinthya | Fase 3 Deploy | asesor-imagen-ai
