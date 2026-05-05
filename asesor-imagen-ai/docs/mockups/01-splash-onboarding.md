# Mockup 01 — Splash Screen + Onboarding (3 pantallas)
**Viewport:** 375x812px | **Safe Area Top:** 44px | **Safe Area Bottom:** 34px

---

## Splash Screen (1/1)

```
┌─────────────────────────────────────┐  375x812
│                                     │
│  ████████████████████████████████   │  ← fondo: neutral.900 dark
│  ████████████████████████████████   │     charcoal #1C1A20
│  ████████████████████████████████   │
│  ████████████████████████████████   │
│                                     │
│                                     │
│                                     │
│         [LOGO ANIMADO]              │  ← Logo: "A" estilizada en Playfair
│                                     │     color: primary.400 #E8A598
│      ✦ Asesor de Imagen             │  ← Playfair Display 32px, bold
│                                     │     color: neutral.50 #FAF6F1
│          Powered by AI              │  ← Plus Jakarta Sans 12px, neutral.500
│                                     │     letter-spacing: 0.10em, uppercase
│                                     │
│                                     │
│                                     │
│       [━━━━━━━━━━━━━━━━━━]          │  ← Loading bar: 
│                                     │     primary.400 sobre neutral.800
│                                     │     animación: fill izq→der, 2s
│                                     │
└─────────────────────────────────────┘
```

**Animación de entrada (750ms total):**
1. Fondo: ya visible
2. Logo: fade + scale (0.8→1.0), duration 400ms, easing enter
3. Texto "Asesor de Imagen": slide-up 12px + fade, delay 200ms, duration 350ms
4. "Powered by AI": fade, delay 400ms, duration 300ms
5. Loading bar: fill inmediato al 100% en 1800ms, luego navigate

**Decisión de diseño:** El splash usa dark mode siempre, independiente de la preferencia del sistema. Establece el carácter premium del producto en el primer segundo.

---

## Onboarding 1 — "Tu stylist personal de IA" 

```
┌─────────────────────────────────────┐
│                                  ⊙  │  ← Skip button: top-right, ghost
│                                     │     Plus Jakarta 14px, neutral.400
│                                     │
│  ┌─────────────────────────────┐    │
│  │                             │    │
│  │    [ILUSTRACIÓN HERO]       │    │  ← Área imagen: 335x380px
│  │                             │    │     Imagen: mujer frente al espejo
│  │  Mujer + silueta IA overlay │    │     con overlay de análisis IA
│  │  Líneas de análisis         │    │     (puntos de análisis en primary.400)
│  │  animadas sobre figura      │    │     Corners radius: 24px
│  │                             │    │
│  └─────────────────────────────┘    │
│                                     │
│  Tu stylist personal                │  ← Playfair Display 40px bold
│  de Inteligencia                    │     neutral.900 (light) / neutral.50 (dark)
│  Artificial                         │     letterSpacing: -0.02em
│                                     │
│  Analiza tu cuerpo, organiza tu     │  ← Plus Jakarta 16px, neutral.600
│  ropa y descubre outfits que        │     lineHeight: 1.5
│  realmente te favorecen.            │
│                                     │
│  ●  ○  ○                           │  ← Dots: page indicator
│                                     │     activo: primary.500 8px
│                                     │     inactivo: neutral.300 6px
│                                     │
│  ┌─────────────────────────────┐    │
│  │       Comenzar →            │    │  ← Button primary, large (56px)
│  └─────────────────────────────┘    │     full width, primary.500
│                                     │
└─────────────────────────────────────┘
```

**Transición entre slides:** slide horizontal con spring physics, drag habilitado.

---

## Onboarding 2 — "Analiza tu tipo de cuerpo"

```
┌─────────────────────────────────────┐
│                                  ⊙  │
│                                     │
│  ┌─────────────────────────────┐    │
│  │                             │    │
│  │   [ILUSTRACIÓN BODY SCAN]   │    │  ← Pantalla del phone en miniatura
│  │                             │    │     mostrando Body Analysis UI
│  │   Silueta con color season  │    │     Colores: blush, warm autumn
│  │   overlay y puntos de       │    │     Scan lines animadas en secondary
│  │   análisis IA               │    │
│  │                             │    │
│  └─────────────────────────────┘    │
│                                     │
│  Conoce tu color season             │  ← Playfair Display 36px bold
│  y tu silueta ideal                 │
│                                     │
│  Sube una foto y en 15 segundos     │  ← Plus Jakarta 16px, neutral.600
│  la IA analiza tu tipo de cuerpo    │
│  y paleta de colores perfecta.      │
│                                     │
│  ┌──────────────────────────────┐   │
│  │  ✦ 98% de precisión          │   │  ← AI Stats card: glass card
│  │  ━━━━━━━━━━━━━━━━ 98%        │   │     secondary.100 bg, secondary border
│  │  Basado en 50k+ análisis     │   │     Plus Jakarta 12px, secondary.700
│  └──────────────────────────────┘   │
│                                     │
│  ○  ●  ○                           │  ← Dots
│                                     │
│  ┌─────────────────────────────┐    │
│  │       Siguiente →           │    │
│  └─────────────────────────────┘    │
│                                     │
└─────────────────────────────────────┘
```

---

## Onboarding 3 — "Virtual Try-On fotorrealista"

```
┌─────────────────────────────────────┐
│                                  ⊙  │
│                                     │
│  ┌─────────────────────────────┐    │
│  │                             │    │
│  │  [BEFORE / AFTER CAROUSEL]  │    │  ← Slider interactivo (drag)
│  │                             │    │     Izquierda: prenda plana
│  │  ←| Prenda |→ Tú con prenda│    │     Derecha: mujer vestida con IA
│  │                             │    │     Divider line draggable
│  │  "Vestida" con prenda en IA │    │     border radius: 24px
│  │                             │    │
│  └─────────────────────────────┘    │
│                                     │
│  Pruébate cualquier prenda          │  ← Playfair Display 36px bold
│  antes de comprarte otra            │
│                                     │
│  ¿Tienes dudas con una prenda?      │  ← Plus Jakarta 16px, neutral.600
│  Pruébatela virtualmente en         │
│  segundos. Sin espejos.             │
│                                     │
│  ┌─────┐  ┌─────┐  ┌─────┐         │  ← 3 mini benefit chips
│  │ 🔴  │  │ ⚡  │  │ 💚  │         │     tags con icons
│  │Gratis│  │ Rápido│  │Realista│  │
│  └─────┘  └─────┘  └─────┘         │
│                                     │
│  ○  ○  ●                           │  ← Dots
│                                     │
│  ┌─────────────────────────────┐    │
│  │      ¡Empezar ya! →         │    │  ← CTA final: primary, large
│  └─────────────────────────────┘    │
│  Iniciar sesión                     │  ← Ghost button, secondary text
│                                     │
└─────────────────────────────────────┘
```

**Notas de interacción:**
- Pantalla 3: el slider before/after es interactivo al drag — primer momento de "magia" antes de registrarse
- El ícono Skip en pantallas 1 y 2 saltea al Login directamente
- Progress dots son también tapeables para navegar libremente
