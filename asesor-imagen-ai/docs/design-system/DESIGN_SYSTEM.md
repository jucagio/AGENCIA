# DESIGN SYSTEM — Asesor de Imagen AI
## Sistema de diseño oficial: Aether Luxe

**Fuente:** Prototipo `stitch_ai_fit_check_ui.zip` — validado por Juan Camilo Gil (2026-05-18)
**Owner:** Erik (diseño) + Brook (implementación Flutter)
**Status:** ✅ APROBADO — usar estos tokens en TODA la app

---

## 0. Decisiones de diseño confirmadas

| Decisión | Valor aprobado |
|----------|---------------|
| **Nombre de la app** | **Asesor de Imagen AI** (marca interna) / **AI Fit Check** (nombre de producto en UI) |
| **Idioma UI** | Español (LATAM) |
| **Estilo visual** | Minimalista editorial + tech premium |
| **Plataforma primaria** | Flutter móvil (iOS + Android) |
| **Plataforma secundaria** | Web responsive (post-launch) |
| **Design system** | Aether Luxe |
| **Tipografía** | Inter (Google Fonts) |
| **Mood board** | Fashion editorial / gallery / clean |

---

## 1. Paleta de colores

### Tokens principales (Material You compatible)

```dart
// lib/core/theme/app_colors.dart

class AppColors {
  // ─── Surfaces ───────────────────────────────────────
  static const surface              = Color(0xFFF8F9FB);
  static const surfaceDim           = Color(0xFFD9DADC);
  static const surfaceBright        = Color(0xFFF8F9FB);
  static const surfaceContainerLowest  = Color(0xFFFFFFFF);
  static const surfaceContainerLow     = Color(0xFFF3F4F6);
  static const surfaceContainer        = Color(0xFFEDEEF0);
  static const surfaceContainerHigh    = Color(0xFFE7E8EA);
  static const surfaceContainerHighest = Color(0xFFE1E2E4);
  static const surfaceVariant          = Color(0xFFE1E2E4);
  static const surfaceTint             = Color(0xFF575E70);
  static const background              = Color(0xFFF8F9FB);

  // ─── On-surface (texto sobre fondos) ─────────────────
  static const onSurface             = Color(0xFF191C1E);  // texto principal
  static const onSurfaceVariant      = Color(0xFF45464C);  // texto secundario
  static const inverseSurface        = Color(0xFF2E3132);
  static const inverseOnSurface      = Color(0xFFF0F1F3);

  // ─── Outlines (bordes) ────────────────────────────────
  static const outline               = Color(0xFF76777D);
  static const outlineVariant        = Color(0xFFC6C6CD);

  // ─── Primary (negro — tipografía y acciones primarias) ─
  static const primary               = Color(0xFF000000);
  static const onPrimary             = Color(0xFFFFFFFF);
  static const primaryContainer      = Color(0xFF141B2B);
  static const onPrimaryContainer    = Color(0xFF7D8497);
  static const inversePrimary        = Color(0xFFC0C6DB);
  static const primaryFixed          = Color(0xFFDCE2F7);
  static const primaryFixedDim       = Color(0xFFC0C6DB);
  static const onPrimaryFixed        = Color(0xFF141B2B);
  static const onPrimaryFixedVariant = Color(0xFF404758);

  // ─── Secondary (azul eléctrico — CTAs e IA) ──────────
  static const secondary             = Color(0xFF0058BE);  // Electric Blue
  static const onSecondary           = Color(0xFFFFFFFF);
  static const secondaryContainer    = Color(0xFF2170E4);
  static const onSecondaryContainer  = Color(0xFFFEFCFF);
  static const secondaryFixed        = Color(0xFFD8E2FF);
  static const secondaryFixedDim     = Color(0xFFADC6FF);
  static const onSecondaryFixed      = Color(0xFF001A42);
  static const onSecondaryFixedVariant = Color(0xFF004395);

  // ─── Tertiary (violeta — AI features) ─────────────────
  static const tertiary              = Color(0xFF000000);
  static const onTertiary            = Color(0xFFFFFFFF);
  static const tertiaryContainer     = Color(0xFF23005C);
  static const onTertiaryContainer   = Color(0xFF9466FF);  // Violet
  static const tertiaryFixed         = Color(0xFFE9DDFF);
  static const tertiaryFixedDim      = Color(0xFFD0BCFF);
  static const onTertiaryFixed       = Color(0xFF23005C);
  static const onTertiaryFixedVariant = Color(0xFF5516BE);

  // ─── Error ────────────────────────────────────────────
  static const error                 = Color(0xFFBA1A1A);
  static const onError               = Color(0xFFFFFFFF);
  static const errorContainer        = Color(0xFFFFDAD6);
  static const onErrorContainer      = Color(0xFF93000A);

  // ─── GRADIENTE PRIMARIO (botón CTA + features IA) ────
  // linear-gradient(135deg, #0058be 0%, #9466ff 100%)
  static const Gradient primaryGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [Color(0xFF0058BE), Color(0xFF9466FF)],
  );
}
```

### Uso del gradiente
```
Gradiente azul→violeta = EXCLUSIVO para:
  ✅ Botón CTA principal ("Generar Outfit Ideal")
  ✅ Estados de carga/procesamiento IA
  ✅ Bordes activos en upload zones (cuando drag over)
  ✅ Chips de AI Insights
  ❌ NO usar en texto normal
  ❌ NO usar en fondos de toda la pantalla
```

---

## 2. Tipografía

```dart
// Fuente: Inter (importar desde Google Fonts)
// pubspec.yaml → google_fonts: ^6.1.0

import 'package:google_fonts/google_fonts.dart';

class AppTypography {
  static TextStyle get h1 => GoogleFonts.inter(
    fontSize: 48, fontWeight: FontWeight.w600,
    height: 1.1, letterSpacing: -0.02 * 48,
  );

  static TextStyle get h2 => GoogleFonts.inter(
    fontSize: 32, fontWeight: FontWeight.w600,
    height: 1.2, letterSpacing: -0.01 * 32,
  );

  static TextStyle get h3 => GoogleFonts.inter(
    fontSize: 24, fontWeight: FontWeight.w500,
    height: 1.3, letterSpacing: -0.01 * 24,
  );

  static TextStyle get bodyLg => GoogleFonts.inter(
    fontSize: 18, fontWeight: FontWeight.w400, height: 1.6,
  );

  static TextStyle get bodyMd => GoogleFonts.inter(
    fontSize: 16, fontWeight: FontWeight.w400, height: 1.6,
  );

  // Etiquetas en mayúsculas (metadata, badges, nav items)
  static TextStyle get labelCaps => GoogleFonts.inter(
    fontSize: 12, fontWeight: FontWeight.w600,
    height: 1.0, letterSpacing: 0.05 * 12,
  ).copyWith(fontFeatures: [FontFeature.enable('smcp')]);
}
```

---

## 3. Espaciado (8px base system)

```dart
class AppSpacing {
  static const double unit   = 4;   // 4px
  static const double xs     = 8;   // 0.5rem
  static const double sm     = 16;  // 1rem
  static const double md     = 24;  // 1.5rem
  static const double lg     = 32;  // 2rem
  static const double xl     = 64;  // 4rem
  static const double gutter = 24;  // 1.5rem — padding lateral estándar
  static const double margin  = 32;  // 2rem — margen entre secciones
}
```

---

## 4. Border radius

```dart
class AppRadius {
  static const double sm   = 4;    // inputs mínimos
  static const double DEFAULT = 8; // radio por defecto
  static const double md   = 12;   // cards pequeñas
  static const double lg   = 16;   // cards principales (rounded-2xl)
  static const double xl   = 24;   // modales
  static const double full = 9999; // pills, chips, botones redondos

  // Flutter BorderRadius shortcuts
  static BorderRadius get card    => BorderRadius.circular(lg);
  static BorderRadius get button  => BorderRadius.circular(full);
  static BorderRadius get input   => BorderRadius.circular(lg);
  static BorderRadius get chip    => BorderRadius.circular(full);
  static BorderRadius get upload  => BorderRadius.circular(lg);
}
```

---

## 5. Sombras (Ambient shadows — sin negro duro)

```dart
class AppShadows {
  // Level 1 — Cards normales (muy sutil)
  static const List<BoxShadow> ambient1 = [
    BoxShadow(
      color: Color(0x0A000000),  // 4% opacity
      blurRadius: 10,
      offset: Offset(0, 4),
    ),
  ];

  // Level 2 — Modales, dropdowns, resultado principal
  static const List<BoxShadow> ambient2 = [
    BoxShadow(
      color: Color(0x14000000),  // 8% opacity
      blurRadius: 25,
      offset: Offset(0, 8),
    ),
  ];
}
```

---

## 6. Componentes UI — especificaciones

### 6.1 Botón CTA Principal (Gradiente)
```
Fondo:      LinearGradient(#0058BE → #9466FF, 135°)
Texto:      white, bodyLg (18px), fontWeight 600
Padding:    16px vertical, 64px horizontal (xl horizontal)
Radius:     full (pill shape)
Sombra:     ambient2
Hover:      opacity 90%
Icono:      material_symbols "magic_button" / "auto_awesome"
```

### 6.2 Botón Secundario (outline)
```
Borde:      1px solid #000000 (primary)
Texto:      #000000, labelCaps (12px)
Fondo:      transparente
Radius:     lg (16px)
Hover:      bg surfaceVariant
```

### 6.3 Botón Primario Sólido (negro)
```
Fondo:      #000000
Texto:      white, labelCaps
Padding:    12px vertical
Radius:     lg (16px)
```

### 6.4 Upload Zone — Foto personal
```
Tamaño:     flex, min-height 400px (adaptable en móvil)
Borde:      2px dashed #C6C6CD (outline-variant)
Radius:     lg (16px)
Fondo:      surfaceContainerLowest (#FFF)
Estado hover: borde → #0058BE (secondary)
Icono:      photo_camera, 36px, color outline
Texto:      "Sube tu foto (de frente y buena luz)"
Sombra:     ambient1
```

### 6.5 Slots de Ropa (grid 2×3 móvil)
```
Proporción: aspect-square (1:1)
Fondo vacío: surfaceContainerLowest
Borde:      1px dashed outline-variant
Radius:     xl (12px)
Icono "+":  material "add", color outline
Hover:      borde → secondary, icono → secondary

Con item:
  Imagen:   object-cover, full bleed
  Botón X:  absoluto top-right, circular, surface/80% bg
  Sombra:   ambient1
```

### 6.6 AI Insights Chip
```
Fondo:      tertiaryFixed (#E9DDFF)
Texto:      onTertiaryContainer (#9466FF — violeta)
Icono:      "auto_awesome" / "colors_spark"
Padding:    4px vertical, 12px horizontal
Radius:     full (pill)
Font:       labelCaps
```

### 6.7 Card de Resultado AI
```
Fondo:      surfaceContainerLow (#F3F4F6)
Radius:     lg (16px)
Padding:    lg (32px)
Sombra:     ambient1
Contenido:  AI chip + h3 título + bodyMd descripción + acciones
```

### 6.8 Navigation (Sidebar web / Rail móvil)
```
Item activo:
  Fondo:    secondaryContainer (#2170E4)
  Texto:    onSecondaryContainer (#FEFCFF)
  Radius:   xl (12px)
  
Item inactivo:
  Texto:    onSurfaceVariant (#45464C)
  Hover:    bg surfaceVariant
  Radius:   xl

Font:       labelCaps (12px, uppercase)
Iconos:     Material Symbols Outlined

En Flutter móvil → NavigationBar (bottom)
En Flutter tablet → NavigationRail (lateral)
```

---

## 7. Pantallas a diseñar (inventario completo)

| # | Pantalla | Prioridad | Sprint | Status |
|---|----------|-----------|--------|--------|
| 1 | **Virtual Try-On** (pantalla ref.) | P0 | 4 | 🟢 Referencia completa |
| 2 | **Onboarding** (3 pasos) | P0 | 0 | 🟡 5 mockups Erik ✅ |
| 3 | **Login / Register** | P0 | 1 | 🟡 5 mockups Erik ✅ |
| 4 | **My Wardrobe** (galería closet) | P0 | 2 | ❌ Pendiente |
| 5 | **Style Insights** (análisis cuerpo + color) | P0 | 3 | ❌ Pendiente |
| 6 | **Body Analysis upload** | P0 | 3 | ❌ Pendiente |
| 7 | **Resultado del análisis** | P1 | 3 | ❌ Pendiente |
| 8 | **Try-On Loading state** | P0 | 4 | ❌ Pendiente |
| 9 | **Collections** (outfits guardados) | P1 | 5 | ❌ Pendiente |
| 10 | **Perfil / Settings** | P1 | 1 | ❌ Pendiente |
| 11 | **Paywall / Upgrade** | P0 | 6 | ❌ Pendiente |
| 12 | **Landing page** (web) | P1 | post-launch | ❌ Pendiente |

---

## 8. UX Flow principal confirmado

```
┌─────────────────────────────────────────────────────────┐
│ VIRTUAL TRY-ON FLOW                                      │
│                                                          │
│  [Estado 1: Upload]                                      │
│  • Upload foto personal                                  │
│  • Seleccionar hasta 5 prendas del wardrobe             │
│  • CTA: "Generar Outfit Ideal"                           │
│                                                          │
│  [Estado 2: Loading] ← FALTA en el prototipo            │
│  • Animación gradiente pulsante                          │
│  • "Nuestra IA está analizando tu estilo..."             │
│  • Progreso: 15-45 segundos (Replicate)                  │
│                                                          │
│  [Estado 3: Resultado]                                   │
│  • Imagen editorial generada (2/3 width)                 │
│  • Panel "Por qué funciona" con AI Insights (1/3 width)  │
│  • Acciones: Guardar / Compartir                         │
│                                                          │
│  Polling: GET /try-ons/{id} cada 3s hasta status=done    │
└─────────────────────────────────────────────────────────┘
```

---

## 9. Equivalencias Flutter de componentes web

| Web (Tailwind) | Flutter |
|----------------|---------|
| `aside.w-64` sidebar | `NavigationRail` (tablet) / `NavigationBar` bottom (móvil) |
| `border-2 border-dashed` | `DashedBorder` custom painter o `Container` con `Border` |
| `gradient-primary button` | `Container` con `BoxDecoration(gradient:)` + `GestureDetector` |
| `grid-cols-2` wardrobe | `GridView.count(crossAxisCount: 2)` |
| `aspect-square` | `AspectRatio(aspectRatio: 1)` |
| `rounded-2xl` | `BorderRadius.circular(16)` |
| `shadow-ambient-1` | `BoxShadow(blurRadius: 10, color: Color(0x0A000000))` |
| `object-cover` | `Image.network(fit: BoxFit.cover)` |
| `material-symbols-outlined` | `Icon` + Material Symbols package |
| `hover:` states | `InkWell` / `MouseRegion` |
| `transition-colors` | `AnimatedContainer` |
| `font-label-caps text-label-caps` | `AppTypography.labelCaps` |

---

## 10. Tailwind config extraído (para web landing page futura)

```js
// tailwind.config.js — tokens exactos del prototipo
module.exports = {
  theme: {
    extend: {
      colors: {
        "background":               "#f8f9fb",
        "surface":                  "#f8f9fb",
        "surface-container-lowest": "#ffffff",
        "surface-container-low":    "#f3f4f6",
        "surface-container":        "#edeef0",
        "surface-container-high":   "#e7e8ea",
        "surface-container-highest":"#e1e2e4",
        "surface-variant":          "#e1e2e4",
        "on-surface":               "#191c1e",
        "on-surface-variant":       "#45464c",
        "outline":                  "#76777d",
        "outline-variant":          "#c6c6cd",
        "primary":                  "#000000",
        "on-primary":               "#ffffff",
        "secondary":                "#0058be",
        "on-secondary":             "#ffffff",
        "secondary-container":      "#2170e4",
        "on-secondary-container":   "#fefcff",
        "tertiary-fixed":           "#e9ddff",
        "on-tertiary-container":    "#9466ff",
        "error":                    "#ba1a1a",
      },
      backgroundImage: {
        "gradient-primary": "linear-gradient(135deg, #0058be 0%, #9466ff 100%)",
      },
      borderRadius: {
        "2xl": "1rem",     // 16px — uso estándar de cards
        "xl":  "0.75rem",  // 12px
        "full": "9999px",  // pills
      },
      fontFamily: { sans: ["Inter", "sans-serif"] },
      boxShadow: {
        "ambient-1": "0 4px 10px rgba(0, 0, 0, 0.04)",
        "ambient-2": "0 8px 25px rgba(0, 0, 0, 0.08)",
      },
    },
  },
}
```

---

**Última actualización:** 2026-05-18
**Fuente de verdad:** `docs/design-system/DESIGN_SYSTEM.md`
**Archivos de referencia:** `stitch_ai_fit_check_ui.zip` (guardado en Drive)
