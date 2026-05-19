# DECISIONES CRÍTICAS UX — Para Juan Camilo

**Owner:** Juan Camilo Gil  
**Fecha límite:** HOY o MAÑANA (2026-05-18/19)  
**Impact:** Bloquea diseño de Erik (S05-S11)  
**Status:** ⏳ PENDIENTE

---

## 🚨 ¿POR QUÉ ESTO ES CRÍTICO?

- Erik no puede finalizar 6 screens (S05-S09, S11) sin estas respuestas
- Cada día de retraso = pérdida de 1-2 días en timeline de implementación
- Sprint 4 (Try-On visual, la feature principal) depende de estas decisiones

---

## DECISIÓN 1: APP NAME (BRANDING)

**Pregunta:** ¿Qué nombre aparece en la UI y marketing?

```
Opción A: "AI Fit Check" (actual, tech-forward, inglés)
Opción B: "Asesor de Imagen" (local, familiar, español)
Opción C: Dual (logo "AI Fit Check", tagline "Tu Asesor de Imagen")
```

**Impacto:**
- Título en splash screen, header, app store
- Branding en landing page, redes sociales
- Tono de voz general (tech vs lifestyle)

**Recomendación comercial (Leo):**  
"AI Fit Check" es mejor para SaaS B2B + LATAM premium (apelar a tech-savvy). "Asesor de Imagen" para lifestyle B2C. ¿Target es B2B o B2C?

**Decision:**  
[ ] A — "AI Fit Check"  
[ ] B — "Asesor de Imagen"  
[ ] C — Dual approach  
[ ] Otra: ___________

---

## DECISIÓN 2: FLUJO TRY-ON (UX FEATURE)

**Pregunta:** ¿Cómo selecciona el usuario prendas en Virtual Try-On?

```
Opción A: Upload directo de foto de prenda (simple, ágil)
Opción B: Seleccionar de Wardrobe existente (requiere onboarding closet)
Opción C: Ambos (hybrid, máxima flexibilidad)
```

**Impacto:**
- S04 Virtual Try-On screen complexity
- S05 My Wardrobe urgencia (¿required antes de try-on o después?)
- Conversion funnel (¿cuán rápido usuario llega a first try-on?)

**Recomendación comercial (Leo):**  
Opción A (upload directo) = DAU aumenta 40% (user tries-on mismo en primer login).  
Opción B = requiere buildup de wardrobe (higher barrier).  
Recomendación: **Opción C con A como default**, B como "next time".

**Decision:**  
[ ] A — Upload directo  
[ ] B — Seleccionar de Wardrobe  
[ ] C — Ambos (hybrid)  
[ ] Otra: ___________

---

## DECISIÓN 3: ONBOARDING CON ANÁLISIS DE CUERPO

**Pregunta:** ¿Body analysis es obligatorio o opcional después de registro?

```
Opción A: Obligatorio en onboarding (3-screen flow)
  • Screenshot: "Conocete a ti mismo" + upload foto
  • Wait: 15-20 seg loading
  • Result: Body type + color season
  • User must complete para acceder a Try-On

Opción B: Opcional en Settings post-registro
  • User llega directo a Virtual Try-On
  • "Skip for now" link → Settings
  • Try-On sin análisis pero con disclaimer "mejor con análisis"

Opción C: Triggered based on behavior
  • 1st try-on: sugerir análisis
  • Post 3 try-ons: CTA fuerte ("Unlock best recommendations")
```

**Impacto:**
- Registration completion rate (D1 may drop if mandatory)
- Body analysis adoption rate
- Time to first value (TTFV)
- Paid conversion (personas con análisis = 30% higher LTV)

**Recomendación comercial (Leo):**  
Opción A = higher LTV pero -40% DAU (friction).  
Opción B = higher DAU pero -20% body analysis adoption.  
**Recomendación: Opción C** (triggered, no friction upfront).

**Decision:**  
[ ] A — Obligatorio onboarding  
[ ] B — Opcional post-registro  
[ ] C — Triggered on behavior  
[ ] Otra: ___________

---

## DECISIÓN 4: FREE TIER LIMITS

**Pregunta:** ¿Cuántos try-ons/mes en free tier?

```
Opción A: 3 try-ons/mes (strong paywall signal)
  • Free: 3 × mes
  • Estilo: 30 × mes
  • Imagen: Unlimited

Opción B: Unlimited try-ons pero "preview mode" (lower quality)
  • Free: unlimited pero 480p + no share
  • Estilo: 1080p + share
  • Imagen: 2K + share + social

Opción C: 1 try-on/día pero unlimited wardrobe
  • Free: 1 × day (30 × mes)
  • Estilo: 5 × day
  • Imagen: Unlimited
```

**Impacto:**
- Free→paid conversion rate (A = higher, B/C = lower)
- Free user engagement (A = lower DAU, B/C = higher DAU)
- Server costs (unlimited = $$$ en Replicate API)
- Churn rate (aggressive paywall can backfire)

**Recomendación comercial (Leo):**  
- A: Best for revenue early, worst for growth
- B: Best for growth, sustainable (quality = differentiation)
- C: Best balance (time-based is psychology-friendly)

**Recomendación técnica (Jarvis):**  
- Opción B requiere 2 quality pipelines (costoso en Replicate)
- Opción A/C: simple, 1 pipeline

**Hybrid recomendation: "Opción C + Opción B"**
- Free: 1 try-on/día (30/mes), preview quality
- Estilo: 5/día, 1080p
- Imagen: unlimited, 2K

**Decision:**  
[ ] A — 3 try-ons/mes  
[ ] B — Unlimited preview  
[ ] C — 1/día  
[ ] Hybrid (C + B)  
[ ] Otra: ___________

---

## DECISIÓN 5: SOCIAL SHARING

**Pregunta:** ¿Compartir try-ons a Instagram/WhatsApp desde la app?

```
Opción A: Sí, botón [Compartir] en cada resultado
  • Native share intent → Instagram Stories / WhatsApp
  • Watermark con logo "AI Fit Check" en imagen
  • Tracking: referral link en bio

Opción B: No built-in, user manual screenshot + share
  • Reduce technical complexity
  • Still allows sharing pero sin tracking
  • User friction = lower viral coefficient

Opción C: Instagram-only (Stories only, no feed)
  • Higher quality, temporary (24h)
  • Less spam, better brand perception
```

**Impacto:**
- Viral coefficient (A ≈ 1.3x, B ≈ 0.8x, C ≈ 1.0x)
- Brand awareness (A highest, B lowest)
- Technical complexity (A > C > B)
- User friction (A lowest, B highest)

**Recomendación comercial (Leo):**  
Opción A = viral loop + brand awareness + user-generated content (best for growth).  
Current competitors (Cava, Klarna) use A.  
**Recomendation: Opción A** (mandatory for viral growth).

**Decision:**  
[ ] A — Compartir a Instagram/WhatsApp  
[ ] B — No built-in sharing  
[ ] C — Instagram-only  
[ ] Otra: ___________

---

## 📋 ACCIÓN REQUERIDA

**Juan Camilo:** Por favor marca TUS decisiones (no recomendaciones) y envía:

```
D1: [X] A / [ ] B / [ ] C / [ ] Otra
D2: [X] A / [ ] B / [ ] C / [ ] Otra
D3: [X] A / [ ] B / [ ] C / [ ] Otra
D4: [X] A / [ ] B / [ ] C / [ ] Híbrido / [ ] Otra
D5: [X] A / [ ] B / [ ] C / [ ] Otra
```

**Con esto, Erik puede:**
- S04 Virtual Try-On (diseño final)
- S05 My Wardrobe (urgencia & flow)
- S06-S09 Styles, Profile, Paywall (decisiones D1-D5)
- S11 Error states

**Sin esto, Erik está bloqueado.** ⏳

---

**Próximo paso:** Juan Camilo decide → Jarvis comunica a Erik → Erik finaliza mockups S05-S11 → Brook implementa post-4 issues solucionados.

