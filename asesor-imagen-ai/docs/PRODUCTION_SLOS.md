# PRODUCTION SLOs — Sprint 1 + Prod

**Owner:** Alejo (Solutions Architect)
**Status:** ✅ DRAFT — Pending Ego validation pre Sprint 1 go-live
**Date:** 2026-05-20
**Stakeholders:** Sasha (impl), Ego (audit), Jarvis (sign-off)

---

## 1. Filosofía

SLOs definen el **contrato de calidad** que prometemos a usuarios. Cada SLO tiene:
- **SLI** (Service Level Indicator): qué medimos
- **Target**: nivel que prometemos
- **Error Budget**: cuánto podemos violar antes de bloquear releases
- **Alert threshold**: cuándo paginar on-call

Error budget = `(1 - SLO target) × period`. Si SLO = 99.9% mensual, budget = 43.2 min de downtime.

---

## 2. Latency SLOs

| Endpoint | SLI | Target (p95) | Target (p99) | Error budget |
|---|---|---|---|---|
| `GET /users/me/usage` | Server-side latency | **<100ms** | <250ms | 5% req >100ms |
| `POST /try-ons` | Validation latency (sync part) | **<300ms** | <800ms | 5% req >300ms |
| `POST /try-ons` (rate limit check) | Lua EVAL execution | **<50ms** | <100ms | 1% req >50ms |
| `GET /try-ons/{id}` | Result fetch | <150ms | <400ms | 5% |
| Worker pipeline (async, end-to-end) | Vision + Replicate + storage | <60s | <120s | 5% |

### Latency budget breakdown (POST /try-ons sync)

```
Total: 300ms p95
├─ Auth (JWT verify):     20ms
├─ Lua rate limit:        50ms
├─ DB write (job queued): 80ms
├─ Response serialize:    20ms
├─ Network + overhead:   130ms
```

---

## 3. Availability SLOs

| Component | SLI | Target | Error budget (monthly) |
|---|---|---|---|
| `/health` | HTTP 200 ratio | **99.9%** uptime | 43.2 min |
| `/ready` | HTTP 200 ratio | 99.5% uptime | 3.6h (pod restarts ok) |
| Redis (Supabase) | Connection success | 99.9% | 43.2 min (vendor SLA) |
| PostgreSQL (Supabase) | Query success | 99.9% | 43.2 min |
| Replicate API | API call success | 99.5% | 3.6h (vendor dependent) |
| Worker queue (async) | Job pickup <30s | 99% | 7.2h |

---

## 4. Accuracy SLOs

| Metric | SLI | Target | Rationale |
|---|---|---|---|
| Rate limit blocks | False negative rate | **0%** | Cannot let users exceed cap (revenue loss) |
| Idempotency duplicates | Double-increment rate | **0%** | Must be perfectly idempotent |
| Cache hit ratio | Hits / total requests | **≥40%** | Margin model breaks below 30% |
| Vision API errors | Failed / total | <2% | Retryable, doesn't break UX |
| Replicate timeouts | Timeout / total | <1% | Circuit breaker engages at 5% |
| DB connection errors | Failed connections | <0.5% | Connection pool saturation signal |

---

## 5. Alert Thresholds (on-call paging)

### P1 — Page immediately (SMS + call)

| Trigger | Threshold | Action |
|---|---|---|
| p95 latency > 500ms | 5 min sustained | Page on-call |
| Error rate > 5% | 5 min sustained | Page on-call |
| Redis unavailable | >30s | Page on-call + fail-over plan |
| Postgres unavailable | >30s | Page on-call + read-only mode |
| Health check failing | >2 min | Page on-call |

### P2 — Slack alert (no paging)

| Trigger | Threshold | Action |
|---|---|---|
| Cache hit ratio < 25% | 15 min sustained | Investigate (cache pollution) |
| Replicate timeouts > 3% | 10 min sustained | Slack #ops, monitor |
| Worker queue depth > 100 | 5 min | Slack #ops, scale workers |
| Free→paid conversion drop >20% | Daily | Slack #product |

### P3 — Dashboard only

| Trigger | Threshold |
|---|---|
| Margin <60% (vs target 67%) | Weekly review |
| Cap-touch rate >85% | Weekly review (pricing signal) |

---

## 6. Error Budget Policy

Cada SLO tiene un budget mensual. Cuando se quema:

| Budget consumed | Action |
|---|---|
| <50% | Normal operations |
| 50-75% | Slack alert, freeze risky changes |
| 75-100% | **Block non-critical releases**, all-hands on reliability |
| >100% (SLO breached) | Post-mortem mandatory, no feature releases until burn rate normalizes |

---

## 7. Observability Stack (required)

| Layer | Tool | Metrics |
|---|---|---|
| App metrics | Prometheus + Grafana | Latency histograms, error rates |
| Logs | Supabase logs + Logflare | Request logs, error traces |
| Tracing | OpenTelemetry → Honeycomb (or Sentry) | Distributed traces |
| Alerts | PagerDuty + Slack | P1/P2/P3 routing |
| Dashboards | Grafana | SLO burn-down per service |

---

## 8. SLO Review Cadence

- **Daily:** Automated burn-rate report → #ops
- **Weekly:** Jarvis + Sasha review dashboard (Mon 9 AM)
- **Sprint retro:** Adjust targets if consistently over/underperforming
- **Quarterly:** Full SLO review with Ego audit

---

## 9. Pre-Production Checklist (Ego validation)

- [ ] All endpoints have latency histograms
- [ ] Error budget dashboards live in Grafana
- [ ] PagerDuty rotation configured (on-call schedule)
- [ ] Runbooks for each P1 alert
- [ ] Synthetic checks (Pingdom) for /health every 30s
- [ ] Load test: 100 concurrent users sustain p95 <300ms
- [ ] Chaos test: Redis down → app degrades gracefully (fail-open to Postgres)
- [ ] Chaos test: Replicate timeout → circuit breaker engages within 30s

---

**Aprobado por:** Alejo
**Pendiente:** Ego validation antes de Sprint 1 go-live
**Owner ongoing:** Sasha (instrumentation) + Jarvis (budget policy enforcement)
