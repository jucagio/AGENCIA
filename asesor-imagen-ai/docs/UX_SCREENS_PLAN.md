# UX & SCREENS PLAN — AI Fit Check
## Inventario de pantallas + flujos de usuario

**Owner:** Erik (diseño) + Brook (implementación Flutter)
**Validado:** Juan Camilo Gil — 2026-05-18
**Referencia de diseño:** `stitch_ai_fit_check_ui.zip` → Aether Luxe design system
**Design system:** `docs/design-system/DESIGN_SYSTEM.md`

---

## 1. Estructura de navegación (confirmada)

```
AI Fit Check
│
├── 🔐 Auth (pre-login)
│   ├── Splash / Onboarding (3 slides)
│   ├── Login
│   └── Register
│
└── 🏠 App (post-login) — NavigationBar (móvil) / NavigationRail (tablet)
    │
    ├── ✨ Virtual Try-On     ← TAB PRINCIPAL (pantalla referencia)
    ├── 👗 My Wardrobe        ← closet digital
    ├── 🔮 Style Insights     ← análisis cuerpo + color season
    └── 📚 Collections        ← outfits guardados
    
    ⚙️ Settings / Profile    ← acceso desde topbar
    💳 Upgrade to Pro        ← CTA en sidebar / paywall
```

**Flutter navigation:**
- Móvil (< 600px): `NavigationBar` en bottom con 4 items
- Tablet (≥ 600px): `NavigationRail` lateral colapsable
- Desktop/Web: Sidebar fijo como en el prototipo

---

## 2. Inventario completo de pantallas

### 🔐 FLUJO AUTH

#### S01 — Splash / Onboarding (3 slides)
```
Estado: ✅ MOCKUPS COMPLETADOS (Erik Sprint 0 paralelo)

Slide 1: "Verte sin probarte"
  • Hero visual: modelo con overlay de IA
  • CTA: "Siguiente"
  
Slide 2: "Vestirte mejor sin gastar más"
  • Hero visual: closet organizado / collage
  • CTA: "Siguiente"
  
Slide 3: "Conocete estilísticamente"
  • Hero visual: paleta de colores personal
  • CTA: "Comenzar gratis"

Tokens: primaryGradient para indicadores activos
```

#### S02 — Login
```
Estado: ✅ MOCKUP COMPLETADO (Erik)

Elementos:
• Logo "AI Fit Check" + tagline
• Campo email (input outlined, radius lg)
• Campo password (con toggle show/hide)
• Botón "Iniciar sesión" (gradiente CTA)
• Link "¿Olvidaste tu contraseña?"
• Divider "o continúa con"
• Google Sign-In (secundario)
• Link "Crear cuenta"

Backend: POST /api/v1/auth/login
```

#### S03 — Register
```
Estado: ✅ MOCKUP COMPLETADO (Erik)

Elementos:
• Nombre completo + email + password
• Checkbox términos
• Botón "Crear cuenta gratis" (gradiente)
• Link "Ya tengo cuenta"

Backend: POST /api/v1/auth/register
Password: min 10 chars, 1 letra + 1 dígito
```

---

### ✨ TAB 1 — VIRTUAL TRY-ON

#### S04 — Virtual Try-On (pantalla principal)
```
Estado: ✅ REFERENCIA COMPLETA (stitch_ai_fit_check_ui.zip)
Sprint: 4

Sub-estados:
  [A] UPLOAD STATE (default)
  [B] LOADING STATE (falta diseñar)
  [C] RESULT STATE (pantalla referencia)

[A] UPLOAD STATE
────────────────
Header:
  • H1: "Virtual Try-On"
  • Subtitle: "Descubre tu mejor combinación impulsada por IA"
  • color: outline (#76777D)

Sección "Tu Foto":
  • Label h3 "Tu Foto"
  • Upload zone grande (min-h 400px móvil: 280px)
  • Dashed border 2px, radius lg
  • Icono photo_camera + texto instrucción
  • Tap → ImagePicker (cámara o galería)
  • Estado filled: imagen preview + botón X

Sección "Tu Ropa" (max 5):
  • Label h3 "Tu Ropa" + badge "Máx 5"
  • Grid 2 columnas, aspect-square
  • Slots vacíos: dashed border + icono "+"
  • Slots llenos: imagen + botón X (hover/tap)
  • Tap vacío → seleccionar de Wardrobe o subir nueva
  • Datos: GET /api/v1/wardrobe/items

CTA:
  • Botón pill gradiente: "Generar Outfit Ideal ✨"
  • Disabled: si no hay foto cargada
  • Tap → POST /api/v1/try-ons (202) → ir a [B]

[B] LOADING STATE ← DISEÑAR (no está en prototipo)
──────────────────
  • Reemplaza el área de resultado
  • Animación: gradiente pulsante (shimmer azul→violeta)
  • Texto: "Nuestra IA está creando tu look..."
  • Subtexto: "Esto puede tardar hasta 30 segundos"
  • Progress bar o spinner con gradiente
  • Polling: GET /api/v1/try-ons/{id} cada 3s
  • Cuando status = "completed" → transición a [C]

[C] RESULT STATE
────────────────
  • H2: "Tu Look" (centrado)
  
  Layout 2/3 + 1/3:
    Izquierda (2/3):
    • Imagen resultado (fotorrealista)
    • Radius lg, shadow ambient2
    • Full-bleed, object-cover
    
    Derecha (1/3):
    • Chip AI Insights (violeta pill)
    • H3: "Por qué funciona"
    • Body text: explicación IA
    • Botones: [Guardar] [Compartir]
    
  En móvil → stacked (imagen arriba, card abajo)
  
Backend:
  • POST /api/v1/try-ons → job_id
  • GET /api/v1/try-ons/{id} → polling
  • GET /api/v1/recommendations/{id} → texto "Por qué funciona"
  • PATCH /api/v1/try-ons/{id}/feedback → Guardar
```

---

### 👗 TAB 2 — MY WARDROBE

#### S05 — Wardrobe (closet digital)
```
Estado: ❌ PENDIENTE diseño
Sprint: 2

Layout:
  • Header: "Mi Closet" + botón "+" (añadir prenda)
  • Filtros horizontales: Todos | Tops | Pantalones | Vestidos | Zapatos
  • Grid 3 columnas (móvil 2)
  • Cards: imagen prenda + categoría label + menú (⋮)
  
Card prenda:
  • Imagen object-cover aspect-square
  • Badge categoría (labelCaps)
  • Tap → detalle prenda
  • Long press / ⋮ → Editar / Eliminar / Usar en Try-On

Vacío state:
  • Ilustración closet vacío
  • CTA: "Añade tu primera prenda" (botón gradiente outline)
  
Añadir prenda modal:
  • Upload foto (cámara o galería)
  • Campos: categoría, talla, marca (todos opcionales)
  • Tags del usuario (chips editables)
  • Botón: "Guardar prenda"
  
Backend:
  • GET /api/v1/wardrobe/items (paginado, filtros)
  • POST /api/v1/wardrobe/items
  • PATCH /api/v1/wardrobe/items/{id}
  • DELETE /api/v1/wardrobe/items/{id}
```

---

### 🔮 TAB 3 — STYLE INSIGHTS

#### S06 — Style Insights (análisis)
```
Estado: ❌ PENDIENTE diseño
Sprint: 3

Layout:
  • Header: "Tu Perfil de Estilo"
  
  Si no hay análisis:
    • Card "Descubre tu tipo de cuerpo"
    • Card "Conoce tu temporada de color"
    • CTA: "Iniciar análisis" (gradiente)
  
  Si hay análisis:
    • Card: Tipo de cuerpo (ilustración silueta + descripción)
    • Card: Color season (paleta personal con chips de colores)
    • Card: Colores recomendados (grid de swatches)
    • Card: Colores a evitar (grid de swatches tachados)
    • Card: Recomendaciones de estilo (text con bullets)

Backend:
  • GET /api/v1/body-analysis (último análisis)
  • POST /api/v1/body-analysis (iniciar nuevo)
```

#### S07 — Body Analysis Upload
```
Estado: ❌ PENDIENTE diseño
Sprint: 3

Similar a upload zone de Try-On:
  • Instrucciones claras (foto de frente, buena luz)
  • Dos opciones: "Usar mi foto de perfil" / "Subir nueva foto"
  • Preview + confirmación
  • CTA: "Analizar mi figura"
  • Loading: animación IA (~15-20 segundos)
  • Resultado: redirige a Style Insights

Backend: POST /api/v1/body-analysis → polling
```

---

### 📚 TAB 4 — COLLECTIONS

#### S08 — Collections (looks guardados)
```
Estado: ❌ PENDIENTE diseño
Sprint: 5

Layout:
  • Header: "Mis Looks"
  • Grid 2 columnas (masonry o uniforme)
  • Cards: resultado try-on + fecha + AI insight snippet
  • Filtros: recientes | favoritos
  
Card look:
  • Imagen generada (aspect 3:4 portrait)
  • Badge con fecha
  • Botón Compartir
  • Tap → detalle con AI insights completos

Vacío state:
  • "Aún no tienes looks guardados"
  • CTA: "Crear tu primer look" → Virtual Try-On

Backend: GET /api/v1/try-ons (filtrado liked=true)
```

---

### ⚙️ UTILITARIAS

#### S09 — Perfil / Settings
```
Estado: ❌ PENDIENTE diseño
Sprint: 1

Secciones:
  • Avatar + nombre + email
  • Plan actual (Free / Estilo / Imagen)
  • Notificaciones (toggle)
  • Idioma
  • Privacidad y términos
  • Cerrar sesión (botón outline error)

Backend: GET/PATCH /api/v1/users/me
```

#### S10 — Paywall / Upgrade to Pro
```
Estado: ❌ PENDIENTE diseño
Sprint: 6

Layout:
  • Header gradiente con crown icon
  • Tabla comparación tiers:
    Free | Estilo | Imagen
  • Feature list con checkmarks
  • CTA por tier: "Empezar con Estilo" / "Ir a Imagen"
  • Precios en COP/USD
  • Social proof (usuarios activos)

Backend: POST /api/v1/subscriptions/stripe/checkout
```

#### S11 — Loading / Estados de error
```
Estado: ❌ PENDIENTE diseño
Sprint: 4

  • Loading shimmer genérico (skeleton screens)
  • Error 404 (ilustración + CTA volver)
  • Error de red (sin conexión)
  • Try-on fallido ("Algo salió mal, intenta de nuevo")
```

---

## 3. Componentes reutilizables (atoms)

| Componente | Descripción | Sprint |
|------------|-------------|--------|
| `GradientButton` | Botón pill azul→violeta | 1 |
| `OutlineButton` | Botón borde negro | 1 |
| `UploadZone` | Área de drop dashed | 2 |
| `ClothingSlot` | Slot cuadrado aspect-ratio | 2 |
| `AIInsightChip` | Pill violeta "AI Insights" | 4 |
| `AIInsightCard` | Card con "Por qué funciona" | 4 |
| `WardrobeCard` | Card prenda en grid | 2 |
| `LookCard` | Card resultado try-on | 4 |
| `NavItem` | Item de navegación activo/inactivo | 1 |
| `GradientLoader` | Shimmer animado gradiente | 4 |
| `ColorSwatch` | Chip de color con hex | 3 |
| `PlanBadge` | Badge Free/Estilo/Imagen | 6 |

---

## 4. Decisiones de UX pendientes (para Juan Camilo)

| # | Decisión | Opciones | Impact |
|---|----------|----------|--------|
| D1 | **Nombre en UI** | "AI Fit Check" vs "Asesor de Imagen" | Branding |
| D2 | **Flujo Try-On** | ¿Selección de prendas desde wardrobe o upload directo? | UX Sprint 4 |
| D3 | **Onboarding con análisis** | ¿Análisis de cuerpo obligatorio al registrarse o opcional? | Conversion |
| D4 | **Free tier limits** | ¿3 try-ons/mes en free o ilimitado con menor calidad? | Monetización |
| D5 | **Social sharing** | ¿Compartir a Instagram/WhatsApp desde la app? | Viral loop |

---

**Última actualización:** 2026-05-18
**Próximo paso:** Triggear a Erik con este documento + DESIGN_SYSTEM.md para producir mockups S05–S11
