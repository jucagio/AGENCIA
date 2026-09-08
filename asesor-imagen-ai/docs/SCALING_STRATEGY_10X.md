# Scaling Strategy — 10x Path (50K → 500K Paid Users)

**Author:** Alejo (Solutions Architect)
**Date:** 2026-05-19
**Status:** ENTREGADO — input para roadmap Q3-Q4 2026 + Q1-Q2 2027
**Audience:** Jarvis (CEO), Sasha (Backend), Juan Camilo (Accionista)
**Related:** ADR-006 (Path A 50K paid), `COST_MODEL_PATH_A.md` rev 2, `ADR_007_RATE_LIMITING.md`, `SECURITY_ARCHITECTURE.md`

---

## 0. TL;DR

**Path:** 50K paid (Mes 12, ~500K MAU) → **500K paid (Mes 36, ~5M MAU)**.

**Veredicto:** ✅ **Arquitectura aguanta hasta 250K MAU sin cambios mayores.** A partir de ahí, migraciones planeadas en 3 escalones: cache distribuido (250K), AWS ECS (500K), DB sharding (2.5M).

**Filosofía:** "Don't pre-optimize, but pre-plan." Cada migración se trigger por métrica medible, NO por fecha calendario.

**Inversión Sasha estimada:** 12-16 semanas-persona distribuidas en 18 meses post-launch.

---

## 1. Bandas de Escala — Triggers y Migraciones

| Escala | MAU total | Paid | Cuándo (proyección Leo) | Trigger métrica | Migraciones activas |
|--------|----------:|-----:|:-----------------------:|-----------------|---------------------|
| **MVP** | 10-50K | 1-5K | Mes 3-6 | — | Setup inicial |
| **Growth** | 50-250K | 5-25K | Mes 6-12 | API p95 >800ms sostenido | Caching agresivo (ADR-004) |
| **Scale-out 1** | 250-500K | 25-50K | Mes 12-18 | Postgres CPU >70% sostenido | **Redis distribuido + R2 multi-region** |
| **Scale-out 2** | 500K-1M | 50K-100K | Mes 18-24 | Railway bill >$5K/mes | **AWS ECS + read replicas** |
| **Hyperscale** | 1M-5M | 100K-500K | Mes 24-36 | DB write QPS >500 | **DB sharding + Celery + Kafka** |

**Regla de oro:** Cada migración requiere RFC + 2 semanas POC + 1 semana cutover. NO migrar reactivo, planear con 30 días de runway.

---

## 2. Por Componente

### 2.1 Database — Supabase PostgreSQL

#### Banda actual (MVP → 250K MAU)
- Supabase Pro plan ($25/mes → $599/mes a 250K)
- Schema actual: ~12 tablas + RLS
- Índices clave: `users(email)`, `try_ons(user_id, created_at DESC)`, `wardrobe(user_id)`
- Backup: Supabase managed (daily PITR)

**Aguanta:**
- ~10K write QPS sostenido (con buen indexing)
- ~50K read QPS con connection pooler (PgBouncer)
- 99p latency <100ms para queries con índice

**Realidad @ 250K MAU:**
- Try-ons: ~50M rows/año (250K MAU × 22 try-ons free + paid promedio)
- Particionar `try_ons` por `created_at` mensual: Sí, en banda 250K-500K MAU
- Users: ~250K rows → trivial

#### Banda 500K-1M MAU
- **Habilitar read replicas Supabase** (Pro plan incluye 1 réplica)
- Routing: lecturas pesadas (GET try-ons history, GET wardrobe) → réplica
- Escrituras (POST try-ons, POST body-analysis) → primary
- Implementación: `app/core/db.py` con dual session factory (`read_session`, `write_session`)
- Tradeoff: réplica lag 50-200ms — aceptable para listados, NO para "acabo de crear, leer"

#### Banda 1M-5M MAU
- **Sharding por user_id** (consistent hashing)
- Shards: 4 inicialmente (cada uno con ~250K usuarios activos)
- Cross-shard queries (analytics, admin dashboards): warehouse separado (ClickHouse o BigQuery)
- **Migración estimada: 4 semanas Sasha + 1 semana cutover**

#### Riesgo crítico
- **RLS performance:** A 1M+ MAU, las policies RLS sobre `try_ons` requieren índice compuesto `(user_id, created_at DESC)` perfecto. Sin él, query planner degrada a sequential scan = catástrofe.
- **Mitigación:** Audit `EXPLAIN ANALYZE` mensual en queries top-10 (Cinthya workflow n8n)

### 2.2 Job Queue — ARQ + Redis

#### Banda actual (MVP → 250K MAU)
- ARQ (Python async) + Redis (Upstash)
- Workers: 2-4 procesos en Railway
- Cola única: `tryon_queue`, `vision_queue`, `claude_queue`

**Aguanta:**
- ~1,000 jobs/segundo en single Redis node (Upstash)
- Latencia enqueue: <5ms p99

**Realidad @ 250K MAU:**
- Peak hour try-ons: ~10K/h = 3 jobs/s → muy holgado
- Workers requeridos: 8-10 (cada try-on ocupa worker 20-30s)

#### Banda 500K-1M MAU
- **Separar colas por prioridad:**
  - `tryon_paid_high` → procesado primero
  - `tryon_free_normal` → segundo
  - `vision_normal`, `claude_low`
- Auto-scaling workers (AWS ECS task count auto-scale por queue depth)
- **Dead-letter queue (DLQ):** jobs que fallan 3 veces → DLQ + Sentry alert

#### Banda 1M-5M MAU
- **Migración a Celery + RabbitMQ** (o Kafka si necesitamos event sourcing)
- Razón: ARQ es excelente <100K jobs/día, pero Celery tiene mejor ecosistema para retry policies complejas, scheduled tasks, chord/group workflows
- Tradeoff: ARQ es 5x más simple. Migrar solo si dolor real.
- **Migración estimada: 3 semanas Sasha + 1 semana cutover**

### 2.3 Storage — Supabase Storage / R2

#### Banda actual (MVP)
- **Decisión recomendada (ya en rev 1):** R2 desde día 1, NO Supabase Storage
- R2: $0.015/GB-mes storage, **$0 egress**
- Bucket: `aifc-tryons-prod`, `aifc-wardrobe-prod`, `aifc-shares-prod`

**Aguanta:**
- Unlimited storage (escala linealmente)
- Throughput: 1000+ writes/seg sin tunning
- Signed URLs S3-compat (compatible con Supabase Storage SDK)

#### Banda 500K-1M MAU
- **CloudFront/CloudFlare CDN frente a R2** para shared URLs (D5)
- TTL: 30d para shares, 24h para tryons normales
- Costo CDN: $0.085/GB vs egress R2 $0 = pero CDN cachea = -80% reads a R2

#### Banda 1M-5M MAU
- **Multi-region R2 replication** (US + EU + LATAM)
- Lifecycle policies: try-ons >1 año → archive tier (-70% storage cost)
- Compresión WebP nivel 9 (vs default 6) — ahorra 25% storage sin pérdida perceptible

### 2.4 API — FastAPI on Railway → AWS ECS

#### Banda actual (MVP → 250K MAU)
- Railway Pro plan ($20-320/mes según MAU)
- 2-4 replicas FastAPI
- Auto-deploy desde main branch

**Aguanta:**
- ~200 QPS por replica (single 4-core Railway pod)
- Total 800 QPS con 4 replicas = suficiente hasta 250K MAU

#### Banda 500K-1M MAU (TRIGGER: Railway bill >$5K/mes O API p95 >500ms sostenido)
- **Migración a AWS ECS Fargate** (mantener Supabase para DB+Auth)
- Componentes nuevos:
  - ALB (Application Load Balancer) → ECS service
  - ECS task definition con auto-scaling policy (target CPU 60%, min 4 / max 20 tasks)
  - VPC + private subnets + NAT gateway
  - CloudWatch Logs + Sentry forward
- **Migración estimada: 3-4 semanas Sasha + Cinthya + 1 semana paralelo cutover**
- **Costo migración: ~$8K en infra paralela durante cutover** (ambos stacks corriendo 2 semanas)

#### Banda 1M-5M MAU
- Multi-region ECS (us-east, eu-west, sa-east) con Route53 latency-based routing
- Edge caching más agresivo (CloudFlare Cache Rules custom)
- gRPC interno entre servicios si dividimos en microservicios (NO recomendado <5M MAU)

### 2.5 Cache — Postgres → Redis Distribuido

#### Banda actual (MVP → 250K MAU)
- Cache de Replicate results en tabla `tryons_cache(hash_key, result_url, created_at)`
- Hit rate: 25-45%
- Latencia: 8-15ms p50 (Postgres index)

#### Banda 250K-1M MAU (TRIGGER: Postgres CPU >70% por cache lookups)
- **Migración a Redis distribuido** (Upstash Pro o ElastiCache)
- Mantener Postgres como source of truth, Redis como hot cache
- Strategy: write-through (escribe a ambos), read-through (read Redis, fallback Postgres)
- Latencia: 1-3ms p50 (~5x faster)
- **Costo Upstash Pro:** $50-280/mes según QPS

#### Banda 1M-5M MAU
- **Redis Cluster** (sharded por hash_key)
- Eviction policy: LRU con max-memory 10GB
- Backup: Snapshots cada 6h (Upstash automated)

### 2.6 Observability — Sentry + PostHog + Logtail

#### Banda actual
- Sentry: errors + performance ($26/mes)
- PostHog: events + funnels ($0 self-hosted o $450/mes cloud)
- Logtail: structured logs ($0-15/mes)

#### Banda 250K-1M MAU
- Sentry Team plan ($85/mes — 100K events/día)
- PostHog Scale plan ($450/mes — 1M events/mes)
- Datadog opcional para APM avanzado ($30/host/mes × 10 hosts = $300/mes)

#### Banda 1M-5M MAU
- **Self-host PostHog** en cluster propio (ahorra ~$15K/año a esa escala)
- Sentry Business plan ($230/mes — 1M events/día)
- OpenTelemetry tracing end-to-end (FastAPI → ARQ worker → Replicate)

---

## 3. Cost Optimization a Escala

| Optimización | Trigger band | Ahorro % | Owner |
|--------------|--------------|---------:|-------|
| Cache Vision API 24h TTL | 50K MAU | -60% Vision calls | Sasha (Sprint 2) |
| Batch Claude recos | 100K MAU | -20% Claude tokens | Sasha (Sprint 3) |
| CloudFlare CDN para shares | 250K MAU | -80% R2 egress | Sasha + Antigravity |
| Model routing Haiku/Sonnet/Opus | 50K MAU | -70% Claude cost en free tier | Sasha (Sprint 2) |
| FASHN base para free tier | 100K MAU | -50% Replicate free | Sasha (Sprint 2) |
| Replicate volume discount | 250K+ MAU | -15-25% | Jarvis + Leo (contrato anual) |
| Supabase Compute scale-down off-hours | 500K MAU | -30% DB cost | Cinthya workflow |
| Reserved Redis Upstash | 500K MAU | -25% Redis | Compra anual |

**Total optimizations potenciales acumuladas @ 1M MAU: ~$140K/mes ahorro** vs baseline naive.

---

## 4. Capacidad Por Componente — Stress Test

### Escenario: Viral spike 1M downloads en 24h @ Mes 12 (500K MAU base)

| Componente | Pre-spike | Spike load | Aguanta? | Mitigación |
|------------|----------:|-----------:|:--------:|------------|
| Railway API (8 replicas) | 200 QPS | 1,500 QPS pico | ⚠️ Marginal | Auto-scale a 16 replicas pre-warm + Cloudflare cache |
| Supabase Auth | 50 signups/min | 5,000 signups/min | ⚠️ | Plan Team upgrade ($599/mes incluye burst) |
| Supabase Postgres | 5K QPS | 30K QPS | ❌ | Read replica activa + connection pool tuning |
| Replicate API | 100 calls/min | 2,000 calls/min | ❌ | Negociar bump a 5K/min + queue overflow CB |
| ARQ workers | 2 jobs/s | 30 jobs/s | ⚠️ | Auto-scale workers (ECS) |
| Upstash Redis | 1K ops/s | 20K ops/s | ✅ | Pro tier handles |
| R2 uploads | 50/s | 500/s | ✅ | Linear scale, sin rate limit |

**Veredicto:** Sin pre-prep, viral spike rompe Postgres + Replicate. **Acción:** Runbook `VIRAL_SPIKE_PLAYBOOK.md` para escalar antes (read replica + worker count + Replicate bump) cuando se planea campaña.

---

## 5. Roadmap por Quarter (proyectado)

### Q3 2026 (Sept-Nov, banda 50-100K MAU)
- [ ] Implementar cache Vision API 24h
- [ ] Implementar model routing Haiku/Sonnet/Opus
- [ ] R2 ya activo (decisión rev 1)
- [ ] Cloudflare Pro $25/mes

### Q4 2026 (Dec-Feb, banda 100-250K MAU)
- [ ] FASHN base model para free tier
- [ ] Batch Claude recommendations
- [ ] PostHog Scale plan
- [ ] Migration `try_ons` particionada por mes

### Q1 2027 (Mar-May, banda 250-500K MAU) — TRIGGER MIGRACIÓN 1
- [ ] Redis distribuido (Upstash Pro)
- [ ] Negociar Replicate volume discount
- [ ] Read replica Supabase activa
- [ ] CloudFront/Cloudflare CDN para shares D5

### Q2 2027 (Jun-Aug, banda 500K-1M MAU) — TRIGGER MIGRACIÓN 2
- [ ] **Migrar Railway → AWS ECS** (3-4 semanas Sasha)
- [ ] VPC + ALB + Fargate + auto-scaling
- [ ] Sentry Team plan
- [ ] Multi-region R2 (US + LATAM)

### Q3-Q4 2027 (banda 1M-5M MAU) — TRIGGER MIGRACIÓN 3
- [ ] DB sharding por user_id (4 shards)
- [ ] Celery + RabbitMQ migration
- [ ] Self-host PostHog
- [ ] Multi-region ECS

---

## 6. Riesgos & Anti-patterns

### Riesgo 1: Premature optimization
**No migrar antes de los triggers.** Sasha tendrá tentación de "modernizar" antes de 250K MAU. **NO.** Railway + Supabase + R2 + ARQ es óptimo hasta 500K MAU. Migrar antes = burn 4 semanas sin payoff.

### Riesgo 2: Migration without rollback
Cada migración requiere:
1. POC en staging 2 semanas
2. Dual-write durante cutover (data flowing a ambos stacks)
3. Validation queries (counts, checksums)
4. Feature flag rollback en <5 min

### Riesgo 3: Cost runaway sin alerting
Cinthya **DEBE** tener workflows n8n que alerten a Slack #arquitectura si:
- Cloud bill mensual >120% del mes anterior
- Replicate spend/día >$1K
- Postgres connection count >80% del max
- Redis memory >80% del max

### Riesgo 4: Vendor lock-in en Supabase
A 1M+ MAU, Supabase Enterprise puede ser limitante ($5K+/mes). Plan B: migrar PostgreSQL a RDS managed manteniendo Supabase Auth/Realtime. **No urgente** — Supabase Team plan aguanta hasta 1M MAU con read replica.

---

## 7. Hand-off & Owners

| Tarea | Sprint | Owner | Status |
|-------|--------|-------|--------|
| Implementar caching Vision 24h | Sprint 2 | Sasha | Pending |
| Model routing skill integration | Sprint 2 | Sasha | Pending |
| FASHN base routing free tier | Sprint 3 | Sasha | Pending |
| Workflow n8n cost alerting | Sprint 2 | Cinthya | Pending |
| RFC "AWS ECS Migration" (POC) | Q1 2027 | Alejo + Sasha | Pre-trigger |
| `VIRAL_SPIKE_PLAYBOOK.md` | Sprint 4 | Alejo + Cinthya | Pending |
| Mensual EXPLAIN ANALYZE audit | Recurrente | Cinthya | Configure n8n |

---

## 8. Métricas a Trackear Mensual (KPIs de escala)

| KPI | Target Mes 12 | Owner |
|-----|--------------:|-------|
| API p95 latency | <500ms | Sasha + Cinthya |
| API p99 latency | <2s | Sasha |
| DB connection pool utilization | <70% | Sasha |
| Cache hit rate Replicate | >45% | Sasha |
| Replicate spend / paid MRR | <12% | Alejo + Leo |
| Total cloud spend / MRR | <25% | Alejo + Juan Camilo |
| Worker queue depth p95 | <50 jobs | Sasha |
| Crash-free sessions | >99.5% | Sentry → Brook |

---

**Reportado a Jarvis. Disponible para Q&A en Junta 2026-05-25.**
**— Alejo, Solutions Architect**
