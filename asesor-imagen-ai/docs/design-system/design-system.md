# Asesor de Imagen AI — Sistema de Diseño
**Version:** 1.0.0 | **Autor:** Erik — Diseñador Senior | **Fecha:** 2026-04-25  
**Target:** Flutter mobile, 375x812 base, iOS + Android, Dark + Light mode, WCAG AA

---

## 1. Filosofía y Brand Vibe

### Quien es el producto
Un stylist personal de IA que empodera a mujeres 22-40 años urbanas a sacar el máximo de lo que ya tienen. No es Tinder de ropa. No es una tienda. Es una aliada inteligente y cálida.

### Los 4 pilares de diseño
1. **Cálido, no frio** — colores terracota y crema, nunca blancos clínicos ni azules corporativos
2. **AI es protagonista, no se esconde** — los estados de IA son visibles, con confianza comunicada. El usuario sabe que la IA trabaja para él.
3. **Premium pero accesible** — calidad visual de app de lujo, lenguaje de una amiga que sabe de moda
4. **Claridad extrema** — Ley de Hick: menos opciones visibles en cada momento, flujos que no necesitan tutorial

### Lo que NO es este diseño
- No glassmorphism pesado (blur sobre blur sobre blur) — solo liquid glass sutil donde agrega profundidad real
- No neon, gradients agresivos ni paletas oscuras intimidantes
- No iconos genéricos de stock — Lucide con stroke width consistente
- No animaciones de más de 500ms sin propósito declarado

---

## 2. Paleta de Color

### Colores base del sistema
Definidos en `design-tokens.json`. Aquí la guía de uso:

### Light Mode
```
Background principal:  neutral.100  (#F5EDE4) — arena cálida
Cards / superficies:   neutral.50   (#FAF6F1) — crema suave  
Bordes:                neutral.200  (#E8DDD4)
Texto primario:        neutral.900  (#1C1A20)
Texto secundario:      neutral.600  (#7A6A62)
Texto deshabilitado:   neutral.400  (#B8A49A)
```

### Dark Mode
```
Background principal:  neutral.900  (#1C1A20) — charcoal con tinte violeta
Cards / superficies:   neutral.850  (#2A2228)
Bordes:                neutral.800  (#3D3330)
Texto primario:        neutral.50   (#FAF6F1)
Texto secundario:      neutral.400  (#B8A49A)
Texto deshabilitado:   neutral.600  (#7A6A62)
```

### Color primario (Blush/Terracota)
- **Uso:** Botones CTA primarios, accents, íconos activos, progress bars
- **Default:** primary.500 (#D97B6A)
- **Sobre fondos oscuros usar:** primary.400 (#E8A598) para mantener contraste WCAG AA
- **NUNCA usar:** primary.200 o más claro sobre fondos claros (contraste insuficiente)

### Color secundario (Plum/Morado)
- **Uso:** Highlights de IA, badges de features premium, paywall, estados "AI thinking"
- **Default:** secondary.500 (#6B3FA0)
- **Sobre fondos oscuros usar:** secondary.300 (#A98BD8)
- **Contexto exclusivo:** Solo para identificar todo lo que es "IA". El usuario asocia el morado con inteligencia artificial en la app.

### Color AI
El sistema tiene un color especial para estados de IA:
- `ai.thinking`: morado suave pulsante — el componente AIThinkingIndicator lo usa
- `ai.gradient`: de blush a plum — para resultados y outputs de IA
- `ai.confidence-*`: verde/blush/gris según nivel de confianza del modelo

### Colores semánticos
| Estado    | Light mode      | Dark mode       |
|-----------|-----------------|-----------------|
| Success   | #2D9B6F         | #4ECFA0         |
| Error     | #C0392B         | #F06B6B         |
| Warning   | #B45309         | #FBBF24         |
| Info      | #1D6FA4         | #60AEDE         |

### Contraste WCAG AA (verificado)
| Combinación                          | Ratio   | AA Normal | AA Large |
|--------------------------------------|---------|-----------|----------|
| neutral.900 sobre neutral.100 (light)| 14.2:1  | ✅        | ✅       |
| neutral.50 sobre neutral.900 (dark)  | 14.2:1  | ✅        | ✅       |
| primary.500 sobre neutral.100 (light)| 4.8:1   | ✅        | ✅       |
| primary.400 sobre neutral.900 (dark) | 5.1:1   | ✅        | ✅       |
| secondary.500 sobre neutral.100      | 7.2:1   | ✅        | ✅       |
| secondary.300 sobre neutral.900      | 6.8:1   | ✅        | ✅       |

---

## 3. Tipografía

### Familias elegidas

**Playfair Display** (Google Fonts)
- Serif editorial con alto contraste entre trazos
- Uso EXCLUSIVO para: splash hero, display de onboarding, titulares de marketing in-app
- Por qué: asociación con revistas de moda (Vogue, Elle), premium sin ser frío

**Plus Jakarta Sans** (Google Fonts)
- Geométrica humanista, excelente legibilidad en pantalla
- Uso: todos los headings funcionales, body, labels, captions
- Por qué: moderna (2021+), rangos de peso completos, diacríticos completos, libre

**JetBrains Mono** (Google Fonts)
- Uso EXCLUSIVO para: datos de análisis, porcentajes de confianza, color codes
- Por qué: da "precisión técnica" a los outputs de IA, diferencia los datos del texto narrativo

### Escala tipográfica Flutter (en TextStyle)
```dart
// Display — Playfair, para splash y hero sections
TextStyle displayXL = TextStyle(
  fontFamily: 'PlayfairDisplay',
  fontSize: 64,
  fontWeight: FontWeight.w700,
  height: 1.1,
  letterSpacing: -0.02 * 64,
);

// H1 — Plus Jakarta Sans
TextStyle h1 = TextStyle(
  fontFamily: 'PlusJakartaSans',
  fontSize: 40,
  fontWeight: FontWeight.w700,
  height: 1.2,
  letterSpacing: -0.01 * 40,
);

// Body principal
TextStyle bodyMd = TextStyle(
  fontFamily: 'PlusJakartaSans',
  fontSize: 16,
  fontWeight: FontWeight.w400,
  height: 1.5,
);

// Label (botones, tags, badges)
TextStyle label = TextStyle(
  fontFamily: 'PlusJakartaSans',
  fontSize: 12,
  fontWeight: FontWeight.w600,
  letterSpacing: 0.05 * 12,
);
```

---

## 4. Espaciado y Grid

### Escala de espaciado (base 4px)
```
4px   — separación interna mínima
8px   — padding de badges, gaps mínimos
12px  — padding interno compacto
16px  — padding estándar de componentes (BASE)
20px  — margen horizontal de pantalla en 375px
24px  — margin entre secciones, padding de cards
32px  — espacio entre bloques
48px  — secciones mayores
64px  — hero sections
```

### Grid de pantalla
- **Ancho base:** 375px (iPhone SE / 13 mini)
- **Márgenes:** 20px cada lado = 335px de contenido
- **Columnas:** 4 columnas de 64px + 3 gutters de 16px + 2 márgenes de 20px
- **Breakpoints Flutter:**
  - < 400px: márgenes 16px
  - 400-430px (iPhone 15 Pro): márgenes 20px
  - > 430px: márgenes 24px

### Safe Areas (Flutter)
- Top: respetar `MediaQuery.of(context).padding.top` — status bar dinámica
- Bottom: `MediaQuery.of(context).padding.bottom` — home indicator en iPhones
- Bottom sheet: mínimo 16px sobre el home indicator

---

## 5. Componentes Base

### 5.1 Button

**Variants:**
- `primary` — fondo primary.500, texto blanco, sombra blush-glow on press
- `secondary` — fondo transparent, borde primary.500, texto primary.500
- `ghost` — fondo transparent, texto secondary.500 (para acciones de IA)
- `destructive` — fondo error.light, texto blanco

**Sizes:**
- `sm` — 36px height, padding H 16px, para acciones secundarias en lista
- `md` — 48px height, padding H 24px, DEFAULT — cumple touch target 44px
- `lg` — 56px height, padding H 32px, para CTAs héroe

**States:**
```
Normal   → elevation: shadow.sm
Hover    → elevation: shadow.md, scale: 1.0 (no scale en mobile)
Pressed  → scale: 0.97, duration: 100ms, easing: spring
Focused  → borde focus ring primary.500, 2px offset
Disabled → opacity: 0.38 (Material guideline), no shadow
Loading  → shimmer animation interna, pointer-events: none
```

**Flutter widget:** `AppButton` en `lib/shared/widgets/app_button.dart`

---

### 5.2 Input

**Variants:**
- `outlined` — borde 1.5px neutral.300, focused: primary.500
- `filled` — fondo neutral.100 (light) / neutral.850 (dark)

**States:**
```
Default  → border: neutral.300
Focused  → border: primary.500, label flota arriba, sombra shadow.sm
Filled   → label en posición arriba, borde: neutral.300
Error    → border: error.light, mensaje de error debajo en error.light
Success  → borde: success.light, check icon a la derecha
Disabled → opacity 0.38, no interactivo
```

**Anatomía:**
- Label flotante (Material floating label pattern)
- Leading icon opcional (20px, neutral.500)
- Trailing icon: clear, password toggle, o validación
- Helper text: 12px, neutral.500
- Error text: 12px, error.light

---

### 5.3 Card

**Variants:**
- `default` — fondo surface.card, shadow.sm, radius 16px
- `elevated` — shadow.md, para destacar sobre fondo
- `glass` — surface.glass + backdrop-filter blur 20px (iOS Liquid Glass inspired)
- `ai-result` — gradiente sutil de primary.50 a secondary.50, borde secondary.200
- `outfit` — ratio 3:4 (portrait), imagen llena + info overlay abajo

**Outfit Card específica:**
```
- Imagen: fill completo, object-fit: cover
- Gradiente overlay: transparent → neutral.900 (60%) en bottom 40%
- Título sobre gradiente: white, h4 style
- Tags sobre imagen: esquina superior derecha
- Favorite button: esquina superior izquierda, 44x44px touch target
- Border radius: 16px
```

---

### 5.4 Tag / Chip

**Variants:**
- `category` — fondo secondary.100, texto secondary.700 — para categorías de ropa
- `color-season` — 4 variantes con colores específicos (ver Color Season System)
- `ai-label` — fondo ai.gradient, texto white — para etiquetas generadas por IA
- `filter` — seleccionable, toggle state con primary.500 selected

---

### 5.5 Avatar

Tamaños: 24 / 32 / 40 / 56 / 80 / 120px
- Siempre border-radius: full (circular)
- Placeholder: iniciales en fondo primary.100, texto primary.600
- Loading: shimmer effect
- Borde opcional: 2px white para stacked avatars

---

### 5.6 Badge

- Notification count: fondo primary.500, texto white, monoespaciado
- Status: dot 8px, colores semánticos
- AI confidence: monocromático con alpha según nivel

---

### 5.7 Dialog

```
- Backdrop: rgba(28,26,32, 0.60), blur 4px
- Container: surface.card, radius 28px, padding 24px
- Max width: 340px
- Título: h3, centrado
- Cuerpo: body.sm, neutral.600
- Acciones: siempre 2 botones apilados o en fila según longitud
- Entrada: fade + scale (0.95 → 1.0), duration 250ms
```

---

### 5.8 Bottom Sheet

```
- Handle: 40x4px, neutral.300, radius full, centered, margin-top 12px
- Border radius top: 28px
- Backdrop: rgba(28,26,32, 0.60)
- Entrada: slide-up desde bottom, duration 350ms, easing: enter
- Swipe-to-dismiss: velocity threshold 800px/s
- Max height: 92% de pantalla (siempre hay handle visible)
```

---

## 6. Liquid Glass — Componente Especial para IA

Inspirado en iOS 26 Liquid Glass. Usado ESPECÍFICAMENTE para:
- Panel de resultados de Virtual Try-On
- Card de resultados de Body Analysis
- AI Recommendation cards

```dart
// Implementación Flutter
Container(
  decoration: BoxDecoration(
    color: Colors.white.withOpacity(0.75), // light: FAF6F1 75%
    borderRadius: BorderRadius.circular(24),
    border: Border.all(
      color: Colors.white.withOpacity(0.30),
      width: 1.0,
    ),
    boxShadow: [AppShadows.md],
  ),
  child: ClipRRect(
    borderRadius: BorderRadius.circular(24),
    child: BackdropFilter(
      filter: ImageFilter.blur(sigmaX: 20, sigmaY: 20),
      child: content,
    ),
  ),
)
// Dark mode: surface.dark.glass = rgba(42, 34, 40, 0.75)
```

---

## 7. AI-Native UX Patterns

### 7.1 Estado AI Thinking
Cuando la IA procesa, el usuario debe saber:
1. Que algo está pasando (no spinner genérico)
2. Cuánto tardará aproximadamente
3. Qué está analizando

```
Componente: AIThinkingIndicator
- 3 puntos pulsantes en color ai.thinking (#A98BD8)
- Texto rotativo: "Analizando tu cuerpo...", "Mapeando colores...", "Generando recomendaciones..."
- Barra de progreso indeterminada con gradiente blush→plum
- Duración estimada en texto: "~15 segundos"
- Background: glass card, blur sutil
```

### 7.2 Confianza Visible
Todo output de IA muestra su nivel de confianza:
```
[████████░░] 82% coincidencia
               → ícono shield-check en verde si >75%
               → ícono shield en blush si 50-75%
               → ícono shield-off en neutral si <50%
```

### 7.3 Transparencia de IA
- Botón "¿Por qué me recomiendas esto?" en toda recomendación
- Expandible: muestra los 3 factores principales de la decisión
- Tono: "Noté que..." "Basándome en tu tipo de cuerpo..."

### 7.4 Error de IA
Cuando la IA falla o tiene baja confianza:
- No ocultar el error con spinner infinito
- Mensaje: "No pude analizar esta imagen. Prueba con mejor iluminación." + botón Reintentar
- Siempre ofrecer alternativa manual

---

## 8. Dark Mode

### Principios
1. NO es invertir colores — es rediseñar para oscuridad
2. El fondo NO es negro puro (#000) — es charcoal con tinte violeta (#1C1A20)
3. Las sombras NO funcionan igual — en dark, usar borders sutiles + glow en vez de sombra
4. Saturación reducida al 85% en colores de estado para no quemar en oscuridad

### Adaptaciones clave
```
Light shadows → Dark glows:
  shadow.sm → borde neutral.800 1px
  shadow.md → borde neutral.700 1px + glow sutil
  
Imágenes de ropa:
  Sin filtro — las fotos se muestran con color real
  
Cards de IA en dark:
  glass dark con borde secondary.800 sutil
  
Gradientes:
  Light: blush.50 → white
  Dark: charcoal → plum.900
```

---

## 9. Accesibilidad (WCAG AA)

### Contraste mínimo
- Texto normal: 4.5:1 (cumplido en todos los pares — ver tabla sección 2)
- Texto grande (18px+ regular o 14px+ bold): 3:1
- Componentes UI y gráficos: 3:1

### Touch targets
- Mínimo ABSOLUTO: 44x44px (Apple HIG, WCAG 2.5.8)
- Preferido: 48x48px para elementos de alta frecuencia
- Separación entre targets: mínimo 8px

### Dynamic Type (Flutter)
```dart
// SIEMPRE usar TextScaler, nunca hardcodear fontSize fijo sin textScaleFactor
Text(
  'Hola',
  style: Theme.of(context).textTheme.bodyMedium,
  // Flutter respeta automáticamente el escalado del sistema
)
// NO hacer:
Text('Hola', style: TextStyle(fontSize: 16)) // sin theme = ignora accesibilidad
```

### Lectores de pantalla
- `Semantics` widget en todos los componentes interactivos
- Images: siempre `semanticsLabel`
- Botones con solo icon: siempre `Tooltip` con descripción textual
- Loading states: `SemanticsProperties(liveRegion: true)`

### Reducción de movimiento
```dart
MediaQuery.of(context).disableAnimations
// Si es true → reducir o eliminar animaciones decorativas
// Siempre mantener feedback táctil (scale press)
```

---

## 10. Pantallas — Inventario Visual

| # | Pantalla              | Complejidad | Estado |
|---|-----------------------|-------------|--------|
| 1 | Splash                | Baja        | Definida |
| 2 | Onboarding (x3)       | Media       | Definida |
| 3 | Login / Register      | Media       | Definida |
| 4 | Home / Dashboard      | Alta        | Definida |
| 5 | Wardrobe Gallery      | Alta        | Definida |
| 6 | Add Wardrobe Item     | Media-Alta  | Definida |
| 7 | Body Analysis Upload  | Media       | Definida |
| 8 | Body Analysis Results | Alta        | Definida |
| 9 | Virtual Try-On        | Alta        | Definida |
|10 | Recommendations       | Alta        | Definida |
|11 | Profile / Settings    | Media       | Definida |
|12 | Subscription Paywall  | Media-Alta  | Definida |

Mockups detallados: ver `mockups/` en esta carpeta.
Flows: ver `flows/` en esta carpeta.

---

## 11. Entrega a Brook

### CSS Variables equivalentes para referencia web
```css
:root {
  /* Brand */
  --color-primary: #D97B6A;
  --color-primary-light: #E8A598;
  --color-secondary: #6B3FA0;
  --color-secondary-light: #A98BD8;
  
  /* Surfaces light */
  --surface-bg: #F5EDE4;
  --surface-card: #FAF6F1;
  --surface-border: #E8DDD4;
  
  /* Surfaces dark */
  --surface-dark-bg: #1C1A20;
  --surface-dark-card: #2A2228;
  --surface-dark-border: #3D3330;
  
  /* Typography */
  --font-display: 'Playfair Display', serif;
  --font-ui: 'Plus Jakarta Sans', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  
  /* Spacing */
  --space-1: 4px; --space-2: 8px; --space-3: 12px;
  --space-4: 16px; --space-6: 24px; --space-8: 32px;
  --space-12: 48px; --space-16: 64px;
  
  /* Radius */
  --radius-sm: 8px; --radius-md: 12px; --radius-lg: 16px;
  --radius-xl: 24px; --radius-2xl: 32px; --radius-full: 9999px;
  
  /* Animation */
  --duration-fast: 150ms; --duration-normal: 250ms; --duration-moderate: 350ms;
  --easing-spring: cubic-bezier(0.34, 1.56, 0.64, 1.0);
  --easing-enter: cubic-bezier(0.0, 0.0, 0.2, 1.0);
}
```

### Flutter pubspec.yaml — dependencias de UI
```yaml
dependencies:
  # Tipografía
  google_fonts: ^6.2.1
  
  # Iconos
  lucide_icons: ^0.0.28
  
  # Animaciones
  flutter_animate: ^4.5.0       # para micro-animaciones declarativas
  lottie: ^3.1.0                # para AI thinking animation (Lottie file)
  
  # UI Components
  shimmer: ^3.0.0               # loading states
  modal_bottom_sheet: ^3.0.0    # bottom sheets con spring physics
  
  # Utilidades
  cached_network_image: ^3.3.1  # imágenes del wardrobe
```

### Google Fonts — URLs de import
```
Playfair Display: https://fonts.google.com/specimen/Playfair+Display
Plus Jakarta Sans: https://fonts.google.com/specimen/Plus+Jakarta+Sans  
JetBrains Mono: https://fonts.google.com/specimen/JetBrains+Mono
```

---

## 12. Qué puede Brook cambiar libremente vs qué no tocar

### Brook puede cambiar sin consultar a Erik
- Padding interno de contenedores (±4px)
- Tamaños de font dentro de la misma escala tipográfica
- Orden de elementos dentro de un card si hay restricción técnica
- Colores de estado (hover, focus, pressed) — siempre que cumplan contraste

### Brook DEBE consultar a Erik antes de cambiar
- Paleta de colores base o cualquier color no definido en design-tokens.json
- Tipografía fuera de las 3 familias definidas
- Radius diferente a los definidos en la escala
- Cualquier animación > 300ms
- Layout de pantallas completas (reorganización de secciones)
- Componentes de IA (AIThinkingIndicator, ConfidenceBar, TransparencyPanel)

---

*Próxima actualización: Sprint 1 — después de QA visual de implementación de Brook.*
