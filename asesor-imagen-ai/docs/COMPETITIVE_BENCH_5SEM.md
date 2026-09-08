# Benchmark Competitivo — Try-On Cap 5/semana (P1)
**Fecha:** 2026-05-19
**Preparado por:** Yang | Para: Leo + Jarvis
**Contexto:** Validar si nuestro plan P1 (5 try-ons/semana, reset domingo 23:59) es único en el mercado global de virtual try-on con AI generativa.

---

## 1. Tabla Comparativa: Caps de Competencia vs P1

| Competidor | Segmento | Free Cap | Reset | Paid Entry | Try-On Reset Semanal | Fuente |
|---|---|---|---|---|---|---|
| **OutfitMaker.ai** | Consumer (wardrobe/styling) | 1 try-on (one-time, nunca resetea) | N/A — one-shot | 5/mes (Premium €7.99/mes) | NO — mensual | Página de pricing oficial |
| **FASHN.ai** | B2B/Brands | 10 credits one-time | N/A | 200 credits/mes ($19/mes) | NO — mensual + daily rollover en Pro/Agency | Pricing page + help center |
| **FitRoom.app** | Consumer | 10 credits/mes | Mensual | $9/mes (50 credits) | NO — mensual | Pricing page oficial |
| **Genlook** | Shopify/SMB | 10 try-ons/mes | Mensual | 100/mes ($19.99/mes) | NO — mensual | Shopify App Store |
| **Magic Hour** | Consumer/Creator | 3 try-ons/dia (sin cuenta) + 100 credits/dia (con cuenta) | DIARIO | $10/mes (Creator) | NO — diario | Pricing page oficial |
| **DLOOK** | Consumer (mobile app) | 3 tokens/dia | DIARIO | ~$40/mes (semanal/mensual) | NO — diario | App Store reviews + Play Store |
| **Fits app** | Consumer (mobile) | 31 generaciones one-time, luego $0.16/imagen | One-time | $3.33/mes | NO — one-time pool | Fits-app.com review |
| **Aiuta / ASOS VTO** | B2B / Retailer embed | 1 prueba gratuita (luego €19.99/mes) | N/A | €19.99/mes | NO — embedded sin cap visible al usuario | ASOS press release + fits-app review |
| **CALA** | B2B (fashion ops) | 75 credits one-time (onboarding) | N/A | Custom pricing | NO — no es consumer try-on | Futurepedia + welcome.ai |
| **Lookiero** | Personal styling (fisico) | N/A (servicio fisico) | N/A | £10/mes (5 prendas en casa) | N/A — no es digital try-on | Lookiero.co.uk |
| **Rent the Runway** | Renta fisica de ropa | N/A | N/A | $94-316/mes (5-30 items) | N/A — no es digital try-on | renttherunway.com + retailtouchpoints |
| **WeShop AI** | B2B/Consumer | Free (no cap publicado) | No especificado | Credit-based | DESCONOCIDO — no publicado | weshop.ai |
| **Krea AI** | Consumer/Creator | Ilimitado sin cuenta | N/A | — | N/A — no cap | krea.ai |
| **The New Black** | B2B | 3 credits one-time | N/A | $8/mes | NO — mensual | claid.ai comparison |
| **Claid.ai** | B2B | 50 credits one-time | N/A | $9/mes | NO — mensual | claid.ai |
| **Botika** | B2B | 8 credits one-time | N/A | $33/mes | NO — mensual | claid.ai comparison |
| **Ayna** | B2B | 50 credits one-time | N/A | $10.4/mes | NO — mensual | claid.ai comparison |
| **Stilab.ai** | LATAM (desconocido) | NO ENCONTRADO | — | NO ENCONTRADO | DESCONOCIDO | Sin presencia verificable en web |
| **Acharaa.ai** | LATAM (desconocido) | NO ENCONTRADO | — | NO ENCONTRADO | DESCONOCIDO | Sin presencia verificable en web |
| **NUESTRO P1** | Consumer | 5 try-ons/semana | SEMANAL (domingo 23:59) | TBD | SI — UNICO ENCONTRADO | — |

---

## 2. Hallazgo Principal: Somos Unicos con Reset Semanal

**Conclusion validada:** Ningun competidor encontrado en el mercado global de virtual try-on AI usa un modelo de cap semanal con reset fijo (domingo 23:59). Los modelos existentes son:

- **Diario:** Magic Hour (3/dia free, 100/dia con cuenta), DLOOK (3 tokens/dia)
- **Mensual:** OutfitMaker (5/mes paid), FASHN (200 credits/mes), FitRoom (10/mes free, 50/mes paid), Genlook (10/mes free)
- **One-time / pool no renovable:** Fits (31 generaciones), FASHN free (10 total), The New Black (3 total), Botika (8 total)
- **Sin cap publico:** Krea AI (ilimitado sin cuenta), WeShop (no publicado)

**El modelo de 5/semana con reset semanal no existe en ningun competidor auditado.**

---

## 3. Analisis de Posicionamiento: Ventaja o Riesgo

### Por que 5/semana es ventaja competitiva clara

**vs modelos diarios (Magic Hour, DLOOK):**
- Magic Hour da 3/dia = 21/mes en teoria, pero son videos e imagenes generales, no try-on especifico de outfit. El usuario no acumula "presupuesto" de la semana — el que no uso hoy se pierde.
- DLOOK da 3 tokens/dia pero el reset diario crea presion de uso diario o perder valor. Produce fatiga si el usuario no entra todos los dias.
- Nuestro modelo semanal permite que el usuario que no entra lunes-miercoles pueda usar sus 5 el fin de semana (cuando hace compras reales). Mas alineado con comportamiento de compra real.

**vs modelos mensuales (OutfitMaker, FitRoom, Genlook):**
- OutfitMaker da 5/mes en el plan Premium de pago ($7.99/mes). Nosotros damos 5/semana (20/mes equivalente) en el plan base. Diferencial de 4x en generosidad.
- FitRoom free: 10/mes. Nosotros P1: ~20/mes equivalente. 2x mas generoso en free.
- Genlook free: 10/mes (pero es B2B Shopify, no consumer). Comparacion indirecta.

**vs one-time pools:**
- Son la experiencia mas frustrante: el usuario prueba, se queda sin creditos y si no paga, nunca regresa. Alta tasa de abandono post-trial.
- Nuestro reset semanal garantiza retention: el usuario sabe que el domingo tiene 5 nuevos try-ons. Crea habito semanal de retorno.

### Riesgo potencial

**Riesgo 1 — Costo de computo:**
5/semana * 4 semanas = 20 try-ons/mes por usuario free. Si el costo de FASHN API o equivalente es ~$0.10/try-on, costo = $2/usuario/mes en free tier. Con base de 1,000 usuarios activos: $2,000/mes en infraestructura solo en free. Validar que el modelo de conversion free-to-paid cubre este costo antes de lanzar sin limite de tiempo.

**Riesgo 2 — Expectativa inflada:**
Si el mercado es "3/dia ilimitado gratis" (Krea AI) o "ilimitado" (TRYO app), el usuario puede percibir nuestro 5/semana como limitado. Contra-argumentar con calidad de output (modelo personalizado) vs cantidad barata.

**Riesgo 3 — Stilab y Acharaa:**
Ambas marcas mencionadas como "LATAM leaders" no tienen presencia verificable en comparaciones globales de herramientas ni en App Store con reviews significativas. Pueden ser empresas muy pequenas, pivotadas, o en stealth. No representan amenaza benchmark validada hoy.

---

## 4. Analisis de Messaging: Como Vende la Competencia Sus Caps

### Modelos de urgencia (diario):
- Magic Hour: "Claim your 100 free credits daily" — activa FOMO diario, gamification de login. Funciona para retener DAU pero no refleja comportamiento de compra de moda (no se compra ropa todos los dias).
- DLOOK: "3 daily tokens" — minimalista, no vende la escasez como feature.

### Modelos de generosidad mensual:
- OutfitMaker: "5 virtual try-ons/month" en el plan Premium — venden el acceso como beneficio del tier, no como limitacion. El free (1 one-time) es tan restrictivo que el paid parece generoso.
- FitRoom: "10 free credits/month" — mensajeria directa, sin dramatismo. No usan urgencia.
- Genlook: "10 monthly try-on included" — tono neutro, orientado a B2B.

### Modelos de ilimitado:
- Krea AI: "Try on as many outfits as you want, completely free. No hidden fees, no accounts required" — mensaje de maxima generosidad. Diferenciador de adquisicion, pero calidad de output es inferior (modelo no personalizado).

### Implicacion para nuestro copy (recomendacion a Leo):

El mercado no tiene un lider claro en como comunicar un cap semanal porque nadie lo usa. Tenemos lienzo en blanco para definir el messaging.

**Opcion A — Generosidad (recomendada para top-of-funnel):**
"5 outfits nuevos cada semana, automaticamente. Sin recordatorios, sin creditos que se vencen en el dia. Tu guardarropa AI se renueva contigo."
- Enfasis en el reset como beneficio, no como limitacion.
- Crea expectativa de novedad semanal (alineado con ciclos de shopping).

**Opcion B — Urgencia suave (recomendada para conversion):**
"Tus 5 try-ons de esta semana estan disponibles. Vencen el domingo."
- Aplica FOMO sin ser agresivo.
- Funciona en push notifications mid-semana para reactivar usuarios inactivos.

**Opcion C — Comparacion directa (para ads de performance):**
"Otras apps te dan 5 try-ons por mes. Nosotros, por semana."
- Directo y factual basado en OutfitMaker Premium como referencia.
- Riesgo: puede generar comparacion de precios si el usuario busca al competidor.

**Recomendacion:** Usar A en onboarding, B en push/email retargeting, C en paid ads solo si se valida que la mayoria del trafico no tiene contexto previo de OutfitMaker.

---

## 5. Mapa de Posicionamiento

```
                    CALIDAD DE OUTPUT
                    (personalizado / generico)
                           |
          Personalizado     |
                           |
          [NUESTRO P1]     |    [Magic Hour]
          5/sem, semanal   |    3/dia, diario
                           |
FRECUENCIA ---------------+--------------- FRECUENCIA
BAJA                      |                ALTA
(mensual/one-time)        |             (diario/ilimitado)
                           |
          [OutfitMaker]    |    [Krea AI]
          5/mes, mensual   |    Ilimitado
                           |
               Generico    |
                           |
```

Ocupamos el cuadrante unico: alta frecuencia de renovacion + alta calidad personalizada. Nadie esta ahi.

---

## 6. Recomendaciones Finales

### Para Leo:
- El cap de 5/semana es un diferenciador real y factual. Usarlo en pitches con confianza: "somos la unica plataforma con reset semanal de try-ons gratuitos".
- Comparacion directa mas fuerte: OutfitMaker Premium cobra $7.99/mes y da 5/mes. Nosotros damos 5/semana en el plan base — 4x mas valor.
- El modelo de retention es el argumento de fondo: reset semanal = habito = mas datos de preferencias = mejor personalizacion = mas conversion a paid.
- Para cierres enterprise/brand: el cap semanal consumer es el gancho de adquisicion; el modelo B2B (sin cap, por volumen) es la conversion final.

### Para Jarvis:
- Costo critico a modelar: 20 try-ons/mes por usuario free @ costo de infraestructura AI. Asegurar que el paywall de funciones premium (mas outfits, guardado, compartir) genere conversion antes de que el costo escale.
- El reset domingo 23:59 debe ser implementado con timezone correcta del usuario. Sin esto, el diferenciador tecnico colapsa para usuarios en zonas horarias distintas.
- Competitor watch recomendado: Magic Hour y FitRoom son los mas activos en consumer. Monitorear si alguno adopta modelo semanal en proximos 90 dias.
- Stilab y Acharaa: no priorizar analisis hasta tener evidencia de traccion real (descargas, pricing publico, reviews verificables).

---

## 7. Fuentes Verificadas

- [OutfitMaker.ai pricing](https://outfitmaker.ai) — verificado via WebFetch directo
- [FASHN.ai pricing](https://fashn.ai/pricing) — verificado via WebFetch directo
- [FitRoom.app pricing](https://fitroom.app/pricing) — verificado via WebFetch directo
- [Genlook Shopify App Store](https://apps.shopify.com/genlook-virtual-try-on) — verificado via WebFetch directo
- [Magic Hour pricing](https://magichour.ai/pricing) — verificado via WebFetch directo
- [claid.ai comparison article](https://claid.ai/blog/article/virtual-try-on-tools) — tabla comparativa de herramientas 2026
- [nightjar.so comparison](https://nightjar.so/blog/best-tools-ai-virtual-try-on) — best tools 2026
- [fits-app.com review](https://www.fits-app.com/posts/top-6-virtual-try-on-apps-to-experiment-with-your-clothes) — top 6 apps revisadas
- [ASOS VTO launch](https://retailtechinnovationhub.com/home/2026/2/17/new-asos-virtual-try-on-experience-launches-in-partnership-with-ai-fashion-platform-aiuta) — ASOS + Aiuta, Feb 2026
- [DLOOK App Store reviews](https://apps.apple.com/us/app/dlook-ai-outfit-stylist/id6745005234) — pricing confirmado via reviews
- [Rent the Runway plans](https://www.renttherunway.com/plans) — pricing page oficial
- [Lookiero review mamabella.uk](https://mamabella.uk/review/stitch-fix-uk-vs-lookiero-reviews-best-how-it-works-price-worth-it/) — modelo fisico confirmado

**Nota sobre Stilab.ai y Acharaa.ai:** No aparecen en ninguna comparativa global verificada (claid, nightjar, camclo3d, fits-app). Sin pricing publico, sin App Store presence significativa. Clasificados como "sin datos" — no representan benchmark validado a mayo 2026.

---
*Preparado por Yang — Investigadora de Inteligencia Comercial | Agencia*
*Fecha: 2026-05-19 | Validez recomendada: 90 dias (revisar si Magic Hour o FitRoom cambian modelo)*
