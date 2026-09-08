# ERIK — SPRINT DESIGN SPECS
## AI Fit Check — 11 Pantallas (Aether Luxe)

**Owner:** Erik (Diseñador Senior)
**Sprint:** SAB 18 — SAB 25 mayo 2026
**Design system:** Aether Luxe — aprobado por Juan Camilo Gil (2026-05-18)
**Entrega a Brook:** SAB 25 mayo 2026

**Referencia de tokens:** `docs/design-system/DESIGN_SYSTEM.md`
**Referencia de flujos:** `docs/UX_SCREENS_PLAN.md`
**Decisiones aprobadas:** `docs/DECISIONES_APROBADAS.md` (D1-D5)

---

## NOTA DE SISTEMA DE DISENO

El sistema previo (Blush Rose / pastel) queda DESCONTINUADO.
El sistema oficial es Aether Luxe. Todos los tokens vienen de `AppColors`, `AppTypography`, `AppSpacing`, `AppRadius`, `AppShadows`.

Gradiente primario: `LinearGradient(135deg, #0058BE → #9466FF)` — uso EXCLUSIVO en CTAs, loaders IA, borders activos.

---

## SEMANA DE ENTREGA

| Dias | Pantallas | Notas |
|------|-----------|-------|
| SAB-DOM (18-19) | S04B + S06 + S07 + S11 | Sin dependencias — empezar ya |
| LUN-JUE (20-23) | S05 + S08 + S09 + S10 | D1-D5 ya aprobadas |
| JUE-SAB (23-25) | S01 + S02 + S03 + S04 + refinamiento | Completar set + handoff |

---

## CANVAS BASE — Figma

Frames principales:
- Mobile: 390 x 844px (iPhone 14 Pro)
- Variant compact: 375 x 812px (iPhone SE / Android small)

Safe areas:
- Top: 59px (status bar + notch)
- Bottom: 34px (home indicator)
- Lateral gutter: 24px (AppSpacing.gutter)

Grid:
- Columns: 4 (mobile), gutters 24px, margins 24px

---

---

# WAVE 1 — SAB-DOM (Sin dependencias)

---

## S04B — Loading State (NUEVO)

**Descripcion:** Estado intermedio entre "submit" del try-on y recepcion del resultado. Dura 15-45 segundos mientras Replicate procesa.

**UX Priority:** P0 — sin esto el usuario no sabe que paso.

### Layout

```
┌─────────────────────────────────────┐  ← Frame 390x844
│                                     │  ↑ Status bar 59px
│                                     │
│                                     │  Espacio superior 48px
│                                     │
│   ┌─────────────────────────────┐   │  Loader card
│   │                             │   │  Margin lateral 24px
│   │                             │   │  Height: 320px
│   │    [Gradient shimmer]       │   │  bg: surfaceContainerLow
│   │    animacion pulsante       │   │  radius: lg (16px)
│   │                             │   │  shadow: ambient2
│   │  ✨ (icono auto_awesome)    │   │  icono 32px, color #9466FF
│   │                             │   │
│   │  "Nuestra IA esta           │   │  h3 (24px Inter 500)
│   │   creando tu look..."       │   │  color: onSurface #191C1E
│   │                             │   │  margin-top: 16px
│   │  "Esto puede tardar         │   │  bodyMd (16px Inter 400)
│   │   hasta 30 segundos"        │   │  color: onSurfaceVariant #45464C
│   │                             │   │
│   └─────────────────────────────┘   │
│                                     │
│   [Progress bar gradiente]          │  margin-top: 32px
│   0% ──────────────────── 100%      │  height: 4px, radius: full
│   color: gradient #0058BE → #9466FF │  animacion: fill indefinida
│                                     │
│   "Analizando proporciones..."      │  bodyMd, color: onSurfaceVariant
│   (texto que rota cada 5s)          │  margin-top: 12px, centrado
│   Secuencia de textos:              │
│     - "Analizando proporciones..."  │
│     - "Combinando colores..."       │
│     - "Aplicando tu estilo..."      │
│     - "Casi listo..."               │
│                                     │
│   [Boton cancelar — outline]        │  margin-top: 48px
│   "Cancelar"                        │  Outline button, text: onSurface
│                                     │  Solo visible si >20s
│                                     │
└─────────────────────────────────────┘  ↓ Bottom 34px
```

### Shimmer Animation spec

```
Componente: GradientLoader
Tipo: shimmer sweep (diagonal)
Gradient: LinearGradient(
  begin: Alignment.topLeft,
  end: Alignment.bottomRight,
  colors: [
    Color(0xFF0058BE).withOpacity(0.15),  // reposo
    Color(0xFF9466FF).withOpacity(0.35),  // pico brillante
    Color(0xFF0058BE).withOpacity(0.15),  // reposo
  ],
  stops: [0.0, 0.5, 1.0],
)
Animacion: TweenAnimationBuilder o AnimationController
  Duration: 1800ms
  Curve: Curves.easeInOut
  RepeatMode: PingPong (va y vuelve)

El fondo de la card late entre:
  surfaceContainerLow (#F3F4F6) — reposo
  primaryFixed (#DCE2F7, azul muy palido) — pico

Ademas: pulse sutil de escala
  Scale: 1.00 → 1.015 → 1.00
  Duration: 2000ms
  RepeatMode: loop
```

### Textos rotativos

```
Intervalo: 5000ms (5 segundos) por texto
Transicion: fade out 300ms → fade in 300ms
Orden:
  0s:   "Analizando proporciones..."
  5s:   "Combinando colores y estilos..."
  10s:  "Aplicando tu look ideal..."
  15s:  "Finalizando detalles..."
  20s+: "Casi listo, valió la pena esperar..."
```

### Tokens usados

```
bg card:        surfaceContainerLow (#F3F4F6)
shadow card:    ambient2
radius card:    lg = 16px
icono color:    onTertiaryContainer (#9466FF)
h3 color:       onSurface (#191C1E)
body color:     onSurfaceVariant (#45464C)
progress bar:   gradient #0058BE → #9466FF
progress track: outlineVariant (#C6C6CD)
```

### Brook implementation notes

```
Widget: GradientLoaderCard (stateful, autostart)
Props:
  - onCancel: VoidCallback? (null = no mostrar boton)
  - rotatingTexts: List<String>
  - durationMs: int (default 45000)

El widget gestiona internamente:
  - AnimationController para shimmer
  - Timer para textos rotativos
  - Timer para mostrar boton cancelar (>20s)

Trigger: se monta cuando POST /try-ons responde 202
Desmonte: cuando polling recibe status = "completed"
Transicion al resultado: FadeTransition 400ms
```

---

## S06 — Style Insights

**Descripcion:** Pantalla de perfil de estilo personal. Dos estados: sin analisis previo (A) y con analisis completado (B).

### Estado A — Sin analisis

```
┌─────────────────────────────────────┐
│                                     │  Status bar 59px
│  "Tu Perfil de Estilo"              │  h2 (32px Inter 600)
│  [AI Fit Check — Asesor de Imagen]  │  labelCaps, onSurfaceVariant
│                                     │  padding-top: 24px, lateral: 24px
│                                     │
│  ┌─────────────────────────────┐    │  Card "Tipo de cuerpo"
│  │  [ic: body_scan]            │    │  bg: surfaceContainerLow
│  │  "Descubre tu tipo          │    │  radius: lg (16px)
│  │   de cuerpo"                │    │  padding: 24px
│  │                             │    │  shadow: ambient1
│  │  "Obtén recomendaciones     │    │  bodyMd, onSurfaceVariant
│  │   personalizadas basadas    │    │
│  │   en tu silueta."           │    │
│  │                             │    │
│  │  [Chip AI Insights violeta] │    │  AIInsightChip component
│  │  "Analisis personalizado"   │    │
│  └─────────────────────────────┘    │
│                                     │
│  ┌─────────────────────────────┐    │  Card "Color season"
│  │  [ic: palette]              │    │  Misma estructura
│  │  "Conoce tu temporada       │    │
│  │   de color"                 │    │
│  │                             │    │
│  │  "Descubre los colores que  │    │
│  │   mejor resaltan tu tono    │    │
│  │   de piel natural."         │    │
│  │                             │    │
│  │  [Chip AI Insights violeta] │    │
│  └─────────────────────────────┘    │
│                                     │
│  ╔═════════════════════════════╗    │  GradientButton CTA
│  ║  ✨ Iniciar analisis        ║    │  pill, gradient azul→violeta
│  ╚═════════════════════════════╝    │  margin-top: 32px, lateral: 24px
│                                     │
│  "El analisis usa solo tu foto      │  bodyMd, onSurfaceVariant
│   — no almacenamos datos biometricos"│  centrado, margin-top: 12px
│                                     │
└─────────────────────────────────────┘
```

### Estado B — Con analisis (resultado completo)

```
┌─────────────────────────────────────┐
│  "Tu Perfil de Estilo"              │  h2
│  [AI Fit Check — Asesor de Imagen]  │  labelCaps, onSurfaceVariant
│                                     │
│  ─────── CARD TIPO DE CUERPO ─────  │  margin-top: 24px
│  ┌─────────────────────────────┐    │
│  │  [Chip AI] "Tipo de Cuerpo" │    │  AIInsightChip arriba
│  │                             │    │
│  │  [Silueta ilustracion SVG]  │    │  Ilustracion 120x160px
│  │  centrada, color: primary   │    │  trazo negro lineal
│  │                             │    │
│  │  h3: "Triangulo invertido"  │    │  h3 (24px Inter 500)
│  │  (ejemplo de resultado)     │    │  onSurface
│  │                             │    │
│  │  bodyMd: descripcion breve  │    │  2-3 lineas maximo
│  │  de que implica este tipo   │    │  onSurfaceVariant
│  └─────────────────────────────┘    │
│                                     │
│  ─── CARD COLOR SEASON ──────────  │  margin-top: 16px
│  ┌─────────────────────────────┐    │
│  │  [Chip AI] "Color Season"   │    │
│  │                             │    │
│  │  h3: "Verano Suave"         │    │  Resultado del analisis
│  │  (ejemplo)                  │    │
│  │                             │    │
│  │  Paleta personal:           │    │  labelCaps, onSurfaceVariant
│  │  ⬤ ⬤ ⬤ ⬤ ⬤ ⬤           │    │  6 color swatches
│  │  (ColorSwatch chips)        │    │  32x32px cada uno, radius full
│  │                             │    │  con hex tooltip on tap
│  └─────────────────────────────┘    │
│                                     │
│  ─── CARD COLORES RECOMENDADOS ──  │  margin-top: 16px
│  ┌─────────────────────────────┐    │
│  │  "Mejores para ti"          │    │  labelCaps, secondary (#0058BE)
│  │  ⬤ ⬤ ⬤ ⬤ ⬤ ⬤           │    │  swatches con borde verde subtil
│  │  (verde sutil = bueno)      │    │
│  │                             │    │
│  │  "Evitar"                   │    │  labelCaps, error (#BA1A1A)
│  │  ⬤ ⬤ ⬤ (con X encima)   │    │  swatches con X overlay
│  └─────────────────────────────┘    │
│                                     │
│  ─── CARD RECOMENDACIONES ───────  │  margin-top: 16px
│  ┌─────────────────────────────┐    │
│  │  [Chip AI] "Recomendaciones"│    │
│  │                             │    │
│  │  • bullet bodyMd punto 1    │    │  max 4 bullets
│  │  • bullet bodyMd punto 2    │    │  onSurfaceVariant
│  │  • bullet bodyMd punto 3    │    │
│  └─────────────────────────────┘    │
│                                     │
│  [Boton: "Repetir analisis"]        │  OutlineButton, al final
│  OutlineButton, text onSurface      │
│                                     │
└─────────────────────────────────────┘
```

### Tokens usados

```
bg cards:       surfaceContainerLow (#F3F4F6)
shadow:         ambient1
radius:         lg = 16px
padding cards:  24px (AppSpacing.md)
AI chip:        AIInsightChip component (fondo tertiaryFixed #E9DDFF, texto #9466FF)
silueta:        SVG trazos, color primary (#000)
color swatches: circles 32px, radius full
  buenos:       border 2px success (#22C55E) [no en tokens — usar hardcode]
  evitar:       overlay X, color error (#BA1A1A)
gap entre cards: 16px (AppSpacing.sm)
```

### Brook implementation notes

```
Widgets:
  - StyleInsightsEmpty (Estado A)
  - StyleInsightsLoaded (Estado B, recibe BodyAnalysis model)

Data: GET /api/v1/body-analysis
  Response tiene: body_type, color_season, recommended_colors[], avoid_colors[], recommendations[]

ColorSwatch widget:
  - Props: hex String, isGood bool, isAvoid bool
  - Shows: circle + label (name) + hex on tap (tooltip)

BodyTypeSilhouette widget:
  - Props: bodyType String (enum: pear, rectangle, inverted_triangle, hourglass, oval)
  - SVG asset per body type: assets/illustrations/body_type_{type}.svg
  - 5 SVG files needed (crear con Illustrator o solicitar a Erik)
```

---

## S07 — Body Analysis Upload

**Descripcion:** Pantalla de captura de foto para iniciar el analisis de tipo de cuerpo y color season.

```
┌─────────────────────────────────────┐
│  [← Atras]                          │  Boton back, icono arrow_back
│  "Analisis de Figura"               │  h2 (32px Inter 600), onSurface
│  [AI Fit Check — Asesor de Imagen]  │  labelCaps, onSurfaceVariant
│                                     │
│  ──────── INSTRUCCIONES ──────────  │  Card instrucciones
│  ┌─────────────────────────────┐    │  bg: primaryFixed (#DCE2F7)
│  │  Como tomar la foto ideal:  │    │  radius: lg, padding: 16px
│  │                             │    │  labelCaps, onPrimaryFixed
│  │  ✓ De frente, posicion      │    │  bodyMd, onSurface
│  │    natural                  │    │
│  │  ✓ Fondo liso o neutro      │    │
│  │  ✓ Ropa ajustada o ceñida   │    │
│  │  ✓ Luz natural (no flash)   │    │
│  │  ✗ No selfie (muy corta)    │    │  texto error (#BA1A1A) para "no"
│  └─────────────────────────────┘    │
│                                     │
│  ──────── UPLOAD ZONE ────────────  │  margin-top: 24px
│  ┌─────────────────────────────┐    │  UploadZone component
│  │                             │    │  min-height: 340px
│  │  [ic: person, 48px]         │    │  borde: 2px dashed outlineVariant
│  │  color: outline #76777D     │    │  radius: lg (16px)
│  │                             │    │  bg: surfaceContainerLowest
│  │  "Tu foto de cuerpo         │    │
│  │   completo"                 │    │  h3 (24px Inter 500), onSurface
│  │                             │    │  margin-top: 12px
│  │  "De frente, buena luz,     │    │  bodyMd, onSurfaceVariant
│  │   figura completa visible"  │    │
│  │                             │    │
│  └─────────────────────────────┘    │
│  Estado filled:                     │  cuando hay foto:
│  ┌─────────────────────────────┐    │  imagen preview full-bleed
│  │  [imagen preview]           │    │  object-cover, radius lg
│  │  object-cover               │    │  boton X top-right 32px circle
│  │              [X]            │    │  bg: surface/80%, icono: onSurface
│  └─────────────────────────────┘    │
│                                     │
│  ╔═════════════════════════════╗    │  GradientButton CTA
│  ║  ✨ Analizar mi figura      ║    │  Disabled: si no hay foto
│  ╚═════════════════════════════╝    │  pill, gradient azul→violeta
│                                     │
│  Tap → POST /api/v1/body-analysis   │  → mostrar S04B loading
│         → polling → redirect S06    │
│                                     │
└─────────────────────────────────────┘
```

### Tokens usados

```
card instrucciones: bg primaryFixed (#DCE2F7), radius lg
upload zone:        2px dashed outlineVariant (#C6C6CD)
  hover/active:     borde → secondary (#0058BE)
  active gradient border (cuando drag over): gradient stroke 2px
icono upload:       person, 48px, color outline (#76777D)
boton X preview:    circle 32px, bg surface (#F8F9FB) 80% opacity
CTA:                GradientButton (pill, gradient)
disabled state:     opacity 0.4, no gradient
```

### Brook implementation notes

```
Widget: BodyAnalysisUploadScreen
Comparte UploadZone widget con S04 (mismo componente)

Props zona upload:
  - promptIcon: Icons.person_outline
  - promptTitle: "Tu foto de cuerpo completo"
  - promptSubtitle: "De frente, buena luz, figura completa visible"
  - aspectRatio: 3/4 (portrait, muestra figura entera)

Flow:
  1. Tap zona → ImagePicker (camera o gallery)
  2. Foto seleccionada → preview en zona
  3. CTA habilitado → POST /body-analysis → 202
  4. → navegar a GradientLoaderCard (S04B variant)
     duration: 20000ms, texts rotatorios especificos:
     "Detectando silueta...", "Analizando proporciones...",
     "Calculando temporada de color...", "Casi listo..."
  5. Polling → redirect a StyleInsightsScreen (S06, Estado B)
```

---

## S11 — Error States (4 estados)

**Descripcion:** Pantalla y componentes para todos los estados de error y carga generica.

### S11a — Skeleton Loading (carga generica)

```
Patron de skeleton para:
  - Lista de wardrobe items cargando
  - Collections grid cargando
  - Style Insights cargando
  - Perfil cargando

Skeleton base:
  bg:     surfaceContainerHigh (#E7E8EA)
  shimmer: sweep blanco 30% opacity, diagonal, 1200ms loop
  radius: matching el componente real (card: lg, circle: full)

Skeleton de card (wardrobe item):
  ┌──────────┐
  │ [rect    │  120x120px, radius md (12px)
  │  shimmer]│  imagen placeholder
  └──────────┘
  ████████     linea titulo: 80px x 12px, radius full
  █████        linea subtitulo: 50px x 10px, radius full

Skeleton de card grande (resultado try-on):
  ┌───────────────────────────────┐
  │                               │  280px height, radius lg
  │          [shimmer]            │
  └───────────────────────────────┘
  ████████████████████████         linea 1: 200px x 14px
  █████████████                    linea 2: 130px x 12px
```

### S11b — Error 404 (pagina no encontrada)

```
┌─────────────────────────────────────┐
│                                     │
│                                     │  padding-top: 80px
│   [Ilustracion: personaje busca     │  ilustracion SVG 240x200px
│    algo con lupa, estilo lineal]    │  color: onSurfaceVariant + trazos
│                                     │
│   "404"                             │  h1 (48px Inter 600)
│                                     │  color: onSurface
│   "No encontramos                   │  h3 (24px Inter 500)
│    esta pagina"                     │  color: onSurface, margin-top: 16px
│                                     │
│   "Es posible que haya sido         │  bodyMd, onSurfaceVariant
│    movida o ya no exista."          │  margin-top: 8px, centrado
│                                     │
│   ╔═════════════════════════════╗   │  GradientButton
│   ║  Volver al inicio          ║   │  margin-top: 48px
│   ╚═════════════════════════════╝   │  → navegar a home (Try-On)
│                                     │
└─────────────────────────────────────┘
```

### S11c — Error de red (sin conexion)

```
┌─────────────────────────────────────┐
│                                     │
│                                     │  padding-top: 80px
│   [Ilustracion: wifi cortado,       │  SVG 200x180px
│    nube rota, estilo lineal]        │  onSurfaceVariant trazos
│                                     │
│   "Sin conexion"                    │  h2 (32px Inter 600), onSurface
│                                     │
│   "Revisa tu conexion a             │  bodyMd, onSurfaceVariant
│    internet e intenta               │  margin-top: 8px, centrado
│    de nuevo."                       │
│                                     │
│   ╔═════════════════════════════╗   │  GradientButton
│   ║  Reintentar                 ║   │  margin-top: 40px
│   ╚═════════════════════════════╝   │  → trigger retry de la accion fallida
│                                     │
│   "Intentando reconectar..."        │  bodyMd, onSurfaceVariant
│   [spinner 24px, color secondary]   │  visible solo cuando retry activo
│                                     │
└─────────────────────────────────────┘
```

### S11d — Try-On fallido

```
┌─────────────────────────────────────┐
│                                     │
│   [ic: error_outline 48px]          │  icono centrado
│   color: error (#BA1A1A)            │  margin-top: 80px
│                                     │
│   "Algo salio mal"                  │  h2 (32px Inter 600), onSurface
│                                     │
│   "No pudimos generar tu look       │  bodyMd, onSurfaceVariant
│    esta vez. Tu try-on diario       │  centrado, margin-top: 8px
│    no fue descontado."              │
│                                     │
│   ╔═════════════════════════════╗   │  GradientButton
│   ║  Intentar de nuevo          ║   │  margin-top: 32px
│   ╚═════════════════════════════╝   │  → retry POST /try-ons
│                                     │
│   [Boton outline]                   │  OutlineButton
│   "Contactar soporte"               │  → email/chat soporte
│                                     │
└─────────────────────────────────────┘
```

### Tokens usados (todos S11)

```
Ilustraciones: SVG estilo lineal, trazos onSurfaceVariant (#45464C)
Fondos: surface (#F8F9FB) — mismo fondo general
Error icon: error (#BA1A1A)
Skeleton bg: surfaceContainerHigh (#E7E8EA)
Skeleton shimmer: white 30% sweep
Botones: GradientButton (primario), OutlineButton (secundario)
```

### Brook implementation notes

```
Widgets:
  - SkeletonCard (props: width, height, radius)
  - SkeletonListItem
  - ErrorView (props: type enum, onRetry callback, onSecondary callback)
    type enum: notFound, networkError, tryOnFailed, generic

ErrorView renderiza condicionalmente la ilustracion correcta.

Ilustraciones SVG (assets/illustrations/):
  - error_404.svg
  - error_network.svg
  - error_tryon.svg

Usar package: shimmer ^3.0.0 para skeleton animation
```

---

---

# WAVE 2 — LUN-JUE (D1-D5 ready)

---

## S05 — My Wardrobe (Closet Digital)

**Descripcion:** Galeria de prendas del usuario. Patron hybrid: upload directo prominente + grid de wardrobe (D2 aprobada).

### Header + filtros

```
┌─────────────────────────────────────┐
│  "Mi Closet"             [+ Añadir] │  h2 (32px Inter 600) + IconButton
│  [AI Fit Check — Asesor de Imagen]  │  labelCaps, onSurfaceVariant
│                                     │  [+] → GradientButton circle 40px
│                                     │
│  FILTROS HORIZONTALES (scrollable):  │  ScrollRow, altura 36px
│  [Todos] [Tops] [Pantalones]         │  chips filtrables, scroll horizontal
│  [Vestidos] [Zapatos] [Accesorios]  │
│                                     │  Chip activo: bg secondaryContainer
│  Chip activo:                       │  (#2170E4), texto onSecondaryContainer
│    bg: secondaryContainer #2170E4   │  (#FEFCFF), radius full
│    text: onSecondaryContainer       │
│    radius: full                     │  Chip inactivo: bg surfaceContainer
│  Chip inactivo:                     │  (#EDEEF0), texto onSurfaceVariant
│    bg: surfaceContainer #EDEEF0     │  radius full
│    text: onSurfaceVariant           │
│                                     │
```

### Grid de prendas

```
│  GRID 2 COLUMNAS (mobile):          │  GridView.count(crossAxisCount: 2)
│                                     │  mainAxisSpacing: 12px
│  ┌───────────────┐ ┌──────────────┐ │  crossAxisSpacing: 12px
│  │               │ │              │ │  padding lateral: 24px
│  │  [Imagen      │ │  [Imagen     │ │
│  │   prenda]     │ │   prenda]    │ │  Cada card:
│  │  aspect 1:1   │ │  aspect 1:1  │ │  - aspect ratio 1:1
│  │  object-cover │ │  object-cover│ │  - radius md (12px)
│  │               │ │              │ │  - shadow ambient1
│  │  [categoria]  │ │  [categoria] │ │  - badge categoria: labelCaps
│  │  labelCaps    │ │  labelCaps   │ │    bg surfaceContainer, bottom
│  │  bottom-left  │ │  bottom-left │ │    padding 4px 8px
│  │         [⋮]   │ │         [⋮] │ │  - menu ⋮: top-right 32px circle
│  └───────────────┘ └──────────────┘ │    opciones: Editar, Usar en Try-On,
│                                     │    Eliminar (error color)
│  (continua con mas prendas...)      │
│                                     │
```

### Estado vacio

```
│  ESTADO VACIO:                      │  cuando wardrobe vacio
│                                     │
│  [Ilustracion: perchas vacias,      │  SVG 200x180px
│   closet organizado pero vacio]     │  centrada en screen
│                                     │
│  "Tu closet esta vacio"             │  h3, onSurface, centrado
│                                     │
│  "Agrega tus primeras prendas       │  bodyMd, onSurfaceVariant
│   para crear outfits increibles"    │  centrado
│                                     │
│  ╔═════════════════════════════╗    │  GradientButton
│  ║  + Añadir primera prenda   ║    │  margin-top: 32px
│  ╚═════════════════════════════╝    │
│                                     │
```

### Modal: Añadir prenda

```
BOTTOM SHEET MODAL (BottomSheet, radius xl top corners):
  Handle: 4px x 32px, color: outlineVariant, centrado, margin-top: 12px

  h3: "Nueva Prenda"
  onSurface, margin-top: 16px, margin-lateral: 24px

  UploadZone mini (height: 200px):
    borde 2px dashed outlineVariant
    icono: camera_alt 32px, color outline
    texto: "Foto de la prenda"

  --- Campos opcionales (todos) ---
  Label: labelCaps "Categoria"
  Select/DropdownButton:
    opciones: Tops, Pantalones, Vestidos, Zapatos, Accesorios, Otro
    bg: surfaceContainerLow, radius lg, border outlineVariant

  Label: labelCaps "Talla"
  TextInput: radius lg, border outlineVariant
  placeholder: "XS, S, M, L, XL o numerico"

  Label: labelCaps "Marca" (opcional)
  TextInput: mismo estilo

  ╔═════════════════════════════╗  GradientButton
  ║  Guardar prenda            ║  margin-top: 24px
  ╚═════════════════════════════╝  Disabled si no hay foto

  Boton cancelar: TextButton, onSurfaceVariant, "Cancelar"
```

### Tokens usados

```
grid gap:       12px
card radius:    md = 12px
card shadow:    ambient1
badge bg:       surfaceContainer (#EDEEF0)
badge text:     onSurfaceVariant (#45464C)
chip activo:    secondaryContainer (#2170E4) / onSecondaryContainer (#FEFCFF)
chip inactivo:  surfaceContainer (#EDEEF0) / onSurfaceVariant (#45464C)
modal radius:   xl = 24px (top corners)
```

### Brook implementation notes

```
Widgets:
  - WardrobeScreen (con FutureBuilder, GET /wardrobe/items)
  - WardrobeCard (props: item WardrobeItem, onTap, onMenu)
  - WardrobeFilterBar (props: selected String, onChange callback)
  - AddWardrobeItemBottomSheet (DraggableScrollableSheet)
  - WardrobeEmptyState

GridView paginated: page size 20, infinite scroll con footer loader
Menu ⋮: PopupMenuButton (Editar, Usar en Try-On, Eliminar)
Eliminar: mostrar AlertDialog de confirmacion antes de DELETE
```

---

## S08 — Collections (Looks guardados)

**Descripcion:** Grid de outfits generados y guardados. Boton Share prominente per D5.

```
┌─────────────────────────────────────┐
│  "Mis Looks"                        │  h2 (32px Inter 600)
│  [AI Fit Check — Asesor de Imagen]  │  labelCaps, onSurfaceVariant
│                                     │
│  FILTROS:                           │
│  [Recientes] [Favoritos]            │  2 chips, mismo estilo que S05
│                                     │
│  GRID 2 COLUMNAS (masonry visual):  │  GridView 2 cols, crossAxisSpacing 12px
│                                     │  Usar aspecto 3:4 para portrait feel
│  ┌─────────────┐ ┌─────────────┐   │
│  │             │ │             │   │  Card look:
│  │  [imagen    │ │  [imagen    │   │  - radius lg (16px)
│  │   resultado │ │   resultado │   │  - shadow ambient1
│  │   try-on]   │ │   try-on]   │   │  - aspecto 3:4 (portrait)
│  │  3:4 ratio  │ │  3:4 ratio  │   │  - overlay gradient bottom
│  │             │ │             │   │    (transparent → black 60%)
│  │  [fecha]    │ │  [fecha]    │   │  - fecha: labelCaps, white, bottom-left
│  │  [AI chip]  │ │  [AI chip]  │   │  - AIInsightChip: bottom, snippet
│  │             │ │             │   │
│  │  [Compartir]│ │  [Compartir]│   │  - Boton Compartir: bottom-right
│  └─────────────┘ └─────────────┘   │    circle 36px, bg white 80%
│                                     │    icono: share, color secondary
│                                     │
│  (mas looks...)                     │
│                                     │
```

### Estado vacio

```
│  ESTADO VACIO:                      │
│                                     │
│  [Ilustracion: camara + estrella,   │  SVG 200x180px centrada
│   "aun no tienes looks"]            │
│                                     │
│  "Aun no tienes looks guardados"    │  h3, onSurface
│                                     │
│  "Crea tu primer look con           │  bodyMd, onSurfaceVariant
│   Virtual Try-On"                   │
│                                     │
│  ╔═════════════════════════════╗    │  GradientButton
│  ║  ✨ Crear mi primer look   ║    │  → navegar a Tab Try-On
│  ╚═════════════════════════════╝    │
│                                     │
```

### Detalle de look (on tap card)

```
FULL SCREEN MODAL (DraggableScrollableSheet o push route):

  [← Cerrar] "Detalle del Look"

  [Imagen grande resultado]           aspect 3:4, full width, radius lg
  shadow ambient2

  [Chip AI] "Por que funciona"        AIInsightChip
  h3: titulo del look                 (fecha o descripcion corta)
  bodyMd: texto completo de AI insights

  --- ACCIONES ---
  ╔═══════════════╗  ╔════════════╗
  ║ ♥ Guardado    ║  ║ Compartir  ║  Dos botones iguales
  ╚═══════════════╝  ╚════════════╝  GradientButton + OutlineButton
  
  Compartir → bottom sheet seleccion plataforma (D5):
    [Instagram Stories] [WhatsApp] [Feed]
    + info de referido: "+1 try-on cuando tu amigo se una"
```

### Tokens usados

```
card aspect:    3:4 portrait
overlay:        LinearGradient transparent → black 60% (bottom 60% de la imagen)
fecha text:     white, labelCaps
share button:   circle 36px, white 80%, icono secondary (#0058BE)
AI chip:        snippet maximo 1 linea en card, texto completo en detalle
```

### Brook implementation notes

```
Widgets:
  - CollectionsScreen (GET /try-ons?liked=true)
  - LookCard (props: tryOn TryOnResult, onTap, onShare)
  - LookDetailSheet (BottomSheet o full route)
  - SharePlatformSheet (muestra Instagram Stories, WhatsApp, Feed)

D5 share flow:
  shareToInstagramStories() → Share.shareXFiles con imagen + deep link referral
  shareToWhatsApp() → WhatsApp intent con mensaje + link
  Track: PATCH /try-ons/{id} con shared=true, platform="instagram_stories"

Free tier: boton Compartir visible pero disabled
  → tap → navegar a S10 Paywall con mensaje "Compartir disponible en plan Estilo"
```

---

## S09 — Profile / Settings

**Descripcion:** Perfil del usuario con branding D1, plan badge D4, y acciones de configuracion.

```
┌─────────────────────────────────────┐
│                                     │  Status bar 59px
│  "Perfil"                           │  h2 (32px Inter 600)
│                                     │
│  ───────── HEADER PERFIL ─────────  │
│  ┌─────────────────────────────┐    │  Card perfil
│  │  [Avatar 80px circle]       │    │  bg: surfaceContainerLow
│  │  Iniciales o foto           │    │  radius: lg, padding: 24px
│  │  bg: primaryContainer       │    │  shadow: ambient1
│  │  (#141B2B), texto: white    │    │
│  │                             │    │
│  │  h3: "Juan Camilo Gil"      │    │  h3 (24px), onSurface
│  │  bodyMd: email del usuario  │    │  bodyMd, onSurfaceVariant
│  │                             │    │
│  │  [Plan Badge]               │    │  PlanBadge component:
│  │  FREE: bg surfaceContainer  │    │  Free: bg surfaceContainer, texto onSurfaceVariant
│  │  ESTILO: bg secondaryFixed  │    │  Estilo: bg secondaryFixed (#D8E2FF), texto secondary
│  │  IMAGEN: bg tertiaryFixed   │    │  Imagen: bg tertiaryFixed (#E9DDFF), texto #9466FF
│  │  labelCaps, radius full     │    │
│  │                             │    │
│  │  [Boton: "Mejorar Plan"]    │    │  GradientButton small
│  │  visible solo si es Free    │    │  → navegar a S10
│  └─────────────────────────────┘    │
│                                     │
│  ─── BRANDING (D1) ───────────────  │  margin-top: 24px
│  ┌─────────────────────────────┐    │
│  │  [Logo AI Fit Check small]  │    │  Logo 24px height
│  │  "AI Fit Check"             │    │  labelCaps, onSurface
│  │  "Tu Asesor de Imagen       │    │  bodyMd, onSurfaceVariant
│  │   Confiable"                │    │
│  └─────────────────────────────┘    │  Card sutil, no sombra
│                                     │
│  ─── CONFIGURACION ───────────────  │  margin-top: 24px
│  Lista de opciones (ListTile style):│
│                                     │
│  [ic: notifications] Notificaciones │  onSurface h-48px
│                          [toggle]   │  toggle right (secondary color)
│                                     │
│  [ic: language] Idioma              │  onSurface
│                          Español >  │  chevron right
│                                     │
│  [ic: privacy_tip] Privacidad       │  onSurface → external link
│                               >     │
│                                     │
│  [ic: description] Terminos         │  onSurface → external link
│                               >     │
│                                     │
│  [ic: star_outline] Calificar app   │  onSurface → app store
│                               >     │
│                                     │
│  ─────────────────────────────────  │  divider outlineVariant
│                                     │
│  [ic: logout] "Cerrar sesion"       │  error (#BA1A1A)
│                               >     │  → AlertDialog confirmacion
│                                     │
│  Version: "v1.0.0 — AI Fit Check"  │  caption 12px, onSurfaceVariant
│                                     │  centrado, bottom
│                                     │
└─────────────────────────────────────┘
```

### Tokens usados

```
avatar bg:          primaryContainer (#141B2B)
avatar text:        white (inverseOnSurface)
plan badge Free:    bg surfaceContainer, text onSurfaceVariant
plan badge Estilo:  bg secondaryFixed (#D8E2FF), text secondary (#0058BE)
plan badge Imagen:  bg tertiaryFixed (#E9DDFF), text onTertiaryContainer (#9466FF)
logout text:        error (#BA1A1A)
toggle active:      secondary (#0058BE)
divider:            outlineVariant (#C6C6CD), height 1px
lista row height:   48px
```

### Brook implementation notes

```
Widgets:
  - ProfileScreen (GET /users/me)
  - PlanBadge (props: plan enum: free/estilo/imagen)
  - ProfileSettingTile (props: icon, label, trailing widget)

Avatar: si el user no tiene foto, mostrar iniciales (first + last char del nombre)
  Generar con CustomPainter o usar CircleAvatar con Text

Logout: AlertDialog("Cerrar sesion?", "Perderas tu sesion actual")
  Confirmar → DELETE token → Navigator.pushAndRemoveUntil(LoginScreen)

Toggle notificaciones: SharedPreferences local + POST /users/me (notifications: bool)
```

---

## S10 — Paywall / Upgrade to Pro

**Descripcion:** Pantalla de tres tiers (D4 aprobada). Objetivo: conversion Free → Estilo o Imagen.

```
┌─────────────────────────────────────┐
│                                     │
│  ─── HEADER GRADIENTE ────────────  │  Container 200px height
│  ┌─────────────────────────────┐    │  bg: gradient primaryGradient
│  │                             │    │  (135deg #0058BE → #9466FF)
│  │  [crown icono 40px]         │    │  icono centrado, color white
│  │  h2: "Desbloquea            │    │  h2 white, centrado
│  │   tu potencial"             │    │
│  │                             │    │
│  │  [Badge social proof]       │    │  bg white 20%, radius full
│  │  "+50K usuarios activos"    │    │  labelCaps white
│  │                             │    │
│  └─────────────────────────────┘    │
│                                     │
│  ─── TIERS ───────────────────────  │  margin-top: -24px (overlap con header)
│                                     │  3 cards con z-index correcto
│                                     │
│  ── CARD FREE (atenuada) ─────────  │
│  ┌─────────────────────────────┐    │  bg: surfaceContainerLow
│  │  "FREE"         labelCaps   │    │  radius: lg, padding: 20px
│  │                             │    │  border: 1px outlineVariant
│  │  "1 try-on / dia"      ✓   │    │
│  │  "Preview 480p"         ✓   │    │  checkmarks: onSurface para free
│  │  "Sin compartir"        ✗   │    │  X: onSurfaceVariant 40% opacity
│  │  "1 coleccion max"      ✗   │    │
│  │                             │    │
│  │  h2: "Gratis"              │    │  precio centrado
│  │  "Tu plan actual"          │    │  labelCaps, onSurfaceVariant
│  └─────────────────────────────┘    │
│                                     │
│  ── CARD ESTILO (destacada) ──────  │  margin-top: 12px
│  ┌─────────────────────────────┐    │  bg: surfaceContainerLowest (#FFF)
│  │  [Badge "POPULAR"]         │    │  border: 2px solid secondary (#0058BE)
│  │  labelCaps, bg secondary   │    │  radius: lg, shadow: ambient2
│  │  text white, radius full   │    │
│  │                             │    │
│  │  "ESTILO"       labelCaps  │    │
│  │                             │    │
│  │  "5 try-ons / dia"     ✓   │    │  checkmarks: secondary (#0058BE)
│  │  "Calidad 1080p"       ✓   │    │
│  │  "Compartir IG Stories ✓   │    │
│  │  "10 colecciones"      ✓   │    │
│  │  "Soporte 24h"         ✓   │    │
│  │                             │    │
│  │  h2: "$9.99"               │    │  precio prominente, onSurface
│  │  "/ mes"  bodyMd           │    │  onSurfaceVariant
│  │                             │    │
│  │  ╔═══════════════════════╗ │    │  GradientButton dentro de card
│  │  ║ Empezar con Estilo   ║ │    │
│  │  ╚═══════════════════════╝ │    │
│  └─────────────────────────────┘    │
│                                     │
│  ── CARD IMAGEN ──────────────────  │  margin-top: 12px
│  ┌─────────────────────────────┐    │  bg: primaryContainer (#141B2B)
│  │  "IMAGEN"       labelCaps  │    │  (dark card para premium feel)
│  │  text: onPrimaryContainer  │    │  radius: lg, shadow: ambient2
│  │  (#7D8497)                  │    │
│  │                             │    │
│  │  "Ilimitado / dia"     ✓   │    │  checkmarks: inversePrimary (#C0C6DB)
│  │  "Calidad 2K"          ✓   │    │  texto: onPrimaryContainer (#7D8497)
│  │  "Sin marca de agua"   ✓   │    │
│  │  "Colecciones ilimit." ✓   │    │
│  │  "Exportar para apps"  ✓   │    │
│  │  "Soporte 2h"          ✓   │    │
│  │  "Sin anuncios"        ✓   │    │
│  │                             │    │
│  │  h2: "$19.99"              │    │  blanco / inversePrimary
│  │  "/ mes"                   │    │
│  │                             │    │
│  │  ╔═══════════════════════╗ │    │  Boton blanco sobre fondo oscuro
│  │  ║ Ir a Imagen           ║ │    │  bg white, text primary (#000)
│  │  ╚═══════════════════════╝ │    │
│  └─────────────────────────────┘    │
│                                     │
│  "Cancela cuando quieras.           │  bodyMd, onSurfaceVariant, centrado
│   Sin compromisos."                 │  margin-top: 16px
│                                     │
│  "Precios en USD. IVA puede         │  caption 12px, onSurfaceVariant
│   aplicar segun tu pais."           │  centrado
│                                     │
└─────────────────────────────────────┘
```

### Tokens usados

```
header:         primaryGradient (135deg #0058BE → #9466FF)
card free:      surfaceContainerLow, border outlineVariant
card estilo:    surfaceContainerLowest, border 2px secondary (#0058BE)
  badge popular: bg secondary, text white
card imagen:    primaryContainer (#141B2B), dark theme
  texto:        onPrimaryContainer (#7D8497)
  checkmarks:   inversePrimary (#C0C6DB)
  boton:        bg white, text primary (#000)
precios:        h2 (32px Inter 600)
badge popular:  radius full, labelCaps, bg secondary
```

### Brook implementation notes

```
Widget: PaywallScreen
Props: trigger String? (de donde viene: try_on_limit, share_attempt, etc.)

Si trigger = "try_on_limit" → mostrar banner arriba:
  "Agotaste tu try-on del dia. Mejora para continuar."
  bg errorContainer (#FFDED6), text onErrorContainer (#93000A)

Si trigger = "share_attempt" → mostrar banner:
  "Compartir disponible desde el plan Estilo"

Botones de compra:
  → POST /subscriptions/stripe/checkout (tierId: "estilo" o "imagen")
  → Recibe checkout_url → launch(checkout_url) en WebView o browser
  
On return del pago:
  → GET /users/me para verificar nuevo plan
  → dismiss paywall, mostrar celebracion (Lottie confetti o simple snackbar)
```

---

---

# WAVE 3 — JUE-SAB (Completar set)

---

## S01 — Splash / Onboarding (3 slides)

**Descripcion:** Primera impresion de la app. 3 slides que comunican el valor sin friccion. Logo "AI Fit Check" + tagline.

### Splash inicial (500ms, autoskip)

```
┌─────────────────────────────────────┐
│                                     │
│          [fondo blanco]             │  bg: surface (#F8F9FB)
│                                     │
│          [Logo AI Fit Check]        │  centrado vertical + horizontal
│          h2 Inter 600, onSurface    │  "AI Fit Check"
│                                     │
│          "Tu Asesor de Imagen       │  bodyMd, onSurfaceVariant
│           Confiable"                │  centrado
│                                     │
│          [spinner 16px secondary]   │  loading minimo, color secondary
│                                     │
└─────────────────────────────────────┘
```

Auto-redirect: 500ms → si JWT valido → Home, si no → Onboarding slide 1

### Onboarding Slide 1 — "Verte sin probarte"

```
┌─────────────────────────────────────┐
│                                     │  bg: surface (#F8F9FB)
│                                     │
│  [Hero ilustracion: figura          │  ilustracion SVG 280x320px
│   femenina con overlay IA,          │  arriba (60% del screen)
│   ropa flotando alrededor,          │  estilo lineal + toque de
│   trazos de luz azul→violeta]       │  gradiente en los trazos de luz
│                                     │
│  ────────────────────────────────   │  padding inferior 48px
│                                     │
│  h2: "Verte sin probarte"           │  h2 (32px Inter 600), onSurface
│                                     │  padding lateral 32px
│                                     │
│  bodyMd: "Prueba outfits completos  │  bodyMd, onSurfaceVariant
│   impulsados por IA — sin salir de  │  padding lateral 32px, margin-top 12px
│   casa."                            │
│                                     │
│  ● ○ ○   [Siguiente →]             │  dots izquierda + boton derecha
│           OutlineButton pill        │  margin-bottom: 48px
│                                     │
│  Dot activo: gradient stroke 2px   │  dot 8px diameter, activo con gradient
│  Dot inactivo: outlineVariant       │  inactivo: outlineVariant, 6px
│                                     │
└─────────────────────────────────────┘
```

### Onboarding Slide 2 — "Vestirte mejor"

```
┌─────────────────────────────────────┐
│                                     │
│  [Hero ilustracion: closet          │  SVG 280x300px
│   organizado con prendas            │  estilo similar al slide 1
│   por colores, brillos sutiles]     │
│                                     │
│  h2: "Vestirte mejor               │  h2, onSurface
│       sin gastar mas"               │
│                                     │
│  bodyMd: "Saca el maximo a lo que  │  bodyMd, onSurfaceVariant
│   ya tienes. Tu IA personal         │
│   combina lo que ya posees."        │
│                                     │
│  ○ ● ○   [Siguiente →]             │  dots + boton
│                                     │
└─────────────────────────────────────┘
```

### Onboarding Slide 3 — "Conocete estilisticamente"

```
┌─────────────────────────────────────┐
│                                     │
│  [Hero ilustracion: paleta de       │  SVG 280x300px
│   colores personal, silueta         │  colores del gradiente Aether
│   con puntos de color correctos]    │  en la paleta
│                                     │
│  h2: "Conoce tu estilo              │  h2, onSurface
│       personal"                     │
│                                     │
│  bodyMd: "Descubre tu tipo de       │  bodyMd, onSurfaceVariant
│   cuerpo y temporada de color.      │
│   Recomendaciones que funcionan."   │
│                                     │
│  ○ ○ ●   [Comenzar gratis →]       │  ultimo dot + CTA final
│                                     │
│  GradientButton pill (full width)   │  GradientButton en slide 3
│  "Comenzar gratis"                  │  reemplaza OutlineButton
│                                     │
│  Link: "Ya tengo cuenta →"          │  TextButton, onSurfaceVariant
│                                     │  → navegar a S02 Login
│                                     │
└─────────────────────────────────────┘
```

### Animaciones Onboarding

```
Transicion entre slides: slide horizontal (PageView flutter)
  Duration: 300ms, Curves.easeInOut

Hero ilustracion:
  Page enter: scale 0.85 → 1.0, opacity 0 → 1
  Duration: 400ms, Curves.easeOut

Texto:
  Enter: slide up 16px + opacity 0 → 1
  Delay: 150ms despues del hero
  Duration: 300ms

Dot cambio:
  Animated: width expand (6px → 24px pill)
  Color: animated a gradient
  Duration: 200ms
```

---

## S02 — Login

```
┌─────────────────────────────────────┐
│                                     │  bg: surface (#F8F9FB)
│                                     │  padding-top: 80px
│  [Logo AI Fit Check]                │  logo centrado, h3 Inter 600
│  "AI Fit Check"                     │  onSurface
│  "Tu Asesor de Imagen Confiable"    │  bodyMd, onSurfaceVariant
│                                     │  margin-bottom: 48px
│                                     │
│  ── FORMULARIO ──────────────────  │
│  Label: labelCaps "EMAIL"           │  labelCaps, onSurfaceVariant
│  ┌─────────────────────────────┐   │  Input:
│  │  [ic: mail_outline] email   │   │  radius: lg (16px)
│  │                             │   │  bg: surfaceContainerLow
│  └─────────────────────────────┘   │  border: 1px outlineVariant
│                                     │  icono prefijo: onSurfaceVariant
│  Label: labelCaps "CONTRASENA"     │  margin-top: 16px
│  ┌─────────────────────────────┐   │
│  │  [ic: lock_outline]  ****   │   │  boton suffix: visibility_off
│  │                  [ojo icon] │   │  → toggle password visible
│  └─────────────────────────────┘   │
│                                     │
│  Input focus state:                 │  border → secondary (#0058BE)
│  Input error state:                 │  border → error (#BA1A1A)
│  Input error text:                  │  caption, error color, bajo input
│                                     │
│  Link: "¿Olvidaste tu contrasena?" │  TextButton, secondary, alineado right
│                                     │  margin-top: 4px
│                                     │
│  ╔═════════════════════════════╗   │  GradientButton pill full width
│  ║  Iniciar sesion             ║   │  margin-top: 24px
│  ╚═════════════════════════════╝   │
│                                     │
│  ─── DIVIDER ─────────────────────  │
│           ── o continua con ──      │  divider + texto, onSurfaceVariant
│                                     │  margin vertical: 24px
│                                     │
│  ┌─────────────────────────────┐   │  Google Sign-In button
│  │  [G logo 20px]              │   │  OutlineButton, full width
│  │  Continuar con Google       │   │  radius: lg, border: outlineVariant
│  └─────────────────────────────┘   │  bg: white
│                                     │
│  "No tienes cuenta?                 │  bodyMd centrado, onSurfaceVariant
│   [Crear cuenta]"                   │  link: secondary color
│                                     │
└─────────────────────────────────────┘
```

### Estados de inputs

```
Default:     border 1px outlineVariant (#C6C6CD)
Focus:       border 2px secondary (#0058BE)
Error:       border 2px error (#BA1A1A) + helper text error
Filled OK:   border 1px outline (#76777D) + checkmark suffix verde
Disabled:    bg surfaceContainerHighest, opacity 0.6
```

---

## S03 — Register

```
┌─────────────────────────────────────┐
│  [← Atras]                          │  back button top-left
│                                     │
│  h2: "Crear cuenta gratis"          │  h2 (32px Inter 600), onSurface
│  "AI Fit Check — Asesor de Imagen"  │  labelCaps, onSurfaceVariant
│                                     │  margin-bottom: 32px
│                                     │
│  Label: "NOMBRE COMPLETO"           │  labelCaps
│  [ic: person] Input nombre          │  mismo estilo que S02
│                                     │
│  Label: "EMAIL"                     │
│  [ic: mail] Input email             │
│                                     │
│  Label: "CONTRASENA"               │
│  [ic: lock] Input password          │  min 10 chars, validacion live
│  [ojo toggle]                       │
│                                     │
│  Helper password:                   │  helper text bajo input
│  "Minimo 10 caracteres, 1 letra     │  caption, onSurfaceVariant
│   y 1 numero"                       │  → verde si ok, rojo si error
│                                     │
│  Indicator strength bar:            │  4 segmentos (1=debil, 4=fuerte)
│  ■ □ □ □  Debil                    │  colores: error / warning / ok / success
│                                     │
│  ┌─── Checkbox + texto ─────────┐  │  CheckboxListTile
│  │  [□] Acepto los              │  │  checkbox: secondary al marcar
│  │       Terminos y Condiciones │  │  link: secondary underline
│  │       y Politica de          │  │
│  │       Privacidad             │  │
│  └──────────────────────────────┘  │
│                                     │
│  ╔═════════════════════════════╗   │  GradientButton pill full width
│  ║  Crear cuenta gratis        ║   │  Disabled: si no todos los campos
│  ╚═════════════════════════════╝   │  completos + checkbox marcado
│                                     │
│  "Ya tienes cuenta?                 │  bodyMd centrado
│   [Iniciar sesion]"                 │  link: secondary
│                                     │
└─────────────────────────────────────┘
```

---

## S04 — Virtual Try-On (pantalla completa)

**Nota:** La referencia visual existe en `stitch_ai_fit_check_ui.zip`. Este documento especifica los 3 sub-estados completos incluyendo D2, D3, D5.

### Estado A — Upload

```
┌─────────────────────────────────────┐
│  "Virtual Try-On"                   │  h2 (32px Inter 600)
│  "AI Fit Check — Asesor de Imagen"  │  labelCaps, onSurfaceVariant
│                                     │
│  bodyMd: "Descubre tu mejor         │  onSurfaceVariant, margin-top: 8px
│           combinacion con IA"        │
│                                     │
│  ─── TU FOTO ─────────────────────  │
│  h3: "Tu Foto"                      │  h3 (24px), onSurface
│                                     │
│  [UploadZone grande]                │  min-height: 280px (mobile)
│  2px dashed outlineVariant          │  radius lg (16px)
│  icono: photo_camera 36px           │  bg: surfaceContainerLowest
│  "Sube tu foto"                     │  h3 centrado, onSurface
│  "(de frente y buena luz)"          │  bodyMd, onSurfaceVariant
│                                     │
│  ─── TU ROPA ─────────────────────  │  margin-top: 24px
│  h3: "Tu Ropa" + badge "Max 5"      │  h3 + badge labelCaps bg surfaceContainer
│                                     │
│  Grid 2 columnas ClothingSlots:     │  GridView 2 cols, aspect 1:1
│  [+] [+]                            │  slots vacios: dashed border + icono add
│  [+] [+]                            │  slots llenos: imagen + boton X
│                                     │
│  Tap slot vacio → BottomSheet:      │  opciones: Desde Mi Closet / Subir Foto
│    [Desde Mi Closet]                │  (D2 hybrid: closet disponible)
│    [Subir nueva foto]               │
│                                     │
│  ─── D3: SOFT CTA ANALISIS ───────  │  visible si user sin body_analysis
│  ┌─────────────────────────────┐   │  Card sutil
│  │  [ic: auto_awesome]         │   │  bg: primaryFixed (#DCE2F7)
│  │  "Mejores combos con tu     │   │  radius: md (12px), padding: 16px
│  │   analisis de cuerpo"       │   │  bodyMd, onSurface
│  │  [Analizar →] [Saltar]      │   │  dos TextButtons
│  └─────────────────────────────┘   │
│                                     │
│  ╔═════════════════════════════╗   │  GradientButton full width pill
│  ║  ✨ Generar Outfit Ideal    ║   │  Disabled si no hay foto personal
│  ╚═════════════════════════════╝   │
│                                     │
│  Free tier counter:                 │  labelCaps, onSurfaceVariant, centrado
│  "1 de 1 try-on disponible hoy"    │  visible si free tier (D4)
│                                     │
└─────────────────────────────────────┘
```

### Estado C — Resultado

```
┌─────────────────────────────────────┐
│  h2: "Tu Look"                      │  centrado
│                                     │
│  [Imagen resultado IA]              │  full width (gutter 24px)
│  ratio 2:3 (portrait)               │  radius lg, shadow ambient2
│                                     │
│  [Chip AI] "Por que funciona"       │  AIInsightChip, margin-top: 16px
│                                     │
│  Card resultado:                    │  bg: surfaceContainerLow
│  bodyMd: texto explicacion IA       │  radius lg, padding 24px, shadow ambient1
│                                     │
│  ─── ACCIONES ────────────────────  │  margin-top: 24px
│  ╔═════════════╗  ╔══════════════╗ │  dos botones lado a lado
│  ║ ♥ Guardar  ║  ║ 📤 Compartir ║ │  GradientButton + OutlineButton
│  ╚═════════════╝  ╚══════════════╝ │
│                                     │
│  Compartir (D5):                    │  Free tier: Compartir → Paywall
│  → bottom sheet plataforma          │  Estilo/Imagen: native share
│    Instagram Stories / WhatsApp    │
│    / Feed                          │
│                                     │
│  [Nuevo Try-On]                     │  TextButton, secondary, centrado
│  → volver a Estado A               │  margin-top: 16px
│                                     │
└─────────────────────────────────────┘
```

---

---

# COMPONENT LIBRARY — Inventario

## Atoms (base)

| Componente | Descripcion | Tokens clave |
|------------|-------------|--------------|
| `GradientButton` | Pill azul→violeta, icono opcional | gradient, radius full, shadow ambient2 |
| `OutlineButton` | Borde 1px primary negro | border primary, radius lg, text onSurface |
| `SolidButton` | Bg negro | primary, onPrimary, radius lg |
| `TextButton` | Solo texto | secondary o onSurface |
| `Input` | Texto, con icono prefix/suffix, estados | radius lg, focus secondary, error error |
| `AIInsightChip` | Pill violeta "AI Insights" | tertiaryFixed, onTertiaryContainer |
| `PlanBadge` | Free / Estilo / Imagen | ver tokens S09 |
| `ColorSwatch` | Circulo color + hex | radius full, 32px |
| `FilterChip` | Activo/inactivo en scrollrow | ver tokens S05 |

## Molecules (compuestos)

| Componente | Descripcion | Pantallas |
|------------|-------------|-----------|
| `UploadZone` | Area dashed con estados vacio/filled/hover | S04, S07 |
| `ClothingSlot` | Grid slot cuadrado aspect 1:1 | S04 |
| `WardrobeCard` | Card prenda con badge + menu | S05 |
| `LookCard` | Card resultado 3:4 portrait con overlay | S08 |
| `AIInsightCard` | Card "Por que funciona" | S04C, S08 |
| `GradientLoaderCard` | Shimmer pulsante + textos rotativos | S04B |
| `BodyTypeSilhouette` | SVG silueta por tipo de cuerpo | S06 |
| `ProfileSettingTile` | Row 48px con icono + label + trailing | S09 |
| `PaywallTierCard` | Card de tier (Free/Estilo/Imagen) | S10 |
| `OnboardingSlide` | Hero + titulo + bodyMd + dots + CTA | S01 |
| `SkeletonCard` | Shimmer placeholder | S11a |
| `ErrorView` | Ilustracion + titulo + CTA | S11b/c/d |
| `SharePlatformSheet` | BottomSheet plataformas D5 | S04C, S08 |

---

# ANIMATION REFERENCE — Specs para Brook

## Duraciones estandar

| Tipo | Duracion | Easing |
|------|----------|--------|
| Micro (feedback touch) | 100-150ms | easeOut |
| Transicion de estado | 200-300ms | easeInOut |
| Enter page / card | 300-400ms | easeOut |
| Shimmer loop | 1800ms | easeInOut PingPong |
| Texto rotativo | 5000ms intervalo / 300ms fade | linear |

## Shimmer GradientLoader (S04B)

```
AnimationController:
  vsync: this
  duration: 1800ms
  repeat (reverse: true)  -- PingPong

GradientAnimation via CurvedAnimation + TweenSequence:
  0%:   opacity azul 0.15, escala 1.00
  50%:  opacity violeta 0.35, escala 1.015
  100%: opacity azul 0.15, escala 1.00

NO usar Lottie para este componente — implementacion nativa Flutter mas eficiente.
Lottie solo si se necesita ilustracion animada compleja (como la de onboarding).
```

## Page transitions

```
Dentro de la app (NavigationBar tab switch):
  Fade: opacity 0 → 1, duration 200ms

Push (ir a pantalla nueva):
  Slide desde derecha: offset Offset(1.0, 0) → Offset(0, 0)
  Duration: 300ms, Curves.easeOut

Pop (volver):
  Slide hacia derecha: offset Offset(0, 0) → Offset(1.0, 0)
  Duration: 250ms, Curves.easeIn

Modal / BottomSheet:
  Slide desde abajo: Offset(0, 1) → Offset(0, 0)
  Duration: 350ms, Curves.easeOut
  Drag to dismiss: DraggableScrollableSheet
```

## Micro-interacciones

```
Boton tap (GradientButton, OutlineButton):
  Scale: 1.0 → 0.97 on tap down, 0.97 → 1.0 on tap up
  Duration: 100ms cada
  Via: GestureDetector con AnimatedScale

Upload Zone hover/active:
  Border color animated: outlineVariant → secondary
  Duration: 200ms AnimatedContainer

Clothing slot fill:
  Imagen entra con: FadeTransition opacity 0 → 1, 250ms

Card de resultado enter:
  SlideTransition + FadeTransition
  From: Offset(0, 0.1) + opacity 0
  To: Offset(0, 0) + opacity 1
  Duration: 400ms, Curves.easeOut

Heart button save:
  Scale pulse: 1.0 → 1.2 → 1.0
  Duration: 300ms, ElasticOutCurve
  Color: outline → error (#BA1A1A) filled
```

---

# QA CHECKLIST — Verificacion para Brook

Al implementar cada pantalla, verificar:

- [ ] Todos los colores de `AppColors` (ningun hardcode fuera del sistema)
- [ ] Tipografia de `AppTypography` (sin fontSize hardcodeado)
- [ ] Spacing de `AppSpacing` (multiples de 4px o 8px)
- [ ] Radius de `AppRadius` (sm/DEFAULT/md/lg/xl/full)
- [ ] Sombras de `AppShadows` (ambient1/ambient2)
- [ ] GradientButton solo en CTAs primarios (maximo 1 por pantalla visible)
- [ ] Gradiente NO en fondos de pantalla completa
- [ ] Touch targets minimo 44x44px (accesibilidad WCAG)
- [ ] Textos en onSurface / onSurfaceVariant (nunca hardcode gris)
- [ ] Error states diseñados (formularios, carga fallida)
- [ ] Empty states diseñados (listas vacias)
- [ ] Safe areas respetadas (top 59px, bottom 34px)
- [ ] D1: branding "AI Fit Check" visible en header de cada pantalla
- [ ] D4: free tier counter visible en S04
- [ ] D5: boton Compartir presente en S04C y S08

---

# ENTREGA A BROOK — SAB 25 mayo

## Protocolo de entrega

```markdown
## Entrega Erik — Sprint Design — 2026-05-25

### Figma
[Link al Figma con los 11 frames organizados por tab:]
  - Auth: S01, S02, S03
  - Try-On: S04, S04B
  - Wardrobe: S05
  - Style Insights: S06, S07
  - Collections: S08
  - Utilities: S09, S10, S11 (4 estados)

### Assets exportados
  - Iconos: Material Symbols Outlined (no assets personalizados)
  - Ilustraciones: assets/illustrations/ (SVG)
    - onboarding_slide_1.svg
    - onboarding_slide_2.svg
    - onboarding_slide_3.svg
    - body_type_pear.svg
    - body_type_rectangle.svg
    - body_type_inverted_triangle.svg
    - body_type_hourglass.svg
    - body_type_oval.svg
    - empty_wardrobe.svg
    - empty_collections.svg
    - error_404.svg
    - error_network.svg
    - error_tryon.svg

### Tokens de diseno
  Archivo: lib/core/theme/app_colors.dart (ya documentado en DESIGN_SYSTEM.md)
  NO hay cambios de tokens — usar DESIGN_SYSTEM.md como fuente de verdad

### Notas de implementacion
  Ver cada pantalla en este documento — seccion "Brook implementation notes"

### Ilustraciones prioritarias (encomendar a generacion IA o Illustrator)
  Prioridad 1: onboarding_slide_1.svg, error_network.svg, error_404.svg
  Prioridad 2: body_type_*.svg (5 archivos)
  Prioridad 3: empty_wardrobe.svg, empty_collections.svg, onboarding_slide_2.svg, onboarding_slide_3.svg

### QA Visual
  Usar la QA checklist al final de este documento.
  Para cada pantalla: screenshot del simulador vs spec en este doc.
  Si hay discrepancias > 8px en spacing o colores incorrectos → abrir issue.
```

---

**Ultima actualizacion:** 2026-05-18
**Sprint cierre:** 2026-05-25
**Fuente de verdad:** Este documento + `docs/design-system/DESIGN_SYSTEM.md`
