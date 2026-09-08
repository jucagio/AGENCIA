# MESSAGING STRATEGY — FINAL

**Owner:** Leo (Comercial Senior)
**Project:** Asesor Imagen AI — Soft cap monetization
**Status:** FINAL — Sprint 1 ready

---

## 1. TONO GLOBAL

### Principio fundacional
**Abundancia, no escasez.** El usuario nunca debe sentirse "bloqueado", "limitado" o "castigado". Completó su semana de exploración — ahora tiene opciones.

### Lenguaje prohibido
- "Limit reached" / "Has alcanzado tu límite"
- "Blocked" / "Bloqueado"
- "You can't" / "No puedes"
- "Restricted" / "Restringido"
- "Out of credits" / "Sin créditos"

### Lenguaje aprobado
- "Ya exploraste tus 3 estilos"
- "Tu semana está completa"
- "Desbloquea más"
- "Continúa explorando"
- "El domingo tendrás nuevos"

### Personalidad de marca
- **Cómplice, no autoridad** — Habla como una amiga estilista, no como un cajero
- **Aspiracional, no pretenciosa** — "La mejor versión de ti", no "estilo premium élite"
- **Honesta, no manipuladora** — Sin countdown timers falsos ni "solo quedan 2 spots"

---

## 2. COPY TONE GUIDE

### Transactional vs Aspirational — Cuándo usar cada uno

| Contexto | Tono | Ejemplo |
|----------|------|---------|
| Mid-week (mar-mié), usuario pragmático | Transactional | "Desbloqueá 3 más por $2.99" |
| End-week (jue-dom), peak emocional | Aspirational | "La mejor versión de ti esta semana" |
| Heavy user, engagement alto | Premium anchor | "Prueba Premium para ilimitadas" |
| Lunes / churn-risk | Retention/habit | "El domingo tendrás 3 nuevos" |

### Reglas de copy

1. **Máximo 2 frases** en pantalla de cap. Si necesita 3, está mal escrito.
2. **CTA verbo de acción + beneficio.** "Unlock 3 more" mejor que "Click here".
3. **Precio siempre visible.** Ocultar precio = desconfianza.
4. **Sin signos de exclamación.** Urgencia se construye con contenido, no con tipografía.
5. **Nunca culpar al usuario.** "Tu semana está completa" ≠ "Te quedaste sin estilos".

---

## 3. DYNAMIC SELECTION LOGIC

### Inputs del usuario (Brook implementa en Flutter)

```dart
class UserContext {
  final int engagementScore;        // 0-10
  final bool isNewUser;             // true si week 1
  final int daysSinceLastSession;   // entero
  final DateTime today;             // para day-of-week
  final int weeklyTriesUsed;        // 0-3
}
```

### Selección de variant

```dart
String selectVariant(UserContext ctx) {
  // Override por segmento (priority order)
  if (ctx.engagementScore >= 7) return 'C';
  if (ctx.isNewUser) return 'B';
  if (ctx.daysSinceLastSession > 5) return 'D';

  // Default por día de semana
  switch (ctx.today.weekday) {
    case DateTime.monday: return 'D';
    case DateTime.tuesday:
    case DateTime.wednesday: return 'A';
    case DateTime.thursday:
    case DateTime.friday:
    case DateTime.saturday:
    case DateTime.sunday: return 'B';
    default: return 'A';
  }
}
```

### Override por A/B test (Sprint 1 week 2+)

Durante el test, override la selección para asignar 25% a cada variant random:

```dart
String variant = abTestActive
    ? assignRandomVariant(ctx.userId)  // 25/25/25/25
    : selectVariant(ctx);              // smart selection
```

---

## 4. SUCCESS METRICS

### Conversion rate targets (por variant)

| Variant | Target conversion | Mejor segmento |
|---------|-------------------|----------------|
| A — Unlock More | 3-4% (mar-mié) → 14-18% (sáb) | Mid-week mainstream |
| B — Complete Your Week | 8-12% overall | End-week + new users |
| C — Premium Anchor | 6-9% | Heavy users (LTV alto) |
| D — Reset Anticipation | 2-3% (lunes), retention focus | Lunes + at-risk |

### Métricas globales del soft cap (target Sprint 1 mes 1)

| Métrica | Target | Stretch |
|---------|--------|---------|
| Cap-to-purchase rate (overall) | 6% | 9% |
| ARPU monthly (free users) | $1.20 | $1.80 |
| 7-day retention post-cap | 65% | 75% |
| Premium upgrade rate (de cap event) | 1.5% | 2.5% |
| Refund rate | <2% | <1% |

### Métricas anti-objetivo (señales de alerta)

- Refund rate >3% → copy es manipulador, ajustar
- 1-star reviews mencionando "limit/blocked" → tono mal calibrado
- Day-1 churn >40% en lunes → variant D fallando
- Conversion <2% sostenido en variant B → reescribir aspirational

---

## 5. ROADMAP DE COPY

### Sprint 1 (esta semana)
- Erik diseña S06 con las 4 variants
- Brook integra selectVariant() en Flutter
- Hardcode mapping día → variant (sin A/B test todavía)

### Sprint 1 — week 2
- Activar A/B test (25% split × 4 variants)
- Recolectar 200 usuarios por variant mínimo
- Dashboard de conversion en tiempo real (Brook)

### Sprint 2
- Análisis post-test
- Promover winner por segmento a 60% traffic
- Iterar 2 challengers nuevos en 40%

### Sprint 3+
- Personalización profunda por behavior (ML-driven copy)
- Localización ES-MX / ES-AR / EN-US (Yang investiga matices culturales)

---

## 6. RESPONSABLES

| Tarea | Owner | Status |
|-------|-------|--------|
| Validación copy 4 variants | Leo | DONE |
| Mapping día × segmento | Leo | DONE |
| Diseño S06 con variants | Erik | EN ESPERA → kickoff hoy |
| Integración Flutter | Brook | EN ESPERA → tras Erik |
| Setup A/B test infrastructure | Sasha | Sprint 1 week 2 |
| Dashboard métricas conversion | Brook | Sprint 1 week 2 |
| Análisis post-test | Leo + Yang | Sprint 2 |

---

**Leo cierra:** Copy validado, mapping definido, métricas claras. Erik tiene todo lo que necesita para S06. El silencio cierra deals — el copy bien escrito los cierra solos.
