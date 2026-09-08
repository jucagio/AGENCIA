# Workers Integration Guide

> Sprint 0.5 — T6. Owner: Sasha (Backend & Security). Audience: Brook (frontend), Cinthya (automation), on-call engineers.

This is the operational manual for the worker layer of `asesor-imagen-ai`. It explains the FSM, the cache, the tier routing, what to do when something breaks, and how to deploy the migration that ships with this sprint.

---

## 1. Architecture overview

```
                    Mobile / Web (Brook)
                            │ POST /api/v1/try-ons (Idempotency-Key required)
                            ▼
              ┌─────────────────────────────┐
              │ FastAPI request handler     │
              │  - auth_middleware          │
              │  - rate_limit_middleware    │  ← weekly cap (3/sem free)
              │  - idempotency_middleware   │
              └──────────────┬──────────────┘
                             │
                             ▼
              ┌─────────────────────────────┐
              │ TryOnService.create_try_on  │
              │  - resolves plan → tier     │
              │  - SHA256 cache key         │
              │  - WARM cache fast path     │
              │  - INSERT try_ons (queued)  │
              │  - enqueue via app.state.queue
              └──────────────┬──────────────┘
                             │
                             ▼
              ┌─────────────────────────────┐
              │ ARQ pool (centralized)      │
              └──────────────┬──────────────┘
                             │
                             ▼
              ┌─────────────────────────────┐
              │ replicate_worker            │
              │   FSM: queued → cache_lookup
              │        → cache_hit | inference_running
              │        → uploading → completed
              │        (or → fallback_triggered → inference_running)
              └─────────────────────────────┘
```

### FSM state diagram

```
   queued ─► cache_lookup ─► cache_hit ─► uploading ─► completed
                  │
                  └─► inference_running ─► uploading ─► completed
                            │
                            └─► fallback_triggered ─► inference_running ─► …
                            │
                            └─► failed (terminal)
```

`status` (pending/processing/completed/failed) is the public-facing field for Brook. `fsm_state` is internal and drives the metrics. Both columns live on `try_ons`.

### Cache hit / miss flow

```
TryOnService                              replicate_worker
─────────────                              ────────────────
SHA256(body_id+garment_id+model+mode)
        │
        ▼
Postgres try_on_cache  ← WARM (90d)
        │
   hit ─┼─► return completed immediately (no enqueue)
        │
   miss ┴─► INSERT pending + enqueue
                                          ┌─► Redis tryon:cache:<sha> (HOT 7d)
                                          │   hit → cache_tier=hot
                                          ▼
                                          Postgres try_on_cache
                                              hit → cache_tier=warm, promote to hot
                                              miss → CALL replicate
                                                       │
                                                       ▼
                                                       store HOT + WARM
```

### Tier routing decision tree

```
user's active subscription
        │
        ├── plan == 'free'   → tier=BASE  → fashn_mode='performance'  (timeout 60s)
        ├── plan == 'estilo' → tier=STD   → fashn_mode='balanced'     (timeout 60s)
        └── plan == 'imagen' → tier=PRO   → fashn_mode='quality'      (timeout 15s)
                                                    │
                                                    └─► timeout? ──► fallback to STD/balanced
```

---

## 2. Worker patterns

### `admin.trusted()` (Service-Role)

ALL worker DB writes go through `admin.trusted()`. This bypasses RLS by design (workers have no user JWT). The guard wrapper still demands the explicit `.trusted()` call so the intent is visible in code review.

```python
# ✅ Correct (worker):
await admin.trusted().table("try_ons").update({...}).eq("id", id).execute()

# ❌ Wrong (worker):
await client.from_("try_ons").update({...}).eq("id", id).execute()
# Would attempt to enforce RLS with no user context → 0 rows affected, silently.
```

For HTTP request handlers the opposite rule applies — use `admin.with_user_check(user_id=...)`.

### Idempotency

Requests that mutate or trigger billable work carry `Idempotency-Key`. Middleware deduplicates at the HTTP layer (24h TTL — see `idempotency_keys` table). Workers should never observe the same `try_on_id` twice for a single user action.

### Error handling + circuit breaker

The Antigravity rate-limit middleware already opens a circuit breaker on consecutive Replicate 429s. Workers should:
1. Catch `replicate.exceptions.ReplicateError` with `status==429` → sleep with exponential backoff (2^n s), max 3 attempts.
2. Catch `asyncio.TimeoutError` on PRO tier → fall back to STD (see `_run_inference_with_fallback`).
3. Any other exception → log with `exc_info=True`, mark FSM state = `failed`, re-raise (ARQ will record the failure).

---

## 3. Failure modes & recovery

| Symptom | Likely cause | Recovery |
|--------|--------------|----------|
| `/ready` returns 503 (redis: down) | Redis unreachable from API pods. | Rate limit middleware falls back to Postgres (CR-4). Cache lookups degrade to WARM only. Worker enqueue fails — see next row. |
| `app.state.queue` is None at request time | ARQ pool not initialized at startup. | TryOnService falls back to ad-hoc `create_pool`. Cold start is slower but correct. |
| Replicate consistently times out | Provider outage. | Circuit breaker stays open. PRO traffic auto-fallbacks to STD. Surface incident banner in app. |
| Vision API quota exceeded | Daily cap hit. | `vision_worker` sets `body_analysis.status='failed'`. User can retry next day. Bump quota via GCP console. |
| FSM stuck in `inference_running` for > 5 min | Worker crashed mid-job. | ARQ retries on next worker boot. Set Sentry alert on `fsm_transitions_total{from_state="inference_running"}` rate dropping to zero. |
| Cross-user data leak suspected | RLS misconfig. | Run `SELECT * FROM verify_rls_policies();` (migration 007). Run cross-tenant `SELECT COUNT(*)` as user JWT — must be 0. |

---

## 4. Monitoring & metrics

### Prometheus metrics emitted

| Metric | Labels | What it measures |
|--------|--------|------------------|
| `rate_limit_hits_total` | endpoint, user_tier | 429 returned to user. |
| `cache_hits_total` | endpoint, cache_tier | hot vs warm hits. |
| `cache_miss_total` | endpoint | full inference required. |
| `fashn_inference_latency_seconds` | tier | BASE/STD/PRO latency histogram. |
| `fashn_fallback_total` | from_tier, to_tier | PRO→STD fallbacks (alert if > 5/hour). |
| `fsm_transitions_total` | from_state, to_state | Heatmap of state changes. |

### Sentry tags (set via `app.core.metrics.tag_sentry`)

`tier`, `endpoint`, `model_version`, `user.id`. Use these to slice issues by tier and pinpoint user-specific failures without leaking PII (only the UUID is sent).

### Alerting rules

1. **High inference latency** — `histogram_quantile(0.95, fashn_inference_latency_seconds_bucket{tier="PRO"}) > 20s` for 5 min.
2. **Error rate > 5%** — `sum(rate(fsm_transitions_total{to_state="failed"}[5m])) / sum(rate(fsm_transitions_total[5m])) > 0.05`.
3. **Cache hit rate < 30%** for paid users — degraded ROI on infra spend.
4. **Fallback storm** — `rate(fashn_fallback_total[10m]) > 0.5` (more than 3 fallbacks per minute).
5. **Lazy reset firing too often** — log line `Lazy reset triggered` > 100/hour means the Antigravity cron is broken.

---

## 5. Deployment checklist

Before opening a release PR for this sprint:

- [ ] Migration 007 applied on staging (`007_optionf_fsm_cache_tier.sql`). Apply with `BEGIN; \i 007...; ROLLBACK;` first to dry-run.
- [ ] Alejo signed off on the Lua / FSM transitions (T2 spec).
- [ ] `/health` returns 200 in < 50ms (curl 20 times, p95).
- [ ] `/ready` returns 200 when all deps OK, 503 when Redis is stopped (manual test).
- [ ] Cache hit rate ≥ 40% on repeat users (run K6 scenario `repeat_user`).
- [ ] Tier routing verified: free→BASE, estilo→STD, imagen→PRO (3 manual try-ons with seeded subscriptions).
- [ ] RLS sanity check:
  ```sql
  -- as service_role:
  SELECT * FROM public.verify_rls_policies();
  -- as user A's JWT:
  SELECT COUNT(*) FROM public.try_ons WHERE user_id != auth.uid();  -- must be 0
  ```
- [ ] Lazy reset smoke test on staging:
  ```sql
  SELECT * FROM public.reset_usage_if_stale('<staging-user-uuid>'::uuid);
  ```
- [ ] Sentry receives all tags: search by `tier:PRO` and confirm at least one event present.
- [ ] FEATURE_MOCK_WORKERS toggle works:
  ```bash
  FEATURE_MOCK_WORKERS=true  pytest tests/test_workers_mock_vs_real.py -k mock_worker_returns_canned -v
  FEATURE_MOCK_WORKERS=false pytest tests/test_workers_mock_vs_real.py
  ```
- [ ] Test coverage ≥ 80% on `app/services/cache_service.py`, `app/models/fsm.py`.
- [ ] Cyber Neo full audit pass (no CRITICAL findings).

---

## 6. Local dev quickstart for new engineers

```bash
# 1. Clone + venv
git clone https://github.com/jucagio/asesor-imagen-ai
cd asesor-imagen-ai/backend
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Env
cp .env.example .env
# Edit .env: set FEATURE_MOCK_WORKERS=true so you don't need real Replicate creds.

# 3. Redis (optional in mock mode, but recommended)
docker run -d --name redis -p 6379:6379 redis:7-alpine

# 4. Apply migrations against your local Supabase project
psql $DATABASE_URL -f migrations/004_consolidated_schema_v2.sql
psql $DATABASE_URL -f migrations/005_rls_policies.sql
psql $DATABASE_URL -f migrations/006_rate_limit_rpc.sql
psql $DATABASE_URL -f migrations/007_optionf_fsm_cache_tier.sql

# 5. Run API + worker
uvicorn app.main:app --reload --port 8000
# in another shell:
arq app.workers.replicate_worker.WorkerSettings
```
