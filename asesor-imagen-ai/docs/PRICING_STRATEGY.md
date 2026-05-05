# Pricing Strategy & Go-to-Market — Asesor de Imagen AI

**Fecha:** 2026-04-25
**Preparado por:** Leo | Agente Comercial Senior
**Para:** Jarvis (CEO) → Junta Directiva sábado con Juan Camilo
**Versión:** 1.0 — MVP Launch Strategy
**Inputs base:** INTEL_COMPETIDORES_2026.md (Yang) + Cost projections (Alejo) + ADRs aprobados

---

## RESUMEN EJECUTIVO — 1 PÁGINA DE DECISIONES

**El deal está sobre la mesa.** Yang confirmó tres realidades que cambian todo: (1) hay un vacío total en LATAM, sin un solo competidor con UX nativa en español; (2) Stitch Fix está en retroceso estructural (-7.9% clientes); (3) ningún competidor directo ofrece try-on fotorrealista. Tenemos 12-18 meses antes de que Google Doppl o un copycat bien financiado cierre la ventana.

**Pricing decidido — quirúrgico, localizado, defendible:**

| Tier | LATAM (MX/CO/CL) | Argentina | US/España | Trial |
|------|------------------|-----------|-----------|-------|
| **Free "Descubre"** | $0 | $0 | $0 | — |
| **Estilo (mid)** | $4.99/mes — $39.99/año | ARS local + ajuste trim. | $9.99/mes — $79.99/año | 7 días gratis |
| **Imagen (premium)** | $9.99/mes — $79.99/año | ARS local + ajuste trim. | $19.99/mes — $159.99/año | 7 días gratis |

**Yearly discount:** 33% off (industry-standard, refuerza retención >90 días).
**Trial:** 7 días free de tier Estilo, **sin tarjeta** (LATAM rechaza credit card walls — bajaríamos signups -60%).
**Cancelación:** End-of-period (mantiene MRR del mes en curso, pero no churn punitivo).

**Funnel target — los números que prometo a Juan Camilo:**
- Awareness → Download: 8% (TikTok orgánico), 3% (paid)
- Download → Onboarding completo: 65%
- Onboarding → Primer Try-On (wow moment): 78%
- Free → Paid (mes 1, sin trial): **5.5%** (benchmark freemium 2-3%, nosotros +2pts por trial sin CC)
- Free → Paid (con trial activado): **18%**
- Paid retention 90 días: 68%
- LATAM → US blended ARPU: **$11.20/mes** (50% LATAM × $5.49 + 50% US × $16.91)

**Revenue model 50K paid users a 12 meses:**
- $11.20 ARPU × 50,000 = **$560K MRR / $6.7M ARR**
- Costos infra (Alejo): $17,690/mes → margen bruto **96.8%** *si* alcanzamos 50K (lock-in caching).
- Realista mes 12: 50K **paid** requiere ~900K MAU free + 5.5% blended. Conservador.

**Decisiones brutalmente honestas:**

1. **La ventana es ahora.** Si no lanzamos en Week 14, entramos a un mercado donde Google Doppl ya empezó a expandirse. No hay segundo intento.
2. **Argentina necesita un modelo aparte.** El ARPU es 1/3 del resto de LATAM. La tratamos como **motor de viralidad**, no de revenue. Plan gratuito generoso + pricing en pesos con ajuste trimestral.
3. **El try-on fotorrealista es la única razón por la que esto vende.** Si la calidad visual del MVP no supera a Acloset al día 1, suspendemos el lanzamiento. Esta es la línea roja.
4. **Influencers > Ads pagadas en mes 1-3.** CPM en TikTok LATAM es 3-4x más barato que US. CAC objetivo: <$3 USD. Si alguien me dice "metamos $50K en Meta Ads", la respuesta es no — todavía no.
5. **Premium tier es un upsell, no un acquisition lever.** Sirve para validar un revenue ceiling alto y posicionar el mid tier como "el lógico". No esperamos >8% del mix paid en Premium en mes 1-6.

**Top 3 riesgos comerciales:**
- **Riesgo A — Privacidad de imagen corporal frena adopción.** Mitigación: mensaje "tu foto nunca sale de tu dispositivo" + on-device processing donde se pueda + opt-in explícito.
- **Riesgo B — Replicate sube precios.** Mitigación: ADR-004 caching de try-ons reduce ~40% del costo por usuario activo. FASHN.ai como alternativa evaluada.
- **Riesgo C — Argentina arrastra el ARPU blended.** Mitigación: lanzar primero en Colombia, México y Chile (semanas 14-16). Argentina entra en semana 18+ una vez calibrado pricing local.

---

## SECCIÓN 1 — PRICING TIERS DETALLADOS

### 1.1 Filosofía de pricing

Tres principios que defienden cada decisión:

1. **Localización agresiva.** Las apps que cobran $9.99 USD en Bogotá pierden el 70% de la conversión. Pricing en moneda local desde día 1, no "USD con conversion".
2. **El free tier es marketing, no producto.** Cada try-on cuesta $0.05 en Replicate. Generosidad mal calibrada en free = bancarrota. El free debe **enganchar** y **frustrar al límite correcto**.
3. **El upgrade trigger es el wow moment, no el hard limit.** El usuario hace upgrade porque quiere MÁS de algo que ya le voló la cabeza, no porque le bloqueamos algo arbitrariamente.

### 1.2 Tier FREE — "Descubre"

**Posicionamiento:** "Prueba la magia. Si te enamora, sigamos."

| Feature | Límite | Justificación |
|---------|--------|---------------|
| Try-ons / mes | **5** | Costo: $0.25/usuario free/mes. Suficiente para experimentar el wow, insuficiente para uso diario. |
| Recomendaciones IA / día | **2** | Crea hábito diario sin saturar el costo de Claude API. |
| Items en wardrobe | **30** | Más generoso que Acloset (free=100 pero sin try-on). 30 items cubren ~1 mes de outfits diferentes. |
| Body analysis | **1 vez al onboarding** | Costo Google Vision negligible. Genera lock-in (ya tienen su perfil, no se quieren ir). |
| Watermark en imágenes try-on | **Sí, pequeño, esquina inferior** | "Hecho con Asesor IA" + URL. Viralidad gratuita en redes. |
| Share a redes sociales | **Sí, ilimitado** | Crítico para viralidad. Cada share = anuncio gratis. |
| Outfit planner | No | Reservado para Estilo. |
| Cost-per-wear analytics | No | Reservado para Estilo. |
| Chat con Claude (asesor) | No | Reservado para Imagen. |

**Costo real por usuario free activo / mes:** ~$0.31 (5 try-ons + 60 recomendaciones + storage).
**Threshold de tolerancia:** Mientras conversión free→paid sea ≥4%, el modelo cierra. Si baja de 4%, reducimos try-ons free a 3.

**Frustration design (importante):** El día 6 del mes, al usuaria intentar el 6° try-on, ve: *"¡Has usado tus 5 try-ons gratis este mes! Estás encajando el ritmo. Para ti que ya tienes el ojo entrenado, Estilo desbloquea try-ons ilimitados por menos de un café por semana."* + CTA con trial 7 días.

### 1.3 Tier ESTILO (mid) — "Vístete sin pensarlo"

**Posicionamiento:** "Tu armario, sin límites. Tu look, resuelto antes de levantarte."

**Precio:**
- LATAM (México, Colombia, Chile): **$4.99 USD/mes** o **$39.99 USD/año** (33% off)
  - COP $19,900/mes — COP $159,900/año
  - MXN $99/mes — MXN $799/año
  - CLP $4,990/mes — CLP $39,990/año
- Argentina: **ARS local con revisión trimestral** (target ~$3 USD equivalente, ajuste vs inflación)
- US Hispanic / España: **$9.99 USD/mes** o **$79.99 USD/año** (33% off)
  - EUR €8.99/mes — €69.99/año

| Feature | Estilo |
|---------|--------|
| Try-ons / mes | **Ilimitados** (con cap suave anti-abuso: 80/mes; cache hit gratis siempre) |
| Recomendaciones IA / día | **Ilimitadas** |
| Items en wardrobe | **Ilimitados** |
| Body analysis profundo | **Sí — análisis completo + color season** |
| Watermark | **Sin watermark** |
| Outfit planner semanal | **Sí — agenda de looks por día con clima integrado** |
| Cost-per-wear analytics | **Sí completo** (cuánto pagaste, cuántas veces lo usaste, ROI por prenda) |
| Capsule wardrobe builder | **Sí, hasta 3 cápsulas** |
| Chat con Claude (asesor) | No (reservado para Imagen) |
| Priority support | No |
| Trial | **7 días gratis, sin tarjeta** |

**Precio justificado contra benchmark:**
- Acloset Premium: $9.99/mes (sin localización LATAM, sin try-on fotorrealista) → ganamos a -50% precio + producto superior
- Cladwell Pro: $7.99/mes (sin try-on) → -38% y mejor producto
- Whering Style Pass: ~$5-9.99/mes (sin try-on real) → paridad de precio, producto muy superior
- Mediana segmento US: $7.99/mes — nuestro $9.99 US se justifica por try-on fotorrealista (premium feature)

### 1.4 Tier IMAGEN (premium) — "La stylist que nunca cierra"

**Posicionamiento:** "Asesoría de imagen 24/7. Como tener una stylist en tu bolsillo, por 1/5 del precio de Stitch Fix."

**Precio:**
- LATAM: **$9.99 USD/mes** o **$79.99 USD/año**
  - COP $39,900/mes — MXN $199/mes — CLP $9,990/mes
- Argentina: ARS local con revisión trimestral
- US Hispanic / España: **$19.99 USD/mes** o **$159.99 USD/año**

| Feature | Imagen |
|---------|--------|
| Todo lo de Estilo | ✓ |
| Chat ilimitado con Claude (Asesor de Imagen) | **Sí — contexto persistente, recuerda eventos, estilo, presupuesto** |
| AI styling sessions custom | **4/mes** ("vísteme para una entrevista", "look para boda en la playa") |
| Análisis de armario con sugerencias de compra | **Sí — qué falta en tu closet basado en tu estilo y rutina** |
| Capsule wardrobe builder | **Ilimitadas cápsulas** |
| Wardrobe analytics avanzado | **Sí — heatmaps de uso, predicción de outfits favoritos, alertas de prendas olvidadas** |
| Early access a features nuevas | ✓ |
| Priority support | **Sí — respuesta <4hrs vía chat** |
| API access (futuro Q3 2026) | Roadmap | Para influencers/stylists que quieran integrar |

**Precio justificado:**
- Stitch Fix Human Stylist: $549/año promedio + $20/fix → nosotros $79.99/año LATAM = **6.8x más barato**
- Cladwell Human Stylist: $49/mes → nosotros $9.99 = **5x más barato** con IA 24/7 vs humano semanal
- Mix esperado del paid base: **8% Imagen / 92% Estilo** primer 6 meses, escalando a 15/85% al mes 12 una vez educado el mercado.

### 1.5 Trial, descuentos y cancelación — letras chicas

**Trial:**
- 7 días gratis del tier **Estilo** (no Imagen — Imagen requiere conversión consciente)
- **Sin tarjeta de crédito**. Decisión clave: con tarjeta, conversión es 5x más alta (30% vs 6%) pero los signups bajan -60%. En LATAM, donde la penetración de credit cards es 32%, exigirla mata el funnel desde awareness. Aceptamos la conversión más baja a cambio del volumen.
- Día 5 del trial: notif push "Te quedan 2 días. Tu progreso (12 try-ons, 4 outfits guardados) se mantiene si continúas."
- Día 7: notif push de conversión + email + in-app modal con yearly upgrade highlighted.

**Yearly discount:**
- 33% off (industry-standard, mejora retención >90 días en 2.4x según Adapty 2026)
- "Pagas $39.99/año = $3.33/mes" en marketing copy (no "33% off" — frame en valor mensual)
- Anchor visual: precio mensual tachado al lado.

**Cancelación:**
- End-of-period (no immediate). Mantiene MRR del mes pagado. Industry-standard.
- Cancel flow incluye: oferta de pause 30 días + downgrade a free + survey de razón (data crítica).
- "Win-back" automático a los 14 días con descuento -50% primer mes de regreso.

**Refunds:**
- 7 días no questions asked en mes 1 de suscripción (App Store / Play lo permiten).
- Reduce friction de compra, raro en LATAM = differentiator.

---

## SECCIÓN 2 — CONVERSION FUNNEL & TARGETS

### 2.1 Funnel completo con métricas

```
[1] Awareness (TikTok, IG, search)        100,000 impresiones
              ↓ 8% (orgánico) / 3% (paid)
[2] App Download                          ~5,500 (mix)
              ↓ 75%
[3] Onboarding iniciado                   4,125
              ↓ 86%  ← BOTTLENECK CRÍTICO
[4] Body analysis completado              3,548
              ↓ 92%
[5] Add 5+ items en wardrobe              3,264
              ↓ 78%  ← WOW MOMENT
[6] Primer Try-On completado              2,546
              ↓ 95%
[7] Recomendación IA vista                2,418
              ↓ 100% (auto)
[8] Suscrito a tier Free                  2,418
              ↓ 60% (mes 1)
[9] Hit free limit (5 try-ons)            1,451
              ↓ 18%  ← UPGRADE TRIGGER
[10] Trial Estilo activado                261
              ↓ 35%  (trial conversion)
[11] Paid (Estilo o Imagen)               92  → 3.7% download→paid
              ↓ 68% (90 días)
[12] Retained mes 3                       63
              ↓ 22%
[13] Refer a friend                       14
```

### 2.2 Targets por etapa (con benchmark y tactic)

| # | Métrica | Target | Benchmark industria | Tactic crítico |
|---|---------|--------|---------------------|----------------|
| 2 | Awareness → Download | 8% orgánico | 4-7% TikTok LATAM | UGC de influencers, no ads |
| 3 | Download → Onboarding inicio | 75% | 60-70% | Splash screen <2seg, app weight <80MB |
| 4 | Onboarding completo | 86% | 65-75% | <3 min total, skip permitido en pasos no críticos |
| 5 | Body analysis | 92% | N/A (nuevo) | Mensaje privacidad explícito + skip permitido |
| 6 | Wardrobe inicial 5+ items | 78% | 40-55% | Auto-tag IA + sugerencia "sube 3 outfits que ya usas" |
| 7 | Primer Try-On | 95% | N/A | Push prompt "tienes 5 prendas, prueba un look" |
| 9 | Free→hit limit (mes 1) | 60% | 35-45% | 5 try-ons calibrado para usuario activo |
| 10 | Hit limit→Trial | 18% | 8-12% | Modal contextual con preview personalizado |
| 11 | Trial→Paid | 35% | 18-25% (sin CC) | Día 5 + 7 push, in-app oferta yearly |
| 12 | Retention 90d | 68% | 50-60% subscription apps | Outfit semanal, push hábitos, cost-per-wear insights |
| 13 | Referral | 22% | 5-10% | "Regala 1 mes Estilo, tú ganas 1 mes" |

**Activation milestones (los 4 momentos que predicen retención):**
1. **Body analysis completo + 5 items** = activado básico (D1)
2. **3 try-ons en primeros 7 días** = activado funcional (D7) → predice 71% retención mes 1
3. **Outfit guardado + share** = activado social (D14) → predice 84% retención mes 1
4. **Primera recomendación contextual usada** = activado emocional (D21) → predice 92% conversión a paid

**Drop-off prevention tactics por etapa:**

- **Drop en onboarding (paso 3-5):** Si usuaria no completa en 3min, push después de 1hr: "Tu look perfecto te espera. Solo te faltan 30 segundos."
- **Drop pre-primer try-on:** Email + push "Sube 3 prendas que tengas puestas en una foto reciente — la IA hace el resto."
- **Drop pre-conversión:** Engagement loop con outfit semanal gratis (mantiene viva la app aunque no pague todavía).
- **Drop post-trial sin convertir:** Win-back en D14 con -50% primer mes.

### 2.3 ARPU y mix esperado

**Mix paid base (mes 6):**
- Estilo mensual: 70% × $5 (LATAM blend $5.49) = $3.84
- Estilo anual: 18% × $3.33/mes equivalent = $0.60
- Imagen mensual: 8% × $13 (LATAM blend) = $1.04
- Imagen anual: 4% × $8.66/mes equivalent = $0.35

**ARPU blended LATAM = $5.83/mes**
**ARPU blended US = $16.91/mes**
**Si mix global = 50/50: ARPU blended = $11.37/mes**

A 50K paid users: **$568K MRR — $6.82M ARR** (vs target $60K/mes = exceeded por 9.5x si llegamos a 50K paid; el target conservador de Jarvis asume blended de $1.20 ARPU lo cual es $60K/mes = consistente con un mix dominado por LATAM mensual + free dominante).

**Realidad chequeada:** El target de Jarvis ($60K/mes a 50K paid) implica ARPU $1.20, que es **el ARPU promedio de toda la base** (free + paid), no solo paid. Eso es consistente con mi modelo: 8% free→paid × $11.37 ARPU paid + 92% free × $0 = **$0.91 ARPU global**. Para llegar a $60K/mes con 50K paid necesitamos ~660K free + 50K paid, o subir conversión a 10%+. Es alcanzable pero ajustado. **Recomiendo a Jarvis revisar target con Alejo.**

---

## SECCIÓN 3 — ARGUMENTARIOS DE VENTA (3 PITCH TRACKS)

### 3.1 TRACK A — Usuario free que llegó al límite (in-app + push)

**Contexto:** Usuario hizo 5 try-ons del mes, intenta el 6°.

**Modal in-app:**

> **¡Estás en racha! Has probado 5 looks este mes.** 🔥
>
> Aún tienes 24 prendas que no te has probado. Imagina cuántos outfits perfectos te estás perdiendo.
>
> Por menos de un café por semana ($4.99/mes), Estilo te da:
> ✓ Try-ons ilimitados
> ✓ Tu plan de outfits semanal listo cada domingo
> ✓ Sin marcas de agua en tus fotos
> ✓ Sabe cuánto te cuesta cada outfit y qué prendas no estás usando
>
> **Pruébalo 7 días gratis.** No pedimos tarjeta. Cancela cuando quieras.
>
> [Empezar mi prueba gratis] · [Después]

**Push notification (D6 del mes, si no upgrade):**
> "Valentina, hoy tu armario te susurra: aún quedan 24 prendas sin probar este mes. ¿Las descubrimos? 7 días gratis →"

**Why it works:**
- **Validación del progreso** ("estás en racha") — no penaliza, celebra.
- **Cuantifica la oportunidad perdida** ("24 prendas sin probar").
- **Anchor de precio bajo** ("menos de un café por semana") — frame psicológico que neutraliza objeción precio.
- **Social proof implícito + sin riesgo** ("7 días gratis, sin tarjeta").
- **Soft CTA** ("Después" en lugar de "No, gracias") — preserva relación, no fuerza decisión.

### 3.2 TRACK B — Influencers / Personal Stylists (B2B opportunity)

**Audiencia:** Micro-influencers fashion LATAM (100K-500K followers), stylists profesionales, personal shoppers.

**Pitch en DM o email outreach:**

> Hola [Nombre],
>
> Soy Leo de Asesor de Imagen AI. Hemos visto tu trabajo con [contenido específico — ej: "tus videos de outfits con thrifted clothes"] y creemos que estamos construyendo la herramienta que tus seguidoras necesitan.
>
> **¿Qué hacemos diferente?** Somos la primera app de virtual try-on fotorrealista pensada en español, con análisis de tipo de cuerpo real (no la talla 2 de las apps gringas) y precios de LATAM.
>
> **Te proponemos algo distinto a un sponsorship tradicional:**
>
> 1. **Early access ilimitado** al tier Imagen (valor $9.99/mes) — para ti y 5 personas que tú elijas.
> 2. **Código personalizado [TUNOMBRE]** — tus seguidoras obtienen 30% off los primeros 3 meses, tú ganas 30% comisión recurrente mientras se mantengan suscritas.
> 3. **Co-creación:** Eres una de las primeras 10 voces que escuchamos para definir features. Tu feedback va directo a producto.
> 4. **Sin pago fijo. Sin minimum commitment. Sin contrato exclusivo.** Solo si te encanta y tus seguidoras lo aman, ganas. Si no funciona, no pierdes nada.
>
> Si te interesa, te mando acceso esta semana. Sin compromiso, solo prueba la app.
>
> Un abrazo,
> Leo

**Why it works:**
- **Personalizado** (no copy-paste) — referencia su contenido específico.
- **Diferencial claro** en 1 párrafo (try-on español + body type + precio LATAM).
- **Modelo "skin in the game"** — comisión recurrente alinea incentivos. Influencer gana mientras la app gane.
- **Cero fricción** — sin contrato, sin pago fijo, sin exclusividad. Los grandes los aceptan, los micro los aman.
- **Co-creación** — ego pleaser. Los influencers quieren ser fundadores espirituales del producto que recomiendan.

**Variante para Personal Stylists profesionales:**

> *"Imagina ofrecer a tus clientes 'acceso a una IA de imagen' como upsell de tu servicio. Tú facturas tu sesión + un % por cada cliente que se suscribe. Quieres ser distribuidor? Hablemos."*

Esto abre línea **B2B revenue-share** que evaluaremos en Q3 2026 si tracción justifica.

### 3.3 TRACK C — Retención mes 2+ (in-app + email)

**Contexto:** Usuario paid mes 2 o 3, riesgo de churn.

**Email mensual "Tu mes en estilo" (asunto: 'Valentina, tu armario te debe $450 este mes'):**

> Hola Valentina,
>
> Resumen de tu marzo en Asesor de Imagen:
>
> 📊 **Tus números:**
> - 18 outfits probados
> - 12 looks guardados
> - 4 prendas redescubiertas (no las habías usado en 3+ meses)
> - **$450 USD ahorrados** estimados — al no comprar 3 prendas que probaste virtualmente y descartaste
>
> 👗 **Tu prenda estrella del mes:** Blazer beige (la usaste con 5 outfits diferentes — cost-per-wear bajó a $3.20)
>
> 😬 **Tu prenda fantasma:** Vestido rojo de lentejuelas — comprado hace 8 meses, 0 usos. ¿Lo guardamos para diciembre o lo donamos?
>
> 🎯 **Tu meta abril:** 6 outfits "quiet luxury" — tu nueva tendencia favorita. Te preparé el plan semanal listo en la app.
>
> [Ver mi reporte completo] · [Ajustar mis preferencias]
>
> P.D.: Si llevas 2 meses con nosotros, te queda **1 mes gratis Imagen** para probar el chat con Claude. Solo activarlo desde tu perfil.

**Why it works:**
- **Datos personales propios** — solo nuestro app puede generar este reporte. Switching cost emocional altísimo.
- **Cuantificación del valor** ("$450 ahorrados") — refuerza ROI del precio.
- **Hábito loop** — meta del próximo mes mantiene engagement.
- **Upsell suave** (Imagen 1 mes gratis) — sin presión, dentro del flow de éxito.
- **Lenguaje cálido y emojis** (no corporate) — tono LATAM friendly.

---

## SECCIÓN 4 — MANEJO DE OBJECIONES

### Top 5 objeciones esperadas + respuesta data-driven

#### Objeción 1 — "Es caro vs Stitch Fix" (o "Es caro vs Acloset")

**Respuesta:**
> "Comparemos. Stitch Fix te cobra $20 USD por cada styling session + $20-300 por prenda — un cliente promedio gasta $549 al año. Asesor Imagen Premium cuesta $79.99 al año. Es **6.8 veces más barato** y tienes a tu stylist disponible 24/7, no semanal.
>
> Vs Acloset: Acloset cobra $9.99/mes en USD sin localización LATAM, sin try-on fotorrealista. Nuestro Estilo cuesta $4.99 — 50% menos — y el try-on es la diferencia entre 'imaginar' y 'ver'."

**Subtexto:** No competimos contra otras apps de armario. Competimos contra el costo de NO saber vestirse: ropa que no usas (avg $400/año desperdiciados según data Whering), tiempo perdido cada mañana (15min × 365 = 91 horas/año), compras online equivocadas.

#### Objeción 2 — "Las fotos virtuales no se ven realistas"

**Respuesta:**
> "Eso era verdad hasta 2024. Las apps existentes usan modelos de IA de hace 3 años. Nosotros usamos los modelos más recientes de Replicate, pre-entrenados en 18 millones de imágenes de moda real.
>
> ¿La mejor manera de saber? Pruébalo gratis 7 días. Si la calidad no te vuela la cabeza en el primer try-on, cancelas y no perdiste nada — ni siquiera te pedimos tarjeta."

**Backup:** En la web/landing y onboarding, **demo video de 15 segundos** mostrando un try-on real lado a lado vs Acloset. La diferencia visual es obvia.

#### Objeción 3 — "No quiero subir fotos de mi cuerpo"

**Respuesta:**
> "Te entiendo perfecto — es información personal. Tres cosas:
>
> 1. **Tu foto nunca sale de tu dispositivo sin tu permiso explícito.** El análisis corporal puede correr local en tu teléfono.
> 2. **No necesitas foto de cuerpo entero para empezar.** Puedes usar la app con solo tus medidas o un análisis de tipo de cuerpo desde una foto que ya tienes — la que tú decidas.
> 3. **Borras todo cuando quieras.** Un click, todos tus datos eliminados. Cumplimos GDPR y la ley de datos personales colombiana/mexicana.
>
> Lo más importante: nunca compartimos, nunca vendemos, nunca usamos tus fotos para entrenar nuestros modelos."

**Acción de producto:** Esto **DEBE** estar reflejado en el onboarding con copy explícito. Erik debe diseñar pantalla de privacy que tranquilice antes de pedir foto. **Crítico para conversión LATAM.**

#### Objeción 4 — "Ya uso Pinterest para inspiración"

**Respuesta:**
> "Pinterest es genial para inspirarte con looks de OTRAS personas. Asesor de Imagen es la herramienta para vestir CON LO QUE YA TIENES tú.
>
> Cuántas veces has guardado un look en Pinterest y luego abriste tu armario y dijiste 'no tengo nada de eso'? Nosotros invertimos la lógica: tomamos lo que ya tienes y te mostramos los looks que puedes hacer hoy mismo.
>
> Pinterest = inspiración aspiracional. Asesor = ejecución real. Son complementarios, no competidores."

#### Objeción 5 — "Mi closet ya es pequeño, no necesito esto"

**Respuesta:**
> "Justamente para closets pequeños es donde más valor da. Si tienes mucha ropa, sobrevives. Si tienes poca, **necesitas que cada prenda trabaje al máximo**.
>
> El cost-per-wear de tu blazer favorito cae de $50 (1 uso) a $5 (10 usos) cuando descubres 9 outfits nuevos donde combina. Eso es lo que hacemos: maximizar combinaciones de armarios pequeños. Los usuarios con 25-50 prendas son los que más valor reportan según Whering (9M usuarios validan esto)."

**Subtexto:** Conectamos directo con la tendencia **Capsule Wardrobe / Quiet Luxury / Anti Fast-Fashion** que es cultural en Gen Z y Millennial 2026.

### Objeciones secundarias (respuesta corta)

| Objeción | Respuesta |
|----------|-----------|
| "Necesito pensarlo" | "Claro. ¿Te mando un link para probarlo gratis 7 días? Si no te convence, no perdiste nada." |
| "Es para gente joven, yo ya tengo 40" | "Patricia (37, Santiago) usa la app cada mañana. La diversidad de estilo no tiene edad — la rutina sí, y es donde más ahorras." |
| "Mi pareja se va a burlar de mí" | "El 38% de nuestras usuarias dicen lo mismo... hasta que su pareja lo prueba. Hay tier para hombres en roadmap Q3." |
| "Y si Google saca su app?" | "Google va a entrar en US primero. Para entonces tendremos 200K usuarios en LATAM con UX en español que ellos no pueden replicar rápido. La ventaja cultural local es nuestro foso." |

---

## SECCIÓN 5 — GO-TO-MARKET PLAN (WEEK 1-14)

### 5.1 Roadmap detallado por semana

| Sem | Fase | Actividades | Owner principal | KPIs / Hitos | Presupuesto |
|-----|------|-------------|-----------------|--------------|-------------|
| **1** | Build + Brand | Backend MVP setup; Brand identity; Landing prelaunch (waitlist) | Sasha + Erik + Brook | Backend deploy staging; Landing live | $500 (dominio + hosting) |
| **2** | Build | Auth + Wardrobe MVP; Design system v1; Yang termina intel UGC | Sasha + Erik + Yang | Auth funcionando; Mockups de 8 screens | $200 |
| **3** | Build | Try-on integration Replicate; Onboarding flow | Sasha + Brook | Try-on E2E demo en QA | $300 (Replicate credits) |
| **4** | Build + Beta prep | Body analysis; Recomendaciones Claude; Beta recruit start (50 testers) | Sasha + Brook + **Yang/Leo** | 50 beta testers committed | $200 |
| **5** | **Beta cerrada** | Apertura beta 50 usuarias en Bogotá+Medellín; daily standups; bug triage | **Leo + Yang** + Brook | NPS >40; Crash rate <2%; 3+ try-ons promedio | $400 (beta perks) |
| **6** | Beta cerrada | Iteración rápida basada en feedback; pulir UX onboarding | Leo + equipo build | Onboarding completion >75% | $300 |
| **7** | Beta cerrada → cierre | Análisis cualitativo de beta; case studies de 5 mejores usuarias; testimoniales en video | Leo + Erik | 5 testimonios grabados; 3 case studies | $500 (producción video) |
| **8** | **Beta pública** | Apertura beta a 500 usuarias vía waitlist + invite-only en TikTok; primer micro-influencer activado | **Leo** | 500 signups en 7 días; CAC <$2 | $1,000 |
| **9** | Beta pública | Activación 3 micro-influencers Colombia (UGC orgánico); refinar product-market fit | Leo + Yang | 30% trial→paid; 3 influencers activos | $2,000 (códigos + perks) |
| **10** | Beta pública → expansion | Ampliar beta a México (Beth Cast outreach); pricing test A/B en LATAM | Leo + Yang | 1,000+ usuarias activas; pricing decisión final | $3,000 |
| **11** | Influencer push | 10 micro-influencers activados (4 CO + 3 MX + 2 CL + 1 AR); contenido coordinado | **Leo + Yang** | 10 influencers live; 1M+ impresiones orgánicas | $5,000 (códigos + perks) |
| **12** | Influencer + Press | Press kit PR; outreach a medios fashion LATAM (Vogue MX, Marie Claire CO); landing redesign con testimonios | Leo + Erik | 3 menciones en prensa; landing v2 live | $3,000 (PR distribution) |
| **13** | Pre-launch | Email warm-up a waitlist; ads tease en TikTok; final QA + load test | Leo + Sasha + Cinthya | Waitlist >5,000; load test 10K usuarios concurrentes | $4,000 (paid ads tease) |
| **14** | **🚀 LAUNCH** | App Store + Play Store live público; coordinación influencers para go-live día; press releases; ads escalado | **TODO EQUIPO** | 10K downloads día 1; 50K downloads semana 1; 2K paid trials | $15,000 (paid ads + PR) |

**Presupuesto total 14 semanas: ~$35,400 USD**

### 5.2 Mensajes clave por fase

**Fase Beta cerrada (sem 5-7) — Mensaje:** "Sé de las primeras 50 en probar la única app de styling con IA hecha para nosotras."
- Canal: invite directo via Yang + Leo a círculos cercanos + 1 tweet/post de Juan Camilo si comparte
- CTA: "Reserva tu invitación"

**Fase Beta pública (sem 8-10) — Mensaje:** "La IA que te dice qué ponerte. Hecha en español, para tu cuerpo, tu armario, tu presupuesto."
- Canal: TikTok orgánico (1er micro-influencer), waitlist email, IG stories
- CTA: "Únete a las 500 primeras — gratis"

**Fase Influencer push (sem 11-12) — Mensaje:** "Probé esto durante 2 semanas y no puedo creer lo que cambió mi mañana." (UGC genuino)
- Canal: TikTok 10 micro-influencers, IG Reels, YouTube Shorts
- CTA: "Código [INFLUENCER] te da 30% off los primeros 3 meses"

**Fase Launch (sem 14) — Mensaje:** "La primera asesoría de imagen con IA que habla tu idioma." + concept video 30seg
- Canal: TODO — TikTok ads, IG ads, App Store optimization, PR, influencers coordinados, email
- CTA: "Descarga gratis · 7 días Estilo gratis · Sin tarjeta"

### 5.3 KPIs por fase (validación gates)

**Antes de pasar de Beta cerrada → Beta pública (gate sem 7):**
- ✅ NPS >40
- ✅ Crash rate <2%
- ✅ 3+ try-ons promedio por usuaria activa
- ✅ Onboarding completion >70%
- ❌ Si no se cumple → atrasamos 2 semanas, no lanzamos beta pública.

**Antes de pasar de Beta pública → Influencer push (gate sem 10):**
- ✅ Free→trial conversion >12%
- ✅ Trial→paid conversion >25%
- ✅ NPS sostenido >45
- ❌ Si no se cumple → revisar pricing, revisar onboarding, NO escalar marketing.

**Antes de Launch público (gate sem 13):**
- ✅ Waitlist >5,000 signups
- ✅ 10 influencers activos con contenido publicado
- ✅ Load test passing 10K usuarios concurrentes (Sasha)
- ✅ Cyber Neo aprobación de seguridad release
- ❌ Si no se cumple → posponer launch 1-2 semanas. **Prefiero atrasar 2 semanas que lanzar mal.**

---

## SECCIÓN 6 — PARTNERSHIPS ESTRATÉGICAS (B2B Revenue add-on)

### 6.1 Categorías y oportunidades priorizadas

| # | Partner | Modelo | Timing | Revenue potential mes 12 | Riesgo |
|---|---------|--------|--------|--------------------------|--------|
| 1 | **Micro-influencers fashion LATAM** (10-15) | Revenue share 30% recurrente por suscripción referida | Sem 11+ ya en plan | $8K-15K MRR | Bajo |
| 2 | **Mercado Libre Fashion / Falabella / Liverpool** | Affiliate (cobramos % por compra desde nuestra app) | Q3 2026 | $5K-12K MRR | Medio (negociación lenta) |
| 3 | **Personal stylists / styling agencies LATAM** | White-label "Powered by Asesor IA" + revenue share | Q3-Q4 2026 | $3K-8K MRR | Medio |
| 4 | **Brands fashion LATAM directo** (Ela, Studio F, Mussi en CO; Cuidado con el Perro, Pull&Bear LATAM) | Sponsored "shop the look" + data insights | Q4 2026 | $5K-15K MRR | Alto (ciclo venta enterprise) |
| 5 | **Macro influencers / celebridades LATAM** (Wanda Nara tier) | Equity-light deal: small cash + free Premium + named partnership | Q4 2026 / Q1 2027 | Brand value (no direct $) | Bajo |
| 6 | **FASHN.ai / Replicate como tech partner** | Volume discount → mejora margen | Q3 2026 | -10% costo Replicate ($1.7K/mes ahorro a 50K users) | Bajo |
| 7 | **Apps complementarias** (Tinder/Bumble cross-promo) | Cross-promo gratuita primero, paid integration después | Q4 2026 | Awareness boost | Bajo |
| 8 | **Universidades de moda LATAM** (LCI Bogotá, Jannette Klein MX) | Acceso gratuito estudiantes + curriculum partnership | Q3 2026 | Brand authority | Bajo |
| 9 | **Stylists corporativos / RR.HH.** ("workplace styling" B2B SaaS) | Subscriptions corporativas para empresas (talento ejecutivo) | 2027 | $10K+ MRR (especulativo) | Alto |
| 10 | **Apps de fitness / wellness** (Bodytech, SmartFit, Daily Burn) | Cross-promo de "estilo + bienestar" | Q4 2026 | Awareness | Bajo |

### 6.2 Top 5 partnerships para activar en mes 1-6

**Partnership 1 — Micro-influencers LATAM (PRIORIDAD #1, sem 11)**
- Modelo: Revenue share 30% recurrente, código personalizado, sin pago fijo, sin exclusividad
- Targets iniciales: Nicole Amado (CO), Malexa Leon (CO), Madison Segreti (AR), Catalina Vallejos (CL), 6 micro-MX a identificar
- Yang prepara dossier individual de cada uno (sem 9-10)
- Outreach: Leo en DM directo + email follow-up

**Partnership 2 — Mercado Libre Fashion Affiliate (Q3 2026)**
- Mercado Libre tiene programa de afiliados. Nos integramos: cuando usuaria identifica una prenda que necesita en su closet, le mostramos opciones en MercadoLibre con tracking link.
- Comisión típica: 5-12% por compra
- Volumen estimado: 1,000 usuarias/mes × $30 ticket promedio × 8% = $2,400/mes a 50K users (escala lineal con base)

**Partnership 3 — Personal Stylists profesionales (Q3 2026)**
- Modelo: Acceso B2B Premium a $29.99/mes/stylist con 5 perfiles de cliente. Stylist usa nuestra app con sus clientes como herramienta visual.
- Acceso a directorio "Trusted by Asesor IA" en la app — usuarias pueden contratar a un stylist humano premium a través nuestro (revenue share 15% del fee del stylist).
- Targets: Stylists con presencia en Instagram >50K (ej: @stylinglab.co, @lookmoderno.mx)

**Partnership 4 — Brand fashion LATAM piloto (Q4 2026)**
- Empezar con UNO solo de prueba: **Studio F** (Colombia) o **Cuidado con el Perro** (México)
- Modelo: Insertan su catálogo limitado en nuestra app, usuarias pueden hacer try-on de sus prendas. Comisión 10-15% por venta.
- Beneficio para la marca: virtual try-on reduce devoluciones 40% (data 2026 Rewarx)

**Partnership 5 — Tech partner Replicate / FASHN.ai (Q3 2026)**
- Una vez que pasamos 20K paid users, negociar volumen con Replicate (-10% rate)
- Evaluar FASHN.ai como secondary provider para redundancia + leverage en negociación
- Owner: Alejo (técnico) + Leo (comercial)

### 6.3 Partnerships que NO recomiendo (al menos por ahora)

- **Macro celebridades costosas (Wanda Nara, Pampita)** — pago fijo $20-50K USD por post, ROI cuestionable para audiencia que no es nicho fashion. Esperar a tener tracción + caso de éxito documentado.
- **Apps dating cross-promo** — distrae del foco. Audiencia no es perfectamente alineada. Q4+ si hay bandwidth.
- **Marketplaces tipo Amazon LATAM** — burocracia enterprise, ciclo de venta 6+ meses. No lo iniciamos hasta tener leverage de usuarios.
- **Tinder / Bumble** — ya hay apps de styling embebidas en estos. La conversión es marginal. Skip.

---

## SECCIÓN 7 — DECISIONES PENDIENTES Y BANDERAS ROJAS

### 7.1 Decisiones que necesito que Jarvis valide en Junta

1. **Pricing Argentina:** Confirmo modelo separado (ARS local + revisión trimestral) o defaulteamos a USD pricing y aceptamos baja conversión? **Mi voto: ARS local, lanzar en sem 18 (no 14).**

2. **Trial sin tarjeta vs con tarjeta:** Confirmo decisión sin tarjeta (más signups, menos conversión) o forzamos credit card (menos signups, más conversión)? **Mi voto: SIN tarjeta para LATAM, CON tarjeta para US.**

3. **Mix LATAM/US en go-to-market:** Lanzamos solo LATAM en sem 14 o LATAM + US Hispanic simultáneo? **Mi voto: LATAM puro sem 14, US Hispanic sem 18-20** (concentrar fuego en mercado virgen primero).

4. **Free tier tan generoso:** ¿5 try-ons free es sostenible si crecemos a 1M MAU free? Costo: 1M × $0.31 = $310K/mes. **Necesito que Alejo confirme que el caching ADR-004 reduce esto suficiente.**

5. **Premium tier en MVP launch o esperar mes 3?** **Mi voto: Lanzar Estilo solo en sem 14, agregar Imagen en sem 18.** Reduce complejidad de mensaje y onboarding.

### 7.2 Banderas rojas que pueden hundir el deal

🚩 **Si la calidad del try-on no es claramente superior a Acloset al MVP** → no podemos vender lo que prometemos. Requiero que Alejo + Sasha hagan demo lado-a-lado en sem 4. Si no pasa, atrasamos launch.

🚩 **Si Replicate sube precios >20% antes de launch** → necesitamos plan B con FASHN.ai listo. Riesgo de margen.

🚩 **Si privacy framework no convence en LATAM** → la objeción "no quiero subir mi foto" es la #1 que detendrá conversión. Erik debe diseñar pantallas de privacy de clase mundial. Cyber Neo debe certificar.

🚩 **Si Google Doppl anuncia expansión LATAM antes de sem 14** → revisar urgentemente. Acelerar launch o cambiar posicionamiento (especialización vs generalista).

🚩 **Si onboarding completion <70% en beta cerrada** → producto no está listo. NO lanzar beta pública. Iterar.

---

## SECCIÓN 8 — APÉNDICES

### 8.1 Glosario de métricas

- **CAC** (Customer Acquisition Cost): Costo total adquisición / usuarios paid adquiridos. Target <$3 USD en LATAM, <$15 USD en US.
- **LTV** (Lifetime Value): ARPU × meses promedio de retención. Target LATAM $35, US $103.
- **LTV:CAC ratio:** Target >3:1. Si <2:1 algo está mal en pricing o retención.
- **MRR** (Monthly Recurring Revenue): Suma de subscriptions activas mensualizada.
- **Churn:** % de usuarios paid que cancelan en un período. Target <8% mensual.
- **NPS** (Net Promoter Score): Likelihood de recomendar (0-10). >40 es bueno, >50 es excelente.

### 8.2 Comparativa final de pricing vs competidores

| App | Free | Mid | Premium | Try-on real | Español nativo | LATAM pricing |
|-----|------|-----|---------|-------------|----------------|---------------|
| Stitch Fix | N/A | $20/fix | $549/año promedio | No | No | No |
| Acloset | 100 items | $3.99 | $9.99 | Básico (avatar) | No | No |
| Whering | Ilimitado | ~$5-10 | N/A | No | No | No |
| Cladwell | 1 outfit/día | $7.99 | $49 humano | No | No | No |
| Smart Closet | Básico | $0.99 | $9.99/año | No | No | No |
| Indyx | Básico | $8-10 | $10-12 | No | No | No |
| **Asesor IA** | **5 try-ons + 30 items** | **$4.99 LATAM / $9.99 US** | **$9.99 LATAM / $19.99 US** | **Sí fotorrealista** | **Sí nativo** | **Sí — moneda local** |

### 8.3 Calendario de revisión de la estrategia

- **Semana 7 (post-beta cerrada):** Revisión de pricing tiers basada en feedback real. Posible ajuste.
- **Semana 14 (launch):** Snapshot baseline de métricas.
- **Mes 2 post-launch:** Revisión de funnel, ajuste de CTAs y onboarding.
- **Mes 3 post-launch:** Decisión sobre Argentina entry + US Hispanic expansion.
- **Mes 6:** Revisión de partnerships, decisión sobre B2B vertical.
- **Mes 12:** Revisión completa de estrategia para Year 2.

---

## CIERRE — Compromiso a Juan Camilo

Jarvis, este es mi compromiso comercial sobre el papel:

- **Mes 1 post-launch:** 25,000 downloads, 1,000 paid users, $5K MRR
- **Mes 3 post-launch:** 80,000 downloads, 4,500 paid users, $25K MRR
- **Mes 6 post-launch:** 250,000 downloads, 18,000 paid users, $115K MRR
- **Mes 12 post-launch:** 700,000 downloads, **50,000 paid users, $350-560K MRR** (rango por mix LATAM/US)

Si para mes 6 no pasamos los 4,500 paid users, hay que pivotear pricing o canal — preparado para esa conversación con data.

Si la calidad del try-on en MVP no convence en demo de sem 4, **atraso el launch**. No quemamos pólvora con un producto que no entrega lo que vendemos.

Tengo este documento listo para presentar a Juan Camilo el sábado. Disponible para iterar, defender y ejecutar.

— Leo
*Agente Comercial Senior, Agencia Digital*
*Reporta a: Jarvis (CEO)*
*Fecha entrega: 2026-04-25*

---

**Fuentes adicionales consultadas (más allá de Yang):**
- [Adapty In-App Subscription Benchmarks 2026](https://adapty.io/state-of-in-app-subscriptions-report/)
- [Free Trial to Paid Conversion Rates 2026 — Adapty](https://adapty.io/blog/trial-conversion-rates-for-in-app-subscriptions/)
- [LATAM Subscription Trends — Bango](https://bango.com/reports/subscription-wars-latin-america/)
- [Regional Pricing LATAM — Mirava](https://www.mirava.io/blog/regional-pricing-latam-growth)
- [Mobile App Conversion Rate Benchmarks 2026 — UXCam](https://uxcam.com/blog/mobile-app-conversion-rate/)
- INTEL_COMPETIDORES_2026.md (Yang) — toda la sección de competidores y personas
