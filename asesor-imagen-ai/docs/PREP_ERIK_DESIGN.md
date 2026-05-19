# PREP — ERIK DESIGN WORK

**From:** Jarvis (CEO)  
**To:** Erik (Designer)  
**Date:** 2026-05-18 (SAB)  
**Task:** Design 11 screens (S01-S11) using Aether Luxe system  
**Status:** ⏳ Awaiting D1-D5 decisions (Juan Camilo)

---

## 📊 CURRENT STATE

### ✅ READY NOW (No dependencies)
- Design System: Aether Luxe (40+ tokens, colors, typography, spacing)
- Reference screens: S01-S04 (mockups in `stitch_ai_fit_check_ui.zip`)
- UX flows: 11 screens documented in `UX_SCREENS_PLAN.md`

### 🟡 BLOCKED (Waiting for Juan Camilo D1-D5 decisions)
- S05: My Wardrobe (depends on D2 — upload vs wardrobe selection flow)
- S04B: Loading state (NEWLY IDENTIFIED — not in prototype, you design from scratch)
- S06-S09: Insights, Profile, Collections, Paywall
- S11: Error states

### ✅ START DESIGNING NOW (No D1-D5 dependency)
- **S04B: Loading State** (new screen, missing from prototype)
  - 15-30 seconds of loading
  - Gradient shimmer animation (primaryGradient: 135° #0058BE→#9466FF)
  - Text: "Nuestra IA está creando tu look..."
  - Subtexto: "Esto puede tardar hasta 30 segundos"
  - Progress indicator (bar or spinner)
  - Reference: Material Design 3 skeleton loaders + Lottie for shimmer

---

## 🎯 DESIGN PLAN (Day-by-day)

### DAY 1-2 (SAB 18 — DOM 19)
**Status:** Waiting for D1-D5  
**Action:** Design S04B in parallel

**S04B — Loading State**
```
Layout:
  Full screen (replaces result area in S04)
  
  Vertical stack, centered:
    • Shimmer animation (gradient blue→violet pulsing)
    • H2: "Nuestra IA está creando tu look..."
    • Body: "Esto puede tardar hasta 30 segundos"
    • Progress bar (gradient gradient) OR spinner
    • Subtle animation (no jarring motion)
  
Motion:
  • Shimmer: 2s cycle, loops forever
  • Progress bar: if visible, fills 0-100% over ~20s
  
Colors:
  • Background: AppColors.surface (#FAFAFA)
  • Shimmer: primaryGradient (#0058BE→#9466FF at 135°)
  • Text: AppColors.black
  
Typography:
  • H2: AppTypography.h2 (32px, w600)
  • Body: AppTypography.bodyMd (16px, w400)

Reference: Lottie animation or CSS-inspired shimmer
```

**Deliverable:** 1 screen design + animations

---

### DAY 2 (DOM 19)
**Action:** Receive D1-D5 from Juan Camilo

Once D1-D5 locked:
- [ ] D1 confirmed (app name in UI)
- [ ] D2 confirmed (try-on flow)
- [ ] D3 confirmed (onboarding)
- [ ] D4 confirmed (free tier)
- [ ] D5 confirmed (social sharing)

---

### DAY 3 (LUN 20)
**Status:** UNBLOCKED (D1-D5 received)  
**Action:** Design S05 + S06 in parallel

**S05 — My Wardrobe** (depends on D2)
```
If D2 = "upload directo":
  • Emphasis on grid of items
  • Large "+" button for add prenda
  • Upload flow prominent

If D2 = "seleccionar existing":
  • Emphasis on wardrobe as gallery
  • Filter chips (Todos, Tops, Pantalones, etc.)
  • Empty state illustration

If D2 = "hybrid":
  • Both options visible
  • Primary CTA: upload, Secondary: select existing
```

**S06 — Style Insights** (no D1-D5 dependency)
```
Two states:

[A] No analysis yet:
  • Card: "Descubre tu tipo de cuerpo"
  • Card: "Conoce tu temporada de color"
  • CTA: "Iniciar análisis" (gradient button)

[B] Has analysis:
  • Card: Body type (silueta illustration + text)
  • Card: Color season (paleta personal, color swatches)
  • Cards: Best colors grid + Avoid colors grid
  • Card: Recomendaciones de estilo (bullets)
```

**Deliverable:** 2 screens

---

### DAY 4 (MAR 21)
**Action:** Design S07-S09

**S07 — Body Analysis Upload**
```
Similar to S04 upload zone:
  • Instructions: "foto de frente, buena luz"
  • Options: "Usar mi foto de perfil" OR "Subir nueva foto"
  • Preview + confirmation
  • CTA: "Analizar mi figura" (gradient)
  • Loading state: reference S04B (similar animation)
  • On complete: redirect to S06 (Style Insights)
```

**S08 — Collections** (depends on D5)
```
Grid layout:
  • Header: "Mis Looks"
  • Filter chips: Recientes | Favoritos
  • Masonry OR uniform grid (your choice)
  
If D5 = "social sharing":
  • Card: imagen + fecha + [Share] button
  
If D5 = "no sharing":
  • Card: imagen + fecha (simpler)

Empty state:
  • "Aún no tienes looks guardados"
  • CTA: "Crear tu primer look" → S04 (Virtual Try-On)
```

**S09 — Profile / Settings**
```
Layout:
  • Header: Avatar + nombre + email
  • Plan badge (Free | Estilo | Imagen)
  • Section: Notificaciones (toggle)
  • Section: Idioma (select)
  • Section: Privacidad & Términos (links)
  • CTA: "Cerrar sesión" (outline error color)
  
If D1 = "Asesor de Imagen":
  • Branding in header
  
If D1 = "AI Fit Check":
  • Logo + branding in header
```

**Deliverable:** 3 screens

---

### DAY 5 (MIÉ 22)
**Action:** Design S10 + S11

**S10 — Paywall / Upgrade to Pro** (depends on D4)
```
Header:
  • Crown icon + gradient background
  • "Upgrade to Premium" headline
  
Tier comparison table:
  • Columns: Free | Estilo | Imagen
  • Feature rows with checkmarks (✓ | ✗)
  
If D4 = "3/mes":
  • Free: 3 try-ons/mes
  • Estilo: 30/mes
  • Imagen: Unlimited

If D4 = "1/día":
  • Free: 1/día (30/mes)
  • Estilo: 5/día
  • Imagen: Unlimited

If D4 = "hybrid":
  • Free: 1/día + preview quality
  • Estilo: 5/día + 1080p
  • Imagen: Unlimited + 2K

CTA buttons:
  • Free: Disabled (current)
  • Estilo: "Empezar con Estilo" (gradient)
  • Imagen: "Ir a Imagen" (gradient)
  
Social proof:
  • "+50K usuarios activos" (badge)
  
Pricing:
  • Display in COP/USD
```

**S11 — Error States** (no dependencies)
```
3 error screens:

[A] Loading Skeleton
  • Shimmer animation (generic)
  • 3 placeholder cards or skeleton items
  • Reference: Material Design 3 skeleton

[B] 404 Not Found
  • Illustration (empty closet / sad try-on box)
  • "Parece que no encontramos lo que buscas"
  • CTA: "Volver a inicio" (outline button)

[C] Network Error
  • Illustration (broken connection)
  • "Sin conexión a Internet"
  • CTA: "Reintentar" (primary gradient)

[D] Try-On Failed
  • Illustration (crash/error)
  • "Algo salió mal durante la creación"
  • CTA: "Intentar de nuevo" (primary gradient)
```

**Deliverable:** 1 screen (4 error states)

---

### DAY 6 (JUE 23)
**Action:** Final polish + exports

- [ ] Review all 11 screens against Aether Luxe tokens
- [ ] Verify color usage (primary, secondary, tertiary consistent)
- [ ] Verify typography (h1-h3, bodyLg, bodyMd, labelCaps consistent)
- [ ] Verify spacing (xs/sm/md/lg/xl consistent)
- [ ] Component library: all reusable elements (GradientButton, UploadZone, ClothingSlot, AIInsightCard)
- [ ] Animations: Lottie specs or CSS-like descriptions (for Brook to implement)
- [ ] Export screens as Figma pages or Stitch design-to-code

---

## 🎨 DESIGN DELIVERABLES

**By EOD DAY 6 (2026-05-23):**

### Figma/Stitch file
- [ ] 11 screens (S01-S11)
- [ ] Component library (12 atoms)
- [ ] Constraints & responsive specs
- [ ] Exported as PNG + design-to-code markdown (DESIGN.md)

### Documentation
- [ ] Animation specs (Lottie JSON or CSS-like description)
- [ ] Color palette usage map (which screens use which colors)
- [ ] Typography usage map
- [ ] Component specs (exact dimensions, padding, border-radius)

### References
- [ ] S01-S04 already in prototype → use as base
- [ ] S04B loading → new, design from scratch
- [ ] S05-S11 → new, design from UI flow specs

---

## 📋 DEPENDENCIES

| Screen | Depends on | Status |
|--------|-----------|--------|
| S01-S03 | Design system only | ✅ Ready |
| S04 | Design system only | ✅ Ready (in prototype) |
| S04B | Design system only | ✅ Ready (START NOW) |
| S05 | D2 decision | 🟡 Waiting |
| S06 | Design system only | ✅ Ready |
| S07 | Design system only | ✅ Ready |
| S08 | D5 decision | 🟡 Waiting |
| S09 | D1 decision | 🟡 Waiting |
| S10 | D4 decision | 🟡 Waiting |
| S11 | Design system only | ✅ Ready |

**Summary:** 
- **CAN START NOW:** S01-S04, S04B, S06, S07, S11 (6 screens)
- **WAIT FOR D1-D5:** S05, S08, S09, S10 (4 screens)

**Strategic:** Start with S04B + S06-S07 + S11. Once D1-D5 arrives, final 4 screens. All 11 done by EOD Day 6.

---

## 🎯 SUCCESS CRITERIA

**By EOD Day 6 (2026-05-23):**

- [ ] 11/11 screens designed
- [ ] All Aether Luxe tokens applied (colors, typography, spacing)
- [ ] Animations specified (Lottie or description)
- [ ] Component library documented
- [ ] Responsive specs clear (mobile 375px, tablet 768px, desktop 1280px)
- [ ] Design-to-code markdown exported
- [ ] Ready for Brook to implement

---

## 📞 SUPPORT

- Jarvis: Strategy + D1-D5 decisions
- Brook: Feedback on implementability
- Reference: `docs/design-system/DESIGN_SYSTEM.md` for all tokens

---

## 🚀 YOUR ROLE

**Days 1-2:** S04B (no wait) + prep for remaining  
**Days 3-6:** S05-S11 (once D1-D5 arrives)  
**Day 6:** Final polish + export for Brook

You're not blocked on most work. D1-D5 is low-priority parallelizeable work — you can design 70% of screens right now and finish the rest once decisions arrive.

Let's make this beautiful. 🎨

