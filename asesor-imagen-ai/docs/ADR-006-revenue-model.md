# ADR-006: Modelo Financiero — 50K Paid Users (Path A)

**Status:** ✅ APROBADO por Juan Camilo (2026-04-29)
**Decided by:** Juan Camilo (Accionista) + Jarvis (CEO) + Leo (Comercial)
**Supersedes:** Modelo financiero original (50K paid implícitamente blend)

---

## Context

El modelo financiero original del MVP indicaba "$24K/mes profit @ 50K users" sin clarificar si los 50K eran paid puros o blend (free+paid).

Leo, durante el diseño de pricing strategy, identificó la ambigüedad y pidió clarificación. Implicaciones drásticamente diferentes:

- **Path A (paid puros):** 50K paid users + ~600K-1M MAU free implícito = **$350-560K MRR**
- **Path B (blend):** 50K total con dominancia free = ~$60K MRR

Path A coincide con benchmarks de competidores (Acloset, Whering) y con el pricing fijado por Leo.

---

## Decision

**Adoptamos Path A:** Target = **50K paid users puros en mes 12.**

### Pricing aplicable (confirmado)

| Tier | LATAM | US |
|------|-------|----|
| Free | $0 | $0 |
| Estilo (Pro) | $4.99/mo | $9.99/mo |
| Imagen (Premium) | $9.99/mo | $19.99/mo |
| Yearly discount | -33% | -33% |
| Trial | 7 días sin tarjeta | 7 días sin tarjeta |

### Forecast aprobado

| Mes | Paid users | MRR | Cumulative ARR |
|-----|-----------|-----|----------------|
| 3 | 4,500 | $25K | $300K |
| 6 | 18,000 | $115K | $1.4M |
| 12 | **50,000** | **$350-560K** | **$4.2-6.7M** |

ARPU blend proyectado: **$7-11.20/mes** (dependiendo mix LATAM/US).

---

## Consequences

### Positivas
- **Margen bruto mejora:** del 71% (modelo original Alejo) a **85%+ esperado** con caching agresivo
- **Espacio para CAC alto:** podemos invertir hasta $20-40 CAC con LTV $60-130 (mantener LTV/CAC > 3)
- **Inversión en producto justificada:** mejor calidad de try-on (Replicate models top tier) viable porque margen lo soporta
- **Path a $5M+ ARR claro** sin requerir 100K+ paid (cuello escala más allá)

### Negativas / Riesgos
- **Conversión free→paid debe ser 5-8%** (industry benchmark 2-3%). Requiere paywall agresivo + value clear
- **Cost de Replicate sigue dominando:** a 50K paid haciendo 30 try-ons/mes = 1.5M try-ons/mes × $0.05 = $75K/mes sin caching
  - **ADR-004 (caching) NO opcional** — sin él, margen colapsa
  - **ADR-003 (idempotency) NO opcional** — un bug de duplicación = $miles perdidos/día a escala
- **MAU free no controlado:** si free crece a 2M+ y cada uno hace 5 try-ons/mes gratis = $500K/mes en costos. Mitigación obligatoria:
  - Free tier: máximo 5 try-ons/mes (definido por Leo)
  - Caching agresivo (ADR-004) reduce 35-40% costos
  - Watermark + límites de export

### Acciones derivadas (handoffs)

1. **Alejo** → Recalcular cost projection con Path A (margen 85%+), validar que ADR-004 aguante 1M+ MAU free
2. **Leo** → Mantener forecast actual (ya alineado con Path A)
3. **Sasha** → Sin cambios al plan técnico — los ADRs 001-005 siguen vigentes
4. **Erik** → Diseñar paywall premium que justifique upgrade $4.99-9.99 (objeción de precio en LATAM real)
5. **Cinthya** → Workflow de notif "Te quedan 2 try-ons este mes" para empujar upgrade
6. **Yang** → Validar que 660K-1M MAU free es alcanzable con marketing budget proyectado

---

## Validación final

Este ADR queda confirmado en la **Junta Estratégica del sábado 2026-05-02**. Si los datos de Alejo (cost recalc) o Leo (CAC viability) no soportan el modelo, se reabrirá la decisión.

**Owners:** Jarvis (gestión), Leo (validación comercial trimestral), Alejo (validación financiera trimestral).
