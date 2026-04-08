# SETTINGS — Configuración
**Versión:** 1.0 | **Diseñador:** Erik | **Fecha:** 2026-04-08

---

## Propósito
Configuración de usuario, preferencias de accesibilidad, logout.

---

## Layout
```
SafeArea Top
├── Header:
│   ├── Back arrow (si viene de HOME)
│   └── Title "Configuración" (text-h1)
├── Profile section:
│   ├── Avatar (80x80px, circular)
│   ├── Name (text-h3)
│   ├── Email (text-body-sm, #6B7280)
│   └── Edit profile button (ghost)
├── Preferences section:
│   ├── "Tamaño de texto" (slider 12px-24px)
│   ├── "Alto contraste" (toggle)
│   ├── "Modo oscuro" (toggle)
│   └── "Notificaciones" (toggle)
├── About section:
│   ├── "Versión de la app" (text-caption)
│   ├── "Términos y condiciones" (link)
│   └── "Política de privacidad" (link)
├── Logout button (destructive, red)
├── Bottom nav (80px)
SafeArea Bottom
```

---

## Componentes

| Componente | Especificación |
|-----------|----------------|
| Profile section | Avatar 80x80px + nombre + email |
| Text size slider | Range 12px-24px, live preview |
| Toggles | High contrast, Dark mode, Notifications |
| Links | Terms, Privacy (open in modal/web) |
| Logout button | destructive-lg (56px), red (#EF4444) |

---

## Estados

1. **Default:** Mostrar perfil actual, toggles en estado actual
2. **Saving:** Spinner en toggle durante save
3. **Saved:** Toast "Cambios guardados"
4. **Text size preview:** Live update de labels

---

## Interacciones

**Edit profile:**
- Tap → navigate → /settings/edit-profile (future)

**Text size slider:**
- Drag 12px-24px
- Live preview de sample text
- onChange → POST /api/v1/settings (save)

**Toggles:**
- Tap → toggle on/off
- onChange → POST /api/v1/settings/{key} (save immediately)

**Logout:**
- Tap → confirm dialog "¿Cerrar sesión?"
  - Cancel → close
  - Confirm → DELETE /auth/logout, clear JWT, navigate → LOGIN

**Links (Terms, Privacy):**
- Tap → open web view o modal (Future)

---

## Accesibilidad (WCAG AA)

- **Profile:** aria-label per field
- **Toggles:** aria-label="Alto contraste", aria-pressed={state}
- **Slider:** aria-label="Tamaño de texto", aria-valuenow={value}
- **Logout:** aria-label="Cerrar sesión", role=button
- **Text:** 16px mínimo
- **Focus:** Ring 3px #0066FF

---

## Animations

- **Fade in:** 250ms ease-out
- **Toggle animation:** 150ms scale + color
- **Slider:** smooth native
- **Text preview:** 100ms opacity transition
- **Toast:** 250ms slide up, 3s duration

---

## Dark Mode

- Background: #111827
- Sections: #1F2937
- Text: #F9FAFB
- Toggle active: #3B82F6
- Logout button: #EF4444

---

## Testing Checklist

- [ ] Profile info loads correctamente
- [ ] Edit profile navegation funciona (future)
- [ ] Text size slider funciona (12-24px)
- [ ] Live preview actualiza
- [ ] POST /api/v1/settings callema al cambiar
- [ ] Toggles (contrast, dark mode, notifications) funcionan
- [ ] Settings persisten entre sesiones
- [ ] Logout confirm dialog muestra
- [ ] Logout realmente clears JWT
- [ ] Navigate a LOGIN después logout
- [ ] Terms/Privacy links funcionan (future)
- [ ] Dark mode aplicado
- [ ] Focus ring visible
- [ ] Responsive 375px/414px/768px

---

*Erik | Design System v1.0 | 2026-04-08*
