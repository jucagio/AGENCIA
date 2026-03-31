---
name: test-driven-development
description: >
  TDD: escribir tests antes que el código de producción siguiendo el ciclo Red-Green-Refactor.
  Usar cuando se implementen nuevas features, se corrijan bugs críticos, o se refactorice
  código existente. Garantiza cobertura de tests y diseño limpio desde el inicio.
  Agentes principales: Sasha, Brook.
---

# Test-Driven Development (TDD)

## El Ciclo Red-Green-Refactor

```
    🔴 RED              🟢 GREEN           🔵 REFACTOR
  Escribe un         Escribe el código    Mejora el código
  test que           mínimo para que      manteniendo los
  FALLA              el test PASE         tests en verde
      ↓                    ↓                    ↓
  "No existe         "Funciona pero       "Funciona Y está
   aún"              es feo"              limpio"
```

**Regla de oro:** nunca escribas código de producción sin un test que falle primero.

---

## TDD en Python (pytest) — Ejemplo completo

### 1. 🔴 RED — Escribe el test primero

```python
# tests/test_user_service.py
import pytest
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository

def test_register_user_successfully():
    # Arrange
    repo = MockUserRepository()
    service = UserService(repo)

    # Act
    user = service.register(email="test@example.com", password="SecurePass123!")

    # Assert
    assert user.email == "test@example.com"
    assert user.id is not None
    assert user.password != "SecurePass123!"  # debe estar hasheada
```

*Este test FALLA porque UserService no existe aún.*

### 2. 🟢 GREEN — Código mínimo para pasar el test

```python
# app/services/user_service.py
import bcrypt
from app.entities.user import User

class UserService:
    def __init__(self, repo):
        self.repo = repo

    def register(self, email: str, password: str) -> User:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User(email=email, password=hashed.decode())
        return self.repo.save(user)
```

*Test pasa. Código funciona pero puede mejorar.*

### 3. 🔵 REFACTOR — Mejorar sin romper tests

```python
# app/services/user_service.py
from app.entities.user import User
from app.repositories.user_repository import UserRepository
from app.utils.password import hash_password, validate_password_strength

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register(self, email: str, password: str) -> User:
        validate_password_strength(password)

        if self.repo.find_by_email(email):
            raise ValueError(f"Email {email} already registered")

        user = User(
            email=email.lower().strip(),
            password=hash_password(password)
        )
        return self.repo.save(user)
```

*Tests siguen pasando. Código más limpio y con validaciones.*

---

## TDD en JavaScript/TypeScript (Jest)

```typescript
// tests/user.service.test.ts
describe('UserService', () => {
  let userService: UserService;
  let mockRepo: jest.Mocked<UserRepository>;

  beforeEach(() => {
    mockRepo = {
      save: jest.fn(),
      findByEmail: jest.fn(),
    };
    userService = new UserService(mockRepo);
  });

  it('should register a new user with hashed password', async () => {
    // Arrange
    mockRepo.findByEmail.mockResolvedValue(null);
    mockRepo.save.mockResolvedValue({ id: '1', email: 'test@test.com' });

    // Act
    const user = await userService.register('test@test.com', 'SecurePass123!');

    // Assert
    expect(user.id).toBeDefined();
    expect(mockRepo.save).toHaveBeenCalledOnce();
  });

  it('should throw if email already exists', async () => {
    // Arrange
    mockRepo.findByEmail.mockResolvedValue({ id: '1' }); // ya existe

    // Act & Assert
    await expect(
      userService.register('test@test.com', 'SecurePass123!')
    ).rejects.toThrow('Email already registered');
  });
});
```

---

## Tipos de tests y cuándo usarlos

### Unit Tests (la base — muchos y rápidos)
```python
# Prueban una unidad en aislamiento — sin BD, sin red
def test_password_hash_is_not_plain_text():
    hashed = hash_password("mypassword")
    assert hashed != "mypassword"
    assert len(hashed) > 20
```

### Integration Tests (capa media — prueban que las capas conectan)
```python
# Prueban múltiples capas juntas
async def test_register_user_saves_to_database(db_session):
    repo = SupabaseUserRepository(db_session)
    service = UserService(repo)

    user = await service.register("integration@test.com", "Pass123!")

    saved = await repo.find_by_email("integration@test.com")
    assert saved is not None
    assert saved.id == user.id
```

### E2E Tests (pocos — prueban el flujo completo)
```python
# Prueban el sistema completo como lo usaría el usuario
async def test_user_can_register_and_login(client):
    response = await client.post("/api/auth/register", json={
        "email": "e2e@test.com",
        "password": "SecurePass123!"
    })
    assert response.status_code == 201

    login_response = await client.post("/api/auth/login", json={
        "email": "e2e@test.com",
        "password": "SecurePass123!"
    })
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
```

---

## Cobertura mínima por capa (Sasha exige esto)

| Capa | Cobertura mínima |
|------|-----------------|
| Lógica de negocio (Use Cases, Services) | **90%+** |
| Endpoints de API | **80%+** |
| Repositorios | **75%+** |
| Utilidades y helpers | **70%+** |
| UI/Frontend (Brook) | **60%+** en componentes críticos |

---

## TDD para bugfixes

Cuando aparece un bug:

```
1. Escribe un test que REPRODUCE el bug (falla)
2. Verifica que el test falla por la razón correcta
3. Corrige el código (el test debe pasar)
4. Verifica que todos los tests anteriores siguen pasando
5. El test del bug queda como regresión permanente
```

```python
# Bug: el usuario puede registrarse con email en mayúsculas
# y crear duplicados (test@TEST.com vs test@test.com)

def test_register_normalizes_email_to_lowercase():
    user = service.register("TEST@EXAMPLE.COM", "Pass123!")
    assert user.email == "test@example.com"  # 🔴 FALLA → 🟢 FIX → ✅ permanente
```

---

## Mocks, Stubs y Fakes — Cuándo usar cada uno

| Tipo | Cuándo usarlo | Ejemplo |
|------|--------------|---------|
| **Mock** | Verificar que se llamó a algo | `mock_repo.save.assert_called_once()` |
| **Stub** | Controlar lo que devuelve | `mock_repo.find.return_value = user` |
| **Fake** | Implementación real en memoria | `InMemoryUserRepository` |
| **Spy** | Observar llamadas sin controlar | `jest.spyOn(service, 'method')` |

*Fuente: ComposioHQ/Antigravity TDD Skill + Martin Fowler's TDD patterns*
