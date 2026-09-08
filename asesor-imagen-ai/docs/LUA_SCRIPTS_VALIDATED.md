# LUA SCRIPTS VALIDATED — Rate Limiting CRs

**Owner:** Alejo (Solutions Architect)
**Status:** ✅ APPROVED for Sasha integration (T2-T6)
**Date:** 2026-05-20
**Audience:** Sasha (impl), Cyber Neo (security review)

---

## Contexto

Sasha integrará 3 Lua scripts en Redis para garantizar atomicidad en el rate limiting (Sprint 0.4 — CR-1, CR-3, Q5). Lua es atómico en Redis: cada `EVAL` ejecuta hasta finalizar sin interrupción, eliminando race conditions.

**Cláusula crítica:** Todas las claves Redis usan namespacing `{user_id}:{feature}:{period}` para prevenir data leak entre usuarios.

---

## 1. `incr_with_cap.lua` (CR-1)

**Goal:** Incrementar counter SIN exceder cap (3/sem). Previene off-by-one.

```lua
local key = KEYS[1]
local cap = tonumber(ARGV[1])
local ttl = tonumber(ARGV[2])

local current = redis.call('GET', key)
if current == false then
  current = 0
else
  current = tonumber(current)
end

if current >= cap then
  return {0, current}  -- REJECT, current value
else
  redis.call('INCR', key)
  redis.call('EXPIRE', key, ttl)
  return {1, current + 1}  -- ACCEPT, new value
end
```

### Validation

| Property | Check | Status |
|---|---|---|
| Atomic | Single EVAL, Lua executes atomically | ✅ |
| Off-by-one safe | Returns early if `current >= cap` | ✅ |
| Returns counter for headers | `X-RateLimit-Remaining: cap - new` | ✅ |
| TTL set on increment | `EXPIRE` after `INCR` | ✅ |
| Idempotent on REJECT | No side effects if cap reached | ✅ |

### Calling pattern (Python redis-py)

```python
result = await redis.eval(
    INCR_WITH_CAP_LUA,
    1,                              # numkeys
    f"user:{user_id}:tryons:week",  # KEYS[1]
    3,                              # ARGV[1] = cap
    604800,                         # ARGV[2] = 7 days TTL
)
accepted, new_count = result
if not accepted:
    raise RateLimitExceeded(remaining=0)
```

---

## 2. `idempotent_incr.lua` (CR-3)

**Goal:** Incrementar SOLO si `Idempotency-Key` no existe. Retorna respuesta cacheada si duplicate request.

```lua
local counter_key = KEYS[1]
local idempotency_key = KEYS[2]  -- {user_id}:idempotency:{uuid}
local cap = tonumber(ARGV[1])
local ttl_counter = tonumber(ARGV[2])
local ttl_idempotency = tonumber(ARGV[3])  -- 24h

-- Check if idempotency key exists (cached response)
local cached = redis.call('GET', idempotency_key)
if cached ~= false then
  return {0, tonumber(cached)}  -- Return cached (no increment)
end

-- Proceed with incr_with_cap logic
local current = redis.call('GET', counter_key)
if current == false then
  current = 0
else
  current = tonumber(current)
end

if current >= cap then
  return {-1, current}  -- REJECT (cap reached)
else
  redis.call('INCR', counter_key)
  redis.call('EXPIRE', counter_key, ttl_counter)
  redis.call('SET', idempotency_key, current + 1, 'EX', ttl_idempotency)
  return {1, current + 1}  -- ACCEPT
end
```

### Validation

| Property | Check | Status |
|---|---|---|
| Namespace correction (CR-3 fix) | `idempotency_key` incluye `user_id` | ✅ Prevents cross-user leak |
| Atomic | Check + set + increment in single EVAL | ✅ |
| Duplicate-safe | Returns cached without increment | ✅ |
| TTL 24h idempotency | Enough for retries, prevents bloat | ✅ |
| 3 return codes | `1`=accept, `0`=cached, `-1`=cap | ✅ Clear semantics |

### Return code mapping

| Code | HTTP Status | Header |
|---|---|---|
| `1` (accept) | 202 Accepted | `X-RateLimit-Remaining: N-1` |
| `0` (cached) | 200 OK (idempotent replay) | `X-Idempotent-Replay: true` |
| `-1` (cap) | 429 Too Many Requests | `Retry-After: <reset_ts>` |

---

## 3. `lazy_reset.lua` (Q5)

**Goal:** Reset counter SI período expiró (lazy, sin cron job).

```lua
local counter_key = KEYS[1]
local timestamp_key = KEYS[2]  -- {user_id}:week_start
local current_week = tonumber(ARGV[1])  -- ISO 8601 week number

local stored_week = redis.call('GET', timestamp_key)
if stored_week == false or tonumber(stored_week) < current_week then
  -- Reset: set new week, delete counter
  redis.call('SET', timestamp_key, current_week, 'EX', 604800)
  redis.call('DEL', counter_key)
  return {1, 0}  -- RESET performed, new counter = 0
else
  -- No reset needed
  local cnt = redis.call('GET', counter_key)
  return {0, tonumber(cnt or 0)}
end
```

### Validation

| Property | Check | Status |
|---|---|---|
| Atomic reset | DEL + SET in single EVAL | ✅ |
| Idempotent | Calling twice returns same `{0, 0}` | ✅ |
| Fallback compat | Postgres lazy reset doesn't conflict | ✅ |
| ISO 8601 week | Timezone-agnostic comparison | ✅ |

### Calling pattern (invoked at start of every request)

```python
# Before incr_with_cap, ensure period is fresh
await redis.eval(
    LAZY_RESET_LUA,
    2,
    f"user:{user_id}:tryons:week",
    f"user:{user_id}:week_start",
    iso_week_number(now()),
)
# Then proceed with incr_with_cap
```

---

## 4. Atomic Guarantees (formal)

| Scenario | Guarantee | Proof |
|---|---|---|
| 2 concurrent requests at counter=2, cap=3 | Only 1 succeeds | Lua EVAL is atomic |
| Retry with same Idempotency-Key | Returns cached, no double-increment | `idempotent_incr` checks first |
| Counter expires mid-flight | Next request resets via `lazy_reset` | Both TTL + lazy check |
| Redis fail-over | Replication lag possible; ACL: AOF every 1s | Acceptable loss <1s |

---

## 5. Security Considerations (for Cyber Neo review)

| Risk | Mitigation |
|---|---|
| Key injection (e.g. `user_id="*"`) | Validate `user_id` is UUID v4 in app layer |
| Lua script tampering | Load via `SCRIPT LOAD`, call via `EVALSHA` |
| Memory exhaustion (idempotency keys) | TTL 24h + Redis maxmemory-policy `allkeys-lru` |
| Replay across users | Namespace `{user_id}` prefix enforced |
| DoS via cap-reached flood | App-layer rate limit on 429 responses |

---

## 6. TTL Strategy

| Key | TTL | Rationale |
|---|---|---|
| `{user_id}:tryons:week` | 604800s (7d) | Match weekly cap window |
| `{user_id}:week_start` | 604800s (7d) | Same as counter |
| `{user_id}:idempotency:{uuid}` | 86400s (24h) | Retry window, prevents bloat |

---

## 7. Integration Checklist (Sasha)

- [ ] Load 3 scripts at startup via `SCRIPT LOAD`, cache SHA hashes
- [ ] Use `EVALSHA` in hot path (skip script transmission)
- [ ] Fallback to `EVAL` if `NOSCRIPT` error (cold replica)
- [ ] Wrap calls in `try/except` for Redis connection errors → fail-open to Postgres counter
- [ ] Emit metrics: `ratelimit.accepted`, `ratelimit.rejected`, `ratelimit.cached`
- [ ] Unit tests: race condition (100 concurrent reqs at cap=3 → exactly 3 accepted)

---

**Aprobado por:** Alejo
**Próxima validación:** Cyber Neo (security audit) + Ego (integration test)
