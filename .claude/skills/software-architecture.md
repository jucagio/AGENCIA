---
name: software-architecture
description: >
  Clean Architecture, SOLID principles, Domain-Driven Design y patrones de diseño.
  Usar cuando se necesite diseñar la arquitectura de un proyecto nuevo, refactorizar
  código existente hacia una estructura más mantenible, o tomar decisiones sobre
  capas, dependencias y separación de responsabilidades. Agentes: Sasha, Jarvis.
---

# Software Architecture — Clean Architecture & SOLID

## Core Principles

### Clean Architecture (Robert C. Martin)

La arquitectura limpia organiza el código en capas concéntricas donde **las dependencias solo apuntan hacia adentro** — nunca hacia afuera.

```
           ┌─────────────────────────┐
           │    Frameworks & Drivers  │  ← Detalles (BD, Web, UI)
           │  ┌───────────────────┐  │
           │  │   Interface Layer  │  │  ← Controllers, Gateways, Presenters
           │  │  ┌─────────────┐  │  │
           │  │  │  Use Cases  │  │  │  ← Reglas de negocio de la aplicación
           │  │  │ ┌─────────┐ │  │  │
           │  │  │ │Entities │ │  │  │  ← Reglas de negocio empresariales
           │  │  │ └─────────┘ │  │  │
           │  │  └─────────────┘  │  │
           │  └───────────────────┘  │
           └─────────────────────────┘
```

**Regla de Dependencia:** el código fuente solo puede apuntar hacia adentro (hacia las políticas de alto nivel).

### Capas y responsabilidades

| Capa | Responsabilidad | Ejemplos |
|------|----------------|---------|
| **Entities** | Reglas de negocio críticas de la empresa | User, Order, Product (con su lógica) |
| **Use Cases** | Reglas de negocio de la aplicación | CreateUser, ProcessPayment, GenerateReport |
| **Interface Adapters** | Convertir datos entre capas | Controllers, Presenters, Gateways |
| **Frameworks & Drivers** | Detalles de implementación | FastAPI, SQLAlchemy, React, PostgreSQL |

---

## SOLID Principles

### S — Single Responsibility Principle
> Una clase debe tener una sola razón para cambiar.

```python
# ❌ MAL — hace demasiado
class User:
    def save_to_db(self): ...
    def send_welcome_email(self): ...
    def generate_report(self): ...

# ✅ BIEN — cada clase tiene una responsabilidad
class User: ...
class UserRepository:
    def save(self, user: User): ...
class UserEmailService:
    def send_welcome(self, user: User): ...
```

### O — Open/Closed Principle
> Abierto para extensión, cerrado para modificación.

```python
# ✅ Usar abstracciones para extender sin modificar
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount: float) -> bool: ...

class StripeProcessor(PaymentProcessor):
    def process(self, amount: float) -> bool: ...

class PayPalProcessor(PaymentProcessor):
    def process(self, amount: float) -> bool: ...
```

### L — Liskov Substitution Principle
> Los subtipos deben ser sustituibles por sus tipos base sin alterar el comportamiento.

```python
# ✅ Cualquier PaymentProcessor puede reemplazar a otro
def checkout(processor: PaymentProcessor, amount: float):
    return processor.process(amount)  # funciona con cualquier implementación
```

### I — Interface Segregation Principle
> Los clientes no deben depender de interfaces que no usan.

```python
# ❌ Interface demasiado grande
class Animal(ABC):
    def fly(self): ...
    def swim(self): ...
    def run(self): ...

# ✅ Interfaces específicas
class Flyable(ABC):
    def fly(self): ...

class Swimmable(ABC):
    def swim(self): ...
```

### D — Dependency Inversion Principle
> Los módulos de alto nivel no deben depender de módulos de bajo nivel. Ambos deben depender de abstracciones.

```python
# ❌ Dependencia directa (acoplado)
class OrderService:
    def __init__(self):
        self.repo = PostgresOrderRepository()  # acoplado a Postgres

# ✅ Inversión de dependencia
class OrderService:
    def __init__(self, repo: OrderRepository):  # depende de abstracción
        self.repo = repo
```

---

## Patrones de Arquitectura

### Repository Pattern
Abstrae el acceso a datos de la lógica de negocio.

```python
from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, id: str) -> User | None: ...

    @abstractmethod
    def save(self, user: User) -> User: ...

class SupabaseUserRepository(UserRepository):
    def find_by_id(self, id: str) -> User | None:
        # implementación con Supabase
        ...

    def save(self, user: User) -> User:
        # implementación con Supabase
        ...
```

### Service Layer
Lógica de negocio separada de los controladores.

```python
class UserService:
    def __init__(self, repo: UserRepository, email_service: EmailService):
        self.repo = repo
        self.email_service = email_service

    def register(self, data: RegisterUserDTO) -> User:
        if self.repo.find_by_email(data.email):
            raise ValueError("Email already exists")

        user = User.create(data)
        saved_user = self.repo.save(user)
        self.email_service.send_welcome(saved_user)
        return saved_user
```

### Factory Pattern
Centraliza la creación de objetos complejos.

```python
class PaymentProcessorFactory:
    @staticmethod
    def create(provider: str) -> PaymentProcessor:
        match provider:
            case "stripe": return StripeProcessor()
            case "paypal": return PayPalProcessor()
            case _: raise ValueError(f"Unknown provider: {provider}")
```

---

## Domain-Driven Design (DDD) — Conceptos clave

| Concepto | Definición | Ejemplo |
|----------|-----------|---------|
| **Entity** | Objeto con identidad única que persiste en el tiempo | User, Order |
| **Value Object** | Objeto sin identidad, definido por sus atributos | Money, Address, Email |
| **Aggregate** | Cluster de entidades tratadas como unidad | Order + OrderItems |
| **Domain Service** | Lógica que no pertenece a ninguna entidad | PricingCalculator |
| **Repository** | Abstracción de persistencia por Aggregate | OrderRepository |
| **Domain Event** | Algo que ocurrió en el dominio | OrderPlaced, PaymentReceived |

---

## Checklist de Arquitectura (Sasha aplica antes de implementar)

```
[ ] ¿Las dependencias apuntan hacia adentro (hacia las entidades)?
[ ] ¿La lógica de negocio está separada de los detalles de infraestructura?
[ ] ¿Cada clase/módulo tiene una sola responsabilidad?
[ ] ¿Se puede cambiar la BD sin tocar la lógica de negocio?
[ ] ¿Se puede cambiar el framework web sin tocar los use cases?
[ ] ¿Las interfaces permiten testear en aislamiento (sin BD real)?
[ ] ¿Las dependencias se inyectan, no se instancian internamente?
[ ] ¿El código expresa el dominio del negocio en su nomenclatura?
```

---

## Estructura de proyecto recomendada (Python/FastAPI)

```
src/
├── domain/
│   ├── entities/          # User, Order, Product
│   ├── value_objects/     # Email, Money, Address
│   ├── repositories/      # Interfaces abstractas
│   └── services/          # Domain services
├── application/
│   ├── use_cases/         # CreateUser, ProcessOrder
│   └── dtos/              # Input/Output data transfer objects
├── infrastructure/
│   ├── repositories/      # Implementaciones concretas (Supabase, Postgres)
│   ├── external/          # APIs externas, email, SMS
│   └── config/            # Settings, env vars
└── presentation/
    ├── api/               # FastAPI routers
    └── schemas/           # Pydantic request/response schemas
```

*Fuente: ComposioHQ Antigravity Skills + The Clean Architecture (Robert C. Martin)*
