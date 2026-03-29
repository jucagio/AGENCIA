# ASESOR DE IMAGEN AI — Quick Start para Sasha

**Duración:** 30 minutos
**Objetivo:** Sasha entiende dónde empezar + qué hacer primero

---

## 1. LEE ESTO PRIMERO (En orden)

1. **ASESOR_IMAGEN_AI_RESUMEN_EJECUTIVO.md** (5 min)
   - Visión general, números, viabilidad
   - Después lees esto, sabes por qué hacemos esto

2. **ASESOR_IMAGEN_AI_ARQUITECTURA.md** (15 min)
   - Secciones 1-4: Stack, APIs, Database Schema, Endpoints
   - Ignora Timelines por ahora (lo verás en Sprint 0)

3. **ASESOR_IMAGEN_AI_SCHEMAS_Y_SERVICIOS.md** (10 min)
   - Secciones 1-2: Schemas + Servicios que implementarás
   - Este es tu "blueprint" para código

4. **ASESOR_IMAGEN_AI_CHECKLIST_EJECUCION.md** (5 min)
   - Sprint 0 (Week 1) — tu primer sprint
   - Esto es tu roadmap de 14 semanas

---

## 2. ANTES DE ESCRIBIR CÓDIGO (PREREQUISITES)

### 2.1 Aprobaciones Necesarias (Pregunta a Jarvis)

- [ ] Supabase project creado (acceso dado a Sasha)
- [ ] Google Cloud Vision API credentials (JSON file)
- [ ] Replicate API key obtenida
- [ ] Anthropic API key obtenida
- [ ] Stripe account creado (test + live keys)
- [ ] Mercado Pago credentials obtenida
- [ ] Railway account creado + GitHub connected
- [ ] GitHub Actions workflow permission

**Sin esto, no puedes empezar Sprint 0.**

### 2.2 Credenciales a Solicitar

Copia esto y envía a Jarvis:

```
Sasha necesita:
1. Supabase URL + service_role key (para backend)
2. Google Cloud Vision service account JSON
3. Replicate API token
4. Anthropic API key
5. Stripe (test) secret key + publishable key
6. Mercado Pago access token (sandbox)
7. Firebase config (para storage)

Todos en .env.example (sin valores reales, solo placeholders)
Checklist cuando tengas todo: ✅
```

---

## 3. SPRINT 0 (SEMANA 1) — QUÉ HACER

**Objetivo:** Production-ready infrastructure. 0 features.
**Duración:** 40 horas (4 días × 10 horas)
**Equipo:** Sasha (40h), Brook (20h setup), Erik (environment)

### 3.1 Infrastructure Setup (12 horas)

```bash
# Paso 1: Supabase Setup
cd agencia/backend
supabase init  # Initialize project
supabase start # Local dev server

# Paso 2: Database Schema (en Supabase Dashboard)
# Copiar SQL de ASESOR_IMAGEN_AI_ARQUITECTURA.md Section 1.2
# Ejecutar en SQL Editor de Supabase

# Paso 3: RLS Policies
# Copiar SQL de ASESOR_IMAGEN_AI_ARQUITECTURA.md Section 1.2
# Verificar: cada tabla tiene RLS enabled

# Paso 4: Storage Buckets
# Dashboard > Storage > Create buckets:
# - avatars/
# - wardrobe/
# - tryons/
```

**Validación:**
- [ ] `supabase status` muestra conexión OK
- [ ] Database tables visible en Dashboard
- [ ] RLS policies aplicadas
- [ ] 3 storage buckets creados

### 3.2 FastAPI Backend Setup (14 horas)

```bash
# Paso 1: Project Setup
mkdir backend
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` en Windows
pip install -r requirements.txt

# Paso 2: Folder Structure
# Copiar estructura de ASESOR_IMAGEN_AI_ARQUITECTURA.md Section 1.1
# Crear archivos vacíos primero:
mkdir -p app/core app/api/v1/endpoints app/models app/schemas app/services app/repositories tests

# Paso 3: Config Setup
# Crear app/config.py (copiar de ASESOR_IMAGEN_AI_SCHEMAS_Y_SERVICIOS.md)
# Crear .env.example con placeholders

# Paso 4: Main App
# Crear app/main.py (copiar de FastAPI skill)
# Verificar: `uvicorn app.main:app --reload` inicia sin errores

# Paso 5: Health Endpoint
# Agregar GET /health en app/main.py
# Test: curl http://localhost:8000/health → {"status": "ok"}
```

**Validación:**
- [ ] `uvicorn app.main:app --reload` inicia sin errores
- [ ] `GET /health` retorna {"status": "ok"}
- [ ] Docs en `http://localhost:8000/docs`

### 3.3 Docker + Railway Setup (8 horas)

```bash
# Paso 1: Dockerfile
# Crear Dockerfile en backend/ (copiar de FastAPI skill)
# Build locally: `docker build -t asesor-imagen .`

# Paso 2: .dockerignore
# Crear .dockerignore (venv/, __pycache__, .pytest_cache, etc.)

# Paso 3: Railway Deploy
# 1. GitHub > Settings > Actions > Allow all actions
# 2. Railway > New Project > GitHub repo connect
# 3. Railway > Variables > Set SUPABASE_URL, SUPABASE_KEY, SECRET_KEY, etc.
# 4. Deploy button en Railway

# Paso 4: Verify
# Railway > Logs > Ver deployment logs
# Test: curl https://[deployment-url].railway.app/health
```

**Validación:**
- [ ] Docker builds locally sin errores
- [ ] Railway deployment exitoso
- [ ] Health endpoint responde desde production URL

### 3.4 CI/CD Setup (6 horas)

```bash
# Paso 1: GitHub Actions Workflow
# Crear .github/workflows/test.yml
# Contenido: Run pytest on every push

# Paso 2: Coverage Reports
# Add coverage flag: `pytest --cov=app --cov-report=html`

# Paso 3: Branch Protection
# GitHub > Settings > Branches > Add protection rule
# Require checks to pass before merge

# Paso 4: Test locally
# `pytest` debe pasar 100%
```

**Validación:**
- [ ] GitHub Actions runs on every push
- [ ] Tests pass (coverage >80%)
- [ ] Cannot merge to main without passing tests

---

## 4. ESTRUCTURA DEL CÓDIGO (Copy-Paste Friendly)

### 4.1 Pydantic Schemas

Todos en `app/schemas/`

```python
# app/schemas/__init__.py
from .auth import LoginRequest, LoginResponse, RegisterRequest
from .user import UserResponse, UserUpdate
from .body_analysis import BodyAnalysisResponse
from .wardrobe import WardrobeItemResponse, WardrobeListResponse
from .outfit import OutfitResponse
from .tryons import TryOnResponse
from .recommendations import RecommendationResponse
from .subscriptions import SubscriptionPlan, SubscriptionStatus
```

**Archivar:** `ASESOR_IMAGEN_AI_SCHEMAS_Y_SERVICIOS.md` Section 1

### 4.2 Service Layer

Todos en `app/services/`

Cada archivo es independiente:
- `auth_service.py` (login, register, refresh)
- `body_analysis_service.py` (Google Vision)
- `wardrobe_service.py` (auto-categorization)
- `tryon_service.py` (Replicate API)
- `recommendation_service.py` (Claude API)
- `subscription_service.py` (Stripe)
- `storage_service.py` (Supabase Storage)

**Para implementar:**
1. Copiar template de `ASESOR_IMAGEN_AI_SCHEMAS_Y_SERVICIOS.md`
2. Reemplazar `TODO` comments
3. Test en `tests/services/`

### 4.3 Endpoints

Todos en `app/api/v1/endpoints/`

Cada archivo corresponde a un domain:
- `auth.py` (6 endpoints)
- `users.py` (5 endpoints)
- `analysis.py` (4 endpoints)
- `wardrobe.py` (7 endpoints)
- `outfits.py` (5 endpoints)
- `tryons.py` (3 endpoints)
- `recommendations.py` (2 endpoints)
- `subscriptions.py` (4 endpoints)

**Template:**

```python
# app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends
from app.services.auth_service import AuthService
from app.schemas.auth import LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["auth"])

def get_auth_service() -> AuthService:
    return AuthService()

@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    service: AuthService = Depends(get_auth_service),
):
    return await service.login(request)
```

---

## 5. TESTING STRATEGY (Desde Día 1)

### 5.1 Estructura de Tests

```bash
tests/
├── conftest.py              # Fixtures compartidos
├── services/
│   ├── test_auth_service.py
│   ├── test_body_analysis_service.py
│   ├── test_wardrobe_service.py
│   └── test_tryon_service.py
├── api/
│   ├── test_auth_endpoints.py
│   ├── test_wardrobe_endpoints.py
│   └── test_tryons_endpoints.py
└── integration/
    └── test_full_user_flow.py
```

### 5.2 Test First Approach

Para cada servicio:
1. Escribir test primero (TDD)
2. Implementar servicio
3. Verify test pasa

**Ejemplo:**

```python
# tests/services/test_auth_service.py
import pytest
from unittest.mock import AsyncMock
from app.services.auth_service import AuthService

@pytest.fixture
def auth_service():
    return AuthService()

@pytest.mark.anyio
async def test_login_success(auth_service):
    # Arrange
    request = LoginRequest(email="test@test.com", password="pass123")

    # Act
    result = await auth_service.login(request)

    # Assert
    assert result.access_token
    assert result.refresh_token
```

### 5.3 Coverage Target

- **Sprint 0-1:** 60% (just infrastructure)
- **Sprint 2-8:** 80%+ (all services + endpoints)
- **Sprint 9:** 90%+ (production ready)

---

## 6. COMMON MISTAKES (Evita Estos)

### ❌ Error 1: No RLS Policies

```sql
-- MAL (cualquier usuario ve todo)
SELECT * FROM users;

-- BIEN (users ven solo su data)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users see own profile" ON users
  FOR SELECT TO authenticated
  USING (id = auth.uid());
```

### ❌ Error 2: Passwords en logs

```python
# MAL
logger.info(f"User login: {email}, password: {password}")

# BIEN
logger.info(f"User login: {email}")
```

### ❌ Error 3: No Validation

```python
# MAL
class LoginRequest(BaseModel):
    email: str
    password: str

# BIEN
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
```

### ❌ Error 4: JWT sin expiry

```python
# MAL
payload = {"sub": user_id}  # No expiry!

# BIEN
payload = {
    "sub": user_id,
    "exp": datetime.now() + timedelta(minutes=30),
    "type": "access"
}
```

### ❌ Error 5: No error handling en APIs externas

```python
# MAL
response = vision_client.detect_objects(image)

# BIEN
try:
    response = vision_client.detect_objects(image)
except google.cloud.exceptions.GoogleCloudError as e:
    logger.error(f"Vision API failed: {e}")
    raise HTTPException(status_code=503, detail="Service unavailable")
```

---

## 7. DAILY CHECKLIST (Cada día de Sprint 0-1)

- [ ] Morning standup (15 min)
  - Qué hice ayer
  - Qué hago hoy
  - Blockers
- [ ] Code review (con Jarvis)
  - PR para cada feature
  - Tests passing
  - Coverage >80%
- [ ] Commit daily (even if small)
  - Messages claros: "feat: auth login endpoint"
  - Never hardcode secrets
- [ ] Update checklist
  - Mark items in ASESOR_IMAGEN_AI_CHECKLIST_EJECUCION.md

---

## 8. HERRAMIENTAS QUE NECESITAS

### CLI Tools

```bash
# Python
python 3.12+
pip

# Database
supabase-cli

# Testing
pytest, pytest-asyncio, pytest-cov

# Formatting
black, isort

# Linting
flake8, mypy

# API client
curl, httpie

# Git
git
```

### IDEs Recomendadas

- **Backend:** VS Code (Python extension) + pylance
- **Database:** Supabase Dashboard (en browser)
- **APIs:** Postman o Insomnia

### Browser Extensions

- Thunder Client (API testing en VS Code)
- JSON Formatter
- JWT Debugger

---

## 9. GIT WORKFLOW (Exacto)

```bash
# 1. Crear rama per feature
git checkout -b feat/auth-endpoints

# 2. Hacer cambios + commits frecuentes
git add app/services/auth_service.py
git commit -m "feat: implement login method"

git add tests/services/test_auth_service.py
git commit -m "test: add login success test"

# 3. Push a GitHub
git push origin feat/auth-endpoints

# 4. Pull Request
# - Click PR button
# - Esperar tests en GitHub Actions
# - Pedir review a Jarvis
# - Merge cuando aprobado

# 5. Delete rama local
git checkout main
git pull
git branch -d feat/auth-endpoints
```

**Rule:** Nunca commitear:
- `.env` (secrets)
- `__pycache__/`
- `.pytest_cache/`
- `*.pyc`

---

## 10. WEEK 1 MILESTONES (Sprint 0)

**Mon-Wed:**
- [ ] Database setup complete
- [ ] FastAPI scaffold done
- [ ] Health endpoint working
- [ ] Docker builds locally

**Thu-Fri:**
- [ ] Railway deployed
- [ ] CI/CD pipeline running
- [ ] Tests passing (pytest)
- [ ] All infrastructure documented

**Friday EOD:**
- [ ] Presentation to Jarvis
- [ ] Sign-off to proceed Sprint 1

---

## 11. AYUDA + REFERENCIAS

### Si Necesitas Ayuda

**Backend Questions:**
- Pregunta a Sasha (la eres tú) en Slack
- Revisar: `ASESOR_IMAGEN_AI_ARQUITECTURA.md`

**Frontend Questions:**
- Pregunta a Brook en Slack
- Revisar: Flutter Expert skill

**Design Questions:**
- Pregunta a Erik en Slack

**Architectural Questions:**
- Pregunta a Jarvis
- Revisar: ASESOR_IMAGEN_AI_RESUMEN_EJECUTIVO.md

### Documentación Externa

- FastAPI: https://fastapi.tiangolo.com/
- Pydantic v2: https://docs.pydantic.dev/
- Supabase: https://supabase.com/docs
- PostgreSQL: https://www.postgresql.org/docs/
- Google Vision: https://cloud.google.com/vision/docs
- Replicate: https://replicate.com/docs
- Anthropic: https://docs.anthropic.com/

---

## 12. PREGUNTAS ANTES DE EMPEZAR

Responde estas sí/no:

1. ¿Tengo acceso a Supabase project?
2. ¿Tengo Google Vision credentials?
3. ¿Tengo Replicate API key?
4. ¿Tengo Anthropic API key?
5. ¿Tengo Stripe test keys?
6. ¿Tengo Railway account?
7. ¿GitHub Actions enabled?
8. ¿He leído ASESOR_IMAGEN_AI_RESUMEN_EJECUTIVO.md?
9. ¿He leído ASESOR_IMAGEN_AI_ARQUITECTURA.md Section 1-4?
10. ¿Estoy listo para empezar código?

Si todos son SÍ → Comienza Sprint 0.
Si alguno es NO → Pregunta a Jarvis.

---

## 13. FIRST COMMIT (Sembra la Semilla)

Cuando hayas completado Sprint 0:

```bash
git commit -m "feat(infra): Sprint 0 infrastructure setup

- Supabase project initialized with schema + RLS policies
- FastAPI scaffold with config, dependencies, main.py
- Docker container for local development + production
- Railway deployment configured + tested
- GitHub Actions CI/CD pipeline (tests + coverage)
- Database migrations version controlled

Technical decisions:
- PostgreSQL RLS for authorization (no app-level auth)
- JWT tokens (access 30min, refresh 7d)
- Async FastAPI throughout
- Pydantic v2 for validation
- pytest + pytest-asyncio for testing

Status: Production-ready infrastructure, 0 features yet.

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

**¡Listo para empezar! Suerte, Sasha. 🚀**

