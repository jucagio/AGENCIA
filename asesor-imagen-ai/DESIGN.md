# DESIGN.md — AI Fit Check (Asesor de Imagen AI)
## Exportado de Stitch — Verificado 2026-05-21
## Fuente: https://stitch.withgoogle.com/projects/2365238704690249989

**Owner:** Erik (Diseño)
**Implementa:** Brook (Flutter)
**Design system:** Aether Luxe (aprobado por Juan Camilo Gil — 2026-05-18)
**Estado:** VERIFICADO — Stitch coincide 100% con captura objetivo de Juan Camilo

---

## VERIFICACION DE MATCH STITCH vs CAPTURA

| Elemento | Objetivo (captura JC) | Stitch actual | Match |
|----------|----------------------|---------------|-------|
| Sidebar nav | Virtual Try-On, My Wardrobe, Style Insights, Collections | Identico | 100% |
| "Tu Foto" upload zone | Icono camara + dashed border | Identico | 100% |
| "Tu Ropa" grid | Max 5, 2 columnas, slots + vacios | Identico | 100% |
| Boton CTA | "Generar Outfit Ideal" degradado azul-violeta | Identico con icono | 100% |
| "Tu Look" resultado | Imagen editorial generada | Imagen editorial hombre casual | 100% |
| "Por que funciona" | Analisis escrito IA | AI Insights chip + texto analisis | 100% |
| Acciones | Guardar + Compartir | Guardar + Compartir | 100% |
| Nombre app | AI Fit Check | AI Fit Check + "Virtual stylist" | 100% |
| Idioma UI | Espanol | Espanol (LATAM) | 100% |

**Conclusion:** El diseno en Stitch es un match exacto con la captura objetivo. No se requieren actualizaciones al proyecto Stitch.

---

## Colors

- Primary: #000000 (negro — tipografia y acciones primarias)
- OnPrimary: #FFFFFF
- PrimaryContainer: #141B2B
- Secondary: #0058BE (Electric Blue — CTAs e IA)
- OnSecondary: #FFFFFF
- SecondaryContainer: #2170E4
- OnSecondaryContainer: #FEFCFF
- Tertiary/Violet: #9466FF (AI features, chips)
- TertiaryFixed: #E9DDFF
- Error: #BA1A1A
- ErrorContainer: #FFDED6
- OnErrorContainer: #93000A
- Surface: #F8F9FB
- SurfaceContainerLowest: #FFFFFF
- SurfaceContainerLow: #F3F4F6
- SurfaceContainer: #EDEEF0
- SurfaceContainerHigh: #E7E8EA
- SurfaceContainerHighest: #E1E2E4
- OnSurface: #191C1E (texto principal)
- OnSurfaceVariant: #45464C (texto secundario)
- Outline: #76777D
- OutlineVariant: #C6C6CD
- Background: #F8F9FB

### Gradiente primario (USO EXCLUSIVO — CTA, loaders IA, borders activos)
- Tipo: LinearGradient
- Direccion: 135deg (top-left a bottom-right)
- Color 1: #0058BE (azul electrico)
- Color 2: #9466FF (violeta)
- Dart: `LinearGradient(begin: Alignment.topLeft, end: Alignment.bottomRight, colors: [Color(0xFF0058BE), Color(0xFF9466FF)])`

### Uso estricto del gradiente
- Boton "Generar Outfit Ideal" (CTA primario)
- Progress bar / shimmer en estados de carga IA
- Borde activo en UploadZone cuando hay drag over
- AI Insights chip border (opcional)
- NO usar en fondos de pantalla completa
- NO usar en texto normal
- NO usar como decoracion gratuita

---

## Typography

- Fuente: Inter (Google Fonts — `google_fonts: ^6.1.0`)
- h1: 48px, weight 600, height 1.1, letterSpacing -0.96
- h2: 32px, weight 600, height 1.2, letterSpacing -0.32
- h3: 24px, weight 500, height 1.3, letterSpacing -0.24
- bodyLg: 18px, weight 400, height 1.6
- bodyMd: 16px, weight 400, height 1.6
- labelCaps: 12px, weight 600, height 1.0, letterSpacing 0.6 (UPPERCASE)

---

## Spacing (base 4px)

- unit: 4px
- xs: 8px
- sm: 16px
- md: 24px
- lg: 32px
- xl: 64px
- gutter: 24px (padding lateral estandar en mobile)
- margin: 32px (margen entre secciones)

---

## Border Radius

- sm: 4px (inputs minimos)
- DEFAULT: 8px (radio estandar)
- md: 12px (cards pequenas, wardrobe slots)
- lg: 16px (cards principales, inputs, upload zones)
- xl: 24px (modales, bottom sheets)
- full: 9999px (pills, chips, botones CTA)

---

## Shadows

- ambient1: `BoxShadow(color: Color(0x0A000000), blurRadius: 10, offset: Offset(0, 4))`
- ambient2: `BoxShadow(color: Color(0x14000000), blurRadius: 25, offset: Offset(0, 8))`

---

## Components

### GradientButton (CTA principal)
- Background: LinearGradient(135deg, #0058BE → #9466FF)
- Text: white, bodyLg (18px), fontWeight 600
- Height: 48px (WCAG 2.1 AA tap target)
- PaddingH: 32px, PaddingV: 16px
- Radius: full (pill)
- Shadow: ambient2
- Icon: Icons.auto_awesome, 20px, white (a la derecha del texto)
- Disabled: opacity 0.4, sin gradient (surfaceContainerHighest)
- Tap feedback: scale 1.0 → 0.97 → 1.0, 100ms easeOut
- USO MAXIMO: 1 por pantalla visible simultaneamente

### OutlineButton (CTA secundario)
- Border: 1px solid #000000
- Text: AppTypography.labelCaps, color #191C1E
- Background: transparente
- Height: 48px
- Radius: lg (16px)
- Hover/focus: background surfaceVariant (#E1E2E4)

### SolidButton (boton primario negro)
- Background: #000000
- Text: white, labelCaps
- PaddingV: 12px
- Radius: lg (16px)

### UploadZone (foto personal S04 y body analysis S07)
- MinHeight: 280px (movil), expandible
- AspectRatio: 3/4 (portrait)
- Border: 2px dashed #C6C6CD (OutlineVariant)
- Background: #FFFFFF (SurfaceContainerLowest)
- Radius: lg (16px)
- Icon: Icons.photo_camera, 48px, color #76777D (outline)
- Text: "Sube tu foto (de frente y buena luz)" — bodyMd, onSurfaceVariant
- Shadow: ambient1
- Estado hover/drag: border → #0058BE, animado 200ms AnimatedContainer
- Estado filled: imagen BoxFit.cover + boton X circular top-right (32px, surface 80%)

### WardrobeSlot (grid slots S04)
- AspectRatio: 1:1 (square)
- Background vacio: SurfaceContainerLowest
- Border vacio: 1px dashed OutlineVariant
- Radius: md (12px)
- Icon "+": Icons.add, color outline (#76777D)
- Estado filled: imagen BoxFit.cover, Radius md
- Boton X: absoluto top-right, circular 32px, bg surface 80%
- Shadow: ambient1
- Grid: 2 columnas, gap 8px, max 5 slots

### AIInsightChip
- Background: #E9DDFF (tertiaryFixed)
- Text: #9466FF (onTertiaryContainer), labelCaps
- Icon: Icons.auto_awesome, 14px, same color
- PaddingH: 12px, PaddingV: 4px
- Radius: full (pill)

### AIInsightCard ("Por que funciona")
- Background: SurfaceContainerLow (#F3F4F6)
- Radius: lg (16px)
- Padding: md (24px)
- Shadow: ambient1
- Contenido: AIInsightChip + h3 titulo + bodyMd descripcion + botones accion
- Enter animation: opacity 0 + translateY +24px → visible, 400ms easeOut

### NavigationSidebar (desktop/tablet)
- Width: 240px
- Background: white
- Item activo: bg secondaryContainer (#2170E4), text white, radius xl (12px)
- Item inactivo: text onSurfaceVariant, hover bg surfaceVariant, radius xl
- Font: labelCaps (12px, uppercase)
- Icons: Material Symbols Outlined

### NavigationBar (mobile — bottom)
- Tabs: Try-On, Closet, Estilo, Looks
- Icons: auto_awesome / checkroom / person_search / collections
- Item activo: indicador secundario con gradient pill
- Background: white, shadow ambient1 top

---

## Screens

### S04 — Virtual Try-On (pantalla principal — REFERENCIA)
Esta es la pantalla que Juan Camilo mostro como objetivo visual.

#### Layout (mobile 390px)
```
┌──────────────────────────────────────┐  ← status bar 59px
│ AI Fit Check          [settings][?]  │  ← header 56px, labelCaps title
├──────────────────────────────────────┤
│ Virtual Try-On                       │  ← h2 titulo pagina
│ Descubre tu mejor combinacion...     │  ← bodyMd, onSurfaceVariant
├──────────────────────────────────────┤
│  Tu Foto               Tu Ropa Max 5 │  ← labels bodyMd/labelCaps
│  ┌──────────────┐  ┌────┐  ┌────┐   │
│  │              │  │img │  │ +  │   │  ← col 1: upload 3/4, col 2: grid 2x3
│  │  [camera]    │  └────┘  └────┘   │
│  │  Sube tu     │  ┌────┐  ┌────┐   │
│  │  foto        │  │ +  │  │ +  │   │
│  └──────────────┘  └────┘  └────┘   │
│                    ┌────┐  ┌────┐   │
│                    │ +  │  │ +  │   │
│                    └────┘  └────┘   │
├──────────────────────────────────────┤
│       [Generar Outfit Ideal ✨]       │  ← GradientButton full width
├──────────────────────────────────────┤
│ Tu Look                              │
│  ┌──────────────────────────────┐   │
│  │   [imagen editorial]         │   │  ← 16:9 o full width portrait
│  └──────────────────────────────┘   │
│  ✨ AI Insights                      │  ← AIInsightChip
│  Por que funciona                    │  ← h3
│  Este conjunto logra un equilibrio...│  ← bodyMd
│  ┌──────────┐  ┌───────────┐        │
│  │ Guardar  │  │ Compartir │        │  ← outline buttons
│  └──────────┘  └───────────┘        │
├──────────────────────────────────────┤
│ [nav] Try-On  Closet  Estilo  Looks  │  ← NavigationBar bottom 80px
└──────────────────────────────────────┘
```

#### Sub-estados de S04
1. **Estado Upload (default):** UploadZone vacia + slots wardrobe + CTA disabled si sin foto
2. **Estado Loading (S04B):** GradientLoaderCard 320px + progress bar + textos rotativos
3. **Estado Resultado (S04C):** imagen resultado + AIInsightCard + botones Guardar/Compartir

#### Flujo de interaccion
1. Usuario sube foto → UploadZone filled, CTA se habilita
2. Usuario selecciona prendas del wardrobe → slots filled (max 5)
3. Tap "Generar Outfit Ideal" → Estado Loading (S04B)
4. Polling GET /try-ons/{id} cada 3s → cuando done → Estado Resultado (S04C)
5. Tap "Guardar" → guarda en Collections (S08)
6. Tap "Compartir" → free: Paywall (S10) / paid: SharePlatformSheet

### S04B — Loading State
- GradientLoaderCard (320px height)
- Shimmer gradient animado: 1800ms PingPong
- Progress bar gradient 4px height
- Textos rotativos cada 5s: "Analizando proporciones...", "Combinando colores...", "Aplicando tu estilo...", "Casi listo..."
- Boton cancelar: OutlineButton, visible solo despues de 20s
- Duration total: max 45000ms

### S05 — My Wardrobe
- Header: "Mi Closet" + GradientButton circle 40px (icono +)
- Filtros scroll horizontal: Todos / Tops / Pantalones / Vestidos / Zapatos / Accesorios
- Grid 2 columnas, gap 12px, WardrobeCard aspect 1:1
- Empty state: empty_wardrobe.svg + GradientButton
- Add prenda: DraggableScrollableSheet desde abajo

### S06 — Style Insights + Soft Cap
- Estado sin analisis: 2 cards descriptivos + GradientButton "Iniciar analisis"
- Estado con analisis: ResultsAnalysisCard + SoftCapBottomSheet (delay 700ms)
- TryOnCounterPill siempre en header (free tier)

### S07 — Body Analysis Upload
- Igual a S04 upload pero con instrucciones extra
- UploadZone icono person, aspecto 3/4
- CTA: "Analizar mi figura"
- Loading: GradientLoaderCard 20000ms

### S08 — Collections (Looks guardados)
- Grid 2 columnas, LookCard aspecto 3:4 portrait
- Overlay gradient bottom + fecha + boton share
- Empty state: empty_collections.svg + GradientButton

### S09 — Profile / Settings
- CircleAvatar 80px + nombre + email + PlanBadge
- 6 ProfileSettingTile items
- Logout: AlertDialog confirmacion

### S10 — Paywall
- Header 200px con primaryGradient + crown icon
- 3 cards: Free (dim) / Estilo (highlighted) / Imagen (dark)
- Trigger banners segun origen (try_on_limit, share_attempt)

### S11 — Error States
- S11a: Skeleton shimmer (todas las pantallas en carga)
- S11b: 404 (error_404.svg)
- S11c: Sin conexion (error_network.svg)
- S11d: Try-On fallido (icono error_outline)

---

## Navigation (Flutter)

### Mobile (< 600dp) — NavigationBar bottom
```
Tab 0: Icons.auto_awesome → "Try-On"   → VirtualTryOnScreen
Tab 1: Icons.checkroom    → "Closet"   → WardrobeScreen
Tab 2: Icons.person_search → "Estilo"  → StyleInsightsScreen
Tab 3: Icons.collections  → "Looks"   → CollectionsScreen
```

### Tablet (>= 600dp) — NavigationRail lateral izquierdo
- Mismo orden, mismo contenido
- Width: 80px (iconos) o 240px (expanded con labels)

### Auth routes (sin NavigationBar)
- /splash → SplashScreen
- /onboarding → OnboardingScreen (3 slides PageView)
- /login → LoginScreen
- /register → RegisterScreen

### Push routes (sobre NavigationBar)
- /profile → ProfileScreen
- /paywall → PaywallScreen (requiere trigger param)
- /body-analysis → BodyAnalysisUploadScreen

---

## Animations

### Duraciones estandar
- Micro (touch feedback): 100-150ms, easeOut
- Transicion estado: 200-300ms, easeInOut
- Enter page/card: 300-400ms, easeOut
- Shimmer GradientLoader: 1800ms, PingPong easeInOut
- Texto rotativo: 5000ms interval / 300ms cross-fade
- Soft cap slide-up: 300ms, easeOut
- Counter numero: 200ms, AnimatedSwitcher

### Page transitions
- Tab switch: Fade opacity 0→1, 200ms
- Push: SlideTransition from Offset(1,0) → Offset(0,0), 300ms easeOut
- Pop: Offset(0,0) → Offset(1,0), 250ms easeIn
- Modal/BottomSheet: Offset(0,1) → Offset(0,0), 350ms easeOut

### Micro-interacciones clave
- Boton tap: scale 0.97, 100ms (onTapDown) / scale 1.0, 100ms (onTapUp)
- Heart save: scale 1.0→1.2→1.0, 300ms ElasticOutCurve
- UploadZone hover: border color 200ms AnimatedContainer
- Results card enter: opacity 0 + translateY +24 → visible, 400ms easeOut
- Counter cambio: AnimatedSwitcher, 200ms, fade + scale 0.8→1.0

---

## Assets necesarios

Ubicacion: `frontend/assets/illustrations/`
Estilo: lineal flat, trazos #45464C, sin shading, sin fotorrealismo

### Prioridad 1 (antes de primera entrega)
- error_network.svg — wifi cortado, nube rota, 200x180px
- error_404.svg — personaje con lupa, 240x200px

### Prioridad 2 (semana de entrega)
- body_type_pear.svg — silueta pera, 120x160px
- body_type_rectangle.svg
- body_type_inverted_triangle.svg
- body_type_hourglass.svg
- body_type_oval.svg

### Prioridad 3 (handoff final)
- empty_wardrobe.svg — perchas vacias, 200x180px
- empty_collections.svg — camara + estrella, 200x180px
- onboarding_slide_1.svg — figura femenina + overlay IA, 280x320px
- onboarding_slide_2.svg — closet organizado, 280x300px
- onboarding_slide_3.svg — paleta de colores personal, 280x300px

---

## Responsividad mobile

### Breakpoints Flutter
- Mobile: < 600dp → NavigationBar bottom
- Tablet: >= 600dp → NavigationRail lateral

### Adaptaciones mobile criticas
- Touch targets: minimo 48x48px (WCAG 2.1 AA)
- Safe area top: 59px (status bar + notch)
- Safe area bottom: 34px (home indicator)
- Gutter lateral: 24px
- UploadZone: min 280px height, expandible
- Grid wardrobe: 2 columnas en mobile, 3 en tablet
- Boton CTA: full width en mobile (con gutter), auto-width en tablet

### Orientacion
- Portrait: diseno principal
- Landscape: no optimizar para MVP (scroll vertical funciona)

---

## QA Visual — Checklist para Brook

### Tokens (cero hardcode)
- Todos los colores desde AppColors (ningun #HEX directo fuera de AppColors)
- Tipografia desde AppTypography (ningun fontSize suelto)
- Spacing multiples de 4px o 8px (desde AppSpacing)
- Radius desde AppRadius (sm/DEFAULT/md/lg/xl/full)
- Sombras desde AppShadows (ambient1/ambient2)

### Componentes
- GradientButton: maximo 1 por pantalla visible
- Gradiente NO en fondos de pantalla completa
- AIInsightChip: solo en contenido generado por IA
- PlanBadge: correcto por tier del usuario

### Accesibilidad
- Touch targets 48x48px minimo
- Contraste de texto verificado con tokens
- Safe areas respetadas
- Inputs con labels visibles (no solo placeholder)

### Estados
- Empty states disenados (S05, S08)
- Error states (S11 ErrorView)
- Loading states (SkeletonCard o GradientLoaderCard)
- Disabled states (opacity 0.4)

---

## Protocolo de entrega Erik → Brook

### Figma
Link: [PENDIENTE — SAB 25 mayo 2026]
Frames organizados: Auth (S01-S03) / Try-On (S04+S04B) / Wardrobe (S05) / Style (S06) / Body (S07) / Collections (S08) / Utilities (S09-S11)

### Assets exportados
Ver `/frontend/assets/illustrations/` — 13 SVG en 3 prioridades (ver seccion assets)

### Tokens Dart
Sin cambios vs DESIGN_SYSTEM.md. Usar ese como fuente de verdad.
Archivos: `lib/core/theme/app_colors.dart`, `app_typography.dart`, `app_spacing.dart`, `app_radius.dart`, `app_shadows.dart`

### Notas de implementacion
Ver `docs/DESIGN_HANDOFF_S01-S11.md` para specs detalladas por pantalla.
Ver `docs/mockups/ERIK_SPRINT_DESIGN_SPECS.md` para layouts ASCII.
Ver `docs/mockups/S06_SOFT_CAP_UI_DESIGN.md` para soft cap flow.

### QA Visual
Usar checklist de este documento.
Discrepancias > 8px de spacing o colores incorrectos → abrir issue en GitHub.

---

**Stitch project:** https://stitch.withgoogle.com/projects/2365238704690249989
**Preview mobile:** https://stitch.withgoogle.com/preview/2365238704690249989?node-id=c42272a5d4df4756a165e4bc57d79d99
**Ultima verificacion:** 2026-05-21 por Erik
**Estado:** DESIGN.md actualizado y verificado contra captura objetivo
**Handoff a Brook:** SAB 25 mayo 2026
