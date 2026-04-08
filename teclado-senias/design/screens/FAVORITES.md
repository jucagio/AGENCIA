# FAVORITES — Mis Favoritos
**Versión:** 1.0 | **Diseñador:** Erik | **Fecha:** 2026-04-08

---

## Propósito
Mostrar todas las señas que el usuario ha marcado como favoritas.

---

## Layout
```
SafeArea Top
├── Header:
│   ├── Title "Mis Favoritos" (text-h1)
│   └── Sort button (dropdown, futuro)
├── Empty state (si no hay favoritos):
│   ├── Illustration (corazón vacío)
│   ├── "No tienes señas favoritas" (text-h2)
│   └── "Crea tu primera..." (text-body-sm)
├── Favorites grid:
│   ├── Sort option (dropdown):
│   │   ├── "Reciente"
│   │   ├── "Alfabético"
│   │   └── "Por categoría"
│   └── Grid 2-columnas (165x180px sign cards)
│       └── Cards tapeables con delete swipe
├── Bottom nav (80px)
SafeArea Bottom
```

---

## Componentes

| Componente | Especificación |
|-----------|----------------|
| Header | Title "Mis Favoritos" text-h1 |
| Empty state | Illustration + texto centered |
| Sort dropdown | Text-button, chevron icon |
| Sign cards | 165x180px, video thumb, nombre, difficulty |
| Delete action | Swipe left → reveal delete button, o long-press menu |
| Bottom nav | 4 items, Favorites active |

---

## Estados

1. **Empty:** No hay favoritos, mostrar empty state
2. **Loaded:** Grid con cards, sort dropdown enabled
3. **Deleting:** Card swipe-left → reveal delete button
4. **Deleted:** Toast "Eliminado de favoritos", remove card from grid

---

## Interacciones

**Sort dropdown:**
- Tap → show menu (Reciente, Alfabético, Por categoría)
- Tap option → sort grid, animation fade 150ms

**Sign cards:**
- Tap → navigate → SIGN_DETAIL/{id}
- Scale press 150ms

**Delete action:**
- Swipe left → reveal red delete button (100% height)
- Tap delete → confirm dialog "¿Eliminar?"
  - Cancel → close swipe
  - Confirm → DELETE /api/v1/favorites/{sign_id}
  - Toast éxito, remove card
- Or: long-press context menu (Future)

---

## Accesibilidad (WCAG AA)

- **Header:** aria-label="Mis señas favoritas"
- **Cards:** Linked to SIGN_DETAIL, aria-label per card
- **Sort:** aria-label="Ordenar mis favoritos"
- **Delete:** Confirm dialog (role=alert, aria-live=assertive)
- **Focus:** Ring 3px #0066FF visible

---

## Animations

- **Fade in:** 250ms ease-out
- **Grid reorder (sort):** 150ms fade
- **Card press:** 150ms scale(0.97)
- **Swipe delete:** 200ms slide-out red background
- **Card remove:** 150ms scale(0) + fade

---

## Dark Mode

- Background: #111827
- Cards: #1F2937
- Text: #F9FAFB
- Delete button: #EF4444
- Sort button: #3B82F6

---

## Testing Checklist

- [ ] Empty state display correcto (sin favoritos)
- [ ] Favoritos load en grid 2-col
- [ ] Cards tapeables navegan a SIGN_DETAIL
- [ ] Sort dropdown abre y cambia orden
- [ ] Swipe left revela delete button
- [ ] Delete con confirm dialog funciona
- [ ] POST DELETE /api/v1/favorites/{id} callema
- [ ] Card removed from grid después delete
- [ ] Toast éxito después delete
- [ ] Back to empty state si último item deleted
- [ ] Dark mode aplicado
- [ ] Focus ring visible
- [ ] Responsive 375px/414px/768px

---

*Erik | Design System v1.0 | 2026-04-08*
