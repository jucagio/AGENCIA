# Decisiones Pendientes — Backend Asesor de Imagen AI

**Última actualización:** 2026-04-25
**Owner:** Sasha (Backend) | **Revisores:** Alejo (Arquitectura), Cyber Neo (Seguridad), Jarvis (CEO)
**Contexto:** Tracking de decisiones diferidas durante Sprint 0 — Entrega 0.1 (Foundation).

---

## 1. Estado de los 5 ADRs de Alejo (auditoría 2026-04-25)

| ADR | Tema | Status 0.1 | Acción 0.2 / 0.3 |
|-----|------|------------|------------------|
| ADR-001 | Supabase Auth nativo (no custom JWT) | ⚠️ Parcial — config preparada, código legacy intacto | Eliminar `security.py`, implementar `supabase_auth.py` con JWKS |
| ADR-002 | Async-first (ARQ + Redis) | ✅ Config + dependencias listas | Worker module + Realtime push (Entrega 0.3) |
| ADR-003 | Idempotency-Key obligatoria | ⚠️ Middleware con presence check, sin store | Tabla `idempotency_keys` + replay logic (Entrega 0.2) |
| ADR-004 | Caching de try-ons por hash | 📝 Documentado solamente | Implementar en `try_on_service` (Entrega 0.3) |
| ADR-005 | Storage Supabase + R2 CDN | 📝 boto3+pillow en requirements, config R2 lista | Module `storage_service` (Entrega 0.3) |

---

## 1.5 Correcciones Urgentes (Post-Sprint 0.1)

- **Supabase-py en Windows:** La librería oficial `supabase-py` arrastra dependencias problemáticas en Windows (`pyiceberg` compila rust extensions que fallan). 
  - **Decisión:** Para evitar mockear Supabase en producción y no bloquear el desarrollo local sin Docker, se reemplazó `supabase-py` por `postgrest-py` nativo en `app/core/database.py`. Storage y Auth se manejarán vía APIs separadas (Auth vía JWKS, Storage vía boto3/S3 config como dicta ADR-005).

---

## 2. Issues encontrados durante auditoría del repo (2026-04-25)

### 2.1 Bloqueantes (corregidos en esta entrega)
1. **`config.py` no tenía `get_settings()`** — `security.py` y `middleware.py` lo importaban → el backend NO arrancaba. ✅ Corregido.
2. **Mismatch de naming entre módulos** — `config.py` exponía `secret_key` (snake), pero `security.py` referenciaba `SECRET_KEY` (SCREAMING). ✅ Normalizado a `SCREAMING_SNAKE_CASE` en todo el config (alineado con env vars).
3. **`config.py` no exponía `is_production` ni `allowed_origins_list`** que `middleware.py` usaba. ✅ Añadidos como `@computed_field`.
4. **`main.py` era stub** — sin router, sin middleware nuevo, sin lifespan, sin exception handlers. ✅ Reescrito con factory pattern + lifespan.
5. **Faltaba `app/core/database.py`** — referenciado por el plan pero inexistente. ✅ Creado con clientes async (admin + user-scoped).

### 2.2 Detectados, no bloqueantes
- **Versiones de dependencias desactualizadas** — `requirements.txt` pineaba FastAPI 0.104, pydantic 2.5, supabase 2.0.1 (octubre 2024). ✅ Actualizadas a versiones verificadas vía web search (FastAPI 0.136.0, supabase 2.28.3, ARQ 0.28.0 — todas abril 2026).
- **`pyproject.toml` declara `target-version = "py312"` para ruff pero `requires-python = ">=3.10"`** — inconsistencia menor. **PENDIENTE:** ¿pinear Python 3.12 o 3.13 para producción? (cache de bytecode en Docker, performance pattern matching). Recomendación Sasha: `python:3.12-slim` en Dockerfile.
- **Cache `.cpython-314.pyc` detectada en `__pycache__/`** — alguien ejecutó con Python 3.14 (alpha). No es problema funcional, pero **PENDIENTE:** alinear versión Python entre dev/CI/prod.
- **Migrations existentes (`001_initial_schema.sql`, `002_storage_buckets.sql`)** — NO leídas en esta entrega. El plan dice eliminar `users.password_hash` (ADR-001) y crear tabla `profiles`. **DECISIÓN 0.2:** ¿reescribimos `001_initial_schema.sql` en sitio o creamos `003_supabase_auth_migration.sql`? Recomendación Sasha: reescribir 001 si nadie lo aplicó aún en Supabase remoto; si ya está aplicado → migration nueva.

### 2.3 Decisiones diferidas explícitamente
- **No se tocaron migrations** (fuera de scope 0.1).
- **No se crearon models / schemas / repositories / endpoints** (fuera de scope 0.1).
- **No se actualizó Dockerfile** (no existía; queda para 0.4 CI/CD).
- **No se reescribieron tests existentes** — `tests/` no auditado en 0.1. **PENDIENTE 0.2:** revisar si `tests/` referencia atributos viejos del config (`settings.secret_key` snake) y refactorizar.

---

## 3. ADR-001 (Supabase Auth) — Plan de migración 0.1 → 0.2

**Estado actual (0.1):**
- `app/core/security.py` mantiene bcrypt + custom HS256 JWT (LEGACY).
- `app/config.py` expone tanto `SECRET_KEY` (legacy) como `SUPABASE_*` y `supabase_jwks_url` (nuevo).
- `app/core/middleware.py` tiene `auth_middleware` como pass-through con docstring del contrato.
- `app/core/database.py` tiene `create_user_scoped_client(user_jwt)` listo para recibir el JWT validado.

**Plan Entrega 0.2:**
1. Crear `app/core/supabase_auth.py`:
   - `JWKSCache` async (TTL 600s — ver guidance Supabase: "no cache too long").
   - `validate_supabase_jwt(token: str) -> SupabaseUser` con `PyJWT[crypto]`, algoritmo `ES256`.
   - Verificar claims: `aud="authenticated"`, `iss=<supabase_url>/auth/v1`, `exp`.
2. Implementar lógica real en `auth_middleware`:
   - Skip `PUBLIC_ROUTES` y `OPTIONS`.
   - Extraer `Authorization: Bearer <token>`.
   - `request.state.user = await validate_supabase_jwt(token)`.
   - 401 con `AuthenticationError` si falla.
3. Crear dependency `get_current_user` y `get_supabase_client` para endpoints.
4. **Eliminar** `app/core/security.py` (deprecation completa).
5. Migration SQL: drop `users.password_hash`, rename `users` → `profiles` con FK a `auth.users(id)`.

**Referencias verificadas (web search 2026-04-25):**
- JWKS endpoint: `https://<project>.supabase.co/auth/v1/.well-known/jwks.json`
- Algorithm: ES256 (asymmetric, no shared secret)
- Cache TTL: ≥20 min entre rotación de claves; recomendado <10 min en app

**Pregunta abierta para Alejo:**
- ¿El proyecto Supabase ya tiene rotación de keys configurada? Si todavía está en HS256 legacy de Supabase, hay que migrarlo en el dashboard antes de poder usar JWKS.

---

## 4. ADR-003 (Idempotency-Key) — Plan 0.2

**Implementación 0.2:**
1. Migration SQL: tabla `idempotency_keys (key TEXT PRIMARY KEY, user_id UUID, request_hash TEXT, response JSONB, status_code INT, created_at TIMESTAMP, expires_at TIMESTAMP)`.
2. Reemplazar `idempotency_middleware` placeholder:
   - Calcular `request_hash = sha256(method + path + body)`.
   - Lookup `(user_id, key)` en tabla.
   - Si existe + mismo hash → retornar response cacheada.
   - Si existe + hash diferente → 422 (key reuse con payload distinto = ataque).
   - Si no existe → ejecutar request, guardar response.
3. **Decisión pendiente:** ¿usar Redis (ARQ ya está) o tabla Postgres? Recomendación Sasha: **Postgres** (durabilidad, transaccionalidad con la operación protegida; Redis es eventual). Cost: 1 SELECT extra por POST cost-sensitive — aceptable.

---

## 5. Preguntas para Cyber Neo (auditoría seguridad pre-Entrega 0.2)

1. ¿`bcrypt` rounds=12 sigue OWASP 2026? (último update sugiere 14 para hardware moderno). Si subimos a 14, costo CPU ~4x — pero como migramos a Supabase Auth en 0.2, probablemente moot.
2. ¿`X-XSS-Protection: 0` correcto para 2026? (CSP es el reemplazo, pero aún no tenemos CSP — aplica para frontend Brook).
3. ¿`Cache-Control: no-store` global es muy agresivo? Endpoints de imágenes públicas (after R2 CDN, Entrega 0.3) deben permitir cache. Excluirlos en middleware o setear per-endpoint.
4. ¿Deberíamos añadir `Content-Security-Policy` desde el backend o lo deja al frontend? (la API solo sirve JSON; CSP afecta más a Brook).

---

## 6. Próximos pasos (Entrega 0.2 — Data Layer)

1. Migrations refactor (eliminar `password_hash`, crear `profiles`, RLS 32 policies).
2. Models / Schemas (Pydantic v2) por dominio: profile, wardrobe, body_analysis, try_on, recommendation, subscription.
3. Repository base + repos específicos (acceso a Supabase via cliente async).
4. `app/core/supabase_auth.py` con validación JWKS real.
5. Refactor `tests/` para nuevos nombres de settings.
6. Smoke test E2E: registrar user en Supabase Auth → llamar endpoint protegido → validar RLS.

---

**Firma Sasha:** Documento vivo. Actualizar al cerrar cada entrega del Sprint 0.

---

## 7. Sprint 0.2 — Cambios + Decisiones (2026-05-05 → 2026-05-12)

### 7.1 Migration 003 vs 004 — Source of Truth

**Decisión:** Migration **004** (`004_consolidated_schema_v2.sql`) es el source of truth para el schema completo de 12 tablas.

**Rationale:**
- Migration 003 (`003_adr001_profiles_migration.sql`) es el camino incremental para producción (upgrade desde un Supabase con datos).
- Migration 004 asume DB vacía o entorno reproducible (CI, staging fresh clone). Es lo que Sasha y Brook usan en dev local.
- En producción futura, si hay datos reales, se aplicará 003 (o un equivalente incremental), NO 004 (que tiene `DROP TABLE CASCADE`).
- Migration 004 ahora está protegida con `CREATE TABLE IF NOT EXISTS` y `DROP TRIGGER IF EXISTS` para mayor idempotencia.
- Se creó `004_consolidated_schema_v2_down.sql` como rollback simétrico.

### 7.2 AdminClient Guard Pattern (Cyber Neo H3)

**Implementación:**
- `AdminClient` envuelve el cliente PostgREST service-role.
- `.with_user_check(user_id, *, id_column="user_id")` inyecta `.eq(id_column, str(user_id))` en cada `.table()`.
- `.trusted()` — sin filtro de usuario. Solo para workers ARQ y webhooks verificados.
- `.table()` directo levanta `PermissionDeniedError` siempre.

**Decisión `id_column`** (H5):
- La tabla `profiles` usa el UUID del usuario como PK (`id`), sin columna `user_id` separada.
- `ProfileRepository` llama `.with_user_check(user_id=uid, id_column="id")`.
- El resto de tablas usan el default `id_column="user_id"`.

**Decisión `schema()`** (M1):
- `_BoundAdminClient.schema()` ahora retorna un **nuevo** `_BoundAdminClient` preservando `user_id`, `id_column`, y `trusted` flags.
- Esto evita que un cambio de schema anule el guard de user_id.

### 7.3 Tests con Mocks — Decisión Consciente para 0.2

**Decisión:** Los tests de 0.2 (unit) usan `unittest.mock`. Los tests de integración contra Supabase real quedan para 0.3+.

**Rationale:**
- En 0.2 no hay Supabase de staging configurado en CI.
- Los mocks validan la **lógica del guard** (inyección de filtros, ownership checks), que es lo crítico de seguridad.
- La integración real (tabla existe, FK funciona, RLS bloquea correctamente) se valida manualmente en Supabase dashboard.

**Mitigación:**
- Se añadió `tests/integration/test_repos_real_schema.py` — sin DB real, parsea el SQL de migration 004 con regex para verificar que los `_table` de cada repo coincidan con las tablas definidas. Esto hubiera capturado el bug H4 (`body_analyses` vs `body_analysis`).

### 7.4 Repositorios — 9 repos implementados

| Repo | Tabla | Nota |
|------|-------|------|
| `ProfileRepository` | `profiles` | id_column="id" (H5) |
| `WardrobeRepository` | `wardrobe_items` | soft-delete |
| `BodyAnalysisRepository` | `body_analysis` | H4: era body_analyses |
| `RecommendationRepository` | `recommendations` | |
| `RecommendationItemRepository` | `recommendation_items` | H6: owner check |
| `TryOnRepository` | `try_ons` | |
| `SubscriptionRepository` | `subscriptions` | |
| `UserStyleProfileRepository` | `user_style_profile` | nuevo en patch |
| `UsageCounterRepository` | `usage_counters` | L1: stored proc |

### 7.5 Security Findings Aplicados (patch 2026-05-12)

| ID | Descripción | Fix |
|----|-------------|-----|
| H4 | `body_analyses` → `body_analysis` | repos.py + docstring |
| H5 | AdminClient no soportaba tablas sin columna `user_id` | `id_column` param |
| H6 | RecommendationItem no verificaba ownership del padre | `_verify_recommendation_owner()` |
| M1 | `_BoundAdminClient.schema()` rompía el guard | retorna nuevo `_BoundAdminClient` |
| M4 | `audit_log` policy permitía writes anónimos | policy eliminada |
| M6 | `usage_counters` INSERT/UPDATE/DELETE por usuario | policies eliminadas |
| L1 | `increment()` no era atómico | stored proc `increment_usage()` en migration 004 |

**Pendiente 0.3:** Activar `.rpc("increment_usage", {...})` en `UsageCounterRepository.increment()` una vez aplicada migration 004 a Supabase remoto. Ver TODO en repos.py.

