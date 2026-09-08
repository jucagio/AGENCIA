# Setup Credenciales Supabase — Asesor de Imagen AI

## ⚠️ Estado Actual
El backend está **funcionando**, pero los endpoints de auth/wardrobe/try-on devuelven **500** porque `.env` tiene SUPABASE_URL vacío.

**Solución:** 3 credenciales de Supabase en `.env` — toma ~5 min.

---

## Paso 1: Obtener Credenciales Supabase

### Si YA tienes un proyecto Supabase:
1. Ve a https://app.supabase.com/projects
2. Selecciona tu proyecto
3. Click "Settings" (esquina inferior izquierda)
4. Click "API" en el sidebar izquierdo
5. Copia estos 3 valores:
   - **Project URL** → `SUPABASE_URL`
   - **anon key (public)** → `SUPABASE_ANON_KEY`
   - **service_role key (secret)** → `SUPABASE_SERVICE_ROLE_KEY`

### Si NO tienes Supabase aún:
1. Ve a https://supabase.com/dashboard
2. Click "New project"
3. **Name:** `asesor-imagen-ai-dev`
4. **Password:** crea una segura (20+ chars, mix de mayús/números/símbolos)
5. **Region:** `us-east-1` (o la más cercana a ti)
6. Espera ~2 min a que se cree el proyecto
7. Sigue los pasos de arriba para copiar las 3 credenciales

---

## Paso 2: Pegar Credenciales en `.env`

**Archivo:** `C:\Users\PCC\Documents\JUAN CAMILO GIL\PERSONAL\PROGRAMACIÓN\AGENCIA\asesor-imagen-ai\backend\.env`

Abre el archivo con VS Code o Notepad. Busca estas líneas (aproximadamente línea 15-17):

```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=xxxxx
SUPABASE_SERVICE_ROLE_KEY=xxxxx
```

Reemplaza los `xxxxx` con tus 3 valores de Supabase. **Ejemplo:**

```env
SUPABASE_URL=https://abcdefghijkl.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Guarda el archivo** (Ctrl+S).

---

## Paso 3: Reiniciar Backend

Si el backend está corriendo, ciérralo (Ctrl+C en la terminal PowerShell).

Reinicia con:
```powershell
cd "C:\Users\PCC\Documents\JUAN CAMILO GIL\PERSONAL\PROGRAMACIÓN\AGENCIA\asesor-imagen-ai\backend"
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

**Espera a ver:**
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## Paso 4: Verificar que Funciona

Abre en navegador: `http://127.0.0.1:8000/docs`

Scrollea hasta **POST /api/v1/auth/register** y expándelo.

Click "Try it out", rellena:
```json
{
  "email": "test@example.com",
  "password": "Test@12345",
  "full_name": "Test User"
}
```

Click "Execute".

**Esperado:**
- Status: **200** (antes era 500)
- Response body: `{"success": true, "data": {"user": {...}, "session": {...}}}`

Si devuelve 200, ✅ **credenciales funcionan**.

---

## Paso 5 (Opcional): Crear las tablas en Supabase

Si quieres que wardrobe/try-on funcionen, necesitas aplicar las migraciones SQL al proyecto Supabase. Eso es más complejo y requiere:

1. Copiar el contenido de `backend/migrations/` 
2. Pegarlas una por una en la SQL Editor de Supabase
3. Ejecutar cada una

Si quieres que yo (Sasha) haga esto automáticamente, dile a Jarvis y lo aplico por ti.

---

## Troubleshooting

| Problema | Solución |
|----------|----------|
| "Invalid API key" | Verificaste que copiaste **service_role_KEY** (no anon key) para SERVICE_ROLE_KEY? |
| "Connection refused" | ¿Copiaste la URL **completa** con `https://`? |
| Register devuelve 403 | Supabase tiene RLS (Row Level Security) activado — normal en dev. Las políticas las aplica Sasha luego. |
| Backend arranca pero `/health` devuelve 503 | Supabase está down. Espera unos segundos y recarga. |

---

## Archivos relacionados
- `.env` — credenciales (NO commits a Git)
- `backend/app/services/auth_service.py` — usa SUPABASE_URL aquí
- `backend/.env.example` — template de variables
