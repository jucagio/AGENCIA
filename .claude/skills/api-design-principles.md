---
name: api-design-principles
description: >
  Principios de diseño de APIs REST y GraphQL: convenciones, versionado, paginación,
  manejo de errores, documentación y seguridad. Usar cuando se diseñe una API nueva,
  se revise la consistencia de endpoints existentes, o se defina el contrato entre
  Sasha (backend) y Brook (frontend). Agentes: Sasha, Jarvis.
---

# API Design Principles — REST & GraphQL

## REST — Convenciones Estándar

### Estructura de URLs

```
# Recursos como sustantivos (nunca verbos)
✅ GET /users
✅ GET /users/{id}
✅ POST /users
✅ PUT /users/{id}       ← reemplaza completo
✅ PATCH /users/{id}     ← actualización parcial
✅ DELETE /users/{id}

# Recursos anidados (máximo 2 niveles)
✅ GET /users/{id}/orders
✅ GET /users/{id}/orders/{order_id}
❌ GET /users/{id}/orders/{order_id}/items/{item_id}/reviews  ← demasiado anidado

# Acciones especiales (cuando REST no alcanza)
✅ POST /orders/{id}/cancel
✅ POST /payments/{id}/refund
✅ POST /users/{id}/verify-email
```

### Métodos HTTP y semántica

| Método | Semántica | Idempotente | Body |
|--------|-----------|-------------|------|
| **GET** | Leer, sin efectos secundarios | Sí | No |
| **POST** | Crear o acción | No | Sí |
| **PUT** | Reemplazar completo | Sí | Sí |
| **PATCH** | Actualizar parcialmente | No | Sí |
| **DELETE** | Eliminar | Sí | Opcional |

### Códigos de respuesta HTTP

```
200 OK              → GET exitoso, PUT/PATCH exitoso
201 Created         → POST que crea recurso (incluir Location header)
204 No Content      → DELETE exitoso, PUT sin body de respuesta
400 Bad Request     → Input inválido (validación fallida)
401 Unauthorized    → No autenticado (falta token)
403 Forbidden       → Autenticado pero sin permiso
404 Not Found       → Recurso no existe
409 Conflict        → Conflicto de estado (email duplicado)
422 Unprocessable   → Validación semántica fallida
429 Too Many Req.   → Rate limit excedido
500 Internal Error  → Error del servidor (nunca exponer detalles)
```

---

## Formato de Respuesta Estándar (contrato con Brook)

### Respuesta exitosa

```json
{
  "success": true,
  "data": {
    "id": "uuid-here",
    "email": "user@example.com",
    "created_at": "2026-03-28T10:00:00Z"
  },
  "message": "Usuario creado exitosamente"
}
```

### Respuesta de listado con paginación

```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 150,
    "total_pages": 8,
    "has_next": true,
    "has_prev": false,
    "next_cursor": "2026-03-01T00:00:00Z"
  }
}
```

### Respuesta de error

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Los datos enviados no son válidos",
    "fields": {
      "email": "El email ya está registrado",
      "password": "Mínimo 8 caracteres requeridos"
    }
  }
}
```

### Códigos de error estandarizados

```python
class ErrorCode:
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    CONFLICT = "CONFLICT"
    RATE_LIMITED = "RATE_LIMITED"
    INTERNAL_ERROR = "INTERNAL_ERROR"
```

---

## Versionado de API

### Versionado en URL (recomendado para APIs públicas)

```
/api/v1/users
/api/v2/users
```

### Versionado por header (APIs internas)

```
API-Version: 2026-03-28
```

### Política de deprecación

```
1. Anunciar deprecación con mínimo 6 meses de anticipación
2. Agregar header Deprecation: date=2026-09-01 en respuestas
3. Mantener versión deprecated funcionando durante el período
4. Migrar clientes antes del sunset
```

---

## Paginación

### Offset-based (simple, para datasets pequeños)

```
GET /users?page=2&per_page=20

Response pagination:
{
  "page": 2,
  "per_page": 20,
  "total": 150
}
```

### Cursor-based (para feeds y datasets grandes)

```
# Primera página
GET /orders?limit=20

# Siguiente página (usando cursor del último item)
GET /orders?limit=20&cursor=2026-03-01T00:00:00Z

Response:
{
  "data": [...],
  "next_cursor": "2026-02-15T10:30:00Z",
  "has_more": true
}
```

---

## Documentación con OpenAPI (Swagger)

```python
# FastAPI genera OpenAPI automáticamente
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Agencia API",
    version="1.0.0",
    description="API de la Agencia — construida por Sasha"
)

class UserCreateRequest(BaseModel):
    email: str = Field(..., example="user@example.com")
    password: str = Field(..., min_length=8, example="SecurePass123!")

class UserResponse(BaseModel):
    id: str
    email: str
    created_at: datetime

@app.post(
    "/api/v1/users",
    response_model=UserResponse,
    status_code=201,
    summary="Registrar nuevo usuario",
    description="Crea una nueva cuenta de usuario. El email debe ser único.",
    responses={
        409: {"description": "Email ya registrado"},
        422: {"description": "Datos de entrada inválidos"}
    }
)
async def register_user(data: UserCreateRequest):
    ...
```

---

## GraphQL — Cuándo usarlo en vez de REST

```
Usar GraphQL cuando:
✅ El cliente necesita flexibilidad para pedir exactamente los campos que necesita
✅ Hay múltiples clientes (móvil, web, dashboard) con necesidades diferentes
✅ Los datos tienen relaciones complejas y los clientes hacen muchas queries relacionadas

Usar REST cuando:
✅ API simple y predecible (CRUD básico)
✅ Caché es importante (REST se cachea mejor)
✅ Equipo más pequeño o menos experiencia con GraphQL
```

---

## Checklist de diseño de API (Sasha verifica antes de entregar a Brook)

```
[ ] URLs son sustantivos, no verbos
[ ] Métodos HTTP usados con su semántica correcta
[ ] Códigos de status HTTP apropiados para cada caso
[ ] Formato de respuesta estándar (success/data/error/pagination)
[ ] Errores tienen código de error + mensaje + campos (si aplica)
[ ] Endpoints de listado tienen paginación
[ ] API documentada con OpenAPI/Swagger
[ ] Autenticación requerida en endpoints que lo necesitan
[ ] Rate limiting en endpoints críticos (auth, uploads)
[ ] Versionado definido si la API es pública
[ ] CORS configurado correctamente
[ ] Documentación incluye ejemplos de request y response
```

*Fuente: Antigravity API Design Principles Skill + REST API Design Rulebook*
