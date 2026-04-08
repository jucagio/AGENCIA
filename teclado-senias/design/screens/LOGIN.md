# LOGIN — Pantalla de Acceso
**Versión:** 1.0 | **Diseñador:** Erik | **Fecha:** 2026-04-08

---

## Propósito
Pantalla inicial de autenticación. Usuarios ingresan email + contraseña para acceder a la aplicación.

---

## Layout
- **Viewport:** 375px ancho (mobile base design)
- **Padding horizontal:** 16px izq/der
- **Logo:** 80x80px, centrado, 24px desde safe area top
- **Inputs:** 56px height, 24px gap vertical, 343px width
- **Botón:** 56px height, 12px radius, 100% width
- **Links:** 44px min touch height

---

## Componentes Utilizados

| Componente | Especificación |
|-----------|----------------|
| Logo | Custom SVG 80x80px |
| Email Input | text-input, validación email |
| Password Input | text-input + icon toggle visibility |
| Botón Ingresar | primary-lg, disabled hasta ambos campos válidos |
| Links | ghost buttons ("Olvidé contraseña", "Crear cuenta") |

---

## Estados

1. **Vacío:** Inputs idle, botón disabled, sin errores
2. **Llenando:** Validación en tiempo real, botón enabled si email válido + pwd 3+ chars
3. **Email Inválido:** Border #EF4444, helper text rojo, shadow-focus-error
4. **Cargando:** Botón + spinner, inputs disabled, "INGRESANDO..."
5. **Error Login:** Toast rojo "Credenciales inválidas", 4s auto-dismiss
6. **Focus:** Border #0066FF, shadow-focus, highlight azul

---

## Interacciones

```
Tab 1:      Email input → focus
Tab 2:      Visibility toggle → click
Tab 3:      Password input → focus
Tab 4:      "Olvidé contraseña" → navigate
Tab 5:      Botón INGRESAR → click/submit
Tab 6:      "Crear cuenta" → navigate
```

**Validación:**
- Email: onBlur, patrón ^[^\s@]+@[^\s@]+\.[^\s@]+$
- Password: min 8 chars (backend validation)
- Botón habilitado si email válido Y password tiene 3+ chars

**Flujo éxito:**
1. POST /auth/login (email, password)
2. Si 200: guardar JWT, fade → HOME
3. Si 401: toast error, limpiar password, volver a idle

---

## Accesibilidad (WCAG AA)

- **Text mínimo:** 16px (inputs, botones) ✓
- **Touch targets:** 44x44px mínimo ✓
- **Contrast:** #0066FF sobre blanco = 7.2:1 (AAA) ✓
- **Focus ring:** 3px #0066FF visible sin zoom ✓
- **Screen reader:** Labels semánticas, alerts para errores
- **Motion:** Respetar prefers-reduced-motion

---

## Animaciones

- **Fade in:** 250ms ease-out (entrada pantalla)
- **Button press:** 150ms scale(0.97)
- **Focus ring:** 150ms ease-out
- **Password toggle:** 150ms rotate + color change
- **Toast error:** 250ms slide up, 4s duration, auto-exit

---

## Dark Mode

- Background: #111827
- Inputs: #1F2937 (background), #374151 (border)
- Text: #F9FAFB
- Primary button: #3B82F6 (más claro para contraste)

---

## Testing Checklist

- [ ] Email validation funciona (válido/inválido)
- [ ] Password visibility toggle funciona
- [ ] Botón deshabilitado hasta campos válidos
- [ ] POST /auth/login callema correctamente
- [ ] Toast error en credenciales inválidas
- [ ] Keyboard emerge en iOS/Android
- [ ] Focus indicators visibles
- [ ] Dark mode aplicado
- [ ] Responsive 375px/414px/768px
- [ ] Screen reader funcional
- [ ] Touch targets 44x44px mínimo

---

*Erik | Design System v1.0 | 2026-04-08*
