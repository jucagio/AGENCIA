# SIGN_DETAIL — Detalle de Seña
**Versión:** 1.0 | **Diseñador:** Erik | **Fecha:** 2026-04-08

---

## Propósito
Mostrar una seña en detalle. Video, descripción, categoría, botones de acción (favorito, compartir).

---

## Layout
```
SafeArea Top
├── Header:
│   ├── Back arrow (24x24px, left)
│   ├── Favorite heart icon (24x24px, right)
│   └── Share icon (24x24px, right)
├── Video player:
│   ├── 343px × 343px (square, centrado)
│   ├── Video thumb con play overlay
│   ├── Controls: play, pause, replay, speed selector
│   └── Progress bar (100% width)
├── Sign info:
│   ├── Nombre (text-h2, 24px SemiBold)
│   ├── Categoría (chip, filtered state)
│   ├── Difficulty dots (1-5 stars)
│   └── Descripción (text-body, 16px)
├── Related signs:
│   ├── "Señas similares" (text-h3)
│   └── Horizontal scroll cards (165px)
├── Bottom nav (80px)
SafeArea Bottom
```

---

## Componentes

| Componente | Especificación |
|-----------|----------------|
| Video player | 343x343px, custom player con controls |
| Favorite button | Heart icon 24x24px, toggle filled/outlined |
| Share button | Share icon 24x24px, opens share sheet |
| Category chip | Filled #0066FF, text-body-sm |
| Difficulty dots | 5-dot indicator + text label |
| Description | text-body (16px) max 300 chars |
| Related cards | Horizontal scroll 165x180px |

---

## Estados

1. **Loading:** Skeleton video + text placeholders
2. **Loaded:** Video player ready, info visible
3. **Favorite toggled:** Heart filled/outlined, animation heart-beat
4. **Sharing:** Native share sheet (iOS/Android)

---

## Interacciones

**Video player:**
- Tap center → play/pause
- Tap progress bar → seek
- Speed button → menu (1x, 1.5x, 2x)
- Replay button → restart from 0

**Favorite button:**
- Tap → toggle favorite
- Animation: scale(1.2) heart-beat 300ms
- POST /api/v1/favorites (add/remove)

**Share button:**
- Tap → native share sheet
- Preset message: "Aprende a hacer esta seña..."

**Related signs:**
- Tap card → navigate → SIGN_DETAIL/{id}
- Horizontal scroll smooth

**Back button:**
- Tap → pop navigation

---

## Accesibilidad (WCAG AA)

- **Video:** aria-label="Video de la seña {nombre}"
- **Controls:** Semantic buttons con aria-label
- **Difficulty:** text-caption + visual dots
- **Description:** text-body 16px mínimo
- **Focus:** Ring 3px #0066FF

---

## Animations

- **Fade in:** 250ms ease-out
- **Video load:** skeleton fade → video fade 250ms
- **Favorite toggle:** heart-beat scale 300ms
- **Share sheet:** slide up 250ms
- **Related cards:** scroll smooth

---

## Dark Mode

- Background: #111827
- Video bg: #1F2937
- Text: #F9FAFB
- Category chip: #3B82F6
- Hearts: #EF4444

---

## Testing Checklist

- [ ] Video player loads correctamente
- [ ] Play/pause funciona
- [ ] Seek en progress bar funciona
- [ ] Speed selector funciona
- [ ] Replay resets video
- [ ] Favorite toggle funciona (POST /api)
- [ ] Heart animation plays
- [ ] Share sheet opens (native)
- [ ] Related signs load y scroll
- [ ] Back button navegation funciona
- [ ] Dark mode aplicado
- [ ] Focus ring visible
- [ ] Screen reader funcional

---

*Erik | Design System v1.0 | 2026-04-08*
