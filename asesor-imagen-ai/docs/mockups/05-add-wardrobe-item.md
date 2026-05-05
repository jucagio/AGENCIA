# Mockup 05 — Add Wardrobe Item
**Viewport:** 375x812px | **Camera + Form + AI tagging**

---

## Add Item — Entry Point (Bottom Sheet desde galería)

```
┌─────────────────────────────────────┐
│              ──────                 │  ← Handle
│                                     │
│  Agregar prenda                     │  ← Plus Jakarta 22px semibold
│                                     │
│  ┌───────────────────────────────┐  │  ← Source selector
│  │                               │  │     3 opciones en tarjetas
│  │  ┌───────┐  ┌───────┐  ┌───┐  │  │
│  │  │  📸   │  │  🖼   │  │🌐 │  │  │
│  │  │Cámara │  │Galería│  │URL│  │  │
│  │  └───────┘  └───────┘  └───┘  │  │     cada opción: 96x88px card
│  └───────────────────────────────┘  │     icon 28px + label 12px semibold
│                                     │     tap → acción correspondiente
│  ── O arrastra una imagen aquí ──   │  ← Drag & drop zone (tablet futuro)
│  ┌───────────────────────────────┐  │     border dashed neutral.300
│  │                               │  │     radio: 16px
│  │   Arrastra una imagen aquí    │  │     neutral.400 text
│  │         o toca arriba         │  │
│  └───────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
```

---

## Add Item — Camera Screen

```
┌─────────────────────────────────────┐
│ ✕                        [Galería]  │  ← NavBar transparente
│                                     │     sobre el viewfinder
│                                     │
│  ╔═════════════════════════════╗    │
│  ║                             ║    │
│  ║                             ║    │  ← Camera viewfinder
│  ║    ┌ ─ ─ ─ ─ ─ ─ ─ ─ ┐     ║    │     full screen
│  ║    |                   |    ║    │     guide frame: 240x300px
│  ║    |   [Centra aquí    |    ║    │     dashed primary.300
│  ║    |    tu prenda]     |    ║    │
│  ║    |                   |    ║    │
│  ║    └ ─ ─ ─ ─ ─ ─ ─ ─ ┘     ║    │
│  ║                             ║    │
│  ║  Mejor resultado:           ║    │  ← Floating tip sobre viewfinder
│  ║  Fondo claro y neutro       ║    │     glass card blanco 80% opacity
│  ║                             ║    │     Plus Jakarta 13px, neutral.700
│  ╚═════════════════════════════╝    │
│                                     │
│  ┌──────┐      ◉       ┌──────┐    │  ← Bottom camera controls
│  │ 🌟   │              │  ⟲   │    │     izq: flash toggle
│  │Flash │   [SHUTTER]  │Girar │    │     centro: shutter 64px, primary.500
│  └──────┘              └──────┘    │     der: flip camera
│                                     │
└─────────────────────────────────────┘
```

---

## Add Item — Preview + AI Analysis (POST foto/selección)

```
┌─────────────────────────────────────┐
│ ←  Vista previa            [Cambiar]│
│                                     │
│  ┌─────────────────────────────┐    │
│  │                             │    │  ← Image preview
│  │      [IMAGEN PRENDA]        │    │     335x300px, radius 16px
│  │                             │    │     object-fit: contain (NO cover)
│  │                             │    │     fondo: neutral.100 checkerboard
│  └─────────────────────────────┘    │
│                                     │
│  ┌─────────────────────────────┐    │  ← AI Analysis Card (en proceso)
│  │                             │    │     glass card, secondary border
│  │  ✦  La IA está analizando   │    │
│  │  ● ● ●                      │    │  ← dots thinking animation
│  │  Detectando categoría...    │    │     texto rotativo
│  │  [━━━━━━░░░░░░░░░░░░░░]    │    │
│  │                             │    │
│  └─────────────────────────────┘    │
│                                     │
│  CUANDO TERMINA EL ANÁLISIS:        │
│                                     │
│  ┌─────────────────────────────┐    │  ← AI Results Card
│  │  ✦ IA detectó:              │    │     success state, border success
│  │                             │    │
│  │  ┌───────┐  ┌───────┐       │    │  ← Tags detectados (editables)
│  │  │ Blusa │  │Casual │       │    │     tap en X para eliminar
│  │  │  ✕    │  │  ✕    │       │    │     tap en "+ Agregar" para más
│  │  └───────┘  └───────┘       │    │
│  │  ┌──────────┐  ┌──────┐     │    │
│  │  │ Floreado │  │  S   │     │    │
│  │  │  ✕       │  │  ✕   │     │    │
│  │  └──────────┘  └──────┘     │    │
│  │                             │    │
│  │  ¿Correcto? Puedes editar   │    │  ← hint text, neutral.500 12px
│  └─────────────────────────────┘    │
│                                     │
└─────────────────────────────────────┘
```

---

## Add Item — Form de detalles (scroll)

```
┌─────────────────────────────────────┐
│ ←  Detalles de la prenda            │
│                                     │
│  ┌────────────────────────────────┐ │  ← Small image preview (top)
│  │  [img 60x80px] Blusa floral    │ │     con botón "Cambiar foto"
│  │  Detectado por IA ✦   [Cambiar]│ │
│  └────────────────────────────────┘ │
│                                     │
│  Nombre *                           │  ← Label flotante style
│  ┌─────────────────────────────┐    │     * = requerido
│  │  Blusa floral               │    │
│  └─────────────────────────────┘    │
│                                     │
│  Categoría *                        │
│  ┌─────────────────────────────┐    │  ← Dropdown select
│  │  Tops ▾                     │    │     options: Tops, Bottoms, Vestidos
│  └─────────────────────────────┘    │     Zapatos, Accesorios, Otro
│                                     │
│  Color principal                    │
│  ● ● ● ● ● ● ● ●  [+ Custom]       │  ← Color picker: swatches
│  (seleccionado: terracota ✓)        │     24px cada swatch, +custom abre picker
│                                     │
│  Talla                              │
│  ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐          │  ← Size chips (toggle, one selection)
│  │XS│ │ S│ │ M│ │ L│ │XL│          │
│  └──┘ └──┘ └──┘ └──┘ └──┘          │
│  ┌──────┐                           │
│  │ Otro │ _______                   │  ← "Otro" + input libre para numeric sizes
│  └──────┘                           │
│                                     │
│  Marca                              │
│  ┌─────────────────────────────┐    │  ← Text input opcional
│  │  Ej: Zara, H&M...           │    │
│  └─────────────────────────────┘    │
│                                     │
│  Etiquetas IA  ✦                    │  ← Tags detectados (editables)
│  ┌───────┐ ┌───────┐ ┌───────┐     │     mismos chips del análisis
│  │Casual │ │Verano │ │Floral │     │
│  └───────┘ └───────┘ └───────┘     │
│  + Agregar etiqueta                 │  ← tappable, abre input
│                                     │
│  Notas personales                   │
│  ┌─────────────────────────────┐    │  ← Textarea, 3 líneas min
│  │  Ej: Combina bien con...    │    │
│  └─────────────────────────────┘    │
│                                     │
│  ┌─────────────────────────────┐    │  ← CTA final
│  │      Guardar en guardarropa │    │     primary button large
│  └─────────────────────────────┘    │     sticky al bottom al scrollear
│                                     │
└─────────────────────────────────────┘
```

**Notas de UX:**
- El formulario es progresivo: solo Nombre + Categoría son requeridos, el resto es opcional
- El análisis IA ocurre en background mientras el usuario revisa la imagen
- Si la IA no detecta nada con confianza suficiente, no muestra el card de AI Results (silencioso)
- "Guardar" button es sticky: siempre visible aunque el usuario scrollee
- Feedback post-guardado: toast "Prenda guardada ✓" + opción "Probar virtual try-on"
