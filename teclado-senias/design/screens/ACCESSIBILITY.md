# ACCESSIBILITY — Guía de Accesibilidad Completa
**Versión:** 1.0 | **Diseñador:** Erik | **Fecha:** 2026-04-08

---

## Contexto Crítico

Nuestros usuarios son personas sordomudas. La comunicación es 100% visual. Por lo tanto:

1. Toda información visual DEBE ser clara, grande, legible
2. NO dependemos de sonido para feedback
3. Iconos SIEMPRE acompañados de texto
4. Animaciones SIEMPRE respetarán prefers-reduced-motion
5. Touch targets SIEMPRE 44x44px mínimo (nuestro estándar es 56px)

---

## WCAG 2.1 Level AA Compliance

### Percepción (Perceivable)

1.1 Alternativas de Texto:
- Todo icono interactivo tiene aria-label o label visible
- Imágenes decorativas tienen alt vacio
- Ilustraciones placeholder tienen alt descriptivo

1.3 Adaptabilidad:
- Contenido en orden lógico (HTML/Dart semantic order)
- Instrucciones no dependen solo de color
- Lista de inputs con fieldset/legend

1.4 Distinguibilidad:

Ratios de contraste (WCAG AAA = 7:1 minimo):
- Text primary sobre bg: 14.8:1 ✓
- Primary button sobre blanco: 7.2:1 ✓
- Secondary text sobre bg: 7.1:1 ✓

Tamaño de texto:
- Minimo 16px para texto principal
- 14px aceptable para secundario
- 12px solo para metadata
- Text scaling soporta hasta 200%

---

### Operabilidad (Operable)

2.1 Accesibilidad de Teclado:
- Todos elementos interactivos accesibles con Tab
- Tab order logico (natural reading order)
- No hay keyboard trap
- Focus visible (ring 3px azul)
- Escape key cierra modales
- Enter key dispara botones

2.3 Sin Seizures:
- No animaciones con flash >3 por segundo
- Respeta prefers-reduced-motion
- En Flutter: MediaQuery.of(context).disableAnimations

2.5 Input Modalities:
- Touch targets 44x44px minimo
- Labels visibles (no solo placeholders)
- Ayuda inline para campos requeridos

---

### Comprensibilidad (Understandable)

3.1 Legibilidad:
- Lenguaje claro, simple
- Frases cortas
- Textos de ayuda visibles
- Instrucciones claras

3.3 Asistencia:
- Labels visibles para cada input
- Error messages especificos
- Sugerencias de correccion
- Confirmacion antes acciones irreversibles

---

### Robustez (Robust)

4.1 Compatibilidad:
- HTML semantico valido
- Roles ARIA correctos
- Atributos accesibles
- iOS VoiceOver compatible
- Android TalkBack compatible

---

## Screen Reader (iOS VoiceOver / Android TalkBack)

**LOGIN screen:**
- Email label: "Email, campo requerido"
- Password label: "Contraseña, campo requerido"
- Login button: "Ingresar a la aplicacion"

**HOME screen:**
- Chip container: "Categorias de senias"
- Sign card: "Senia: {nombre}, categoria {cat}, dificultad {level}"
- Bottom nav: "Navegacion principal"

**Key implementations:**
- aria-label para todos elementos sin visible text
- aria-pressed para toggles
- aria-live=polite para cambios dinamicos
- role=alert para mensajes de error

---

## Dark Mode & Vision Accessibility

### Alto Contraste
- Dark mode implementado en DESIGN_SYSTEM.md
- Colores vibrantes en dark mode

### Daltonismo
- Nunca usar solo rojo/verde
- Siempre acompañar color con icono/texto/forma
- Example: Success + verde + checkmark (no solo verde)

### Zoom & Text Scaling
- Flutter: MediaQuery.textScaleFactor
- Soporta hasta 200% zoom sin romper layout

---

## Video & Notificaciones

### Video Content
- Videos actualmente sin audio (son visuales = perfecto)
- Futuro: agregar captions si hay narración
- Usar formato H.264/MP4 (universal support)

### Notificaciones
- NO usar sonido
- Toast visual con:
  - Color distintivo
  - Icono + texto
  - Duracion 4 segundos minimo
  - Position: top o bottom visible

---

## Testing Checklist

**Keyboard:**
- [ ] Tab order correcto
- [ ] Focus ring visible
- [ ] Escape cierra modales
- [ ] Enter/Space dispara botones

**Vision:**
- [ ] Contrast ratios verificados
- [ ] Text 200% zoom no rompe layout
- [ ] Sin dependencia en color solo
- [ ] Iconos tienen labels

**Motor:**
- [ ] Touch targets 44x44px minimo
- [ ] Sin tiempo limite para interacciones
- [ ] Gestos alternos disponibles

**Screen Readers:**
- [ ] iOS VoiceOver navega todos las pantallas
- [ ] Android TalkBack interpreta correctamente
- [ ] Labels y hints claros
- [ ] Errores anunciados

---

## References

- WCAG 2.1: https://www.w3.org/WAI/WCAG21/quickref/
- Flutter A11y: https://flutter.dev/docs/development/accessibility-and-localization/accessibility

---

*Erik | Design System v1.0 | 2026-04-08*
