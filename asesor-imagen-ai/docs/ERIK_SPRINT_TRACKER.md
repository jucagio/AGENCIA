# ERIK — SPRINT TRACKER
## Design Sprint SAB 18 - SAB 25 mayo 2026

**Owner:** Erik
**Entrega final:** SAB 25 mayo 2026 — handoff a Brook
**Design system:** Aether Luxe (APROBADO por Juan Camilo)
**Specs completas:** `docs/mockups/ERIK_SPRINT_DESIGN_SPECS.md`

---

## Status por pantalla

| Screen | ID | Wave | Specs | Figma | Assets | Brook-ready |
|--------|----|------|-------|-------|--------|-------------|
| Loading State | S04B | 1 | COMPLETO | pendiente | ninguno | - |
| Style Insights + Soft Cap | S06 | 1 | COMPLETO + S06_SOFT_CAP_UI_DESIGN.md | pendiente | body_type_*.svg | - |
| Body Analysis Upload | S07 | 1 | COMPLETO | pendiente | ninguno | - |
| Error States (4) | S11 | 1 | COMPLETO | pendiente | error_*.svg | - |
| My Wardrobe | S05 | 2 | COMPLETO | pendiente | empty_wardrobe.svg | - |
| Collections | S08 | 2 | COMPLETO | pendiente | empty_collections.svg | - |
| Profile / Settings | S09 | 2 | COMPLETO | pendiente | ninguno | - |
| Paywall | S10 | 2 | COMPLETO | pendiente | ninguno | - |
| Splash / Onboarding | S01 | 3 | COMPLETO | pendiente | onboarding_*.svg | - |
| Login | S02 | 3 | COMPLETO | pendiente | ninguno | - |
| Register | S03 | 3 | COMPLETO | pendiente | ninguno | - |
| Virtual Try-On | S04 | 3 | COMPLETO | pendiente | ninguno | - |

**Leyenda:** COMPLETO = specs escritas y validadas | pendiente = tarea aun no iniciada

---

## Ilustraciones SVG necesarias (13 archivos)

### Prioridad 1 — Necesarias el Dia 1 o 2
- [ ] `onboarding_slide_1.svg` — figura femenina + overlay IA + ropa flotando + trazos azul/violeta
- [ ] `error_network.svg` — wifi cortado, nube rota, estilo lineal, onSurfaceVariant
- [ ] `error_404.svg` — personaje busca algo con lupa, estilo lineal, onSurfaceVariant
- [ ] `error_tryon.svg` — usar icono Material error_outline 48px (no necesita SVG custom)

### Prioridad 2 — Dias 2-4
- [ ] `body_type_pear.svg` — silueta pera, trazos lineales, color primary
- [ ] `body_type_rectangle.svg` — silueta rectangulo
- [ ] `body_type_inverted_triangle.svg` — triangulo invertido
- [ ] `body_type_hourglass.svg` — reloj de arena
- [ ] `body_type_oval.svg` — oval / manzana

### Prioridad 3 — Dias 4-6
- [ ] `empty_wardrobe.svg` — perchas vacias, closet organizado vacio
- [ ] `empty_collections.svg` — camara + estrella, "aun no tienes looks"
- [ ] `onboarding_slide_2.svg` — closet organizado con prendas por colores
- [ ] `onboarding_slide_3.svg` — paleta de colores personal + silueta

**Estrategia de generacion:** Usar Nano Banana 2 o Claude Banana para prompts de generacion.
Las ilustraciones son SVG estilo lineal minimalista — no fotorealistas.
Exportar de Adobe Illustrator o Figma como SVG optimizado.

---

## Componentes a documentar en Figma

### Atoms (base) — documentar primero
- [ ] GradientButton (3 tamaños: sm/md/lg, estado disabled)
- [ ] OutlineButton (igual)
- [ ] SolidButton (negro)
- [ ] TextButton
- [ ] Input (5 estados: default/focus/error/filled/disabled)
- [ ] AIInsightChip
- [ ] PlanBadge (3 variants: free/estilo/imagen)
- [ ] ColorSwatch (2 variants: good/avoid)
- [ ] FilterChip (activo/inactivo)

### Molecules — documentar despues
- [ ] UploadZone (3 estados: vacio/filled/hover)
- [ ] ClothingSlot (2 estados: vacio/filled)
- [ ] WardrobeCard
- [ ] LookCard
- [ ] AIInsightCard
- [ ] GradientLoaderCard
- [ ] BodyTypeSilhouette (5 variants)
- [ ] ProfileSettingTile
- [ ] PaywallTierCard (3 variants: free/estilo/imagen)
- [ ] OnboardingSlide
- [ ] SkeletonCard (2 variants: small/large)
- [ ] ErrorView (3 variants: 404/network/tryon)
- [ ] SharePlatformSheet

---

## Dias del sprint

| Dia | Fecha | Objetivo | Status |
|-----|-------|----------|--------|
| Dia 1 | SAB 18 | Specs S04B + S06 + S07 + S11 — DONE ✓ | SPECS COMPLETO |
| Dia 2 | DOM 19 | Figma Wave 1 (4 pantallas) + ilustraciones P1 | pendiente |
| Dia 3 | LUN 20 | S06 Soft Cap UI Design completo + DESIGN_HANDOFF_S01-S11.md | COMPLETO ✓ |
| Dia 4 | MAR 21 | Figma Wave 1 — S04B + S06 + S07 + S11 en Figma | pendiente |
| Dia 5 | MIE 22 | Figma Wave 2 — S05 + S08 + S09 + S10 | pendiente |
| Dia 6 | JUE 23 | Figma Wave 3 — S01 + S02 + S03 + S04 | pendiente |
| Dia 7 | VIE 24 | QA visual + component library final + ilustraciones P1-P3 | pendiente |
| Dia 8 | SAB 25 | Handoff a Brook — link Figma + DESIGN_HANDOFF_S01-S11.md | pendiente |

---

## Criterios de cierre del sprint

- [ ] 11 pantallas en Figma (high-fidelity, no wireframes)
- [ ] Component library completa (atoms + molecules)
- [ ] 13 SVG ilustraciones exportadas en assets/illustrations/
- [ ] Animation specs claras para cada pantalla (en ERIK_SPRINT_DESIGN_SPECS.md — DONE)
- [ ] Color/typography tokens bloqueados al Aether Luxe system
- [ ] QA checklist pasada para las 11 pantallas
- [ ] Link Figma en el repo
- [ ] Brook confirmacion de recibido

---

**Proxima accion (ahora mismo):** Abrir Figma, crear el archivo "AI Fit Check — Design Sprint", crear frames Mobile 390x844, e iniciar con SoftCapBottomSheet (S06) — el componente mas urgente para Brook.

**Ultima actualizacion:** 2026-05-20 (Dia 3)
**Specs Wave 1:** `docs/mockups/ERIK_SPRINT_DESIGN_SPECS.md`
**Soft Cap UI:** `docs/mockups/S06_SOFT_CAP_UI_DESIGN.md` — COMPLETADO HOY
**Handoff completo:** `docs/DESIGN_HANDOFF_S01-S11.md` — COMPLETADO HOY
