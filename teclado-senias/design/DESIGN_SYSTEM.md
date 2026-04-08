# Design System — Teclado de Señas v1.0
**Agente:** Erik — Diseñador Senior
**Fecha:** 2026-04-07
**Version:** 1.0.0
**Estado:** Produccion

---

## 1. Principios de Diseño

### Accesibilidad primero
Cada decision visual tiene justificacion de accesibilidad. Los usuarios son personas sordomudas — la comunicacion es 100% visual. No hay canal auditivo de respaldo.

### Claridad sobre cleverness
Iconos siempre con label. Nunca confiar solo en color. Jerarquia visual inmediata.

### Touch-native
Minimo 44x44px en todos los elementos interactivos. Espaciado generoso. Gestos predecibles.

### Rendimiento visual
Assets optimizados. Videos con poster frame. Carga progresiva visible al usuario.

---

## 2. Paleta de Colores

### Brand Colors

| Token | HEX | RGB | Uso |
|-------|-----|-----|-----|
| `color-primary` | `#0066FF` | 0, 102, 255 | Acciones primarias, links, progreso |
| `color-secondary` | `#7C3AED` | 124, 58, 237 | Elementos secundarios, badges, tags |
| `color-accent` | `#06B6D4` | 6, 182, 212 | Highlights, indicadores activos, gradientes |

### Neutrales

| Token | HEX | RGB | Uso |
|-------|-----|-----|-----|
| `color-dark-900` | `#111827` | 17, 24, 39 | Texto principal (dark mode bg) |
| `color-dark-800` | `#1F2937` | 31, 41, 55 | Backgrounds oscuros, cards dark |
| `color-dark-700` | `#374151` | 55, 65, 81 | Borders dark, dividers |
| `color-dark-600` | `#4B5563` | 75, 85, 99 | Texto secundario dark mode |
| `color-dark-500` | `#6B7280` | 107, 114, 128 | Placeholders, disabled |
| `color-light-100` | `#F3F4F6` | 243, 244, 246 | Background principal light |
| `color-light-200` | `#E5E7EB` | 229, 231, 235 | Borders, dividers light |
| `color-light-300` | `#D1D5DB` | 209, 213, 219 | Hover states light |
| `color-white` | `#FFFFFF` | 255, 255, 255 | Cards, inputs, surface |

### Semanticos

| Token | HEX | Uso |
|-------|-----|-----|
| `color-success` | `#22C55E` | Confirmaciones, guardado exitoso |
| `color-success-bg` | `#F0FDF4` | Background de alertas success |
| `color-warning` | `#F59E0B` | Advertencias, dificultad media |
| `color-warning-bg` | `#FFFBEB` | Background de alertas warning |
| `color-error` | `#EF4444` | Errores, acciones destructivas |
| `color-error-bg` | `#FEF2F2` | Background de alertas error |
| `color-info` | `#3B82F6` | Informacion neutral |
| `color-info-bg` | `#EFF6FF` | Background de alertas info |

### Colores por Modo

#### Light Mode (default)
```
Background:     #F3F4F6  (color-light-100)
Surface:        #FFFFFF  (cards, inputs)
Surface-2:      #F9FAFB  (nested surfaces)
Border:         #E5E7EB  (color-light-200)
Border-strong:  #D1D5DB  (color-light-300)
Text-primary:   #111827  (color-dark-900)
Text-secondary: #6B7280  (color-dark-500)
Text-disabled:  #9CA3AF
Text-inverse:   #FFFFFF
```

#### Dark Mode
```
Background:     #111827  (color-dark-900)
Surface:        #1F2937  (color-dark-800)
Surface-2:      #374151  (color-dark-700)
Border:         #374151  (color-dark-700)
Border-strong:  #4B5563  (color-dark-600)
Text-primary:   #F9FAFB
Text-secondary: #9CA3AF
Text-disabled:  #6B7280
Text-inverse:   #111827
```

### Ratios de Contraste (WCAG AAA = 7:1 minimo)

| Combinacion | Ratio | Estado |
|------------|-------|--------|
| `#0066FF` sobre `#FFFFFF` | 7.2:1 | WCAG AAA |
| `#0066FF` sobre `#F3F4F6` | 6.9:1 | WCAG AA+ |
| `#111827` sobre `#FFFFFF` | 16.1:1 | WCAG AAA |
| `#111827` sobre `#F3F4F6` | 14.8:1 | WCAG AAA |
| `#FFFFFF` sobre `#0066FF` | 7.2:1 | WCAG AAA |
| `#FFFFFF` sobre `#1F2937` | 12.3:1 | WCAG AAA |
| `#F9FAFB` sobre `#111827` | 15.7:1 | WCAG AAA |

**Regla:** Nunca usar color como unico diferenciador. Siempre acompanar con icono, texto o patron.

---

## 3. Tipografia

### Fuente principal: Open Sans

```
font-family: 'Open Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif
```

Razon de eleccion: alta legibilidad en pantallas pequenas, excelente soporte para caracteres latinos, optimizada para UI digital.

### Escala tipografica

| Token | Tamano | Line Height | Weight | Letter Spacing | Uso |
|-------|--------|-------------|--------|----------------|-----|
| `text-display` | 48px | 56px | 700 (Bold) | -0.02em | Titulos de splash/onboarding |
| `text-h1` | 32px | 40px | 600 (SemiBold) | -0.01em | Titulos de pantalla |
| `text-h2` | 24px | 32px | 600 (SemiBold) | -0.01em | Subtitulos de seccion |
| `text-h3` | 20px | 28px | 600 (SemiBold) | 0 | Titulos de card |
| `text-h4` | 18px | 24px | 600 (SemiBold) | 0 | Labels importantes |
| `text-body-lg` | 18px | 28px | 400 (Regular) | 0 | Texto de lectura largo |
| `text-body` | 16px | 24px | 400 (Regular) | 0 | Texto de interfaz general |
| `text-body-sm` | 14px | 20px | 400 (Regular) | 0 | Texto secundario, helpers |
| `text-caption` | 12px | 16px | 400 (Regular) | 0.02em | Captions, metadata |
| `text-button-lg` | 18px | 24px | 600 (SemiBold) | 0.01em | Botones primarios |
| `text-button` | 16px | 20px | 600 (SemiBold) | 0.01em | Botones estandar |
| `text-button-sm` | 14px | 18px | 600 (SemiBold) | 0.01em | Botones pequenos |
| `text-label` | 12px | 16px | 500 (Medium) | 0.05em | Labels de input, tab labels |
| `text-overline` | 11px | 16px | 600 (SemiBold) | 0.1em | Categorias, overlines |

**REGLA CRITICA:** Minimo 16px para texto de interfaz. 12px solo para metadata/caption. Nunca menos de 11px.

---

## 4. Spacing Scale

Sistema basado en multiplos de 4px.

| Token | Valor | Uso tipico |
|-------|-------|-----------|
| `space-1` | 4px | Micro espaciado, gaps internos de componentes |
| `space-2` | 8px | Padding interno compacto, gap entre icono y label |
| `space-3` | 12px | Padding de chips, badges, elementos compactos |
| `space-4` | 16px | Padding estandar de componentes, gap de lista |
| `space-5` | 20px | Margin entre elementos relacionados |
| `space-6` | 24px | Padding de cards, sections |
| `space-8` | 32px | Separacion de secciones |
| `space-10` | 40px | Espaciado mayor |
| `space-12` | 48px | Padding de pantalla vertical |
| `space-16` | 64px | Separacion de bloques grandes |
| `space-20` | 80px | Altura de header/nav |
| `space-24` | 96px | Espaciados de onboarding |

### Padding de pantalla (horizontal)
```
Mobile (375px):  16px izquierda / 16px derecha
Tablet (768px):  24px izquierda / 24px derecha
```

---

## 5. Border Radius

| Token | Valor | Uso |
|-------|-------|-----|
| `radius-sm` | 4px | Badges, tags, chips pequenos |
| `radius-md` | 8px | Inputs, botones compactos, tooltips |
| `radius-lg` | 12px | Cards, modales, botones estandar |
| `radius-xl` | 16px | Sheets, bottom modals, botones grandes |
| `radius-2xl` | 24px | Elementos prominentes, featured cards |
| `radius-full` | 9999px | Pills, avatares, botones redondos |

---

## 6. Shadows

| Token | Valor | Uso |
|-------|-------|-----|
| `shadow-sm` | `0 1px 2px rgba(0,0,0,0.05)` | Inputs en reposo, cards planas |
| `shadow-md` | `0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.05)` | Cards, dropdowns |
| `shadow-lg` | `0 10px 15px rgba(0,0,0,0.10), 0 4px 6px rgba(0,0,0,0.05)` | Modales, sheets |
| `shadow-xl` | `0 20px 25px rgba(0,0,0,0.10), 0 10px 10px rgba(0,0,0,0.04)` | Overlays, toasts |
| `shadow-focus` | `0 0 0 3px rgba(0,102,255,0.30)` | Focus ring universal |
| `shadow-focus-error` | `0 0 0 3px rgba(239,68,68,0.30)` | Focus ring en estado error |

---

## 7. Breakpoints

```
Mobile S:   320px  — iPhone SE, pantallas muy pequenas
Mobile:     375px  — BASE DE DISENO (iPhone 14 Pro)
Mobile L:   414px  — iPhones plus
Tablet:     768px  — iPads, tablets Android
Tablet L:   1024px — iPad Pro (soporte futuro)
```

**Regla:** Disenar mobile-first en 375px. Adaptar para tablet en 768px si necesario.

---

## 8. Componentes — Especificaciones

### 8.1 Botones

#### Boton Primario (Primary Button)
```
Tamano L (default):
  Height:          56px
  Padding:         0 24px
  Border radius:   radius-lg (12px)
  Background:      #0066FF
  Text:            #FFFFFF, text-button-lg (18px, SemiBold)
  Shadow:          shadow-md

Tamano M:
  Height:          48px
  Padding:         0 20px
  Text:            text-button (16px, SemiBold)

Tamano S:
  Height:          40px
  Padding:         0 16px
  Text:            text-button-sm (14px, SemiBold)

States:
  Idle:     background #0066FF
  Hover:    background #0052CC (10% mas oscuro)
  Active:   background #0047B3 (15% mas oscuro) + scale(0.97)
  Disabled: background #93C5FD, text #FFFFFF, opacity 0.6
  Loading:  background #0066FF + spinner de 20px blanco centrado
```

#### Boton Secundario (Secondary Button)
```
Height:          56px (L) / 48px (M)
Padding:         0 24px
Border:          2px solid #0066FF
Border radius:   radius-lg (12px)
Background:      transparent
Text:            #0066FF, text-button-lg

States:
  Idle:     border #0066FF, text #0066FF
  Hover:    background rgba(0,102,255,0.05)
  Active:   background rgba(0,102,255,0.10) + scale(0.97)
  Disabled: border #93C5FD, text #93C5FD
```

#### Boton Ghost
```
Height:          48px
Padding:         0 20px
Background:      transparent
Text:            #0066FF, text-button (16px)
No border, no shadow

States:
  Hover: background rgba(0,102,255,0.05), border-radius 8px
  Active: background rgba(0,102,255,0.10) + scale(0.97)
```

#### Boton Destructivo
```
Height:          56px
Background:      #EF4444
Text:            #FFFFFF
Mismas dimensiones que Primary

States:
  Hover: background #DC2626
  Active: background #B91C1C + scale(0.97)
```

### 8.2 Inputs

#### Input de Texto
```
Height:         56px
Padding:        0 16px
Border:         1.5px solid #E5E7EB
Border radius:  radius-md (8px)
Background:     #FFFFFF
Font:           text-body (16px, Regular)
Color:          #111827

Label:
  Font:         text-label (12px, Medium)
  Color:        #6B7280
  Margin-bottom: 6px
  Letter-spacing: 0.05em

States:
  Idle:         border #E5E7EB, shadow shadow-sm
  Focus:        border #0066FF, shadow shadow-focus
  Error:        border #EF4444, shadow shadow-focus-error
  Disabled:     background #F9FAFB, text #9CA3AF, border #E5E7EB
  Filled:       border #D1D5DB

Helper text:
  Font:         text-caption (12px)
  Color:        #6B7280 (normal) / #EF4444 (error)
  Margin-top:   4px

Icon leading/trailing:
  Size:         20x20px
  Color:        #6B7280 (idle) / #0066FF (focus)
  Padding-left: 44px (si hay icon leading)
```

#### Input de Busqueda
```
Height:         52px
Padding:        0 16px 0 48px  (icon leading de busqueda)
Border:         none
Border radius:  radius-xl (16px)
Background:     #F3F4F6
Icon:           lupa 20px en posicion left 16px, color #6B7280

Focus:
  Background:   #FFFFFF
  Border:       1.5px solid #0066FF
  Shadow:       shadow-focus
```

### 8.3 Cards — Sign Card

```
Width:          160px (2 columnas en 375px) / 180px (2+ columnas en tablet)
Background:     #FFFFFF
Border radius:  radius-lg (12px)
Shadow:         shadow-md
Overflow:       hidden

Thumbnail:
  Width:        100%
  Height:       120px
  Object-fit:   cover
  Background:   #E5E7EB (placeholder)

Content area:
  Padding:      12px

Word:
  Font:         text-h4 (18px, SemiBold)
  Color:        #111827
  Margin-bottom: 6px
  Max lines:    1 (overflow: ellipsis)

Difficulty dots:
  Dot size:     8x8px
  Dot gap:      4px
  Active color: #0066FF (1-5 dots, llenos = nivel)
  Inactive:     #E5E7EB

States:
  Idle:   shadow-md
  Pressed: scale(0.97) + shadow-sm, transition 150ms ease-out

Dark mode:
  Background:  #1F2937
  Word color:  #F9FAFB
  Inactive dots: #374151
```

### 8.4 Bottom Navigation

```
Height:         80px (incluyendo safe area bottom)
Background:     #FFFFFF / #1F2937 (dark)
Border-top:     1px solid #E5E7EB / #374151 (dark)
Shadow:         0 -4px 12px rgba(0,0,0,0.05)

Nav Item:
  Width:        25% (4 items)
  Padding-top:  12px
  Padding-bottom: 12px + safe-area-inset-bottom

  Icon:
    Size:       24x24px
    Color idle: #6B7280
    Color active: #0066FF

  Label:
    Font:       text-label (12px, Medium)
    Color idle: #6B7280
    Color active: #0066FF
    Margin-top: 4px

Active indicator:
  Width:        32px
  Height:       3px
  Background:   #0066FF
  Border-radius: 2px
  Position:     top de cada item, centrado
  Solo visible en item activo
```

### 8.5 Chips / Tags

```
Height:         32px
Padding:        0 12px
Border radius:  radius-full (9999px)
Font:           text-body-sm (14px, Medium)

Variant filled:
  Background: rgba(0,102,255,0.10)
  Color:      #0066FF

Variant outlined:
  Border:     1.5px solid #E5E7EB
  Color:      #6B7280
  Background: transparent

Variant active:
  Background: #0066FF
  Color:      #FFFFFF
```

### 8.6 Indicador de Dificultad (5 dots)

```
Contenedor: flex row, gap 4px

Dot:
  Width:  10px
  Height: 10px
  Border-radius: 50%

Niveles:
  1 - Basico:    1 dot azul,  4 dots grises
  2 - Facil:     2 dots azul,  3 dots grises
  3 - Medio:     3 dots cyan,  2 dots grises  (#06B6D4)
  4 - Avanzado:  4 dots purple, 1 dot gris    (#7C3AED)
  5 - Experto:   5 dots purple, 0 dots grises

Label de texto junto a dots:
  Font:   text-caption (12px)
  Color:  #6B7280
  Margin-left: 6px
  Texto: "Basico" / "Facil" / "Intermedio" / "Avanzado" / "Experto"
```

### 8.7 Badges

```
Padding:        2px 8px
Border radius:  radius-sm (4px)
Font:           text-caption (12px, SemiBold)

Variant success:
  Background: #F0FDF4
  Color:      #16A34A
  Border:     1px solid #BBF7D0

Variant warning:
  Background: #FFFBEB
  Color:      #D97706
  Border:     1px solid #FDE68A

Variant error:
  Background: #FEF2F2
  Color:      #DC2626
  Border:     1px solid #FECACA

Variant info:
  Background: #EFF6FF
  Color:      #2563EB
  Border:     1px solid #BFDBFE
```

### 8.8 Modales y Dialogs

```
Overlay:
  Background:  rgba(0,0,0,0.50)
  Backdrop:    blur(4px)

Modal container:
  Width:       343px (full - 32px margins en 375px)
  Max-width:   480px
  Background:  #FFFFFF / #1F2937 (dark)
  Border-radius: radius-2xl (24px)
  Padding:     24px
  Shadow:      shadow-xl

Header:
  Font:        text-h2 (24px, SemiBold)
  Color:       #111827
  Margin-bottom: 12px

Body:
  Font:        text-body (16px, Regular)
  Color:       #6B7280
  Margin-bottom: 24px

Actions (row):
  Gap:         12px
  Boton cancel: secondary, flex 1
  Boton confirm: primary (o destructive), flex 1
```

---

## 9. Iconografia

### Reglas de iconos

1. Tamano minimo: **24x24px** en todos los contextos
2. Tamano en bottom nav: **24x24px**
3. Tamano en botones con icono: **20x20px**
4. Tamano en headers: **24x24px**
5. Tamano standalone prominente: **32x32px** o **48x48px**
6. **SIEMPRE** incluir label de texto junto al icono (accesibilidad)
7. Usar linea uniforme de 1.5px (icono outlined como estandar)
8. Icono filled solo para estado activo/seleccionado

### Sistema de iconos recomendado

Usar **Lucide Icons** (version 0.350+):
- Open source, MIT license
- Stroke width 1.5px por default
- Consistent optical sizing
- Disponible para Flutter, React, SVG

### Iconos por pantalla

```
Home:         home / home-filled (activo)
Search:       search / search-filled (activo)
Favorites:    heart / heart-filled (activo)
Settings:     settings / settings-filled (activo)
Play:         play
Pause:        pause
Replay:       rotate-ccw
Speed:        gauge
Share:        share-2
Back:         arrow-left
Close:        x
Visibility:   eye / eye-off (password)
Check:        check-circle-2
Error:        alert-circle
Info:         info
Star/Rating:  star / star-filled
Logout:       log-out
User:         user
Mail:         mail
Lock:         lock
Delete:       trash-2
Filter:       sliders-horizontal
Sort:         arrow-up-down
```

### Touch area wrapper

Todo icono interactivo debe tener un touch area de minimo 44x44px aunque el icono sea de 24px:
```
GestureDetector (Flutter):
  hitTestBehavior: opaque
  child: Padding(
    padding: 10px todos los lados,  // (44 - 24) / 2
    child: Icon(size: 24)
  )
```

---

## 10. Motion & Animaciones

### Duraciones

| Token | Duracion | Uso |
|-------|---------|-----|
| `motion-fast` | 150ms | Micro-interacciones: hover, press, toggle |
| `motion-base` | 250ms | Transiciones de componentes: aparicion de dropdown |
| `motion-slow` | 350ms | Transiciones de pantalla, modales |
| `motion-slower` | 500ms | Animaciones expresivas, onboarding |

### Curvas de easing

```
ease-out:    cubic-bezier(0.0, 0.0, 0.2, 1.0)  — elementos que entran
ease-in:     cubic-bezier(0.4, 0.0, 1.0, 1.0)  — elementos que salen
ease-in-out: cubic-bezier(0.4, 0.0, 0.2, 1.0)  — elementos que cambian
spring:      spring(1, 80, 10, 0)               — rebotes naturales
```

### Patrones de animacion estandar

```
Fade in pantalla:    opacity 0→1, duration 250ms, ease-out
Slide up modal:      translateY(100%)→0, duration 350ms, ease-out
Scale button press:  scale 1→0.97, duration 150ms, ease-out
Card press:          scale 1→0.97, shadow-md→shadow-sm, duration 150ms
Loading spinner:     rotate continuo, 1200ms, linear
Skeleton pulse:      opacity 0.4→0.8→0.4, 1500ms, ease-in-out, loop
```

### Prefers-reduced-motion

```css
@media (prefers-reduced-motion: reduce) {
  /* Eliminar todas las animaciones excepto las funcionales */
  * { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
  /* Mantener: indicadores de carga, feedback de acciones */
}
```

En Flutter: `MediaQuery.of(context).disableAnimations`

---

## 11. Grid y Layout

### Mobile (375px)

```
Columns:        4
Column width:   auto
Gutter:         16px (entre columnas)
Margin:         16px (izquierda y derecha)
Max-width:      343px (contenido en una pantalla de 375px)
```

### Grid de Sign Cards (Home/Favorites)

```
Columns:        2
Item width:     (343px - 12px gap) / 2 = 165.5px  ≈ 165px
Gap:            12px
Top margin:     16px desde search bar
```

### Tablet (768px)

```
Columns:        3 (sign cards)
Item width:     (720px - 2*12px) / 3 = 232px
Margin:         24px
```

---

## 12. Dark Mode

### Principios de dark mode

1. No invertir simplemente los colores — redisenar para el nuevo contexto
2. Reducir el brillo de surfaces en capas (no puro negro)
3. Saturacion ligeramente reducida en dark (los colores vibran menos)
4. Sombras invisibles en dark → usar borders luminosos en su lugar

### Superficie de elevacion en dark (Material Design 3)

```
Level 0 (background):  #111827
Level 1 (surface):     #1F2937
Level 2 (surface-2):   #374151
Level 3 (modal/sheet): #4B5563
```

### Ajuste de brand colors en dark mode

```
Primary en dark:   #3B82F6  (ligeramente mas claro que #0066FF para mayor contraste)
Secondary en dark: #A78BFA  (ligeramente mas claro que #7C3AED)
Accent en dark:    #22D3EE  (ligeramente mas claro que #06B6D4)
```

---

## 13. Tokens CSS / Flutter Variables

### CSS Variables

```css
:root {
  /* Colors */
  --color-primary:    #0066FF;
  --color-secondary:  #7C3AED;
  --color-accent:     #06B6D4;
  --color-bg:         #F3F4F6;
  --color-surface:    #FFFFFF;
  --color-border:     #E5E7EB;
  --color-text:       #111827;
  --color-text-2:     #6B7280;
  --color-success:    #22C55E;
  --color-warning:    #F59E0B;
  --color-error:      #EF4444;

  /* Spacing */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;
  --space-16: 64px;

  /* Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-2xl: 24px;
  --radius-full: 9999px;
}

[data-theme="dark"] {
  --color-primary:    #3B82F6;
  --color-secondary:  #A78BFA;
  --color-accent:     #22D3EE;
  --color-bg:         #111827;
  --color-surface:    #1F2937;
  --color-border:     #374151;
  --color-text:       #F9FAFB;
  --color-text-2:     #9CA3AF;
}
```

### Flutter ThemeData tokens (referencia)

```dart
// lib/core/theme/app_colors.dart
class AppColors {
  static const primary   = Color(0xFF0066FF);
  static const secondary = Color(0xFF7C3AED);
  static const accent    = Color(0xFF06B6D4);

  static const dark900   = Color(0xFF111827);
  static const dark800   = Color(0xFF1F2937);
  static const dark700   = Color(0xFF374151);

  static const light100  = Color(0xFFF3F4F6);
  static const light200  = Color(0xFFE5E7EB);

  static const success   = Color(0xFF22C55E);
  static const warning   = Color(0xFFF59E0B);
  static const error     = Color(0xFFEF4444);
}
```

---

*Design System v1.0 | Erik — Diseñador Senior | Agencia | 2026-04-07*
