# Mockup 03 — Home / Dashboard
**Viewport:** 375x812px | **Pantalla principal post-login**

---

## Home — Estado con datos (usuario activo)

```
┌─────────────────────────────────────┐
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │  ← Status bar (sistema)
├─────────────────────────────────────┤
│                                     │
│  Buenos días, Camila ✦              │  ← Plus Jakarta 22px semibold
│                                     │     "✦" en primary.400, animated sparkle
│                                     │     neutral.900 / neutral.50
│  ┌─────────────────────────────┐    │  ← AI Daily Tip Card (glass card)
│  │  ✦ Sugerencia de hoy        │    │     border-left: 3px secondary.400
│  │                             │    │     fondo: glass light/dark
│  │  "Con tu color season       │    │     Plus Jakarta 15px, neutral.700
│  │  Warm Autumn, el mostaza    │    │     italic
│  │  y el terracota son tus     │    │     
│  │  mejores aliados esta       │    │
│  │  semana."                   │    │
│  │                             │    │
│  │  [Ver mis colores]          │    │  ← ghost link, secondary.500 14px
│  └─────────────────────────────┘    │
│                                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │  ← Section divider: neutral.200
│                                     │
│  Acciones rápidas                   │  ← Plus Jakarta 18px semibold
│                                     │
│  ┌────────┐ ┌────────┐ ┌────────┐   │  ← Quick Actions Grid (3 col)
│  │   📸   │ │   ✨   │ │   👕   │   │     cards 100x88px, radius 16px
│  │        │ │        │ │        │   │     sombra shadow.sm
│  │Analizar│ │Try-On  │ │Agregar │   │     label Plus Jakarta 12px semibold
│  │cuerpo  │ │prenda  │ │prenda  │   │     icon 28px, primary.500
│  └────────┘ └────────┘ └────────┘   │
│                                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                     │
│  Tu guardarropa    Ver todo →       │  ← Header de sección con CTA
│                                     │     "Ver todo →" primary.500 14px
│  [Añadir  ] ┌─────┐ ┌─────┐ ┌────┐ │  ← Wardrobe Preview horizontal scroll
│  [ prenda ] │ img │ │ img │ │img │ │     primero: Add card (dashed border)
│  [  +     ] └─────┘ └─────┘ └────┘ │     resto: outfit cards 80x100px
│             Blusa   Jeans  Vestido  │     texto debajo: 11px neutral.500
│                                     │     scroll no visible (clean)
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                     │
│  Recomendaciones de hoy             │  ← Header
│                                     │
│  ┌────────────────────────────────┐ │  ← Outfit Recommendation Card
│  │ [Imagen outfit completo]       │ │     ratio 16:9 imagen
│  │                                │ │     height: ~180px
│  │  ────────────────────────────  │ │
│  │  Casual viernes casual ✦ IA    │ │  ← Título + AI badge
│  │  3 prendas de tu guardarropa   │ │     Plus Jakarta 15px semibold
│  │  [🤍] [↗] [Probar →]          │ │  ← Actions: like, share, try-on
│  └────────────────────────────────┘ │
│                                     │
│  [Ver más recomendaciones]          │  ← ghost button, secondary
│                                     │
├─────────────────────────────────────┤
│  [🏠]    [👗]    [✨]    [👤]        │  ← Bottom Nav Bar
│  Inicio   Gardrob Explore Perfil    │  ← height: 64px + safe area bottom
│                                     │     active: primary.500 icon + label
│                                     │     inactive: neutral.400
└─────────────────────────────────────┘
```

---

## Home — Estado vacío (primera sesión)

```
┌─────────────────────────────────────┐
│                                     │
│  Hola, Camila ✦                    │
│  ¡Empecemos!                        │  ← Plus Jakarta 22px semibold
│                                     │
│  ┌─────────────────────────────┐    │
│  │                             │    │  ← Setup Progress Card
│  │  Tu perfil está al 0%       │    │     primary.50 fondo
│  │  [░░░░░░░░░░░░░░░░░░░░░░]  │    │     progress bar primary.500
│  │                             │    │
│  │  Pasos para comenzar:       │    │
│  │                             │    │
│  │  ○ 1. Analiza tu cuerpo     │    │  ← Checklist steps
│  │  ○ 2. Agrega tus primeras   │    │     ○ pendiente (neutral.400)
│  │       5 prendas             │    │     ● completado (success)
│  │  ○ 3. Tu primer outfit IA   │    │
│  │                             │    │
│  │  [Analizar mi cuerpo ahora] │    │  ← primary button dentro del card
│  └─────────────────────────────┘    │
│                                     │
│  ┌─────────────────────────────┐    │  ← Motivational state
│  │  ✦ ¿Sabías que...?          │    │     glass card, secondary border
│  │                             │    │
│  │  Las usuarias de Asesor IA  │    │
│  │  usan 3x más su ropa        │    │
│  │  cuando la organizan.       │    │
│  └─────────────────────────────┘    │
│                                     │
│  [Empezar con mi guardarropa]       │  ← CTA secundario
│                                     │
└─────────────────────────────────────┘
```

---

## Bottom Navigation Bar — Especificación

```
┌──────────────────────────────────────┐
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  │
│  │  🏠  │  │  👗  │  │  ✨  │  │  👤  │  │
│  │      │  │      │  │      │  │      │  │
│  │ Inicio│ │Guardar│ │Explore│ │Perfil│  │
│  └──────┘  └──────┘  └──────┘  └──────┘  │
└──────────────────────────────────────┘
```

**Especificación técnica:**
- Height: 64px + MediaQuery.padding.bottom (safe area)
- Fondo: surface.card con blur 8px (frost efecto sutil)
- Border top: 0.5px neutral.200 (light) / neutral.800 (dark)
- Tab activo: icon primary.500 + label primary.500 12px semibold
- Tab inactivo: icon neutral.400 + label neutral.400 12px regular
- Indicador activo: punto 4px primary.500 debajo del label (NO la barra top que es muy 2018)
- Transición entre tabs: 200ms standard easing
- Touch target por tab: mínimo 80px width × 64px height

**Tabs:**
1. **Inicio** — `home` icon — Dashboard + recomendaciones diarias
2. **Guardarropa** — `shirt` icon — Galería de prendas + colecciones
3. **Explorar** — `sparkles` icon — Virtual Try-On + Body Analysis
4. **Perfil** — `circle-user` icon — Settings + suscripción + historial
