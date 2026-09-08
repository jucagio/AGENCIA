# COPY SOFT CAP — APPROVED VARIANTS

**Owner:** Leo (Comercial Senior)
**Status:** APPROVED — Ready for Erik (UI design) + Brook (Flutter integration)
**Context:** Opción F — 3 estilos/semana soft cap, FASHN tier routing

---

## Filosofía global

**Tono:** Abundancia, no escasez. Nunca usar lenguaje de "limit reached" o "blocked". El usuario completó su semana — ahora elige si quiere más o espera al reset del domingo.

---

## VARIANT A — "Unlock More" (Transactional)

| Campo | Valor |
|-------|-------|
| Text | "Ya usaste tus 3 estilos de esta semana. Desbloqueá 3 más por $2.99" |
| CTA | "Unlock 3 more" |
| Price visible | Sí — $2.99 inline |
| Psychology | Transactional directa, pragmático |
| Conversion target | 3-4% lunes / 14-18% sábado |
| Mejor uso | Martes a viernes (mid-week) |

**Leo verdict:**
- Psicología: APROBADO (transactional, directo)
- Honestidad: APROBADO (no esconde nada)
- CTA: APROBADO ("Unlock" + "$2.99" visible)
- Conversion: APROBADO (3-4% realista mid-week)
- **VEREDICTO: APROBADO**

---

## VARIANT B — "Complete Your Week" (Aspirational/FOMO)

| Campo | Valor |
|-------|-------|
| Text | "3 conjuntos explorados. El que más te gusta está cerca. Desbloquea la mejor versión de ti esta semana." |
| CTA | "Unlock premium looks" |
| Price visible | Secondary ($2.99 below CTA) |
| Psychology | Aspirational + urgencia FOMO |
| Conversion target | 8-12% overall (mejor jueves-sábado) |
| Mejor uso | Jueves a domingo (end-week) |

**Leo verdict:**
- Psicología: APROBADO (aspiracional, FOMO sano)
- Honestidad: APROBADO (emocional pero verdadero)
- CTA: APROBADO ("Unlock premium looks")
- Conversion: APROBADO (8-12% end-week realista)
- **VEREDICTO: APROBADO**

---

## VARIANT C — "Premium Anchor" (Monthly Upgrade)

| Campo | Valor |
|-------|-------|
| Text | "Acabas de explorar los 3 estilos libres. Prueba Premium ($9.99/mes) para ilimitadas." |
| CTA | "Try Premium" |
| Price visible | $9.99/mes inline + "or $2.99 esta semana" secondary |
| Psychology | Anchor mensual (precio alto, valor percibido alto) |
| Conversion target | 6-9% (heavy users, conversion premium) |
| Mejor uso | Repeat users con engagement score >=7 |

**Leo verdict:**
- Psicología: APROBADO (anchor pricing, premium positioning)
- Honestidad: APROBADO (mensual explícito)
- CTA: APROBADO ("Try Premium" + $9.99/mes visible)
- Conversion: APROBADO (6-9% heavy users)
- **VEREDICTO: APROBADO**

---

## VARIANT D — "Reset Anticipation" (Retention/Habit)

| Campo | Valor |
|-------|-------|
| Text | "Tu semana de estilo está completa. El domingo tendrás 3 nuevos. ¿O prefieres explorar YA?" |
| CTA | "Explore now" (primary) + "Esperar al domingo" (secondary) |
| Price visible | $2.99 si tap "Explore now" |
| Psychology | Habit loop (Sunday ritual) + opcional upgrade |
| Conversion target | 2-3% lunes (bajo urgency, refuerza habit) |
| Mejor uso | Lunes (reset day) + at-risk churn users |

**Leo verdict:**
- Psicología: APROBADO (refuerza ritual dominical)
- Honestidad: APROBADO (reset timing es verdadero)
- CTA: APROBADO ("Explore now" primary, espera secondary)
- Conversion: APROBADO (2-3% lunes, meta es retention)
- **VEREDICTO: APROBADO**

---

## MAPPING — Day of Week × User Segment

### Por día de la semana

| Día | Variant | Razón |
|-----|---------|-------|
| Lunes | D | Reset anticipation, refuerza ritual |
| Martes | A | Transactional pragmático |
| Miércoles | A | Transactional pragmático |
| Jueves | B | FOMO aspirational |
| Viernes | B | FOMO aspirational |
| Sábado | B | Urgencia máxima weekend |
| Domingo | B | Último día antes reset, peak FOMO |

### Por segmento de usuario (override día)

| Segmento | Variant | Trigger |
|----------|---------|---------|
| Heavy user | C | engagement_score >= 7 OR 3+ tries/week regulares |
| New user (week 1) | B | first_week_completed = false (sin urgency, aspirational) |
| At-risk churn | D | days_since_last_session > 5 |
| Default | (por día) | Tabla anterior |

### Lógica de selección (pseudo-code)

```
def select_variant(user, today):
    if user.engagement_score >= 7:
        return "C"
    if user.is_new_user:
        return "B"
    if user.days_since_last_session > 5:
        return "D"
    return DAY_MAP[today.weekday()]  # A/B/D por día
```

---

## A/B TESTING STRATEGY (Sprint 1 — week 2)

**Setup:**
- Split 25% × 4 variants (igual peso inicial)
- Population: usuarios que llegan a cap (3 estilos completados en semana)
- Duración: 14 días (2 ciclos semanales completos)
- Sample size mínimo: 200 usuarios por variant (800 total)

**Métricas primarias:**
- Conversion rate (cap shown → payment completed)
- Revenue per cap-event (RPC)

**Métricas secundarias:**
- 7-day retention post-cap
- Sentiment (rating si app pide review post-purchase)
- Refund rate

**Decisión post-test:**
- Variant ganador por segmento (no global)
- Si winner statistical significance >95%, promover a 60% traffic
- Iterar 2 variants challengers en 40% traffic restante

---

## COPY SNIPPETS — JSON para Erik UI

```json
[
  {
    "variant_id": "A",
    "name": "Unlock More",
    "text": "Ya usaste tus 3 estilos de esta semana. Desbloqueá 3 más por $2.99",
    "cta_text": "Unlock 3 more",
    "cta_color": "#FFB800",
    "cta_secondary": null,
    "price_display": "$2.99",
    "price_position": "inline"
  },
  {
    "variant_id": "B",
    "name": "Complete Your Week",
    "text": "3 conjuntos explorados. El que más te gusta está cerca. Desbloquea la mejor versión de ti esta semana.",
    "cta_text": "Unlock premium looks",
    "cta_color": "#D4AF37",
    "cta_secondary": null,
    "price_display": "$2.99",
    "price_position": "below_cta"
  },
  {
    "variant_id": "C",
    "name": "Premium Anchor",
    "text": "Acabas de explorar los 3 estilos libres. Prueba Premium ($9.99/mes) para ilimitadas.",
    "cta_text": "Try Premium",
    "cta_color": "#8B5CF6",
    "cta_secondary": "Solo esta semana — $2.99",
    "price_display": "$9.99/mes",
    "price_position": "inline"
  },
  {
    "variant_id": "D",
    "name": "Reset Anticipation",
    "text": "Tu semana de estilo está completa. El domingo tendrás 3 nuevos. ¿O prefieres explorar YA?",
    "cta_text": "Explore now",
    "cta_color": "#FFB800",
    "cta_secondary": "Esperar al domingo",
    "price_display": "$2.99",
    "price_position": "on_tap"
  }
]
```

---

**Status:** Listo para Erik (S06 design) + Brook (Flutter state machine cap screen).
