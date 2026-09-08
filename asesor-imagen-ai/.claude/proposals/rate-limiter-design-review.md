# Rate Limiter Design Review — Task A1

**Reviewer:** Alejo (Solutions Architect Senior)
**Date:** 2026-05-20
**Gate:** A1 — Pre-coding architectural approval
**Spec source:** `.claude/proposals/rate-limiter-design.md`
**Decision authority:** Alejo (delegated by Jarvis for architectural decisions)

---

## 1. Veredicto

**APROBADO CONDICIONAL**

La arquitectura propuesta es sólida en sus fundamentos: PRE-API blocking, fail-closed semantics, dynamic TTL alineado a la regla de negocio (domingo 23:59 UTC-5) y reconciliación Redis↔Postgres. Sin embargo, hay **4 change requests bloqueantes** y **2 decisiones arquitectónicas pendientes (Q1, Q2)** que Antigravity debe incorporar antes de codear. Una vez aplicados los CRs, Antigravity tiene luz verde sin re-review.

**Justificación corta:** El diseño actual tiene un bug de race-condition en idempotency (SETNX+GET no es atómico), un orden de operaciones invertido (INCR antes de validar el cap permite "off-by-one consumption") y un fallback a Postgres mal modelado (un `SELECT usage_this_week` no garantiza atomicidad bajo concurrencia). Son fixes quirúrgicos, no rediseño.

---

## 2. Criterios de aprobación — checklist

### 2.1 PRE-API blocking — ✅ CUMPLIDO (con ajuste)
- ✅ Validación PRE enqueue del worker (Replicate nunca se llama sin gate).
- ✅ UX correcta: 429 inmediato, sin esperar al worker.
- ⚠️ **Ajuste requerido (CR-1):** El INCR debe usarse en patrón "check-then-increment atómico" vía script Lua o `INCR` + compensación. Tal como está, si el INCR pasa de 3→4 y devuelve 4, se bloquea pero **el counter quedó en 4**, no en 3. La siguiente reconciliación lo verá como "1 sobre el cap" y dispara Sentry falso-positivo cada vez que un usuario topa el cap. Ver CR-1.

### 2.2 Redis key design — ✅ CUMPLIDO
- ✅ Formato `user:{uuid}:tryons:week:{ISO_WEEK}` único por usuario × semana. UUID elimina colisión.
- ✅ TTL dinámico a domingo 23:59 UTC-5 (no hardcoded 7 días). Correcto: usuario que paga lunes no debería esperar 7 días para reset.
- ✅ Fallback a Postgres documentado.
- ⚠️ **Ajuste menor (CR-2):** Documentar explícitamente que `ISO_WEEK` se computa en timezone **UTC-5 (America/Bogota)**, no UTC ni server-local. Riesgo: el usuario que hace try-on viernes 23:00 UTC-5 (= sábado 04:00 UTC) caería en semana ISO siguiente si se computa en UTC. Fix: `now_in_utc_minus_5.isocalendar()`.

### 2.3 Idempotency — ⚠️ CUMPLIDO PARCIAL
- ✅ Header `Idempotency-Key` validado.
- ✅ TTL 24h sobre response cache.
- ✅ Cached response retornado en repeat.
- ❌ **Bloqueante (CR-3):** El patrón `SETNX lock` + `GET response` + `INCR` no es atómico. Ventana de race: dos requests simultáneas con la misma key, ambas ven `lock=null`, ambas hacen SETNX, una gana el lock pero la otra **no espera** y procede a INCR. Resultado: double-increment posible. Fix: usar **Lua script** que en una sola roundtrip haga `EXISTS response → return cached | SET lock NX EX 5 → proceed`. Ver CR-3.

### 2.4 Fallback strategy — ⚠️ CUMPLIDO PARCIAL
- ✅ Timeout Redis 100ms (no bloqueo indefinido).
- ✅ Logging + Sentry.
- ✅ Fail-closed (503 vs fail-open).
- ❌ **Bloqueante (CR-4):** El fallback a Postgres `SELECT usage_this_week` no es atómico bajo concurrencia. Dos requests concurrentes leerían el mismo valor (ej. 2) y ambas pasarían el gate, llevando el counter real a 4. Fix: usar `UPDATE users SET usage_this_week = usage_this_week + 1 WHERE id = $1 AND usage_this_week < 3 RETURNING usage_this_week;` — la condición en el WHERE garantiza atomicidad. Si `RETURNING` retorna 0 filas, es 429. Ver CR-4.

---

## 3. Respuestas a preguntas abiertas

### Q1 — ¿slowapi obligatorio o middleware custom?

**Decisión: HÍBRIDO — slowapi para endpoints estándar, middleware custom para `POST /try-ons`.**

**Justificación:**

| Criterio | slowapi puro | Custom puro | Híbrido (recomendado) |
|----------|--------------|-------------|----------------------|
| Cobertura del cap 3/week con TTL dinámico domingo 23:59 UTC-5 | ❌ No soporta TTL custom por key | ✅ Full control | ✅ Full control donde importa |
| Idempotency con Lua script | ❌ No nativo | ✅ Nativo | ✅ Nativo en endpoint crítico |
| Boilerplate para `/auth/login`, `/users/me`, `/health` (rate limits triviales) | ✅ Decorator `@limiter.limit("10/minute")` | ❌ Reinventar middleware | ✅ slowapi cubre 80% gratis |
| Bug surface | Bajo en rutas simples | Alto si todo es custom | Mínimo (custom solo donde aporta) |
| Mantenimiento futuro | Comunidad | Equipo solo | Comunidad + 1 archivo custom |

**Implementación:**
- `slowapi.Limiter` global con `@limiter.limit(...)` para todos los endpoints excepto `POST /try-ons`.
- `TryOnRateLimitMiddleware` custom (un solo archivo, ~120 LOC) montado **solo en la ruta `/try-ons`**, con Lua script para INCR+idempotency atómicos.
- Razón clave: el cap 3/week con TTL hasta domingo 23:59 UTC-5 + idempotency con cache de response **no es soportable** con slowapi sin parchearlo. Mejor aislar la lógica custom a la ruta crítica que monkey-patchear slowapi.

**Veredicto Q1:** Híbrido. No es "slowapi + custom INCR para todo" como decía la spec — es **slowapi para lo trivial, custom middleware aislado para `/try-ons`**.

---

### Q2 — ¿503 fail-closed aplica a ALL endpoints o solo POST /try-ons?

**Decisión: política por clase de endpoint, no global.**

| Clase de endpoint | Comportamiento bajo Redis down | Razón |
|-------------------|-------------------------------|-------|
| `POST /try-ons` (mutación + costo Replicate $0.024) | **503 fail-closed** | Proteger margen $233K/yr. Mejor degradar UX 30s que leak cap |
| `GET /users/me/usage` (counter read) | **200 con valor stale de Postgres + header `X-Data-Freshness: stale`** | Es solo display; falsear el contador a 503 rompe el dashboard del usuario. Postgres tiene el valor (eventual ~hourly via reconciliación) |
| `GET /health`, `GET /healthz`, `GET /ready` | **200 siempre** (Redis es dependencia opcional para liveness) | Health checks deben reflejar **liveness del proceso**, no de dependencias. Si Redis down → reportar en `/ready` (readiness), no en `/health` (liveness). K8s/Railway dependen de esto para no matar el pod |
| `GET /ready` (readiness probe) | **503 si Redis down >30s** | Indica al orquestador que no rutee tráfico nuevo, pero no mata el pod |
| Mutaciones sin costo externo (`POST /users/me/preferences`) | **200 con rate limit bypass + log warning** | Sin costo externo, no hay margen que proteger. Mejor disponibilidad que rigor |
| Otras lecturas (`GET /try-ons/{id}`) | **200 + bypass rate limit + log** | Read-only, sin costo, sin riesgo de leak |

**Principio rector:** *Fail-closed donde hay dinero en juego; fail-open con observabilidad donde no.*

**Veredicto Q2:** La spec actual ("503 solo para POST /try-ons") está casi correcta pero **debe explicitar el comportamiento de los otros endpoints** (CR-5, no bloqueante). Sin esto, Antigravity podría aplicar 503 global por defecto y romper health checks → pods matados en producción.

---

## 4. Change Requests para Antigravity

### CR-1 (BLOQUEANTE) — Atomic check-then-increment vía Lua
**Problema:** `INCR` siempre incrementa. Si el cap es 3 y el usuario está en 3, el INCR lo lleva a 4 antes de chequear. Resultado: counter inflado, falsos positivos en reconciliación.

**Fix:** Lua script en `app/services/rate_limit/scripts/incr_with_cap.lua`:
```lua
-- KEYS[1] = counter key, ARGV[1] = cap, ARGV[2] = ttl_seconds
local current = tonumber(redis.call('GET', KEYS[1]) or '0')
if current >= tonumber(ARGV[1]) then
  return {0, current}  -- denied, current value
end
local new = redis.call('INCR', KEYS[1])
if new == 1 then redis.call('EXPIRE', KEYS[1], ARGV[2]) end
return {1, new}  -- allowed, new value
```
Garantiza atomicidad sin off-by-one.

### CR-2 (MENOR) — Timezone explícito para ISO_WEEK
**Fix:** Computar `ISO_WEEK` como `datetime.now(ZoneInfo("America/Bogota")).isocalendar()`. Documentar en docstring del helper. Test unitario: viernes 23:30 UTC-5 y sábado 03:30 UTC deben producir la misma semana ISO.

### CR-3 (BLOQUEANTE) — Idempotency atómico vía Lua
**Problema:** SETNX + GET separados → race condition.

**Fix:** Lua script `idempotency_check.lua` que en una roundtrip:
1. `GET idempotency:{key}:response` → si existe, retorna cached.
2. Si no, `SET idempotency:{key}:lock 1 NX EX 5` → si gana lock, retorna `proceed`.
3. Si no gana lock → retorna `retry_in_50ms` (cliente espera y reintenta una vez; segunda vez espera el response).

### CR-4 (BLOQUEANTE) — Fallback Postgres atómico
**Fix:** Reemplazar `SELECT usage_this_week` por:
```sql
UPDATE users
   SET usage_this_week = usage_this_week + 1,
       last_tryon_at = NOW()
 WHERE id = $1
   AND usage_this_week < 3
   AND week_iso = $2
 RETURNING usage_this_week;
```
0 filas retornadas → 429. >0 filas → proceed. Atomicidad garantizada por row lock de Postgres.

Requiere migración: añadir columna `week_iso text NOT NULL DEFAULT to_char(now(), 'IYYY-IW')` con trigger de reset semanal (o computar en aplicación).

### CR-5 (NO BLOQUEANTE) — Documentar política por endpoint
**Fix:** Antigravity añade tabla §5 de la spec con los 6 casos de Q2. Sin esto, riesgo de aplicar fail-closed global por defecto.

---

## 5. Risk Assessment

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Lua script con bug en producción | Media | Alto (gate completamente roto) | Tests unitarios + integración del Lua antes de deploy. Code review obligatoria de los .lua por Sasha |
| Redis eviction borra counter activo | Baja (Redis configurado `noeviction` para keys con TTL) | Medio (counter resetea silencioso, usuario gana 1-3 extra) | Reconciliación horaria (ya en spec §6). Verificar que `maxmemory-policy = volatile-ttl` en Redis config |
| Reloj del server desincronizado → ISO_WEEK incorrecto | Baja | Alto (reset semanal disparado en momento erróneo) | NTP obligatorio en hosts. Health check valida `abs(now() - ntp_now()) < 1s` |
| Idempotency-Key colisión entre usuarios (key reutilizada por cliente buggy) | Baja | Alto (usuario A ve respuesta de usuario B) | Namespacear: `idempotency:{user_id}:{key}` en vez de `idempotency:{key}` global. **Añadir a CR-3** |
| Postgres fallback genera contención de row lock bajo carga | Media (solo bajo Redis-down sostenido >5min) | Medio (latencia sube, 503 propagado) | Circuit breaker: tras 50 fallbacks/min, retornar 503 sin tocar Postgres. Reduce contención |
| Worker reintenta job idempotente y double-bills Replicate | Media | Alto ($) | Idempotency en `replicate_worker` usando job-id, no solo HTTP-layer. Sasha lo gestiona en T4 |

**Adición a CR-3:** Namespacear `Idempotency-Key` por user_id. Sin esto, un cliente malicioso podría leer responses de otros usuarios si adivina su UUID. **Esto sube CR-3 a severidad CRÍTICA.**

---

## 6. Decisiones finales (Alejo authority)

1. ✅ **Stack:** slowapi (rutas triviales) + custom `TryOnRateLimitMiddleware` (ruta crítica). No "slowapi + custom INCR para todo".
2. ✅ **Fail-closed policy:** Por clase de endpoint (tabla §3 Q2). No global.
3. ✅ **Atomicidad:** Lua scripts obligatorios para INCR+cap e Idempotency. No secuencias separadas.
4. ✅ **Idempotency namespace:** `idempotency:{user_id}:{key}`. No global.
5. ✅ **Timezone:** `America/Bogota` explícito en ISO_WEEK helper.
6. ✅ **Postgres fallback:** `UPDATE ... WHERE usage_this_week < 3 RETURNING ...`, no `SELECT`.

---

## 7. Comunicación a Antigravity

**Mensaje sugerido para Jarvis → Antigravity:**

> APROBADO CONDICIONAL. Procede con A1 incorporando 4 change requests bloqueantes (CR-1, CR-3, CR-4, + namespace idempotency) y 1 no bloqueante (CR-5). CR-2 es polish. No requiere re-review por Alejo si los CRs se aplican literal. Sasha valida los Lua scripts antes de merge. ETA sin cambios: A1 codeable hoy MAR 20, listo MIE 21 EOD.

---

## 8. Anexo — Definition of Done para A1

Para que Alejo cierre el gate sin re-review:

- [ ] CR-1 implementado: Lua `incr_with_cap.lua` + tests unitarios (cap=3, cap=0, edge: race de 5 requests concurrentes).
- [ ] CR-2 implementado: helper `current_iso_week_bogota()` + test de borde viernes 23:30 UTC-5.
- [ ] CR-3 implementado: Lua `idempotency_check.lua` + namespace `{user_id}:{key}` + test de race.
- [ ] CR-4 implementado: migración `week_iso` + UPDATE con WHERE clause + test de race con 5 conexiones Postgres simultáneas.
- [ ] CR-5 implementado: tabla de política fail-closed en `rate-limiter-design.md` §5.
- [ ] Métricas Prometheus de spec §7 expuestas en `/metrics`.
- [ ] Sentry alert configurada en `rate_limit_redis_fallback_total > 10/min`.
- [ ] Load test (Antigravity A5): 100 RPS sostenido 5min, p95 < 50ms, 0 double-increments validados contra Postgres.

Fin del review.
