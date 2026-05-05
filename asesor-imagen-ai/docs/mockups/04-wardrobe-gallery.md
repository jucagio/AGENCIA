# Mockup 04 — Wardrobe Gallery
**Viewport:** 375x812px | **Tab: Guardarropa**

---

## Wardrobe Gallery — Vista principal

```
┌─────────────────────────────────────┐
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │  ← Status bar
├─────────────────────────────────────┤
│                                     │
│  Mi Guardarropa          [+ Agregar]│  ← NavBar de pantalla
│                                     │     "Mi Guardarropa": Plus Jakarta 24px semibold
│  42 prendas                         │     "42 prendas": 14px neutral.500
│                                     │     "+ Agregar": button primary, sm height 36px
│  ┌────────────────────────────────┐ │  ← Search bar
│  │  🔍  Buscar por prenda...      │ │     filled input, 44px height
│  └────────────────────────────────┘ │     trailing: filter icon (sliders-horizontal)
│                                     │
│  ─  Todas  Tops  Bottoms  Vestidos  │  ← Category filter chips
│     Zapatos  Accesorios  +          │     horizontal scroll
│                                     │     chip activo: primary.500 bg, white text
│                                     │     chip inactivo: neutral.100 bg, neutral.700 text
│  ┌────────────┐  ┌────────────┐     │
│  │            │  │            │     │  ← Grid 2 columnas
│  │  [imagen]  │  │  [imagen]  │     │     cada card: 160x200px
│  │            │  │            │     │     radius: 16px
│  │ 🤍  ┌───┐  │  │ 🤍  ┌───┐  │     │     gap: 12px
│  │     │✦AI│  │  │     │✦AI│  │     │     padding: 20px horizontal
│  │     └───┘  │  │     └───┘  │     │
│  │            │  │            │     │
│  │ Blusa floral│  │ Jeans slim │     │  ← Nombre prenda: 13px semibold
│  │ Zara · S   │  │ H&M · 28   │     │  ← Marca + talla: 11px neutral.500
│  └────────────┘  └────────────┘     │
│                                     │
│  ┌────────────┐  ┌────────────┐     │  ← Segunda fila
│  │            │  │            │     │
│  │  [imagen]  │  │  [imagen]  │     │
│  │            │  │            │     │
│  │ 🤍          │  │ 🤍  ┌───┐  │     │
│  │            │  │     │✦AI│  │     │
│  │            │  │     └───┘  │     │
│  │ Vestido    │  │ Blazer     │     │
│  │ negro      │  │ camel      │     │
│  └────────────┘  └────────────┘     │
│                                     │
│         (scroll continúa)           │
│                                     │
├─────────────────────────────────────┤
│  [🏠]  [👗●] [✨]  [👤]             │
└─────────────────────────────────────┘
```

**Anatomía de cada Wardrobe Card:**
```
┌────────────────────────────┐
│                            │  Imagen: top 75% de la card
│                            │  object-fit: cover
│       [imagen prenda]      │  background: neutral.100 (placeholder)
│                            │
│ 🤍                    ✦AI  │  ← Floating actions sobre imagen
│                            │     🤍 = favorite (top-left 36x36 touch)
├────────────────────────────┤     ✦AI = etiqueta si fue analizada por IA
│ Nombre prenda              │     badge secondary, 28px height
│ Marca · Talla              │
└────────────────────────────┘

Touch target de toda la card → abre item detail bottom sheet
Long press → selection mode (checkboxes aparecen para bulk actions)
```

**AI Badge:**
- Solo aparece si la prenda fue analizada por IA y tiene tags automáticos
- Fondo: gradient secondary.500 → primary.500
- Texto "✦IA", 10px, white, bold
- Posición: top-right sobre la imagen, 8px de margen

---

## Wardrobe Gallery — Selection Mode (bulk actions)

```
┌─────────────────────────────────────┐
│  ✕  3 seleccionadas       [Mover ▾] │  ← TopBar cambia
│                            [Borrar] │     X para cancelar, cuenta, acciones
│                                     │
│  [✓] ┌────────┐  [ ] ┌────────┐    │  ← Checkboxes en esquina top-left
│      │  img   │      │  img   │    │     ✓ = seleccionada (primary.500 bg)
│      │   ✓    │      │        │    │
│      └────────┘      └────────┘    │
│                                     │
│  [✓] ┌────────┐  [✓] ┌────────┐    │
│      │  img   │      │  img   │    │
│      │   ✓    │      │   ✓    │    │
│      └────────┘      └────────┘    │
│                                     │
├─────────────────────────────────────┤
│  [Crear outfit]  [Mover colección]  │  ← Bottom action bar emerge
│                                     │     slide-up 200ms
└─────────────────────────────────────┘
```

---

## Wardrobe Gallery — Estado vacío

```
┌─────────────────────────────────────┐
│  Mi Guardarropa          [+ Agregar]│
│                                     │
│  0 prendas                          │
│                                     │
│                                     │
│         [ILUSTRACIÓN]               │  ← Ilustración: percha vacía
│                                     │     style: línea limpia, colores brand
│                                     │
│  Tu guardarropa está vacío          │  ← Plus Jakarta 22px semibold
│                                     │
│  Agrega tus primeras prendas        │  ← Plus Jakarta 15px neutral.500
│  para que la IA empiece a          │
│  sugerirte outfits.                 │
│                                     │
│  ┌─────────────────────────────┐    │
│  │  + Agregar primera prenda   │    │  ← primary button large
│  └─────────────────────────────┘    │
│                                     │
│  [Importar desde fotos]             │  ← secondary ghost button
│                                     │
└─────────────────────────────────────┘
```

---

## Filter Bottom Sheet

```
┌─────────────────────────────────────┐
│              ──────                 │  ← Handle
│                                     │
│  Filtrar prendas            [Reset] │
│                                     │
│  Categoría                          │
│  ┌─────┐ ┌─────┐ ┌────────┐         │  ← Multi-select chips
│  │Tops │ │Faldas│ │Vestidos│         │     tap para toggle
│  └─────┘ └─────┘ └────────┘         │
│  ┌────────┐ ┌──────────┐             │
│  │Pantalón│ │Accesorios│             │
│  └────────┘ └──────────┘             │
│                                     │
│  ── Colores ──                       │
│  ● ● ● ● ● ● ●                      │  ← Color swatches: 32x32px circles
│  (blanco negro rojo azul...)         │     seleccionado: borde primary.500 2px
│                                     │
│  ── Talla ──                         │
│  ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐            │
│  │XS│ │ S│ │ M│ │ L│ │XL│            │
│  └──┘ └──┘ └──┘ └──┘ └──┘            │
│                                     │
│  ── Analizada por IA ──              │
│  [        ○━━━━━━━━━━━━━━━━      ] │  ← Toggle switch
│                                     │
│  ┌─────────────────────────────┐    │
│  │      Aplicar filtros        │    │
│  └─────────────────────────────┘    │
│                                     │
└─────────────────────────────────────┘
```
