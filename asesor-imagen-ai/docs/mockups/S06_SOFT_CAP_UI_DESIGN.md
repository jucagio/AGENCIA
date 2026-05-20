# S06 — SOFT CAP UI DESIGN
## Style Insights Post-Analysis + Cap Screen

**Owner:** Erik (Diseñador Senior)
**Fecha:** 2026-05-20
**Status:** COMPLETADO — listo para Figma + entrega Brook
**Depende de:** COPY_SOFT_CAP_APPROVED.md (Leo), DECISIONES_APROBADAS.md (D4), DESIGN_SYSTEM.md (Aether Luxe)

---

## CONTEXTO DE DISEÑO

El usuario completó su try-on (vision_worker procesó). El backend retornó `body_analysis` + estilo recomendado. La pantalla muestra el resultado primero — sin interrupciones. Solo después, cuando el usuario ya consumió el valor, aparece el mensaje de soft cap en un bottom sheet no intrusivo.

**Regla de oro S06:** Resultado primero, soft cap después. Nunca al revés.

---

## FLOW COMPLETO S06

```
Usuario sube foto + prenda
         ↓
Backend retorna resultado (body_type + color_season + estilo)
         ↓
[S06-A] Results Card aparece — full screen, sin interrupción
         ↓  (300ms delay post-render)
[S06-B] Soft cap slide-up — bottom sheet no intrusivo
         ↓
[S06-C] Counter visible en header en todo momento
```

---

## S06-A — RESULTS CARD (aparece primero)

### Layout frame: 390 x 844px (iPhone 14 Pro)

```
┌─────────────────────────────────────────┐  ← safe top 59px
│                                         │
│  [← Atras]          [X/3 esta semana]   │  header row
│                      counter pill       │  h=48px, padding lateral 24px
│                                         │
│  ─── IMAGEN ANALIZADA ──────────────── │  margin-top: 16px
│  ┌───────────────────────────────────┐  │  card imagen
│  │                                   │  │  radius lg (16px)
│  │     [imagen del look analizado]   │  │  shadow ambient2
│  │     aspect 3:4 portrait           │  │  object-cover full bleed
│  │     full width con gutter 24px    │  │
│  │                                   │  │
│  └───────────────────────────────────┘  │
│                                         │
│  ─── RESULTADO ANALISIS ─────────────  │  margin-top: 16px
│  ┌───────────────────────────────────┐  │  AI Insight Card
│  │  [Chip AI Insights violeta]       │  │  bg: surfaceContainerLow (#F3F4F6)
│  │  "AI Insights"                    │  │  radius: lg (16px)
│  │                                   │  │  padding: 24px
│  │  h3: "Tu tipo de cuerpo es        │  │  shadow: ambient1
│  │       Triangulo Invertido."       │  │
│  │  bodyMd: "Color season: Verano    │  │  onSurface
│  │  Suave. Estilo recomendado:       │  │  onSurfaceVariant
│  │  Minimalista editorial."          │  │
│  │                                   │  │
│  │  [ic: check_circle 16px success]  │  │  success #22C55E (hardcode ok)
│  │  "Analisis completado"            │  │  caption 12px, success color
│  └───────────────────────────────────┘  │
│                                         │
│  ─── ACCIONES ───────────────────────  │  margin-top: 24px
│  ╔══════════════╗  ╔════════════════╗  │  dos botones
│  ║ ♥ Guardar   ║  ║ 📤 Compartir  ║  │  GradientButton + OutlineButton
│  ╚══════════════╝  ╚════════════════╝  │  height 48px cada uno
│                                         │
│                                         │  ← bottom sheet aparece aquí
└─────────────────────────────────────────┘  ← safe bottom 34px
```

### Tokens Results Card

```
Imagen analizada:
  - aspect: 3/4 portrait
  - radius: lg = 16px
  - shadow: ambient2
  - margin lateral: 24px

AI Insight Card:
  - bg: surfaceContainerLow (#F3F4F6)
  - radius: lg = 16px
  - padding: 24px (AppSpacing.md)
  - shadow: ambient1
  - gap interna: 8px entre chip / h3 / body

AI Chip (AIInsightChip):
  - bg: tertiaryFixed (#E9DDFF)
  - text: onTertiaryContainer (#9466FF)
  - padding: 4px 12px
  - radius: full

h3 resultado:
  - Inter 24px w500
  - color: onSurface (#191C1E)

bodyMd resultado:
  - Inter 16px w400
  - color: onSurfaceVariant (#45464C)
  - line-height: 1.6

Botones acciones:
  - Guardar: GradientButton (gradient #0058BE → #9466FF)
  - Compartir: OutlineButton (borde 1px #000)
  - height: 48px (tap target WCAG)
  - radius: full (pill)
```

### Animacion Results Card enter

```
Trigger: results recibidos del backend

1. AIInsightCard:
   - from: opacity 0, translateY +24px
   - to: opacity 1, translateY 0
   - duration: 400ms
   - easing: Curves.easeOut
   - delay: 0ms (inmediato)

2. Imagen analizada:
   - from: opacity 0, scale 0.95
   - to: opacity 1, scale 1.0
   - duration: 350ms
   - easing: Curves.easeOut
   - delay: 0ms

3. Botones acciones:
   - from: opacity 0
   - to: opacity 1
   - duration: 250ms
   - easing: Curves.easeOut
   - delay: 200ms (salen despues del card)
```

---

## S06-B — SOFT CAP BOTTOM SHEET (aparece despues)

### Principio de timing

```
Results Card termina de animar (400ms) → espera 300ms adicional
→ soft cap slide-up aparece
Total delay desde render: 700ms

Razon: usuario debe ver y "consumir" el resultado antes de ver el cap.
No interrumpir la satisfaccion del resultado.
```

### Layout Bottom Sheet

```
┌─────────────────────────────────────────┐
│                                         │
│  [Results card visible arriba]          │  partial visible, dimmed 40%
│  [opacity overlay 0.4, bg #191C1E]      │  SCrim detras del sheet
│                                         │
│  ─────────────────────────────────────  │  BottomSheet handle
│  ════════════════════════════════       │  4px x 32px, color outlineVariant
│                                         │  centrado, margin-top 12px
│                                         │
│  ─── MENSAJE SOFT CAP ──────────────  │  margin-top: 8px, padding: 16px
│                                         │
│  [Heading — VARIANT por dia/segmento]   │  Inter 18px w600
│  ver COPY_SOFT_CAP_APPROVED.md          │  color: onSurface (#191C1E)
│                                         │  line-height: 1.4
│                                         │
│  ╔═══════════════════════════════════╗  │  CTA button principal
│  ║  [CTA text del variant]          ║  │  GradientButton pill
│  ╚═══════════════════════════════════╝  │  height: 48px
│                                         │  gradient #0058BE → #9466FF
│  "$2.99 / $9.99/mes" (si aplica)       │  bodyMd, onSurfaceVariant
│  posicion: segun price_position JSON    │  centrado bajo boton
│                                         │
│  ─────────────────────────────────────  │  divider outlineVariant 1px
│                                         │  margin vertical: 12px
│                                         │
│  "El domingo tendras 3 nuevos gratis"   │  caption 12px, onSurfaceVariant
│  o: "[Esperar al domingo]"              │  TextButton, onSurfaceVariant
│     (si el variant lo tiene)           │  centrado
│                                         │
│                                         │  margin-bottom: 16px + safe area
└─────────────────────────────────────────┘
```

### Variants mapeados a layout

**Variant A — "Unlock More" (Lun→Mie)**
```
Heading:    "Ya usaste tus 3 estilos de esta semana.
             Desblockeá 3 más por $2.99"
             (18px w600, onSurface, multiline)

CTA:        "Unlock 3 more"
             GradientButton, color #0058BE → #9466FF

Price:      "$2.99" inline en heading (color secondary #0058BE, w600)

Reset msg:  "El domingo tendras 3 nuevos gratis"
             caption, onSurfaceVariant, sin boton
```

**Variant B — "Complete Your Week" (Jue→Dom)**
```
Heading:    "3 conjuntos explorados. El que mas te gusta
             esta cerca. Desbloquea la mejor version
             de ti esta semana."
             (18px w600, onSurface, 3 lineas max)

CTA:        "Unlock premium looks"
             GradientButton

Price:      "$2.99" bajo CTA
             bodyMd, onSurfaceVariant, centrado

Reset msg:  "El domingo tendras 3 nuevos gratis"
             caption, onSurfaceVariant
```

**Variant C — "Premium Anchor" (heavy users)**
```
Heading:    "Acabas de explorar los 3 estilos libres.
             Prueba Premium ($9.99/mes) para ilimitadas."
             (18px w600, onSurface)

CTA:        "Try Premium"
             GradientButton (violeta mas prominente — usar color #9466FF solid)

Secondary CTA: "Solo esta semana — $2.99"
             OutlineButton, debajo del GradientButton
             borde 1px secondary, text secondary

Price:      "$9.99/mes" inline en heading, color: onTertiaryContainer (#9466FF)

Reset msg:  no mostrar (heavy user debe convertir, no esperar)
```

**Variant D — "Reset Anticipation" (Lun + churn-risk)**
```
Heading:    "Tu semana de estilo esta completa.
             El domingo tendras 3 nuevos.
             ¿O prefieres explorar YA?"
             (18px w600, onSurface)

CTA:        "Explore now"
             GradientButton

Secondary:  "Esperar al domingo"
             TextButton, onSurfaceVariant, centrado debajo del gradient
             → tap: dismiss sheet, mostrar solo reset counter

Price:      $2.99 aparece solo cuando usuario toca "Explore now"
             → bottom sheet secundario con detalle de pago
```

### Tokens Bottom Sheet

```
Bottom sheet:
  - bg: surface (#F8F9FB) — no surfaceContainerLow, queremos claridad
  - radius top: xl = 24px (BorderRadius.only topLeft/topRight)
  - padding: 16px horizontal, 8px vertical (AppSpacing.sm)
  - elevation: sincronizado con ambient2

Handle:
  - color: outlineVariant (#C6C6CD)
  - width: 32px
  - height: 4px
  - radius: full

Heading soft cap:
  - Inter 18px w600
  - onSurface (#191C1E)
  - line-height: 1.4
  - max 3 lineas antes de truncar

CTA GradientButton:
  - gradient: #0058BE → #9466FF (135deg)
  - height: 48px (tap target WCAG)
  - radius: full (pill)
  - margin-top: 16px

CTA secundario (si variant C o D):
  - OutlineButton o TextButton segun caso
  - margin-top: 8px

Price below CTA:
  - Inter 14px w400
  - onSurfaceVariant (#45464C)
  - centrado

Divider:
  - outlineVariant (#C6C6CD), 1px height

Reset message:
  - Inter 12px w400
  - onSurfaceVariant (#45464C)
  - centrado
  - margin-top: 8px

Sheet margin bottom edge:
  - 16px + MediaQuery.of(context).viewInsets.bottom
```

### Animacion Bottom Sheet

```
Slide-up:
  - from: Offset(0, 1.0) → Offset(0, 0)
  - duration: 300ms
  - easing: Curves.easeOut

Scrim (overlay oscuro detras):
  - from: opacity 0 → 0.4
  - duration: 300ms
  - sincronizado con sheet

CTA button:
  - Ripple on tap: Material ripple, color #0058BE 30% opacity
  - Scale feedback: 1.0 → 0.97 tap down, 0.97 → 1.0 tap up (100ms)

Secondary TextButton:
  - fade-in: 200ms delay de 100ms despues del sheet
  - (da tiempo de que el CTA principal sea lo primero que el ojo ve)

Dismiss:
  - usuario puede swipe down para cerrar
  - DraggableScrollableSheet con initialChildSize: 0.4 (40% pantalla)
  - minChildSize: 0.0 (cierra), maxChildSize: 0.5 (50% max)
```

---

## S06-C — COUNTER HEADER (visible en todo momento)

### Counter Pill

```
Posicion: header row de la pantalla S06 (y S04)
Alineacion: right, vertical-center con el titulo

Estados del counter:

Estado normal (X < 3):
  "2/3 esta semana"
  ─────────────────────────────
  Layout: pill horizontal
  bg: surfaceContainerHigh (#E7E8EA)
  text: onSurfaceVariant (#45464C)
  padding: 4px 12px
  radius: full
  font: labelCaps (12px w600 uppercase)
  icono: none

Estado alerta (X = 2, ultimo libre):
  "1/3 esta semana"
  ─────────────────────────────
  bg: errorContainer (#FFDED6)
  text: onErrorContainer (#93000A)
  icono: warning_amber 14px, mismo color
  padding: 4px 10px 4px 8px (icono left, text right)
  radius: full

Estado cap (X = 3, 0 restantes):
  "0/3 (reset domingo 23:59 UTC)"
  ─────────────────────────────
  bg: errorContainer (#FFDED6)
  text: onErrorContainer (#93000A)
  icono: lock_outline 14px, mismo color
  radius: full
  text: labelCaps, sin uppercase (el texto es mas largo)

Tap en counter (cualquier estado):
  → Tooltip inline aparece debajo del pill:
    "Tus try-ons se renuevan el domingo a medianoche"
    bg: primaryContainer (#141B2B), text: onPrimaryContainer (#7D8497)
    radius: md (12px), padding: 8px 12px
    arrow up pointing al pill
    dismiss: tap anywhere
```

### Counter animation

```
Cambio de numero (cuando se completa un try-on):
  - AnimatedSwitcher (child swap)
  - from: opacity 1, scale 1.0
  - to: opacity 0, scale 0.8 (salida)
  - nuevo valor: opacity 0, scale 0.8 → opacity 1, scale 1.0 (entrada)
  - duration: 200ms

Transicion normal → alerta (pasar a 1/3):
  - AnimatedContainer: color bg change
  - duration: 300ms

Transicion alerta → cap (pasar a 0/3):
  - AnimatedContainer: color change
  - pulse: scale 1.0 → 1.1 → 1.0 una vez (llamar atencion)
  - duration: 400ms total
```

---

## VALIDATION CHECKLIST S06

- [ ] Results card aparece ANTES del soft cap (timing 0-700ms)
- [ ] Soft cap aparece como slide-up (nunca fullscreen interrupt)
- [ ] Counter pill visible en header en todos los estados
- [ ] Variant A: heading con precio $2.99 inline
- [ ] Variant B: precio $2.99 bajo el CTA
- [ ] Variant C: secondary CTA "Solo esta semana — $2.99"
- [ ] Variant D: CTA primario "Explore now" + secondary "Esperar al domingo"
- [ ] Reset message siempre visible (excepto Variant C)
- [ ] Animacion slide-up 300ms ease-out
- [ ] CTA button ripple + scale feedback
- [ ] Counter: 3 estados visuales (normal / alerta / cap)
- [ ] Counter tap → tooltip
- [ ] Tokens Aether Luxe en todos los componentes
- [ ] Touch targets minimo 48px height en todos los botones
- [ ] Bottom sheet DraggableScrollableSheet con swipe-dismiss

---

## BROOK IMPLEMENTATION NOTES

```dart
// Componentes a crear:

// 1. ResultsAnalysisCard
// Muestra imagen analizada + AI insight card + acciones
// Props: analysisResult BodyAnalysisResult, onSave VoidCallback, onShare VoidCallback
// Animaciones: ver "Animacion Results Card enter"

// 2. SoftCapBottomSheet
// Muestra variant segun dia/segmento
// Props:
//   variant SoftCapVariant {A, B, C, D}
//   onCTA VoidCallback
//   onSecondary VoidCallback?
//   resetsAt DateTime
// Logica:
//   Recibe variant del backend: GET /api/v1/users/me/usage retorna soft_cap_variant String
//   o calcula localmente segun DAY_MAP (fallback si backend no lo retorna)
// Timing: mounted 700ms despues de que ResultsAnalysisCard termina de animar

// 3. TryOnCounterPill
// Siempre visible en header de S06 y S04
// Props: used int, cap int, resetsAt DateTime
// Estados: normal / warning / cap (ver specs arriba)
// Tap: showTooltip() con texto de reset

// Estructura widget tree S06:
//
// StyleInsightsScreen
//   └── Column
//       ├── S06Header (titulo + counter pill)
//       ├── ResultsAnalysisCard (entra con animacion)
//       └── [SoftCapBottomSheet se monta 700ms despues via showModalBottomSheet]

// SoftCapBottomSheet:
// showModalBottomSheet(
//   context: context,
//   isScrollControlled: true,
//   backgroundColor: Colors.transparent,
//   builder: (_) => DraggableScrollableSheet(
//     initialChildSize: 0.40,
//     minChildSize: 0.0,
//     maxChildSize: 0.50,
//     builder: (_, controller) => SoftCapSheet(
//       scrollController: controller,
//       variant: variant,
//       ...
//     ),
//   ),
// );

// El backend debe retornar en GET /api/v1/users/me/usage:
// {
//   "soft_cap_reached": true,          // si uses >= 3 esta semana
//   "soft_cap_variant": "B",           // segun logica de Leo (dia + segmento)
//   "tryons_used_week": 3,             // para el counter pill
//   "tryons_cap_week": 3,
//   "cap_resets_at": "2026-05-24T23:59:00Z"  // proximo domingo
// }
```

---

**Ultima actualizacion:** 2026-05-20
**Owner:** Erik
**Entrega en Figma:** Wave 1 — antes del DOM 21 EOD
**Handoff Brook:** SAB 25 mayo 2026
