# SPRINT 0.5 PROMPT — Worker Integration & Real API Calls
## Para: Antigravity
## Owner: Jarvis (CEO)
## Duración estimada: 1 semana (paralelo a Sprint 0.4 DevOps)
## Status: 🟡 LISTO PARA INICIAR (tras aprobación Juan Camilo design system)

---

## 0. CONTEXTO — Por qué este sprint existe

En Sprint 0.3, creaste los **stubs** de los tres workers (ARQ):
- `vision_worker.py` — comentario: `# await google_vision_api.analyze(image_url)`
- `replicate_worker.py` — comentario: `# replicate.run(...)`
- `claude_worker.py` — comentario: `# anthropic.messages.create(...)`

Los endpoints devuelven **202 Accepted** (async-first, ADR-002), pero **nadie procesa realmente los jobs**.

**Sprint 0.5 = activar los workers reales** para que la app funcione end-to-end cuando Erik y Brook entreguen las pantallas.

---

## 1. SCOPE CONFIRMADO — 3 tareas principales

### T1 — Vision Worker: Análisis corporal (Body Analysis)
```
Cuando: POST /api/v1/body-analysis {image_url}
  → enqueue_job("vision_analyze_body", payload)
  
Implementación (reemplaza stub):
  • Descargar imagen desde image_url (HTTPS validada, AnyHttpUrl)
  • Llamar a Google Vision API
    - VISION_LABELS: obtener etiquetas (body type keywords)
    - FACE_DETECTION: skin tone analysis
  • LLM post-processing con Claude API:
    Input: labels + face colors → Output: body_type, skin_tone_category, color_season
  • Guardar en DB: UPDATE body_analysis SET (body_type, skin_tone_category, color_season, status='completed')
  • Enviar webhook a cliente (opcional): WebSocket o polling GET /api/v1/body-analysis/{id}

Tokens Vision API: {GOOGLE_CLOUD_VISION_API_KEY}
Modelos Claude: anthropic==0.40.0 (ya en requirements)

Archivos a modificar:
  - app/workers/vision_worker.py
  - app/services/body_analysis_service.py (añadir métodos de post-process)
  - tests/test_workers.py (reemplazar stubs con tests reales)
```

### T2 — Replicate Worker: Virtual Try-On (Generación de outfit)
```
Cuando: POST /api/v1/try-ons {wardrobe_item_id, body_analysis_id, user_photo_url, content_hash}
  → enqueue_job("process_try_on", payload)
  
Implementación:
  • Descargar body_analysis (figura de usuario)
  • Descargar wardrobe_item (prendas seleccionadas)
  • Llamar a Replicate API con modelo de virtual try-on
    - Model: replicate/replicate/tryon (o similar disponible 2026)
    - Input: {person_image, garment_images, ...}
  • Guardar imagen generada en Supabase Storage (`/try-ons/{user_id}/{id}.jpg`)
    - Retornar signed URL válida por 24h
  • Generar AI insight (Claude: "por qué funciona este outfit")
  • UPDATE try_on SET (image_url, status='completed', ai_insight)
  • Webhook a cliente

Tokens Replicate: {REPLICATE_API_TOKEN}

Archivos a modificar:
  - app/workers/replicate_worker.py
  - app/services/try_on_service.py (añadir métodos de post-processing, signed URLs)
  - tests/test_workers.py
```

### T3 — Claude Worker: Recomendaciones de outfit (AI Recommendations)
```
Cuando: POST /api/v1/recommendations {user_id, occasion, season}
  → enqueue_job("generate_reco_claude", payload)
  
Implementación:
  • Obtener:
    - body_analysis del usuario (body_type, color_season)
    - wardrobe_items del usuario (filtrados por season/occasion)
    - histórico de recommendations (para aprender preferencias)
  • Llamar a Claude Opus con prompt:
    Prompt template:
    """
    Eres un asesor de estilo IA. Basándote en:
    - Tipo de cuerpo: {body_type}
    - Temporada de color: {color_season}
    - Ocasión: {occasion}
    - Prendas disponibles: {wardrobe_items_json}
    
    Genera 3 combinaciones de outfits (top, bottom, shoes) 
    que maximicen armonía visual y comodidad.
    
    Devuelve JSON:
    {
      "outfits": [
        {
          "items": [wardrobe_item_ids],
          "why": "explicación breve por qué funciona",
          "confidence": 0.95
        }
      ]
    }
    """
  • Parsear response JSON
  • INSERT recomendations records (1 per outfit)
  • UPDATE recomendation SET status='completed'
  • Webhook a cliente

Tokens Claude: anthropic==0.40.0

Archivos a modificar:
  - app/workers/claude_worker.py
  - app/services/recommendation_service.py
  - tests/test_workers.py
```

---

## 2. ALINEACIÓN CON DESIGN SYSTEM APROBADO

Las respuestas del backend DEBEN matchear exactamente lo que Erik y Brook esperan:

### Body Analysis Response (cuando status='completed')
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "status": "completed",
  "body_type": "hourglass",  // enum: pear, apple, hourglass, rectangle, inverted_triangle
  "skin_tone_category": "warm",  // enum: warm, cool, neutral
  "color_season": "autumn",  // enum: spring, summer, autumn, winter
  "best_colors": ["#8B4513", "#D2B48C", "#FF6347", ...],  // 5-7 colores recomendados
  "avoid_colors": ["#00CED1", "#9370DB", ...],  // 3-5 colores a evitar
  "face_shape": "oval",  // opcional
  "measurements": {  // opcional (si Vision lo detecta)
    "estimated_height": "tall",
    "proportions": "balanced"
  },
  "created_at": "2026-05-18T10:30:00Z",
  "updated_at": "2026-05-18T11:45:00Z"
}
```

### Try-On Response (cuando status='completed')
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "wardrobe_item_ids": ["id1", "id2"],
  "status": "completed",
  "image_url": "https://storage.supabase.co/try-ons/{user_id}/{id}.jpg?token=...",  // signed URL 24h
  "cache_hit": false,
  "ai_insight": {
    "why_it_works": "Este conjunto logra un equilibrio perfecto entre lo casual y lo refinado...",
    "style_notes": ["Contraste cromático", "Silueta moderna"],
    "occasion_fit": "business_casual"
  },
  "created_at": "2026-05-18T10:30:00Z",
  "updated_at": "2026-05-18T11:45:00Z"
}
```

### Recommendation Response (cuando status='completed')
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "status": "completed",
  "occasion": "casual friday",
  "season": "autumn",
  "items": [
    {
      "wardrobe_item_id": "id1",
      "position": 1,
      "role": "top",  // enum: top, bottom, shoes, accessory
      "reason": "Color harmonious with your autumn palette"
    },
    {
      "wardrobe_item_id": "id2",
      "position": 2,
      "role": "bottom"
    }
  ],
  "ai_insight": "Esta recomendación enfatiza...",
  "created_at": "2026-05-18T10:30:00Z"
}
```

---

## 3. REQUISITOS NO-NEGOCIABLES

### 3.1 SSRF Prevention (Cyber Neo A08-HIGH1)
```python
# En vision_worker.py:
from pydantic import AnyHttpUrl

# Validar ANTES de descargar
image_url = AnyHttpUrl(payload["image_url"])  # raises si no es http/https
allowed_domains = ["supabase.co", "storage.googleapis.com", "replicate.com"]
if not any(domain in str(image_url) for domain in allowed_domains):
    raise ValueError(f"Image URL from untrusted domain: {image_url}")
```

### 3.2 Error Handling (Cyber Neo A04-MED1, A09-MED1)
```python
# Cuando un worker falla:
# ✅ CORRECTO:
try:
    result = google_vision.analyze(image)
    db.update_status("completed", result)
except Exception as e:
    logger.error(f"Vision worker failed: {e}")
    db.update_status("failed")  # Allow retry
    # NO swallow the error — let ARQ retry or alert

# ❌ INCORRECTO:
try:
    result = google_vision.analyze(image)
except:
    db.update_status("completed", {})  # Silent failure = data loss
    return
```

### 3.3 Rate Limiting (Cyber Neo A04-HIGH1 — Sprint 0.4 pero afecta workers)
```python
# En config.py, los workers RESPETAN:
# - Vision API: 1 request/second (Google free tier limit)
# - Replicate: queue based, auto-retry on 429
# - Claude: 50 req/min (Anthropic free tier), batch cuando sea posible

# Implementa backoff exponencial:
import time
retry_count = 0
while retry_count < 3:
    try:
        result = replicate.run(...)
        break
    except RateLimitError:
        retry_count += 1
        sleep_time = 2 ** retry_count
        logger.warning(f"Rate limited, retrying in {sleep_time}s")
        time.sleep(sleep_time)
```

### 3.4 Testing (Coverage ≥85% de workers)
```
Cada worker DEBE tener tests:
  ✅ test_vision_worker_valid_image()
  ✅ test_vision_worker_invalid_url_raises()
  ✅ test_vision_worker_timeout()
  ✅ test_replicate_worker_generates_image()
  ✅ test_replicate_worker_invalid_payload()
  ✅ test_claude_worker_generates_recommendations()
  ✅ test_claude_worker_respects_user_preferences()
```

---

## 4. ARCHIVOS A MODIFICAR — checklist específica

### Modificar (reemplazar stubs):
- [ ] `app/workers/vision_worker.py` — stub → real Google Vision + Claude
- [ ] `app/workers/replicate_worker.py` — stub → real Replicate API
- [ ] `app/workers/claude_worker.py` — stub → real Claude Opus
- [ ] `app/services/body_analysis_service.py` — añadir métodos helper para Vision response
- [ ] `app/services/try_on_service.py` — añadir image storage + signed URL logic
- [ ] `app/services/recommendation_service.py` — JSON parsing + filtering

### Tests (nuevos o reemplazar):
- [ ] `tests/test_workers.py` — reemplazar por tests reales (mock Vision, Replicate, Claude)
- [ ] `tests/test_vision_worker_integration.py` (opcional — test real si credenciales disponibles)

### Config (valores por defecto):
- [ ] `app/config.py` — añadir si faltan:
  - `GOOGLE_CLOUD_VISION_API_KEY`
  - `REPLICATE_API_TOKEN`
  - `VISION_BATCH_SIZE` (default 5)
  - `REPLICATE_MODEL_VERSION` (default: latest TryOn model)

### Documentación:
- [ ] `docs/WORKERS_IMPLEMENTATION.md` (NUEVO) — detalles de integración, credenciales, debugging

---

## 5. DECISION TREE — cuando algo es ambiguo

| Caso | Decisión |
|------|----------|
| Vision API falla en análisis de body_type | Devolver status="failed", intentar retry en 5 min |
| Imagen descargada es <100px | Rechazar antes de Vision (validación cliente + server) |
| Replicate timeout después de 45s | Fallback: usar imagen de entrada + placeholder (no fail) |
| Claude rechaza generar recommendations | Log + retry con prompt simplificado |
| ¿Debo cachear respuestas Vision? | SÍ — guardar body_analysis, reutilizar si user sube misma foto (SHA256) |
| ¿Debo hacer batch jobs en Replicate? | NO en Sprint 0.5 — uno a uno es OK. Sprint 0.6 optimiza |

---

## 6. DEFINICIÓN DE DONE (DoD)

✅ **Sprint 0.5 completado cuando:**

- [ ] Todos 3 workers tienen código real (no stubs)
- [ ] Respuestas JSON matchean exactamente los schemas de Boot
- [ ] Coverage de tests ≥85% (incluye test_workers.py)
- [ ] Ruff: all checks passed
- [ ] Funciona end-to-end: POST /try-ons → 202 → polling GET /try-ons/{id} → 200 con resultado
- [ ] Errores loggean correctamente (no silent failures)
- [ ] Documentación: `docs/WORKERS_IMPLEMENTATION.md` con guía setup credenciales + debugging
- [ ] Credentials en .env (nunca en código)
- [ ] 1 integration test manual ejecutado (si credenciales de prueba disponibles)

**Definition of Ready (DeR):**
- [ ] Credenciales Google Vision API → Juan Camilo entrega clave
- [ ] Credenciales Replicate → Juan Camilo entrega token
- [ ] Anthropic API key → ya en config, disponible
- [ ] Supabase Storage bucket creado (`/try-ons/`) → Jarvis prepara

---

## 7. DECISIONES DE DISEÑO YA TOMADAS (NO cambiar)

| Decisión | Por qué | Validez |
|----------|---------|---------|
| Workers son **async-first** (202 Accepted) | Mobile app expects instant response, real work en background | ✅ Vinculante |
| Respuestas Vision → Claude → JSON | Vision labels + face colors → LLM interpreta en contexto color season | ✅ Vinculante |
| SHA256 try-on caching (ADR-004) | Evita reprocesar misma foto + outfit | ✅ Implementado (T2) |
| Signed URLs Supabase 24h válidas | Seguridad + evita leaks permanentes de generaciones | ✅ Vinculante |
| Todos los workers usan ARQ + Redis | Escalable, permite retry automático, compatible con Kubernetes | ✅ Vinculante |

---

## 8. TIMELINE & BLOCKERS

**Ideal sequence:**
```
Día 1-2: T1 (Vision worker) + tests
Día 3-4: T2 (Replicate worker) + tests + Supabase Storage signed URLs
Día 5-6: T3 (Claude worker) + integration test end-to-end
Día 7: DoD verification + docs + buffer
```

**Blocker = Sprint no puede ser "done" sin:**
- [ ] Credenciales Google Cloud Vision API (Juan Camilo debe compartir)
- [ ] Credenciales Replicate API (Juan Camilo debe compartir)
- [ ] Supabase Storage bucket `/try-ons/` creado

**si alguno falta:** usar mocks en tests, implementar real cuando credenciales lleguen.

---

## 9. REFERENCIA — qué ya está hecho (reutilizar)

Estos archivos ya existen y funcionan — úsalos como base:

```python
# Repositorio pattern ya existe:
from app.repositories.admin_client import AdminClient
admin = AdminClient(supabase_admin_client)
body_analysis_repo = admin.with_user_check(user_id, id_column="user_id")
body_analysis_repo.table("body_analysis").update({...}).eq("id", id).execute()

# Exception handling ya existe:
from app.core.exceptions import (
    ValidationError, AuthenticationError, NotFoundError
)

# SSRF validation ya existe:
from pydantic import AnyHttpUrl

# Logger pattern ya existe:
import logging
logger = logging.getLogger(__name__)
logger.info("Vision worker started", extra={"user_id": str(user_id)})
```

---

**Sprint 0.5 es tu último sprint de backend puro.** Después, Sasha entra con Sprint 0.4 (DevOps) en paralelo, y tú podrías ayudar con Sprint 1 (Auth avanzado) o esperar feedback de producción.

¿Listos para activar?

Co-Authored-By: Jarvis (CEO)
