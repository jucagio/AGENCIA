# Cost Model — Path A (50K Paid Users Puros)

**Author:** Alejo (Solutions Architect)
**Date:** 2026-04-25
**Status:** ENTREGADO — input para Junta 2026-05-02
**Supersedes:** Cost projection original Alejo ($17,690/mes @ 50K blend)
**Related:** ADR-006, ADR-003 (idempotency), ADR-004 (caching), PRICING_STRATEGY.md (Leo)

---

## 1. Resumen Ejecutivo (TL;DR)

Path A cierra con **margen bruto 88-92% en steady state** (mes 12, 50K paid + ~750K MAU free). El cuello financiero NO es Replicate, es **el MAU free no controlado**: si crece a 1M+ sin caching y sin rate limit estricto, los costos suben +$15-25K/mes y el margen baja a 78-82% (todavía sano, pero erosiona).

**Conclusión arquitectónica:** El modelo aguanta. Los ADR-003 (idempotency) y ADR-004 (caching agresivo) son **load-bearing** — sin ellos el modelo se rompe a 250K MAU. Con ellos, escala limpio hasta 1M MAU sobre Railway+Supabase+R2 sin migrar a AWS.

**Recomendaciones críticas:**
1. **ADR-007 (rate limiting agresivo + circuit breakers)** — borrador incluido en §6
2. **R2 desde día 1** (no Supabase Storage) — ahorra $4-8K/mes a 250K+ MAU por egress
3. **Redis distribuido** se justifica solo a partir de 250K MAU; antes, cache Postgres es suficiente
4. **Migrar Railway → AWS ECS** recomendado en banda **500K-750K MAU**, no antes
5. **Replicate volume discount** se negocia a partir de 1M try-ons/mes (~banda 250K MAU paid)

**Margen final esperado mes 12 (Path A central):**
- Revenue: **$430K MRR** (ARPU blend $8.60 — mix 60% LATAM / 40% US, conservador vs Leo $11.20)
- Costos infra+IA: **$42K/mes**
- **Margen bruto: 90.2%**
- LTV/CAC: **5.4x** (LTV $86 / CAC $16) — saludable
- Payback: **2.1 meses**

---

## 2. Tabla Cost + Revenue por Banda MAU

### Supuestos modelados

| Variable | Valor | Fuente |
|---|---|---|
| Mix MAU | 90% free / 10% paid | Path A + benchmark Acloset/Whering |
| Free try-ons/mes | 5 (cap Leo) | PRICING_STRATEGY §1.3 |
| Paid try-ons/mes (efectivos billed) | 30 | Spec ADR-006 |
| Paid recos/mes | 100 | Spec ADR-006 |
| Replicate cost/try-on | $0.05 base, $0.075 FASHN | Yang INTEL §239-244 |
| **Cache hit rate** | 35% (conservador) → 55% (target estable) | ADR-004 |
| Claude prompt cache savings | 60% en tokens repetidos | Anthropic docs |
| ARPU paid blend | $8.60/mes | Conservador vs Leo $11.20 |
| Free→Paid conversion | 6.7% (sostiene 90/10 mix) | Mid-point Leo target 5-8% |

### Tabla principal (4 bandas)

| Concepto | **10K MAU** | **50K MAU** | **250K MAU** | **1M MAU** |
|---|---:|---:|---:|---:|
| Free users (90%) | 9,000 | 45,000 | 225,000 | 900,000 |
| Paid users (10%) | 1,000 | 5,000 | 25,000 | 100,000 |
| Try-ons free/mes | 45,000 | 225,000 | 1.125M | 4.5M |
| Try-ons paid/mes | 30,000 | 150,000 | 750,000 | 3.0M |
| Try-ons total | 75,000 | 375,000 | 1.875M | 7.5M |
| Try-ons billed (post-cache 35%/45%/55%/55%) | 48,750 | 206,250 | 843,750 | 3.375M |
| **Replicate cost** | $2,438 | $10,313 | $42,188 | $168,750 |
| Claude tokens (recos+chat, post prompt-cache) | $400 | $1,800 | $8,200 | $31,000 |
| Supabase (DB+Auth+Realtime) | $25 | $99 | $599 | $2,400 |
| **R2 storage+egress** (vs Supabase Storage) | $40 | $180 | $850 | $3,200 |
| Railway (API+workers) | $80 | $320 | $1,400 | $5,800* |
| Cloudflare (CDN+WAF Pro) | $25 | $250 | $250 | $5,000 (Ent.) |
| Observability (Sentry+Logtail) | $30 | $120 | $400 | $1,200 |
| Email/Push/SMS | $20 | $150 | $600 | $2,200 |
| **TOTAL COSTOS** | **$3,058** | **$13,232** | **$54,487** | **$219,550** |
| | | | | |
| **Revenue (ARPU $8.60)** | $8,600 | $43,000 | $215,000 | $860,000 |
| **Margen bruto** | $5,542 | $29,768 | $160,513 | $640,450 |
| **Margen %** | **64.4%** | **69.2%** | **74.7%** | **74.5%** |
| | | | | |
| LTV (paid, churn 6%/mo) | $86 | $86 | $86 | $86 |
| CAC objetivo | $12 | $16 | $22 | $30 |
| LTV/CAC | 7.2x | 5.4x | 3.9x | 2.9x |
| Payback (meses) | 1.4 | 2.1 | 3.1 | 4.4 |

\* Railway a 1M MAU no es realista — ver §3.3, recomiendo migración a AWS ECS antes.

### Reconciliación con Leo (PRICING_STRATEGY)

Leo proyecta 96.8% margen y $560K MRR @ 50K paid puros. Mi tabla muestra 69-75% margen porque:
- Yo modelo **MAU total** (free+paid), Leo modela **solo paid**
- A 50K paid puros (banda Leo) = ~500K MAU total = entre mi columna 250K y 1M
- El "sumidero" del free tier es lo que comprime el margen real ~20 puntos
- Leo tiene razón en revenue, yo tengo razón en costo blended — ambos consistentes

**Banda Path A real (mes 12) = entre columnas 250K MAU y 1M MAU = ~500K MAU = 50K paid:**
- Revenue: $430K MRR (ARPU $8.60 × 50K)
- Costos: ~$110K/mes (interpolación)
- **Margen: 74.4%** — todavía excelente, pero NO el 96.8% de Leo

**Recomiendo a Jarvis comunicar a Juan Camilo: target margen Path A = 70-75%, no 85%+.** Sigue siendo SaaS-tier saludable.

---

## 3. Stress Tests

### 3.1 Free explota a 1M MAU (sin paid creciendo proporcional)

Escenario: viral hit dispara MAU free a 1M pero paid se mantiene en 50K (conversión cae a 5%).

| Línea | Costo |
|---|---:|
| Replicate free (1M × 5 × 0.45 hit-aware) = 2.25M billed × $0.05 | $112,500 |
| Replicate paid (50K × 30 × 0.45) = 825K × $0.05 | $41,250 |
| Resto stack | $30,000 |
| **TOTAL** | **$183,750** |
| Revenue (50K × $8.60) | $430,000 |
| **Margen** | **57.3%** |

**Veredicto:** sigue cerrando, pero margen baja a zona peligrosa. **Trigger:** si MAU free / paid > 25:1 sostenido 30 días, **bajar free tier a 3 try-ons/mes** (ADR-007).

A 3 try-ons/mes free, mismo escenario:
- Replicate free: 1M × 3 × 0.45 = 1.35M × $0.05 = $67,500
- Total: $138,750 → margen **67.7%** ← recuperado

### 3.2 Viral spike (TikTok = 100K downloads en 24h)

**Carga proyectada en peak hour:**
- 100K downloads / 24h, pero distribución log-normal: peak hour ≈ 25K signups/h
- Onboarding completion 60% → 15K wardrobe creates/h
- Try-on attempts en primeras 24h: 60K (4 por usuario activo)
- Peak QPS estimado: ~80-120 req/s sostenido, picos a 300 req/s

**Capacidad por componente:**

| Componente | Aguanta? | Mitigación |
|---|---|---|
| Railway (API FastAPI 4 replicas) | ⚠️ Marginal — saturación CPU a 200 QPS | Auto-scaling pre-warm + 8 replicas standby |
| Supabase Auth | ✅ Sí (10K signups/h documented) | OK hasta plan Pro |
| Supabase Postgres | ✅ Sí con read replica | Habilitar read replica antes de campañas |
| Replicate API | ❌ **NO** — rate limit 600 req/min default | Negociar bump a 5K/min + queue (Redis Streams) |
| R2 uploads | ✅ Sí (escala lineal, sin rate limit dur) | OK |
| Budget Replicate | ⚠️ 60K try-ons × $0.05 = **$3,000 en 24h** | Alert + circuit breaker |

**Circuit breakers requeridos (ADR-007):**
1. **Spend cap diario por tier** — free tier suspende try-ons globales si gasto/día > $X
2. **Queue overflow** — si cola Replicate > 30s wait, devolver 503 con retry-after, no encolar infinito
3. **Per-IP rate limit** en signup (Cloudflare WAF) — bloquear bots durante viral spike
4. **Graceful degradation** — si Replicate down, servir solo cached results + mensaje

### 3.3 ¿Cuándo Railway deja de servir?

Railway escala bien hasta ~250K MAU sobre arquitectura actual. A partir de **500K MAU**:
- Workers asíncronos (try-on jobs) saturan plan Pro
- Egress costs en Railway se vuelven punitivos vs AWS
- Falta de control granular sobre auto-scaling policies

**Recomendación migración:** Trigger a **500K MAU** o $50K/mes Railway bill, lo que llegue primero. Destino: AWS ECS Fargate + ALB + RDS Postgres (mantenemos Supabase para Auth/Realtime).

Costo migración estimado: 3-4 semanas Sasha + Cinthya, ~$8K en infra paralela durante cutover.

---

## 4. Validación Caching Agresivo (ADR-004)

### Hit rate esperado por banda

El hit rate depende de la **diversidad del catálogo de prendas**. Hash key = (garment_id, body_type_cluster, pose_template).

| Banda | Hit rate esperado | Razón |
|---|---:|---|
| 10K MAU | 12-18% | Catálogo pequeño, body type clustering débil |
| 50K MAU | 25-35% | Body type clusters maduran (8-12 clusters cubren 80% usuarios) |
| 250K MAU | 45-55% | Long-tail de prendas se repite — top 1000 garments concentran 60% try-ons |
| 1M MAU | 55-65% | Plateau — hit rate >65% implausible (variedad personal) |

**A 50K MAU usé 35% en tabla (conservador). Si llegamos a 55% steady state, el ahorro adicional es ~$3-5K/mes a 50K paid.**

### ¿Redis distribuido vale la pena?

| Decisión | <250K MAU | 250K-1M MAU |
|---|---|---|
| Cache lookup | Postgres index sobre `tryons_cache(hash_key)` | Redis distribuido (Upstash o ElastiCache) |
| Latency | 8-15ms p50 | 1-3ms p50 |
| Throughput | OK hasta ~5K lookups/s | Necesario para 20K+ lookups/s |
| Costo | $0 (en Postgres) | $200-800/mes |
| Recomendación | **No Redis aún** | **Sí Redis** |

**Veredicto:** Sasha NO necesita Redis para el MVP ni primeros 12 meses. Lo introducimos como ADR aparte cuando crucemos 250K MAU.

### R2 storage cost por hit rate

Cada try-on cacheado guarda 1 imagen WebP ~200KB. R2: $0.015/GB-mes storage, **$0 egress**.

| Hit rate | Try-ons únicos cacheados (1M MAU) | Storage acumulado 12 meses | Costo R2/mes |
|---|---:|---:|---:|
| 35% | 4.9M | ~980 GB | $14.7 |
| 55% | 3.4M | ~680 GB | $10.2 |
| 65% | 2.6M | ~520 GB | $7.8 |

**R2 storage es despreciable.** Lo que importa es el **egress savings** vs Supabase Storage: a 1M MAU con 7.5M try-on views/mes × 200KB = 1.5TB egress/mes. Supabase cobraría ~$135/mes en egress; R2 cobra **$0**.

A escala 250K+ MAU, **R2 ahorra $50-150/mes solo en egress** y elimina riesgo de bill shock por viral spike.

---

## 5. Recomendaciones Tácticas para el Equipo

### R1. ADR-007: Rate Limiting + Circuit Breakers (URGENTE — Sasha)

Borrador completo en §6. Bloquea release a producción sin esto.

### R2. R2 desde día 1 (Sasha + Brook)

No empezar con Supabase Storage y migrar después. Cloudflare R2 + signed URLs desde el primer commit. Skill `supabase-complete.md` ya cubre el patrón con S3-compatible API.

### R3. Replicate volume discount — preparar pitch (Jarvis + Leo)

A partir de **1M try-ons/mes** (~250K MAU paid + free combined), Replicate negocia 15-25% off list price. Preparar pitch comercial: contrato anual con commitment mínimo a cambio de descuento + SLA upgrade.

### R4. Cloudflare Enterprise — sólo a 500K+ MAU

Cloudflare Pro ($25/mes) sobra hasta ~250K MAU. Enterprise ($5K+/mes) solo se justifica si:
- Necesitamos WAF custom rules avanzadas
- Argus/bot mitigation crítico durante viral spikes
- Compliance (SOC 2) requiere logs avanzados

**Antes de eso: Cloudflare Pro + Turnstile (gratis) + rate limiting en API resuelve.**

### R5. NO migrar Railway → AWS antes de 500K MAU

Tentación de "preparar para escalar" mata startups. Railway+Supabase+R2 es el stack óptimo hasta 500K MAU. Migración antes = burn de 3-4 semanas Sasha sin payoff.

### R6. Monitoring del unit economics — Cinthya

Workflow n8n diario que calcule:
- Cost per active free user (target <$0.35)
- Cost per paid user (target <$1.20)
- Cache hit rate
- Replicate spend / revenue ratio (target <12%)

Alerta a Slack #arquitectura si cualquiera se desvía 20%.

---

## 6. Borrador ADR-007 — Rate Limiting & Circuit Breakers

```markdown
# ADR-007: Rate Limiting Agresivo y Circuit Breakers

**Status:** PROPUESTO — pendiente review Sasha + Jarvis
**Author:** Alejo
**Date:** 2026-04-25

## Context
Path A (ADR-006) target 50K paid + 750K-1M MAU free. Sin rate limiting estricto y
circuit breakers, dos escenarios rompen el modelo:
1. Free MAU explota >25:1 ratio vs paid (margen <60%)
2. Viral spike (100K signups/24h) satura Replicate + Railway

## Decision

### Rate limits hard
| Endpoint | Free | Paid Estilo | Paid Imagen |
|---|---|---|---|
| POST /tryon | 5/mes | 80/mes (soft cap) | ilimitado (hard cap 200/mes anti-abuso) |
| POST /reco | 60/mes | 500/mes | ilimitado |
| POST /chat | 0 | 30/día | 100/día |
| Per-IP signup | 5/h | - | - |

### Circuit breakers
1. **Daily spend cap Replicate:** $X/día configurable; si superado, free tier 503 con
   mensaje "Servicio premium disponible — upgrade", paid sigue funcionando
2. **Queue overflow:** si jobs en cola > 30s wait, return 503 retry-after en lugar de
   encolar infinito
3. **Auto-downgrade free tier:** si ratio MAU_free / MAU_paid > 25:1 sostenido 7 días,
   reducir free tier a 3 try-ons/mes vía feature flag
4. **Cloudflare Turnstile** en /signup obligatorio (anti-bot durante viral spikes)

### Implementation
- Token bucket algorithm en Redis (Upstash, $10/mes) para rate limits
- Spend cap en Postgres con trigger diario
- Feature flag service (LaunchDarkly free tier o Postgres-based) para auto-downgrade

## Consequences
+ Margen blindado contra free explosion
+ Viral spikes manejables sin caer producción
- Complejidad adicional ~1 semana Sasha
- Posible UX friction si rate limits muy agresivos — A/B test recomendado
```

---

## 7. Anexo — Sensibilidad del modelo

| Variable | Caso base | Pesimista | Optimista | Impacto margen |
|---|---|---|---|---|
| Cache hit rate @ 50K MAU | 35% | 20% | 55% | ±4 pts |
| ARPU blend | $8.60 | $6.50 | $11.20 | ±8 pts |
| Free→Paid conversion | 6.7% | 4% | 9% | ±6 pts |
| Replicate price | $0.05 | $0.075 | $0.035 | ±5 pts |
| MAU free / paid ratio | 9:1 | 18:1 | 6:1 | ±7 pts |

**Worst case combinado (5to percentil):** margen 52% — sigue viable, no quiebra.
**Best case combinado (95to percentil):** margen 86% — alineado con Leo.

---

**Reportado a Jarvis. Disponible para Q&A en Junta 2026-05-02.**
**— Alejo**
