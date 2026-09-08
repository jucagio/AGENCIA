# IMAGE ADVISOR AI + VIRTUAL TRY-ON
## Sistema de Diseño Completo v1.0

---

## 1. IDENTIDAD DE MARCA

**Nombre:** Image Advisor AI (o similar según naming final)
**Tagline:** "Vístete con confianza. Siéntete bien."
**Tono:** Empoderador, inclusivo, accesible, genuino
**Propósito:** Ayudar a cualquier persona a encontrar outfits que la hagan sentir hermosa, sin importar su tipo de cuerpo

**Core Values:**
- Inclusión radical (todos los cuerpos son bellos)
- Tecnología al servicio del bienestar, no de crítica
- Privacidad y seguridad (análisis de cuerpo sin juzgar)
- Creatividad personalizada (no hay dos usuarios iguales)

---

## 2. PALETA DE COLORES

### Colores Primarios (Pasteles Premium)

| Color | Uso | Hex | RGB | Accessibility |
|-------|-----|-----|-----|----------------|
| **Blush Rose** | Accent principal, CTAs, highlights | #E8B4C4 | (232, 180, 196) | WCAG AA+ |
| **Lavender Calm** | Backgrounds secundarios, components | #D8C9E8 | (216, 201, 232) | WCAG AA+ |
| **Mint Fresh** | Success, confirmaciones, positivos | #B8E6D9 | (184, 230, 217) | WCAG AA+ |
| **Honey Warm** | Warnings, atención suave | #F0D49A | (240, 212, 154) | WCAG AA+ |
| **Sky Soft** | Información, backgrounds terciarios | #C8DFE8 | (200, 223, 232) | WCAG AA+ |

### Colores Neutros

| Color | Uso | Hex | RGB |
|-------|-----|-----|-----|
| **Charcoal** | Texto principal, headings | #2A2A2A | (42, 42, 42) |
| **Slate Grey** | Texto secundario, labels | #5F6B7A | (95, 107, 122) |
| **Off White** | Backgrounds principales | #F8F7F6 | (248, 247, 246) |
| **White** | Cards, modals, espacios puros | #FFFFFF | (255, 255, 255) |
| **Light Grey** | Borders, dividers, subtle | #E8E6E4 | (232, 230, 228) |

### Colores Funcionales

| Color | Uso | Hex |
|-------|-----|-----|
| **Error** | Validaciones, alerts | #D65D5D |
| **Success** | Confirmación, checkmarks | #6FB889 |
| **Warning** | Caution | #E8A747 |
| **Disabled** | Estados inactivos | #ABABAB |

### Gradientes (Uso en onboarding y momentos de celebración)

```
Gradient Sunrise: #E8B4C4 → #F0D49A
Gradient Dream: #D8C9E8 → #C8DFE8
Gradient Fresh: #B8E6D9 → #D8C9E8
Gradient Warm: #F0D49A → #E8B4C4
```

**Nota sobre accesibilidad:** Todos los colores pastel cumplen WCAG AA minimum. Se evitaron rojo-verde para daltonismo. Las combinaciones de contraste son:
- Blush Rose + Charcoal: 5.8:1 (WCAG AAA)
- Lavender Calm + Charcoal: 4.2:1 (WCAG AA)
- Mint Fresh + Charcoal: 6.1:1 (WCAG AAA)

---

## 3. TIPOGRAFÍA

### Fuentes

**Primary Font (Headlines & Bold Statements):** Inter Tight Bold / Outfits Bold
- Familia: Sans-serif moderno
- Uso: H1, H2, botones principales, CTAs
- Peso: 700 (Bold)
- Características: Geométrica, amigable, moderna

**Secondary Font (Body & UI):** Inter (Fallback: SF Pro Display)
- Familia: Sans-serif versátil
- Uso: Body text, labels, buttons secundarios
- Pesos: 400 (Regular), 500 (Medium), 600 (Semibold)
- Características: Legibilidad óptima, excelente en small sizes

**Accent Font (Microinteractions):** Crimson Text (Italic)
- Familia: Serif clásico
- Uso: Testimonios, frases motivacionales, "Sí puedes" moments
- Peso: 400 Italic
- Características: Elegancia, feminidad sin forzar, accesible

### Escala Tipográfica

| Uso | Font | Size (Mobile) | Size (Desktop) | Weight | Line Height | Letter Spacing |
|-----|------|---------------|----------------|--------|-------------|----------------|
| **H1** | Inter Tight | 28px | 36px | 700 | 1.2 | -0.5px |
| **H2** | Inter Tight | 24px | 28px | 700 | 1.25 | -0.3px |
| **H3** | Inter Tight | 20px | 24px | 600 | 1.3 | 0px |
| **H4** | Inter Tight | 18px | 20px | 600 | 1.35 | 0px |
| **Body Large** | Inter | 16px | 18px | 400 | 1.5 | 0.3px |
| **Body Regular** | Inter | 14px | 16px | 400 | 1.5 | 0.3px |
| **Body Small** | Inter | 12px | 14px | 400 | 1.4 | 0.2px |
| **Button** | Inter | 14px | 16px | 600 | 1.4 | 0.5px |
| **Label/Tag** | Inter | 12px | 12px | 500 | 1.2 | 0.2px |
| **Caption** | Inter | 11px | 12px | 400 | 1.3 | 0px |

---

## 4. COMPONENTES UI

### Buttons

**Primary Button**
- Background: Blush Rose (#E8B4C4)
- Text: Charcoal (#2A2A2A)
- Border Radius: 12px
- Padding: 12px 24px (mobile: 12px 20px)
- Height: 48px (mobile), 44px (tap targets accessible)
- Shadow: 0 4px 12px rgba(232, 180, 196, 0.3)
- Hover: Background +5% darker, shadow +2px
- Active: Background +10% darker, scale 0.98
- Disabled: #ABABAB, opacity 0.5

**Secondary Button**
- Background: Transparent
- Border: 2px Lavender Calm (#D8C9E8)
- Text: Charcoal (#2A2A2A)
- Border Radius: 12px
- Padding: 12px 24px
- Hover: Background Lavender Calm at 20% opacity
- Disabled: Border #ABABAB, text #ABABAB

**Tertiary Button (Text-only)**
- Background: Transparent
- Text: Blush Rose (#E8B4C4)
- Font Weight: 600
- Underline: None (hover: underline appears)
- Padding: 8px 12px (touch-friendly)

**Ghost Button (Floating Actions)**
- Background: White with 1px border Light Grey
- Icon color: Blush Rose
- Border Radius: 24px (fully rounded)
- Padding: 12px 12px
- Shadow: 0 2px 8px rgba(0, 0, 0, 0.08)
- Hover: Shadow +4px, scale 1.05

### Cards

**Standard Card**
- Background: White
- Border Radius: 16px
- Padding: 16px
- Border: 1px Light Grey (#E8E6E4)
- Shadow: 0 2px 8px rgba(0, 0, 0, 0.06)
- Hover (interactive): Shadow 0 8px 20px rgba(0, 0, 0, 0.1)
- Transition: 300ms ease-out

**Elevated Card** (Outfit preview)
- Background: White
- Border Radius: 20px
- Padding: 20px
- Border: None
- Shadow: 0 8px 24px rgba(232, 180, 196, 0.15)
- Aspect ratio: 1:1 (square para fotos de outfits)

**Glass Morph Card** (Premium feel)
- Background: Lavender Calm at 30% opacity with backdrop filter blur(10px)
- Border: 1px White at 50% opacity
- Border Radius: 16px
- Padding: 16px
- Shadow: Inset 0 1px 2px rgba(255, 255, 255, 0.5)

### Input Fields

**Text Input**
- Background: Off White (#F8F7F6)
- Border: 2px Light Grey (#E8E6E4)
- Border Radius: 12px
- Padding: 14px 16px
- Font: Inter Regular 14px
- Height: 48px (mobile tap target)
- Focus: Border 2px Blush Rose, shadow 0 0 0 3px rgba(232, 180, 196, 0.2)
- Error: Border 2px #D65D5D
- Label: Above input, Inter Medium 12px, Slate Grey

**Textarea**
- Same as text input
- Min-height: 100px
- Resize: Vertical only
- Row indicator bottom-right: "0/280 caracteres" (Slate Grey)

**Dropdown/Select**
- Same input styling
- Arrow: Blush Rose (#E8B4C4)
- Option hover: Background Lavender Calm 20%
- Option selected: Background Blush Rose, text White

**Toggle Switch**
- Width: 52px (mobile: 48px)
- Height: 28px
- Border Radius: 14px (pill shape)
- Off state: Background Light Grey, thumb White
- On state: Background Mint Fresh (#B8E6D9), thumb White
- Animation: 250ms ease-in-out
- Label: Right-aligned or above, Inter Medium 14px

### Icons

**Style:** Rounded, minimalist, 2-3px stroke width
**Size system:** 16px, 20px, 24px, 32px, 40px
**Colors:**
- Primary: Blush Rose (#E8B4C4)
- On surfaces: Slate Grey (#5F6B7A)
- On colored bg: White or Charcoal depending on contrast
**Icon set recommended:** Feather Icons or Phosphor Icons (customized to pastels)

### Tags/Chips

**Neutral Tag**
- Background: Lavender Calm (#D8C9E8) at 40% opacity
- Text: Charcoal (#2A2A2A)
- Border Radius: 20px (pill)
- Padding: 6px 12px
- Font: Inter Medium 12px

**Color Tag** (Body type, style, season)
- Background: Corresponding Blush/Mint/Sky color at 60% opacity
- Text: Charcoal
- Border: 1px corresponding color
- Border Radius: 20px

**Removable Chip**
- Same as neutral tag
- With small "X" icon right-aligned
- Hover: Background opacity +20%
- Click to remove

---

## 5. SPACING SYSTEM (8px base)

| Size | px | Use |
|------|----|----|
| **xs** | 4px | Micro-spacing between inline elements |
| **sm** | 8px | Padding in small components, space between related items |
| **md** | 16px | Standard padding in cards, spacing between sections |
| **lg** | 24px | Section spacing, vertical rhythm |
| **xl** | 32px | Major section breaks |
| **2xl** | 48px | Full-screen vertical gaps |
| **3xl** | 64px | Hero spacing |

**Example application:**
- Card padding: 16px (md)
- Button padding horizontal: 24px (lg)
- Section margin-bottom: 32px (xl)
- Input label margin-bottom: 8px (sm)

---

## 6. ESTADOS & MICROINTERACTIONS

### Button States

**Idle → Hover → Active → Disabled**

```
Idle:     Scale 1.0, opacity 1.0, shadow base
Hover:    Scale 1.02, opacity 1.0, shadow +4px (100ms ease)
Active:   Scale 0.98, opacity 0.9, shadow -2px (50ms ease)
Disabled: Scale 1.0, opacity 0.5, no pointer-events
```

### Loading State

**Indicator:** Animated dots or spinner
- Color: Blush Rose
- Animation: 1.5s infinite
- Position: Center or inline with text
- Text: "Analizando tu estilo..." (empowering, never negative)

### Success Animation

**Trigger:** After outfit analysis, wardrobe uploaded, outfit saved
- Animation: Checkmark circle scale-in (300ms)
- Duration: 2s hold, then fade out (300ms)
- Color: Mint Fresh (#B8E6D9)
- Confetti micro-moments (optional, 500ms)

### Empty States

**Illustration:** Friendly, warm character (illustration style TBD)
- Heading: "Tu inventario está vacío"
- Body: "Sube fotos de tu ropa para empezar a crear outfits mágicos"
- CTA: Primary button "Subir ropa"
- Background: Light Lavender wash (D8C9E8 at 10% opacity)

### Error States

**Toast Notification:**
- Background: Error color (#D65D5D) with 95% opacity
- Text: White, Inter Medium 14px
- Icon: Alert circle icon
- Action: Dismiss button or auto-close in 5s
- Position: Bottom center (mobile), top-right (desktop)
- Animation: Slide up + fade in (300ms)

---

## 7. LAYOUT & GRID

### Mobile (375px - 568px)

**Safe Area:** 16px padding on left/right
**Grid:** 2-column or full-width cards
**Max width:** 343px (content area)
**Vertical rhythm:** 24px sections

### Tablet (600px - 768px)

**Safe Area:** 24px padding on left/right
**Grid:** 3-column layout
**Max width:** 720px (content area)

### Desktop (1024px+)

**Safe Area:** 32px padding on left/right
**Grid:** 4-column or masonry layout
**Max width:** 1200px (content area)
**Sidebar option:** For wardrobe inventory view

---

## 8. TONE & VOICE FOR COPYWRITING

### Core Principles

1. **Never shame or judge** — Analyze, don't critique
2. **Empower always** — Every message should make users feel capable
3. **Use "you" language** — Personal, conversational, direct
4. **Celebrate bodies** — Acknowledge diversity naturally
5. **Be honest but kind** — No false advertising, genuine support

### Example Copy

| Situation | DO ✓ | DON'T ✗ |
|-----------|------|--------|
| **Body analysis screen** | "Entendiendo tu forma para crear outfits perfectos" | "Analizando tus defectos" |
| **Empty wardrobe** | "Tu armario está listo para brillar" | "Wardrobe is empty" |
| **Failed upload** | "Intenta de nuevo con mejor luz" | "Upload failed - invalid image" |
| **Outfit suggestion** | "Este look celebra tu estilo" | "This outfit is recommended" |
| **Virtual try-on result** | "¿Te ves hermosa? Guardarlo →" | "Preview outfit" |
| **Feedback moment** | "¿Cómo se siente este look?" | "Rate this outfit" |
| **Diversity message** | "Todos los cuerpos son hermosos en [brand]" | "All sizes welcome" |

### Tone Examples by Feature

**Onboarding:**
> "Hola! Soy tu asesor de imagen. Juntos vamos a encontrar outfits que te hagan sentir increíble, sin importar tu forma o talla. ¿Comenzamos?"

**Wardrobe Analysis (post-upload):**
> "¡Qué colección! 🎨 He visto tus colores preferidos, tu estilo y tus piezas claves. Ahora podemos crear combinaciones que nunca habías imaginado."

**Virtual Try-On (moment of empowerment):**
> "Mírате. Este eres tú. Completa. Segura. Hermosa. ¿Guardas este look?"

**Inventory Alert (low items):**
> "Noté que necesitas más opciones en [color/categoria]. ¿Exploramos juntas nuevas piezas que combinen con tu estilo?"

**Feature Discovery:**
> "Pro tip: El análisis de cuerpo es privado (encriptado). Solo tú sabes cómo se ven estos datos. Seguridad y confianza, siempre."

---

## 9. ICONOGRAPHY

### Icon Categories & Examples

**Navigation Icons:**
- Home, Heart (saved), Wardrobe/Closet, Análisis, Perfil
- Style: Rounded, 24px default

**Action Icons:**
- Plus (add), Trash, Edit, Share, Download, Camera
- Style: Rounded, 20px or 24px

**Status Icons:**
- Checkmark, X, Alert, Info, Loading spinner
- Style: Rounded, 20px

**Body/Clothing Icons:**
- Body shape (rounded pear, rectangle, hourglass, etc.)
- Clothing category (shirt, pants, dress, shoes, accessories)
- Style: Friendly, inclusive, stylized not realistic

### Icon Library

**Recommended:** Phosphor Icons + custom modifications or Feather Icons with rounded corners
- Stroke width: 2-2.5px
- Corner radius: 2-3px (subtle rounding)
- Colors: Use primary/secondary palette

---

## 10. ACCESSIBILITY CHECKLIST (WCAG 2.1 AA)

- [ ] All text has minimum 4.5:1 contrast ratio (normal text)
- [ ] Interactive elements 3:1 contrast ratio minimum
- [ ] Buttons min 44x44px tap targets (mobile)
- [ ] No color alone conveys information (pair with icon/text)
- [ ] Focus indicators visible (ring or outline)
- [ ] Form labels associated with inputs (<label> tags)
- [ ] Images have descriptive alt text
- [ ] Video/audio have captions and transcripts
- [ ] Keyboard navigation works fully (Tab, Enter, Arrow keys)
- [ ] Screen reader friendly (ARIA labels where needed)
- [ ] Motion/animation can be disabled (prefers-reduced-motion)
- [ ] Sufficient line height (1.4x minimum)
- [ ] Sufficient letter spacing (0.2em minimum)
- [ ] Font size 16px minimum for body text
- [ ] No infinite scrolling without alternative pagination
- [ ] Error messages are descriptive and constructive
- [ ] Links have descriptive text (not "click here")

---

## 11. MOTION & ANIMATION

### Principles

- **Duration:** 300ms standard, 150ms for micro, 500ms for emphasis
- **Easing:** ease-out for entries, ease-in-out for transitions
- **Respect:** Always check prefers-reduced-motion
- **Purpose:** Every animation should communicate or delight

### Animation Library

| Animation | Duration | Easing | Use |
|-----------|----------|--------|-----|
| **Fade in** | 300ms | ease-out | Elements entering screen |
| **Scale up** | 300ms | ease-out | Cards, buttons appearing |
| **Slide left → right** | 400ms | ease-out | Page navigation |
| **Bounce** | 600ms | cubic-bezier(0.34, 1.56, 0.64, 1) | Celebratory moments |
| **Spin** | 1.5s | linear | Loading states |
| **Pulse** | 2s | ease-in-out | Breathing effect on key elements |
| **Shimmer** | 2s | linear | Loading skeleton screens |

### Page Transitions

- Mobile: Slide in from right (400ms ease-out)
- Desktop: Fade in + subtle scale (300ms ease-out)
- No jarring jumps; smooth visual continuity

---

## 12. DARK MODE (Future Consideration)

**Colors to invert:**
- Off White (#F8F7F6) → #1F1F1F (Dark charcoal)
- Charcoal (#2A2A2A) → #F0F0F0 (Off white)
- Light Grey (#E8E6E4) → #2A2A2A (Darker)
- Pastels: Increase saturation +10%, decrease brightness -5% to maintain visibility

**Implementation:** CSS custom properties (var(--color-primary)) + @media (prefers-color-scheme)

---

## 13. COMPONENTS BREAKDOWN

### Screen 1: Onboarding & Body Analysis

**Goal:** Make body analysis feel safe, empowering, not invasive

**Elements:**
1. Welcome illustration (friendly, warm character)
2. Heading: "Conoce tu estilo"
3. Subheading: "Nuestro análisis es privado y encriptado"
4. 4-step process indicator (dots, subtle animation)
   - Step 1: Fotos
   - Step 2: Preferencias
   - Step 3: Colores
   - Step 4: Lista de tamaños
5. Body type selector (visual, not text-heavy)
   - Icons showing 6-8 body shapes (pear, rectangle, hourglass, etc.)
   - Labels: "(Esto no define tu belleza, solo nos ayuda)"
6. CTA: "Continuar con el Análisis" (Primary button)

**Copy tone:** Warm, reassuring, no judgment
**Color usage:** Pastels background (Lavender 10%), cards in white
**Animation:** Smooth transitions between steps, checkmark on completion

---

### Screen 2: Wardrobe Upload & Organization

**Goal:** Make uploading clothes fun and organized

**Elements:**
1. Camera button (large, prominent, Blush Rose)
2. Upload status (photos count, organizing animation)
3. Auto-categorized items preview
   - Grid layout (mobile: 2 col, desktop: 4 col)
   - Cards with clothing photo + auto-detected category
   - Tags for color, type, season
4. Manual organization options
   - Drag to category
   - Add custom tags
5. CTA: "Mi primer outfit ✨" (celebratory tone)

**Copy tone:** Encouraging, "You're building something amazing!"
**Color usage:** Mint Fresh accents for success, Lavender backgrounds
**Animation:** Skeleton loading → item reveal with fade-in

---

### Screen 3: Outfit with Virtual Try-On

**Goal:** Show outfit on diverse body type; celebrate the result

**Elements:**
1. Header: "Tu look para hoy" with user's body type indicator
2. Outfit preview section (central focus)
   - 1:1 aspect ratio card
   - High-res composite image (AI-generated virtual try-on)
   - User's body type in outfit
3. Details breakdown:
   - Item names (clickable to wardrobe)
   - Color palette of outfit (3-4 color circles)
   - "Mood" tag (Casual, Professional, Date night, etc.)
4. Action buttons:
   - Heart icon (save to favorites)
   - Share icon (export/social)
   - "Ver en espejo" (AR try-on if available)
5. Rating section: "¿Cómo se siente este look?" (sentiment, not numeric)
   - Options: 😍 Adorado | 🤔 Undecided | 👎 Guardalo para después

**Copy tone:** Celebratory, empowering, "You look amazing"
**Color usage:** Elevated card with soft shadow, pastel accents
**Animation:** Outfit reveal with staggered item appearance, success confetti on save

---

### Screen 4: Wardrobe Inventory + Smart Carousel

**Goal:** Organize and visualize wardrobe; discover new combos

**Elements:**
1. Inventory summary
   - Total items count
   - Color distribution pie chart (visual)
   - "Coverage" indicator (clothes per category)
2. Filter/sort bar
   - Color, Type, Season, Mood
3. Grid view of wardrobe items
   - Swipeable cards (mobile) or grid (desktop)
   - Item photo + tags
   - Tap to view outfits using this item
4. "Smart Suggestions" carrousal
   - "5 outfits usando esto" for a selected item
   - Pre-generated from wardrobe data
5. CTA: "Crear nuevo outfit" (Primary button)

**Copy tone:** Informative, inspiring, "Look at what you have!"
**Color usage:** Light backgrounds, colorful tags, neutral cards
**Animation:** Smooth carousel swipe, filter transitions

---

## 14. VISUAL LANGUAGE

### Illustration Style

**Character/Avatar:**
- Rounded, soft forms (no sharp angles)
- Warm colors (use pastel palette)
- Diverse body types represented
- Empowering poses (standing tall, smiling, confident)
- Style: Cheerful but sophisticated (not cartoonish, not hyper-realistic)
- Recommended: Illustration style similar to Bumble or Headspace (modern, friendly, inclusive)

**Recommended illustrator style:** "Flat + soft shadows" or "Minimalist character design"

### Photography Style (for try-on results & inspiration)

**Approach 1: AI-Generated Virtual Try-On**
- Photorealistic composite images
- Diverse model bodies (varied sizes, shapes, skin tones)
- Lighting: Natural, flattering (golden hour aesthetic)
- Background: Clean, neutral (white, light grey)

**Approach 2: User-Generated Content**
- Real customer photos in outfits
- Authentic, unretouched
- Community celebration ("Your looks" gallery)
- Model diversity requirement: At least 60% diverse body types

**Photographer/AI Platform Recommendation:**
- AI: Use Runway ML, Stable Diffusion with custom model, or partnership with fashion tech like CLO 3D
- Real photography: Hire diverse photographers, create shooting guidelines emphasizing body diversity

---

## 15. MICRO-COPY LIBRARY

### Common UI Labels

| Component | Copy |
|-----------|------|
| Primary CTA | "Crear Outfit" / "Guardar Look" / "Continuar" |
| Secondary CTA | "Editar" / "Compartir" / "Ver más" |
| Destructive CTA | "Eliminar" / "Descartar" |
| Loading | "Analizando tu estilo..." / "Creando tu look..." |
| Success | "¡Lo guardé!" / "¡Listo!" / "¡Qué hermoso!" |
| Error | "Intenta de nuevo" / "Algo salió mal. Reintentar" |
| Empty state | "Aquí irán tus outfits guardados" |
| Placeholder text | "Ej: Casual chic" / "Escribe..." |
| Toggle on | "Activado" |
| Toggle off | "Desactivado" |

### Empowerment Phrases

- "Tu estilo, tus reglas"
- "Siéntete increíble hoy"
- "Mírате. Completa. Hermosa."
- "Ningún cuerpo es 'equivocado'"
- "Aquí celebramos TU belleza"
- "Confía en ti misma"

---

## 16. DESIGN DELIVERABLES CHECKLIST

- [ ] Figma file with all screens
- [ ] Component library (buttons, cards, inputs, icons)
- [ ] Responsive breakpoints (mobile 375, tablet 768, desktop 1280)
- [ ] Interactive prototypes (basic flow onboarding → outfit creation)
- [ ] Accessibility annotations (contrast, focus states, ARIA)
- [ ] Icon set (downloaded or custom-created)
- [ ] Typography file (font weights, sizes, line heights)
- [ ] Color tokens (CSS variables ready)
- [ ] Animation specs (Lottie files or CSS animations)
- [ ] Dark mode variants (for future)
- [ ] Design handoff docs (for developers)

---

## 17. NEXT STEPS FOR IMPLEMENTATION

1. **Week 1:** Set up Figma workspace, create component library
2. **Week 2:** Design 3 key screens (onboarding, outfit, inventory)
3. **Week 3:** Create interactive prototype, user test with 5-8 users
4. **Week 4:** Refine based on feedback, create all remaining screens
5. **Week 5:** Design handoff, developer collaboration

**Tools:**
- Figma (design + prototyping)
- Lottie/Rive (animations)
- Accessibility checker plugin (Stark, WAVE)
- Figma to code plugin (optional, for CSS export)

---

## DOCUMENT INFO

- **Version:** 1.0
- **Last updated:** March 29, 2026
- **Created by:** Erik, Senior Designer
- **For:** Image Advisor AI + Virtual Try-On App
- **Status:** Ready for implementation
