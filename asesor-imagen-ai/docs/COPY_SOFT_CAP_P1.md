# Copy Soft Cap P1 — Asesor Imagen AI
**Fecha:** 2026-05-19
**Autor:** Leo (Agente Comercial Senior)
**Para:** Brook (UI), Erik (visual), Jarvis (decisión)
**Status:** Listo para implementar — pendiente confirmación stack de Alejo
**Contexto:** Usuario llega a 5/5 try-ons esta semana. Chat muestra mensaje contextual + CTA. NO bloquea keyboard. Soft incentive a upgrade.

---

## Principios psicológicos aplicados

Todo el copy obedece 5 reglas no negociables:

1. **Abundancia, no escasez.** El reset semanal es un REGALO, no un límite. Nunca usar "solo tienes", "se acabó", "límite alcanzado".
2. **Empowerment, no transacción.** El usuario es protagonista de su estilo, no consumidor de créditos.
3. **Tiempo como variable activa.** El día de la semana cambia la urgencia. El copy DEBE variar por día.
4. **Reframe del cap como logro.** "Has explorado 5 conjuntos" suena a hito, no a frustración.
5. **CTA específico, no genérico.** "Upgrade" es vago. "Desbloquea 5 más para el viernes" es accionable.

**Reglas de tono:**
- 2-3 líneas máximo (cabe en chat mobile en una pantalla sin scroll)
- Nunca usar signos de exclamación duplicados ni emojis (rompe el tono aspiracional Aether Luxe)
- Nunca usar palabras transaccionales: "comprar", "pagar", "límite", "bloqueado"
- Usar palabras aspiracionales: "desbloquea", "completa", "descubre", "explora", "tu mejor versión"

---

## Estructura del mensaje (anatomía)

```
[LÍNEA 1 — RECONOCIMIENTO]   "Has explorado X / Tu semana de estilo está activa"
[LÍNEA 2 — REFRAME + OFERTA]  "El conjunto perfecto está cerca. [Precio]"
[BOTÓN CTA]                   "Acción específica" (no "Upgrade" genérico)
[LINK SECUNDARIO]             "Opción menor / esperar reset"
```

---

## 4 Variantes para A/B testing

### VARIANTE A — "Unlock More" (transactional-friendly)

**Hipótesis:** Usuarios pragmáticos responden a oferta clara, precio visible, beneficio inmediato.

```
Has explorado 5 conjuntos esta semana.
Desbloquea 5 más ahora por $2.99.

[Botón primario] Desbloquear 5 más
[Link secundario] Ver Estilo+ (mensual)
```

**Cuándo brillar:** Usuario que ya valoró el producto, quiere más HOY sin compromiso recurrente.
**Conversion esperada (touchpoint blended):** 9-11% al one-shot, 2-3% al mensual.

---

### VARIANTE B — "Complete Your Week" (emotional + aspirational)

**Hipótesis:** Usuarios emocionales (fashion-forward, Gen Z, mujer 25-40) responden mejor a narrativa de logro y completitud.

```
5 looks creados. El sexto podría ser EL look.
Completa tu semana con Estilo+ por $9.99/mes.

[Botón primario] Activar Estilo+
[Link secundario] Solo esta semana — $2.99
```

**Cuándo brillar:** Usuario que llega al cap en jueves-sábado, contexto emocional (busca outfit para evento).
**Conversion esperada:** 4-6% al mensual, 5-7% al one-shot. **Mejor LTV** porque captura recurring.

---

### VARIANTE C — "Premium Anchor" (aspirational positioning)

**Hipótesis:** Anchor del producto premium primero hace que el one-shot parezca "el camino fácil" (decoy effect).

```
Tu estilo merece más que 5 looks por semana.
Estilo+ — try-ons ilimitados, looks guardados, asesoría premium. $9.99/mes.

[Botón primario] Probar Estilo+ (primer mes $4.99)
[Link secundario] O desbloquea 5 más — $2.99
```

**Cuándo brillar:** Usuario heavy (cap por 2da-3ra vez), claramente engaged, listo para commitment.
**Conversion esperada:** 7-9% al mensual con descuento, 3-4% al one-shot. **Mayor ARPU.**

---

### VARIANTE D — "Reset Anticipation" (delay tolerance test)

**Hipótesis:** Si reset está cerca (domingo), validar si el usuario prefiere esperar vs pagar. Este copy MIDE elasticidad real.

```
Has completado tu semana de estilo.
El domingo a las 23:59 tienes 5 try-ons nuevos. ¿O los necesitas ya?

[Botón primario] Desbloquear ahora — $2.99
[Link secundario] Esperaré al domingo
```

**Cuándo brillar:** Solo lunes-martes (reset lejos). Mide quién paga vs quién espera. Insight de pricing elasticity.
**Conversion esperada:** 3-5% al one-shot (menor, pero data invaluable para pricing).

---

## Variantes contextuales por día de la semana

Sobre las 4 variantes base, el SISTEMA escoge la versión por día. Esto NO es A/B — es contextual targeting:

| Día del cap | Variante recomendada | Razón | Conversion esperada |
|---|---|---|---|
| **Domingo (post-reset)** | NUNCA mostrar cap — reset es inmediato. Caso edge improbable. | — | — |
| **Lunes** | Variante D (Reset Anticipation) | Reset cerca, mide elasticidad. Baja urgencia. | 3-4% |
| **Martes** | Variante A (Unlock More) | Pragmático, sin urgencia emocional. | 5-7% |
| **Miércoles** | Variante A o B (split test) | Fin de semana asoma — empieza a importar. | 6-8% |
| **Jueves** | Variante B (Complete Your Week) | Pico de planificación de outfit del finde. | 9-12% |
| **Viernes** | Variante B con urgencia "hoy" | Outfit del viernes/sábado se decide HOY. | 12-15% |
| **Sábado** | Variante B + Variante C (heavy users) | Pico de necesidad real. Máxima urgencia. | 14-18% |

### Implementación práctica para Brook

```typescript
function getSoftCapCopy(dayOfWeek: number, capCountThisMonth: number) {
  // Heavy user (3+ caps este mes) — siempre Variante C
  if (capCountThisMonth >= 3) return VARIANT_C;

  // Por día de la semana
  switch (dayOfWeek) {
    case 1: return VARIANT_D;          // Lunes
    case 2: return VARIANT_A;          // Martes
    case 3: return Math.random() > 0.5 ? VARIANT_A : VARIANT_B;  // Miércoles split
    case 4: return VARIANT_B;          // Jueves
    case 5: case 6: return VARIANT_B_URGENT;  // Viernes/Sábado
    default: return VARIANT_A;
  }
}
```

---

## Versiones con urgencia explícita (viernes/sábado)

### Variante B-URGENT (Viernes)
```
5 conjuntos explorados. Tu look del viernes está a un try-on.
Estilo+ por $9.99/mes — ilimitado este fin de semana.

[Botón primario] Activar para esta noche
[Link secundario] Solo 5 más — $2.99
```

### Variante B-URGENT (Sábado)
```
Tu sábado merece el outfit correcto.
Desbloquea try-ons ilimitados con Estilo+ — $9.99/mes.

[Botón primario] Estilo+ ahora
[Link secundario] Solo este look — $2.99
```

---

## Versión Domingo (celebración del reset)

**No es soft cap, es notificación push o welcome message.** Cuando usuario abre app domingo post-reset:

```
Tu semana de estilo empieza ahora.
5 try-ons frescos te esperan. ¿Cuál será tu primer look?

[Botón primario] Crear mi primer look
```

**Propósito:** Refuerza el habit loop semanal. Confirma percepción de "regalo renovable". Genera retorno al app cada domingo (clave para retention D30).

---

## A/B Testing Strategy

### Fase 1 — Validation (Semanas 1-2)
- **Test:** Variante A vs B vs C, mismo segmento (todos los caps, sin variar por día)
- **Sample:** Mínimo 300 caps/variante (900 total) para significancia 95%
- **Métrica primaria:** Conversion total (one-shot + mensual) por cap
- **Métrica secundaria:** ARPU resultante por variante (mensual pesa más)
- **Decisión:** Ganadora avanza a Fase 2

### Fase 2 — Contextual targeting (Semanas 3-4)
- **Test:** Ganadora Fase 1 (estática) vs sistema contextual por día (tabla arriba)
- **Hipótesis:** Contextual sube conversion 25-35% vs estática
- **Métrica:** Conversion blended + LTV cohort

### Fase 3 — Optimización fina (Mes 2+)
- Variantes copy con micro-cambios (palabras, longitud, posición CTA)
- Test de precio one-shot ($2.99 vs $3.99 vs $4.99)
- Test de oferta mensual first-month ($4.99 vs $6.99 vs $7.99)

---

## Casos especiales

### Usuario premium (ya pagó Estilo+)
No aplica soft cap. Try-ons ilimitados. Si llega a algún rate limit técnico (raro), mostrar:
```
Estás generando muchos looks. Dame un momento para crear el siguiente.
```

### Usuario nuevo (primera vez que cap, día 1-2)
Override de la lógica por día — mostrar VARIANTE C (Premium Anchor) para capturar discovery momentum:
```
5 looks creados en tu primer día. Tu estilo merece más.
Estilo+ — primer mes $4.99. Después $9.99/mes.

[Botón primario] Activar Estilo+
[Link secundario] Solo 5 más — $2.99
```

### Usuario que rechazó upgrade 2+ veces
Soft fatigue — reducir intensidad. Mostrar VARIANTE D con mensaje suave:
```
Has explorado tu semana. El domingo se reinicia.
Si lo necesitas antes, son $2.99.

[Botón primario] No, gracias — espero al domingo
[Link secundario] Desbloquear ahora
```

(Botones invertidos: el "no gracias" es PRIMARIO. Reduce presión. Aumenta retention long-term. Vendedor sabio: no quema al lead.)

---

## Plan de pivote según decisión de Alejo

### Si Opción A (3/sem FASHN)
Reemplazar "5" por "3" en todo el copy. Mensaje sigue funcionando — incluso mejor (cap llega más rápido, más touchpoints). Ajuste de precio one-shot a "+3 más por $2.99".

### Si Opción D (5/sem PAID-ONLY, 1 try-on free)
COPY DISTINTO — soft cap se reemplaza por hard paywall después de 1 try-on. Mensaje:
```
Tu primer look está listo. ¿Listo para descubrir tu estilo completo?
Estilo+ — try-ons ilimitados, looks guardados. $9.99/mes.

[Botón primario] Activar Estilo+
[Link secundario] Ver demo de Estilo+ (sin compromiso)
```
**ADVERTENCIA:** Esta opción mata el discovery loop. Mi recomendación (Leo) en STRATEGY_P1_WEEKLY_RESET.md es rechazarla salvo que margen sea imposible con free tier.

### Si Opción E (5/sem con Flux $0.04)
Copy IDÉNTICO a las 4 variantes propuestas. Es el escenario óptimo — confirma 5/sem como diferencial Yang.

---

## Checklist de implementación (Brook)

- [ ] Crear componente `<SoftCapModal>` con 4 variantes parametrizadas
- [ ] Implementar lógica `getSoftCapCopy()` por día de semana
- [ ] Implementar tracking de eventos: `soft_cap_shown`, `soft_cap_cta_primary`, `soft_cap_cta_secondary`, `soft_cap_dismissed`
- [ ] Implementar `capCountThisMonth` (heavy user detection)
- [ ] Implementar override de "usuario nuevo" (primer cap, día 1-2)
- [ ] Implementar fatigue logic (2+ rechazos → variante D suave)
- [ ] A/B test framework: feature flag por variante
- [ ] Welcome message domingo post-reset (push opcional + in-app banner)

---

## Métricas de éxito del copy

**Por touchpoint (cada soft cap mostrado):**
- Click-through rate al CTA primario: target 18-25%
- Conversion del CTA primario a compra: target 35-50% (de los que clickearon)
- **Conversion total (compra / cap mostrado): target 8-14% blended**

**Por usuario (cohort):**
- Usuarios que convierten en su primer cap: target 6-10%
- Usuarios que convierten al 2do-3er cap: target acumulado 15-22%
- ARPU del cohort que vio soft cap: target $1.40+

**Kill criteria copy:**
- Si CTR primario <12% en semana 1 → rework de copy
- Si conversion <6% blended → revisar precio + valor percibido
- Si "dismiss" rate >70% → reducir frecuencia del modal o suavizar tono

---

**Próximos pasos:**
1. Esperar decisión de Alejo (stack E/A/D)
2. Brook implementa componente con variantes A, B, C, D
3. Cinthya configura tracking de eventos en n8n
4. Launch con Fase 1 A/B testing en semana 1 post-launch
5. Leo revisa métricas semana 2 y decide ganadora

**Firmado:** Leo, 2026-05-19
