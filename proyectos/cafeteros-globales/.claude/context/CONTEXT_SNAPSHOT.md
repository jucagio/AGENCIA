# CAFETEROS GLOBALES — Context Snapshot (27 mayo 2026)

**Status:** ⚠️ Validación pendiente (PAUSA recomendada antes de desarrollo)

## Elevator Pitch

Marketplace B2B que conecta 557K cafeteros colombianos con compradores distribuidores globales. Diferenciador: Sello FNC + Logística DHL integrada + Compliance OFAC/KYC. MVP target: 100 tx/mes, 10 cafeteros, ~100 toneladas/mes año 1.

## Métricas de Éxito

| Métrica | Target | Timeline |
|---------|--------|----------|
| Cafeteros activos | 10 (año 1) | Q4 2026 |
| Transacciones/mes | 100 (año 1) | Q4 2026 |
| Volumen café/mes | ~100 toneladas | Q4 2026 |
| Conversión leads→sellers | >30% | Q4 2026 |
| NPS cafeteros | >40 | Q4 2026 |
| NPS buyers | >50 | Q4 2026 |

## Stack Técnico

- **Frontend:** Next.js 15 + Tailwind 4 (Vercel)
- **Backend:** Python FastAPI (Railway)
- **Database:** PostgreSQL Supabase (RLS multi-tenant)
- **Payments:** Stripe Connect Express (KYC + OFAC)
- **Mobile:** Flutter (MVP, no Beta)
- **Logistics:** Freight forwarder partner (DHL Express manual Beta)
- **Observability:** Sentry, Better Stack, PostHog

## Equipo Asignado

- **Jarvis:** CEO proyecto, coordinación
- **Sasha:** Backend (auth, catálogo, órdenes, Stripe)
- **Brook:** Frontend web + mobile Flutter
- **Erik:** UI/UX, sistema de diseño
- **Cinthya:** Automatización n8n (notificaciones, tracking)
- **Alejo:** Arquitectura, review decisiones críticas

## Timeline Propuesto (PAUSADO)

**OPCIÓN A (Recomendado):**
- Jun 1–30: Validación (legal, Stripe, FNC, discovery, logística)
- Jul 1: Kickoff técnico (si GO)
- Ago 15: Beta launch
- Dic 15: MVP launch

**OPCIÓN B (NOT RECOMMENDED):**
- Jun 1: Kickoff directo
- Ago 15: Beta (probable fail sin validación)
- Dic 15: MVP

## Presupuesto (año 1)

| Categoría | Monto | Notas |
|-----------|-------|-------|
| Desarrollo Beta | $34.8–44.4K | 580–740 horas equipo |
| Desarrollo MVP | $29.9–39.0K | 510–670 horas equipo |
| Infraestructura | ~$1.8K | Hosting, services |
| Terceros (Stripe, DHL, etc) | ~$43K | Variable GMV |
| Costos ocultos | $15–30K | Legal, compliance, marketing, support |
| **TOTAL realista** | **$100–130K** | Año 1 completo |

## Riesgos Críticos (Ego)

### Los 5 Killers (prioritarios)

1. 🔴 **Stripe Connect rechaza aplicación** — High risk vertical (agricultural commodities), KYB cafeteros rurales débil
2. 🔴 **Responsabilidad tributaria desconocida** — DIAN, retención fuente, IVA; sin abogado
3. 🔴 **FNC no alía formalmente** — "Bendición informal" no es contrato
4. 🔴 **DHL Express no es solución logística** — Toneladas van por flete aéreo/marítimo, no courier
5. 🔴 **Cero clientes validados** — Sin LOIs de cafeteros/buyers a 3 meses de Beta

### 20 riesgos identificados

Ver `proyectos/cafeteros-globales/.claude/context/EGO_AUDIT.md` para lista completa con probabilidad/impacto.

## Intel de Mercado (Jade)

### Oportunidad

- 557K familias cafeteras Colombia
- 96% son pequeños (<5 hectáreas)
- $5.5B en exportaciones 2025 (+30% vs 2024)
- 96% sin acceso directo a buyers globales = dependencia de intermediarios que capturan 70–90% valor

### Competencia

- **Algrano:** 10 años, 4K conexiones, modelo validado (Suiza)
- **CAFIX:** Plataforma FNC, pero solo conecta conocidos
- **Cropster:** Herramienta operacional, no marketplace
- **Alibaba/TradeKey:** Genéricas, sin especialización

### Diferenciador Nuestro

Triada única:
- Sello FNC (confianza institucional)
- Logística DHL integrada
- Compliance OFAC/KYC automático
= Única plataforma donde tostador global compra directo de cafetero local

## Arquitectura (Alejo)

### Patrón

Monolito modular FastAPI (NO microservicios por tamaño 100 tx/mes).

```
Frontend (Next.js)  →  Backend (FastAPI)  →  PostgreSQL RLS
                           ↓
                    Stripe Connect
                           ↓
                    Workers + Webhooks
```

### ADRs Críticos

- ADR-001: Monolito vs Microservicios → **Monolito**
- ADR-002: Stripe Connect Custom vs Express → **Express** (faster onboarding)
- ADR-003: DHL API Beta vs Manual → **Manual** (quote estático)
- ADR-004: RLS vs separate schemas → **RLS** (scalable)
- ADR-005: OFAC vendor vs Stripe nativo → **Stripe** (year 1)

## Próximos Pasos (ESTA SEMANA)

**Decisión requerida:** ¿PAUSA 4 semanas para validación (recomendado) O kickoff inmediato (no recomendado)?

| # | Acción | Owner | Deadline |
|---|--------|-------|----------|
| 1 | Decisión PAUSA vs NO-PAUSA | Juan Camilo + Jarvis | HOY |
| 2 | Contratar abogado comercio exterior | Juan Camilo | MAY 29 |
| 3 | Abrir Stripe Connect application | Sasha + Jarvis | MAY 29 |
| 4 | Contacto ProColombia → FNC intro | Yang + Leo | MAY 30 |
| 5 | Kickoff técnico (si GO) | Jarvis | JUN 1 ó JUL 1 |

---

**Documentos completos:**
- `PLAN.md` — Plan ejecutivo completo (7 secciones)
- `CLAUDE.md` — Instrucciones proyecto, equipo, riesgos
- `EGO_AUDIT.md` — Auditoría de riesgos detallada (adjunto follow-up)
- `JADE_INTEL.md` — Análisis mercado, FNC, regulación (adjunto follow-up)
- `ALEJO_ARQUITECTURA.md` — Stack, presupuesto, timeline, ADRs (adjunto follow-up)

---

**Actualizado:** 27 mayo 2026 | **Siguiente revisión:** 10 junio 2026 (checkpoint validación)
