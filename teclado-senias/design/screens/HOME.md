# HOME — Pantalla Principal
**Versión:** 1.0 | **Diseñador:** Erik | **Fecha:** 2026-04-08

---

## Propósito
Pantalla principal post-login. Usuarios ven categorías, señas populares, búsqueda rápida.

---

## Layout
```
SafeArea Top
├── Header:
│   ├── Logo/Title (16px left)
│   └── Settings icon (24x24px, right 16px)
├── Search bar (búsqueda rápida, sticky top)
│   └── Placeholder: "Busca una seña..."
├── "Categorías" section:
│   └── Horizontal scroll chips (32px height)
│       ├── "Todas" (active: #0066FF bg)
│       ├── "Saludo"
│       ├── "Números"
│       ├── "Emociones"
│       └── ...
├── "Señas Populares" section:
│   └── Grid 2-columnas, cards 165px width
│       ├── Sign card (video thumb, nombre, difficulty dots)
│       ├── Sign card
│       └── ...
├── Bottom Nav (80px, 4 items):
│   ├── Home (active: #0066FF)
│   ├── Search
│   ├── Favorites (heart)
│   └── Settings (gear)
SafeArea Bottom
```

---

## Componentes

| Componente | Especificación |
|-----------|----------------|
| Header | Logo left, settings icon right |
| Search bar | 52px height, search-input con lupa icon |
| Category chips | 32px height, filled/outlined, auto-scroll |
| Sign cards | 165x180px, video thumb, nombre, dots |
| Bottom nav | 80px, 4 items, active indicator |
| Empty state | Splash si no hay datos |

---

## Estados

1. **Loading:** Skeleton loaders en cards grid
2. **Loaded:** Cards mostradas, categorías disponibles
3. **Empty:** "No hay señas en esta categoría"
4. **Filtered:** Cambiar categoría → grid refiltra, animation fade

---

## Interacciones

**Search bar:**
- Tap → navigate → SEARCH screen (full-screen search)
- Placeholder dinámico sugiriendo búsquedas populares

**Category chips:**
- Tap → filtrar grid, animation fade 150ms
- Horizontal scroll si overflow

**Sign card:**
- Tap → navigate → SIGN_DETAIL
- Long press → context menu (compartir, agregar favorito) (Future)
- Press animation: scale(0.97) 150ms

**Settings icon:**
- Tap → navigate → SETTINGS

**Bottom nav:**
- Smooth transition entre pantallas, fade 250ms
- Active indicator (3px bar) se mueve suave

---

## Accesibilidad (WCAG AA)

- **Text mínimo:** 16px para títulos, 14px para chips
- **Touch targets:** 44x44px (nav 56px per item) ✓
- **Cards:** 165px × 165px ✓
- **Focus ring:** Visible en todos los elementos interactivos
- **Labels:** "Popular signsection", "Category filter"
- **Live region:** Anunciar cuando se filtra

---

## Animaciones

- **Fade in:** 250ms ease-out
- **Category filter:** Grid fade 150ms, chips scroll smooth
- **Card press:** Scale 0.97 150ms
- **Bottom nav:** Fade 250ms entre pantallas
- **Skeleton pulse:** 1.5s opacity loop

---

## Dark Mode

- Background: #111827
- Cards: #1F2937
- Text: #F9FAFB
- Active button: #3B82F6
- Inactive text: #9CA3AF

---

## Testing Checklist

- [ ] Categorías se cargan correctamente
- [ ] Filtrar por categoría funciona
- [ ] Señas populares muestran en grid 2-col
- [ ] Search bar navega a SEARCH
- [ ] Settings icon navega a SETTINGS
- [ ] Bottom nav switching funciona
- [ ] Cards tapeable y navegan a SIGN_DETAIL
- [ ] Skeleton loaders muestran durante carga
- [ ] Empty state display correcto
- [ ] Dark mode aplicado
- [ ] Focus ring visible
- [ ] Responsive 375px/414px/768px

---

*Erik | Design System v1.0 | 2026-04-08*
