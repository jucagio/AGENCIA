# SEARCH — Búsqueda de Señas
**Versión:** 1.0 | **Diseñador:** Erik | **Fecha:** 2026-04-08

---

## Propósito
Full-screen search experience. Usuarios buscan señas por texto y filtran por categoría.

---

## Layout
```
SafeArea Top
├── Header:
│   ├── Back arrow (24x24px)
│   ├── Search input (full-width, 52px)
│   │   └── Placeholder: "Busca una seña..."
│   └── Clear button (X icon, si input filled)
├── Filters (sticky):
│   └── Horizontal chips (32px height)
│       ├── "Todas" (default active)
│       ├── "Saludo"
│       ├── "Números"
│       └── ...
├── Results section:
│   ├── "XX resultados encontrados" (si > 0)
│   ├── Grid 2-columnas (sign cards 165px)
│   │   └── Cards (video thumb, nombre, difficulty)
│   └── "No hay resultados" (si == 0)
├── Bottom nav (80px)
SafeArea Bottom
```

---

## Componentes

| Componente | Especificación |
|-----------|----------------|
| Search input | 52px height, text-input, magnifying icon left |
| Category filters | Chips 32px height, autoscroll horizontal |
| Result cards | Grid 2-col, 165x180px sign cards |
| Result counter | text-body-sm (#6B7280) |
| No results | Text + illustration placeholder |
| Clear button | (X) icon 24x24px trailing del input |

---

## Estados

1. **Empty query:** Mostrar frecuentes (recent searches o trending)
2. **Typing:** Results update en tiempo real (debounced 300ms)
3. **Loading:** Skeleton grid mientras se busca
4. **Results found:** Grid con cards, contador
5. **No results:** Mensaje "No encontramos señas con ese nombre"

---

## Interacciones

**Search input:**
- onChange → debounced GET /api/v1/signs/search?q={query} (300ms delay)
- onClear (X button) → limpiar input, volver a empty state

**Category filter:**
- Tap chip → GET /api/v1/signs/search?q={query}&category={cat}
- Animation fade 150ms

**Result cards:**
- Tap → navigate → SIGN_DETAIL/{id}
- Scale press 150ms

**Back button:**
- Tap → pop navigation, mantener search history

---

## Accesibilidad (WCAG AA)

- **Search input:** aria-label="Buscar señas"
- **Result counter:** aria-live=polite (anunciar cambios)
- **Cards:** Semantically linked to SIGN_DETAIL navigation
- **Focus:** Visible ring 3px #0066FF
- **Text:** 16px mínimo

---

## Animaciones

- **Fade in:** 250ms ease-out
- **Results update:** 150ms fade between grids
- **Skeleton pulse:** 1.5s loop
- **Card press:** 150ms scale(0.97)

---

## Dark Mode

- Background: #111827
- Input: #1F2937
- Cards: #1F2937
- Text: #F9FAFB
- Filter active: #3B82F6

---

## Testing Checklist

- [ ] Search input captures texto correctly
- [ ] Query debounced (300ms) antes de API call
- [ ] Results actualizan en tiempo real
- [ ] Category filters funciona
- [ ] Clear button (X) limpia input
- [ ] Back button navega correctamente
- [ ] Cards tapeables navegan a SIGN_DETAIL
- [ ] No results message display
- [ ] Skeleton loaders muestran
- [ ] Dark mode aplicado
- [ ] Focus ring visible
- [ ] Screen reader funcional

---

*Erik | Design System v1.0 | 2026-04-08*
