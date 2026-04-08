# REGISTER — Pantalla de Registro
**Versión:** 1.0 | **Diseñador:** Erik | **Fecha:** 2026-04-08

---

## Propósito
Crear nueva cuenta. Usuarios ingresan nombre, email, contraseña, confirman contraseña.

---

## Layout
- **Logo:** 80x80px centrado, 24px top
- **Título:** "Crear Cuenta", text-h2 (24px, SemiBold), 24px margin-bottom
- **Campos:**
  - Nombre (text-input 56px)
  - Email (email-input 56px)
  - Contraseña (password-input 56px con toggle)
  - Confirmar Contraseña (password-input 56px con toggle)
  - Spacing: 16px entre campos
- **Checkbox:** Términos y Condiciones (44px height)
- **Botón:** CREAR CUENTA, 56px, disabled si:
  - Nombre vacío
  - Email inválido
  - Password < 8 chars
  - Passwords no coinciden
  - Términos no aceptados
- **Link:** "¿Ya tienes cuenta? INGRESAR"

---

## Componentes

| Componente | Especificación |
|-----------|----------------|
| Inputs | 4x text-input (nombre, email, pwd, pwd-confirm) |
| Checkbox | 24x24px + label "Acepto términos y privacidad" |
| Botón | primary-lg, disabled/enabled estados |
| Links | "Terms" y "Privacy" abiertos en modal o web |

---

## Validaciones

- **Nombre:** 2-50 caracteres, no números, no caracteres especiales
- **Email:** RFC 5322 pattern
- **Contraseña:** 8+ chars, puede incluir cualquier carácter
- **Confirmar:** debe coincidir exactamente con contraseña
- **Términos:** debe estar checked

**Feedback visual:**
- Helper text rojo si validación falla
- Border #EF4444 en campo inválido
- Check verde en campo válido (opcional)

---

## Interacciones

**Flujo éxito:**
1. Llenar todos los campos válidos
2. Check términos
3. Tap CREAR CUENTA
4. POST /auth/register (nombre, email, password)
5. Si 201: toast éxito, navigate → LOGIN (pre-filled email)
6. Si 400 (email existe): toast error, no limpiar campos

**Validación en tiempo real:**
- onBlur para email (verificar formato)
- onChange para password confirm (verificar coincidencia)
- onChange para checkbox (enable/disable botón)

---

## Accesibilidad (WCAG AA)

- **Text mínimo:** 16px
- **Touch targets:** 44x44px (checkbox 24x24 + padding)
- **Contrast ratios:** WCAG AAA para texto
- **Focus:** Ring 3px #0066FF visible
- **Screen reader:** fieldset por sección, labels semánticas

---

## Animaciones

- **Fade in:** 250ms ease-out
- **Field validation:** 150ms color/border transition
- **Checkbox toggle:** 150ms scale + rotate check mark
- **Button press:** 150ms scale(0.97)
- **Success toast:** 250ms slide up, 3s duration

---

## Dark Mode

- Background: #111827
- Inputs: #1F2937
- Text: #F9FAFB
- Borders: #374151
- Primary button: #3B82F6

---

## Testing Checklist

- [ ] Nombre validation (2-50 chars, no números)
- [ ] Email validation (RFC 5322)
- [ ] Password strength (8+ chars)
- [ ] Password confirm match funciona
- [ ] Términos checkbox required
- [ ] Botón deshabilitado si algún campo inválido
- [ ] POST /auth/register callema
- [ ] Toast éxito después de registro
- [ ] Navigate a LOGIN pre-filled email
- [ ] Toast error si email ya existe
- [ ] Dark mode aplicado
- [ ] Focus ring visible
- [ ] Screen reader funcional

---

*Erik | Design System v1.0 | 2026-04-08*
