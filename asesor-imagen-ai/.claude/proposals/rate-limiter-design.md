# Rate Limiter Design Proposal (Task A1)

## 1. Architecture Overview
The rate limiting layer operates **PRE-API call**, functioning as a critical defense mechanism against abuse, double-billing, and unnecessary external API costs. It acts as a middleware wrapping FastAPI's request lifecycle.

The primary engine is `slowapi` paired with a fast Redis backend (`redis.prd.supabase.co`). For dynamic or custom limits (like the hard 3/week cap resetting specifically on Sunday 23:59 UTC-5), we augment `slowapi` with a custom Redis `INCR` strategy inside the `RateLimiterMiddleware`.

## 2. PRE-API Blocking Flow
When a request hits `POST /try-ons`:
1. **Idempotency Check**: The middleware extracts the `Idempotency-Key` header. It checks `idempotency:{key}` in Redis. If a cached response exists, it short-circuits and returns 200 without incrementing usage.
2. **Rate Limit Evaluation**: 
   - Generates the dynamic key: `user:{uuid}:tryons:week:{YYYY-WW}`.
   - Executes a Redis `INCR`. If `INCR` > 3, it blocks the request, sets `X-RateLimit-*` headers, and returns `429 Too Many Requests` (Body: "Weekly cap reached").
   - If Redis is down, it falls back to a synchronous Postgres `SELECT usage_this_week FROM users` (Layer 2 defense).
3. **Endpoint Execution**: If permitted, the FastAPI route handles the request and ARQ enqueues the worker logic.
4. **Result Storage**: Upon successful enqueue or completion, the `idempotency:{key}` is set with the final response JSON (TTL 24h).

*Note: The workers (`vision_worker`, `replicate_worker`, `claude_worker`) process jobs outside of the HTTP context. They will not be blocked by this HTTP middleware, ensuring background robustness. Furthermore, workers enforce RLS via `admin.trusted().table(...)` instead of user context.*

## 3. Redis Key Design & TTL
- **Standard limits**: Uses default `slowapi` key format `LIMITER:{endpoint}:{user_id}`.
- **Weekly Try-on Cap**: `user:{user_id}:tryons:week:{ISO_WEEK}`.
  - The TTL is calculated dynamically to expire exactly on Sunday at 23:59 UTC-5 of the current week. 
  - This prevents accumulating stale keys and guarantees a clean start for the next week.
- **Idempotency**: `idempotency:{uuid}` with a fixed TTL of 24h.

## 4. Idempotency Logic
- **Header**: `Idempotency-Key: <uuid>`.
- **Validation**:
  - The middleware intercepts requests specifying this header.
  - Attempts `SETNX idempotency:{uuid}:lock "1"` (TTL 5s) to prevent concurrent races on the identical key.
  - Checks if `idempotency:{uuid}:response` exists.
  - If it exists, returns the cached response bypassing rate limit increments.
  - If not, processes request, caches the status code and body in Redis, and removes the lock.

## 5. Fallback & Graceful Degradation Strategy
If the Redis `INCR` times out (timeout > 100ms) or errors:
- A `rate_limit_redis_fallback` exception is logged and sent to Sentry.
- The middleware degrades to Postgres via `fallback_to_postgres(user_id, endpoint)`.
- It executes `SELECT usage_this_week FROM users`. If this also fails, the system responds with a `503 Service Unavailable`. We default to fail-closed (`503`) rather than fail-open to protect the $233K margin target from potential abuse spikes during outages.

## 6. Counter Reconciliation
A Scheduled ARQ Job (`reconcile_counters`) runs every hour to ensure consistency between Redis and Postgres:
1. Queries `keys user:*:tryons:week:CURRENT_WEEK`.
2. Compares the values against `SELECT id, usage_this_week FROM users`.
3. If a discrepancy > 1 is detected, Sentry alerts ops. Postgres is used as the source of truth to overwrite Redis if eviction corrupted the counter.

## 7. Metrics & Observability
Prometheus counters will track the rate limit efficacy:
- `rate_limit_hits_total{endpoint, user_tier}`
- `rate_limit_redis_fallback_total`
- `rate_limit_redis_latency_seconds{p50, p95, p99}`
- `rate_limit_idempotency_cache_hits`
