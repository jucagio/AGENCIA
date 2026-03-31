# QUICK REFERENCE GUIDE
## Image Advisor AI + Virtual Try-On Design System

**For:** Everyone on the team
**Use:** Quick lookup without reading 200+ pages

---

## COLOR PALETTE AT A GLANCE

### Primary Pastels (Use in UI)

```
┌─────────────────────────────────────────┐
│ BLUSH ROSE (#E8B4C4)                    │
│ Primary accent, CTAs, important buttons │
│ Contrast: 5.8:1 with text              │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ LAVENDER CALM (#D8C9E8)                 │
│ Secondary backgrounds, hover states     │
│ Contrast: 4.2:1 with text              │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ MINT FRESH (#B8E6D9)                    │
│ Success, positive states, checkmarks    │
│ Contrast: 6.1:1 with text              │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ HONEY WARM (#F0D49A)                    │
│ Warnings, subtle alerts, warmth         │
│ Contrast: Safe for all text sizes      │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ SKY SOFT (#C8DFE8)                      │
│ Information, tertiary elements          │
│ Contrast: WCAG AA+                      │
└─────────────────────────────────────────┘
```

### Neutrals (Use for text & backgrounds)

| Color | Use | Hex |
|-------|-----|-----|
| Charcoal | Primary text, headings | #2A2A2A |
| Slate Grey | Secondary text, labels | #5F6B7A |
| Off White | Main background | #F8F7F6 |
| White | Cards, containers | #FFFFFF |
| Light Grey | Borders, dividers | #E8E6E4 |

---

## TYPOGRAPHY AT A GLANCE

### Fonts
- **Headlines:** Inter Tight Bold (modern, geometric)
- **Body:** Inter Regular (legible, accessible)
- **Accents:** Crimson Text Italic (for empowerment phrases)

### Sizes (for developers)
```
H1  → 36px desktop, 28px mobile | Bold | -0.5px letter-spacing
H2  → 28px desktop, 24px mobile | Bold | -0.3px
H3  → 24px desktop, 20px mobile | Semibold
Body → 16px (desktop) / 14px (mobile) | Regular | 1.5 line-height
Small → 12px | Regular
Label → 12px | Medium | uppercase
```

---

## COMPONENTS QUICK SPECS

### Buttons

**Primary Button**
```
Background:  Blush Rose (#E8B4C4)
Text:        Charcoal (#2A2A2A) | Bold 600
Padding:     12px vertical, 24px horizontal
Height:      48px (min tap target)
Border:      12px radius
Shadow:      0 4px 12px rgba(232,180,196,0.3)
Hover:       +5% darker bg, +2px shadow
Active:      scale 0.98, opacity 0.9
```

**Secondary Button**
```
Background:  Transparent
Border:      2px Lavender Calm
Text:        Charcoal
Hover:       bg Lavender 20% opacity
```

**Ghost Button**
```
Background:  White + 1px Light Grey border
Icon:        Blush Rose color
Border:      24px radius (pill shape)
Hover:       shadow increase, scale 1.05
```

### Cards

**Standard Card**
```
Background:   White
Border:       1px Light Grey (#E8E6E4)
Padding:      16px
Border-radius: 16px
Shadow:       0 2px 8px rgba(0,0,0,0.06)
Hover:        shadow 0 8px 20px rgba(0,0,0,0.1)
```

**Elevated Card** (Outfits)
```
Background:    White
Border-radius: 20px
Padding:       20px
Shadow:        0 8px 24px rgba(232,180,196,0.15)
Aspect ratio:  1:1 (square)
```

### Inputs

**Text Input**
```
Background:     Off White (#F8F7F6)
Border:         2px Light Grey
Height:         48px
Border-radius:  12px
Padding:        14px 16px
Focus:          border 2px Blush Rose, shadow 0 0 0 3px rgba(232,180,196,0.2)
Error:          border 2px #D65D5D
```

---

## SPACING SYSTEM

```
xs  →  4px  (micro-spacing)
sm  →  8px  (between related items)
md  → 16px  (standard padding)
lg  → 24px  (section spacing)
xl  → 32px  (major breaks)
2xl → 48px  (full-screen gaps)
3xl → 64px  (hero spacing)
```

**Common applications:**
- Card padding: `md` (16px)
- Button h-padding: `lg` (24px)
- Section margin: `xl` (32px)
- Input label margin: `sm` (8px)

---

## ANIMATIONS AT A GLANCE

### Standard Timings

| Animation | Duration | Easing |
|-----------|----------|--------|
| Fade in | 300ms | ease-out |
| Scale up | 300ms | ease-out |
| Slide | 400ms | ease-out |
| Bounce | 600ms | cubic-bezier(0.34, 1.56, 0.64, 1) |
| Loading spin | 1.5s | linear |
| Pulse | 2s | ease-in-out |

**Rule:** Always respect `prefers-reduced-motion`

---

## ACCESSIBILITY CHECKLIST

Quick test before shipping any screen:

- [ ] Text: 4.5:1 contrast (normal text)
- [ ] Buttons: 44x44px minimum tap target
- [ ] Focus: Visible outline or ring visible
- [ ] Keyboard: Tab/Enter/Arrow keys work
- [ ] Images: Alt text present
- [ ] Forms: Labels associated with inputs
- [ ] Error: Messages clear & constructive
- [ ] Links: Text describes destination (not "click here")
- [ ] Motion: Can be disabled
- [ ] Color: Not the only way to convey info

---

## TONE & VOICE RULES

### DO ✓
- "Vamos a..." (empowering)
- "Sin presión" (reassuring)
- "¿Cómo te sientes?" (emotional)
- "¡Lo hicimos!" (celebratory)
- "Tu privacidad es importante" (trustworthy)

### DON'T ✗
- "Deberías..." (directive)
- "Problema" (negative frame)
- "Correcto/Incorrecto" (judgmental)
- "Body positive" (performative)
- "Algoritmo" (cold/corporate)

### Key Phrases

**Empowerment:**
```
"Te ves increíble"
"Confía en ti"
"Vamos juntas"
"Ese es tu estilo"
```

**Inclusion:**
```
"Todos los cuerpos son hermosos"
"Sin importar tu forma"
"Tu cuerpo es hermoso"
"Aquí no hay estándares"
```

**Error Handling:**
```
"Intenta de nuevo"
"¿Mejor luz?"
"Sin presión, más adelante tal vez"
```

---

## MOCKUP OVERVIEW

### Screen 1: Onboarding
- Step-by-step body type selection (8 options)
- Copy: "Esto no define tu belleza"
- Color: Lavender backgrounds, white cards
- Animation: Staggered entrance

### Screen 2: Outfit Result
- **Hero:** Elevated card with outfit on user's body
- **Details:** Item names, color palette, mood tags
- **Action:** Heart button (save) + emoji rating
- **Copy:** "MÍRАТЕ. Completa. Hermosa."

### Screen 3: Inventory
- Summary stats (47 items, 8 categories)
- Filters (color, type, season, mood)
- 2-4 column grid (responsive)
- Carousel: "5 outfits using this item"

---

## FILE LOCATIONS

All design documents in: **`/erik/`**

| File | Purpose | Size |
|------|---------|------|
| `design-system-image-advisor-ai.md` | Complete system | 70KB |
| `mockups-detailed-specs.md` | 3 screens with spacing | 45KB |
| `tone-voice-copywriting-guide.md` | Copy library | 60KB |
| `illustration-photography-style-guide.md` | Character + try-on | 50KB |
| `EXECUTIVE-SUMMARY.md` | Overview for leadership | 30KB |
| `HANDOFF-TO-JARVIS.md` | Technical implementation | 50KB |
| `QUICK-REFERENCE.md` | This file | 10KB |

---

## WHO NEEDS WHAT

### Jarvis (Gerente de Programación)
1. Read: `EXECUTIVE-SUMMARY.md`
2. Read: `HANDOFF-TO-JARVIS.md`
3. Bookmark: `QUICK-REFERENCE.md`
4. Share with team: All files

### Sasha (Backend Developer)
1. Read: `HANDOFF-TO-JARVIS.md` (section 4: Backend)
2. Reference: `design-system-image-advisor-ai.md` (section 2: Accessibility)
3. Use: Code examples in `HANDOFF-TO-JARVIS.md`

### Brook (Frontend Developer)
1. Read: `HANDOFF-TO-JARVIS.md` (sections 2-3: Frontend Stack)
2. Deep dive: `design-system-image-advisor-ai.md` (complete system)
3. Reference: `mockups-detailed-specs.md` (spacing & sizing)
4. Create: Figma component library (from specs)

### Cinthya (Automation)
1. Read: `tone-voice-copywriting-guide.md`
2. Use: Copy library for email/push templates
3. Create: Automation for onboarding copy

### Jade (Training)
1. Read: `tone-voice-copywriting-guide.md`
2. Train: All team on brand voice
3. Create: Style guide for future copywriters

### Illustration Vendor
1. Read: `illustration-photography-style-guide.md` (Part 1)
2. Study: Reference artists (Bumble, Headspace, Calm)
3. Deliver: Adora character design

### Virtual Try-On Vendor
1. Read: `illustration-photography-style-guide.md` (Part 2)
2. Study: Platform recommendations
3. Deliver: 100+ outfit images

---

## QUICK DECISION TREE

### "What color should I use for X?"

```
Is it a button that does something?
  → YES: Blush Rose (#E8B4C4)
  → NO:

Is it background or secondary container?
  → YES: Lavender Calm (#D8C9E8)
  → NO:

Is it a success/positive state?
  → YES: Mint Fresh (#B8E6D9)
  → NO:

Is it a warning or needs attention?
  → YES: Honey Warm (#F0D49A)
  → NO:

Is it information?
  → YES: Sky Soft (#C8DFE8)
  → NO:

Is it text or heading?
  → YES: Charcoal (#2A2A2A)
  → NO: Use White or Off White
```

### "What size should this text be?"

```
Is it a page heading (H1)?
  → YES: 36px desktop, 28px mobile, Bold
  → NO:

Is it a section heading (H2)?
  → YES: 28px desktop, 24px mobile, Bold
  → NO:

Is it body text?
  → YES: 16px desktop, 14px mobile, Regular
  → NO: 12px (small text), 14px (button)
```

### "What spacing should I use?"

```
Micro spacing between icons/text?
  → xs (4px)

Between related items (button + label)?
  → sm (8px)

Standard padding inside cards?
  → md (16px)

Between sections on a page?
  → lg (24px) or xl (32px)

Between major sections?
  → xl (32px) or 2xl (48px)
```

---

## COPY TEMPLATES (For quick reference)

### Empty States
```
"Tu [feature] está vacío"
"[Action] para empezar a [outcome]"
"CTA button"
```

Example: "Tu inventario está vacío. Sube fotos de tu ropa para crear outfits. [Upload button]"

### Loading
```
"[Action]ing tu estilo..."
```

Example: "Analizando tu estilo..."

### Success
```
"¡Lo hicimos!" OR "¡Listo!"
"Brief positive statement"
```

Example: "¡Lo guardé! Ahora tienes 5 looks favoritos"

### Error
```
"Brief description of what went wrong"
"Helpful hint for fixing"
"[Retry button]"
```

Example: "La foto no se cargó. Intenta con mejor luz. [Reintentar]"

---

## QUICK METRICS

### Performance Targets
- Page load: <2 seconds
- Outfit generation: <3 seconds
- Image load: <1.5 seconds
- Tap response: <100ms

### Accessibility Targets
- WCAG AA compliance: 100%
- Contrast ratio: >4.5:1
- Keyboard navigation: 100% of screens
- Screen reader compatible: 100%

### User Targets
- Onboarding completion: >70%
- Wardrobe upload: >60%
- Outfit saves: >50% per session
- User retention week 1→4: >40%

---

## GOTCHAS & REMINDERS

### Common Mistakes to Avoid

❌ **Using color alone to convey info** (not accessible)
✓ Use color + text + icon

❌ **Text smaller than 14px** (not readable on mobile)
✓ Minimum 16px for body

❌ **Buttons smaller than 44px** (not tap-friendly)
✓ Always 44x44px or larger

❌ **No focus indicator on buttons** (not keyboard accessible)
✓ Always add visible focus ring

❌ **Copy that judges or shames**
✓ Use empowering, warm language

❌ **Showing outfits only on one body type**
✓ Show on multiple body types

❌ **Animations that can't be disabled**
✓ Always respect `prefers-reduced-motion`

---

## CONTACT & QUESTIONS

- **Design questions?** → Erik
- **Implementation questions?** → Jarvis
- **Copy/brand voice?** → Jade or Erik
- **Technical specs?** → Read `HANDOFF-TO-JARVIS.md`

---

## VERSIONING

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | March 29, 2026 | Initial system |
| TBD | TBD | Dark mode variant |
| TBD | TBD | Tablet layout refinements |
| TBD | TBD | Additional illustrations |

---

**Print this page or bookmark it. Reference it daily.** 💙

