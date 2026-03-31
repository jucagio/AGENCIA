# FastAPI Expert — Skill para Claude Code

## Descripcion
Skill experta en FastAPI para construir APIs de produccion rapidas, seguras y bien estructuradas. Cubre arquitectura, seguridad OWASP, Pydantic v2, async patterns, y conexion con Supabase/PostgreSQL. Optimizada para el agente Sasha de la Agencia.

## Instrucciones

Cuando el usuario pida ayuda con FastAPI o backend Python, sigue estas directrices:

### Arquitectura del Proyecto

```
app/
  main.py                  # FastAPI app instance, startup/shutdown, middleware
  config.py                # Settings con Pydantic BaseSettings
  dependencies.py          # Dependencias compartidas (DB session, auth)
  core/
    security.py            # JWT, hashing, auth middleware
    exceptions.py          # Exception handlers personalizados
    middleware.py           # CORS, rate limiting, logging
  api/
    v1/
      router.py            # Router principal que agrupa todos los endpoints
      endpoints/
        auth.py            # Login, register, refresh token
        users.py           # CRUD de usuarios
        orders.py          # Endpoints de negocio
  models/
    user.py                # SQLAlchemy / Supabase models
    order.py
  schemas/
    user.py                # Pydantic schemas (request/response)
    order.py
    common.py              # PaginatedResponse, ErrorResponse
  services/
    user_service.py        # Logica de negocio
    order_service.py
    email_service.py
  repositories/
    user_repository.py     # Acceso a datos (queries)
    order_repository.py
  utils/
    pagination.py          # Helper de paginacion
    validators.py          # Validadores custom
tests/
  conftest.py              # Fixtures compartidos
  api/
    test_auth.py
    test_users.py
  services/
    test_user_service.py
```

### Configuracion Base

```python
# app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # App
    APP_NAME: str = "API"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"

    # Database
    SUPABASE_URL: str
    SUPABASE_KEY: str  # service_role key para backend
    DATABASE_URL: str  # PostgreSQL direct connection

    # External
    ANTHROPIC_API_KEY: str = ""

    # CORS
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    model_config = {"env_file": ".env", "case_sensitive": True}

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.api.v1.router import api_router
from app.core.exceptions import register_exception_handlers

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: init DB pool, cache, etc.
    yield
    # Shutdown: close connections

def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.APP_NAME,
        lifespan=lifespan,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routes
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    # Exception handlers
    register_exception_handlers(app)

    return app

app = create_app()
```

### Pydantic v2 Schemas

```python
# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=100)

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)

class UserUpdate(BaseModel):
    full_name: str | None = Field(None, min_length=2, max_length=100)
    avatar_url: str | None = None

class UserResponse(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserInDB(UserResponse):
    hashed_password: str

# app/schemas/common.py
from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int

class ErrorResponse(BaseModel):
    detail: str
    code: str | None = None
```

### Seguridad — JWT + OWASP

```python
# app/core/security.py
from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config import get_settings

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security_scheme = HTTPBearer()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(user_id: UUID, expires_delta: timedelta | None = None) -> str:
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload = {
        "sub": str(user_id),
        "exp": expire,
        "type": "access",
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(user_id: UUID) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {
        "sub": str(user_id),
        "exp": expire,
        "type": "refresh",
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> UUID:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
        user_id = UUID(payload["sub"])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    return user_id
```

### Conexion con Supabase

```python
# app/repositories/base.py
from supabase import create_client, Client
from app.config import get_settings

settings = get_settings()

def get_supabase_client() -> Client:
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

# app/repositories/user_repository.py
from uuid import UUID
from app.repositories.base import get_supabase_client

class UserRepository:
    def __init__(self):
        self.client = get_supabase_client()
        self.table = "users"

    async def get_by_id(self, user_id: UUID) -> dict | None:
        response = self.client.table(self.table).select("*").eq("id", str(user_id)).single().execute()
        return response.data

    async def get_by_email(self, email: str) -> dict | None:
        response = self.client.table(self.table).select("*").eq("email", email).maybe_single().execute()
        return response.data

    async def create(self, user_data: dict) -> dict:
        response = self.client.table(self.table).insert(user_data).execute()
        return response.data[0]

    async def update(self, user_id: UUID, update_data: dict) -> dict:
        response = (
            self.client.table(self.table)
            .update(update_data)
            .eq("id", str(user_id))
            .execute()
        )
        return response.data[0]

    async def list_paginated(self, page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        offset = (page - 1) * page_size
        # Count
        count_resp = self.client.table(self.table).select("id", count="exact").execute()
        total = count_resp.count or 0
        # Data
        data_resp = (
            self.client.table(self.table)
            .select("*")
            .order("created_at", desc=True)
            .range(offset, offset + page_size - 1)
            .execute()
        )
        return data_resp.data, total
```

### Endpoints Pattern

```python
# app/api/v1/endpoints/users.py
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.schemas.user import UserResponse, UserUpdate
from app.schemas.common import PaginatedResponse
from app.services.user_service import UserService
from app.core.security import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

def get_user_service() -> UserService:
    return UserService()

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user_id: UUID = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    user = await service.get_by_id(current_user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.patch("/me", response_model=UserResponse)
async def update_profile(
    update_data: UserUpdate,
    current_user_id: UUID = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    return await service.update(current_user_id, update_data)

@router.get("/", response_model=PaginatedResponse[UserResponse])
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: UserService = Depends(get_user_service),
):
    return await service.list_paginated(page=page, page_size=page_size)
```

### Error Handling

```python
# app/core/exceptions.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

class AppException(Exception):
    def __init__(self, message: str, code: str, status_code: int = 400):
        self.message = message
        self.code = code
        self.status_code = status_code

class NotFoundError(AppException):
    def __init__(self, resource: str, id: str):
        super().__init__(
            message=f"{resource} with id {id} not found",
            code="NOT_FOUND",
            status_code=404,
        )

class ConflictError(AppException):
    def __init__(self, message: str):
        super().__init__(message=message, code="CONFLICT", status_code=409)

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message, "code": exc.code},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        # Log the error (use structlog or logging)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "code": "INTERNAL_ERROR"},
        )
```

### Testing con pytest

```python
# tests/conftest.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def auth_headers():
    from app.core.security import create_access_token
    from uuid import uuid4
    token = create_access_token(uuid4())
    return {"Authorization": f"Bearer {token}"}

# tests/api/test_auth.py
import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_login_success(client: AsyncClient):
    response = await client.post("/api/v1/auth/login", json={
        "email": "test@test.com",
        "password": "password123",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

@pytest.mark.anyio
async def test_login_invalid_credentials(client: AsyncClient):
    response = await client.post("/api/v1/auth/login", json={
        "email": "test@test.com",
        "password": "wrong",
    })
    assert response.status_code == 401
```

### Seguridad OWASP — Checklist para APIs

1. **Input Validation**: Pydantic valida automaticamente. Agregar `Field(max_length=...)` a TODOS los strings.
2. **Authentication**: JWT con expiracion corta (30min access, 7d refresh). Rotar refresh tokens.
3. **Authorization**: Verificar que el usuario tiene permisos en CADA endpoint. Usar Supabase RLS como segunda capa.
4. **Rate Limiting**: Usar slowapi o middleware custom. Limitar login a 5 intentos/minuto.
5. **CORS**: Especificar origenes exactos, nunca `"*"` en produccion.
6. **Headers**: Agregar security headers (X-Content-Type-Options, X-Frame-Options, etc.).
7. **SQL Injection**: Usar Supabase SDK o SQLAlchemy ORM. NUNCA concatenar strings en queries.
8. **Logging**: Loggear requests, errores y eventos de seguridad. NO loggear passwords ni tokens.
9. **Dependencies**: Mantener actualizados los paquetes. Correr `pip audit` regularmente.
10. **Secrets**: Usar variables de entorno. NUNCA commitear `.env` o secrets al repositorio.

### Deploy

**Railway:**
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "$PORT"]
```

**Render:**
```yaml
# render.yaml
services:
  - type: web
    name: api
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: SUPABASE_URL
        sync: false
      - key: SUPABASE_KEY
        sync: false
```

### Paquetes Esenciales (requirements.txt)

```
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
pydantic>=2.7.0
pydantic-settings>=2.3.0
python-jose[cryptography]>=3.3.0  # O PyJWT
passlib[bcrypt]>=1.7.4
supabase>=2.5.0
httpx>=0.27.0
python-multipart>=0.0.9
structlog>=24.0.0
slowapi>=0.1.9

# Dev
pytest>=8.2.0
anyio[trio]>=4.4.0
pytest-anyio>=0.0.0
httpx>=0.27.0  # AsyncClient para tests
```

### Mejores Practicas

1. **Siempre usar async** para endpoints que hagan I/O (DB, HTTP, file).
2. **Pydantic para todo**: request bodies, responses, settings, config.
3. **Dependency injection**: Usar `Depends()` para servicios, repos, auth. Facilita testing.
4. **Versionado de API**: Prefijo `/api/v1/`. Cuando haya breaking changes, crear `/api/v2/`.
5. **Documentacion**: FastAPI genera OpenAPI automaticamente. Agregar descriptions y examples a schemas.
6. **Health check**: Siempre tener `GET /health` que retorne `{"status": "ok"}`.
7. **Structured logging**: Usar structlog en lugar de print(). Incluir request_id en cada log.
8. **Background tasks**: Usar `BackgroundTasks` de FastAPI para tareas que no bloqueen la response.
9. **Pagination**: Toda lista debe ser paginada. Usar page/page_size, nunca retornar todo.
10. **Idempotency**: POST endpoints criticos deben soportar idempotency keys para evitar duplicados.
