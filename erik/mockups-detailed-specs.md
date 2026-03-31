# MOCKUPS DETALLADOS
## Image Advisor AI + Virtual Try-On

---

## MOCKUP 1: ONBOARDING & BODY ANALYSIS
### "Análisis seguro, privado, empoderador"

### Layout (Mobile 375px width)

```
┌─────────────────────────────┐
│                             │  ↑ Safe area 16px
│    [Illustration]           │
│  (Friendly avatar)          │
│                             │
│ ─────────────────────────── │
│                             │
│ "Conoce tu estilo"          │ H1: Inter Tight Bold 28px
│                             │ Charcoal (#2A2A2A)
│ "Nuestro análisis es        │
│  privado y encriptado"      │ Body: Inter Regular 14px
│                             │ Slate Grey (#5F6B7A)
│ ─────────────────────────── │
│                             │
│ Step indicator (4 dots)     │ Current step: Blush Rose
│ ● ○ ○ ○                     │ Inactive: Light Grey
│                             │
│ "PASO 1: TU FORMA"          │ Label: Inter Medium 12px
│ (Body type visual cards)    │
│                             │
│ ┌─────────┐ ┌─────────┐    │ 2-column grid
│ │   [Pear]│ │[Rectangle]   │ Cards: 150x150px
│ │ Pera    │ │Rectángulo    │ Border radius: 12px
│ └─────────┘ └─────────┘    │ Selected: Blush Rose border 2px
│                             │
│ ┌─────────┐ ┌─────────┐    │
│ │[Hourglass]   │[Apple] │ │
│ │Reloj de Arena │Manzana │ │
│ └─────────┘ └─────────┘    │
│                             │
│ "(Esto no define tu         │ Caption: Inter Regular 12px
│  belleza, solo nos ayuda)"  │ Honey Warm (#F0D49A) text
│                             │
│ ─────────────────────────── │
│                             │
│ ╔═════════════════════════╗ │ Primary button
│ ║  CONTINUAR CON ANÁLISIS ║ │ Height: 48px
│ ║      (Pink Blush)       ║ │ Width: full - 32px margin
│ ╚═════════════════════════╝ │ Shadow: 0 4px 12px
│                             │ rgba(232, 180, 196, 0.3)
│                             │
│                             │ ↓ Safe area 16px
└─────────────────────────────┘
```

### Color breakdown:
- **Background:** Off White (#F8F7F6)
- **Illustration area:** Lavender Calm (#D8C9E8) at 20% opacity
- **Selected card:** Border 2px Blush Rose, bg White
- **Button:** Blush Rose bg (#E8B4C4), Charcoal text

### Animation specs:
- Page load: Fade in 300ms + slide up 400ms
- Body cards: Stagger entrance 100ms each
- Button: Subtle scale on hover (1.02x)
- Tap feedback: Scale down 0.98x for 150ms

### Copy tone:
> "Conoce tu estilo" — Warm, welcoming heading
> "Nuestro análisis es privado y encriptado" — Security + trust
> "(Esto no define tu belleza, solo nos ayuda)" — Affirmation, never judgment

### Accessibility notes:
- Body type cards have visible focus ring (2px Blush Rose outline)
- Alt text for illustrations: "Friendly character illustration"
- Tab order: body type cards → button
- Keyboard: Arrow keys to navigate cards, Enter to select

---

## MOCKUP 2: WARDROBE ANALYSIS & VISUAL TRY-ON RESULT
### "Tu look perfecto en 10 segundos"

### Layout (Mobile 375px width)

```
┌─────────────────────────────┐
│ [←] "Mi primer Outfit" [⋯]  │ Header bar
│                             │ Back button + Title + Menu
│ ─────────────────────────── │
│                             │
│        Your Body Shape      │ Tag: Lavender Calm bg
│        [Rectangle]          │ "Tu forma: Rectángulo"
│                             │
│ ═════════════════════════════ │ Elevated card begin
│                             │
│    [High-res outfit         │ 1:1 aspect ratio
│     on model/AI body]       │ Border radius: 20px
│                             │ Composite image:
│                             │ Real clothing + your body
│                             │ (Virtual try-on result)
│                             │
│                             │
│ ═════════════════════════════ │ Elevated card end
│                             │
│ DETALLES DEL LOOK:          │ H3: Inter Tight 20px Bold
│                             │
│ ┌─────────────────────────┐ │
│ │ Blusa: Lino blanco      │ │ Item name (clickable)
│ │ (click para ver en      │ │ Subtext: "Ver en armario"
│ │ armario)                │ │
│ └─────────────────────────┘ │
│                             │
│ ┌─────────────────────────┐ │
│ │ Pantalones: Denim       │ │
│ │ classic azul            │ │
│ └─────────────────────────┘ │
│                             │
│ ┌─────────────────────────┐ │
│ │ Accesorios: Bolso       │ │
│ │ caramelo + sandalias    │ │
│ └─────────────────────────┘ │
│                             │
│ PALETA DE COLORES:          │ Label
│ ⭕ #FFFFFF ⭕ #4A90A4      │ 3-4 color circles
│ ⭕ #E8B4C4 ⭕ #F0D49A      │ (colors from outfit)
│                             │
│ MOOD: Casual Elegante       │ Tag style
│ ESTACIÓN: Primavera         │ Secondary tags
│                             │
│ ─────────────────────────── │
│                             │
│ ¿CÓMO SE SIENTE ESTE LOOK?  │ Empowerment moment
│                             │
│ 😍 ADORADO  🤔 UNDECIDED   │ 3 emoji buttons
│ 👎 GUARDAR PARA DESPUÉS     │ (not numeric rating)
│                             │
│ ─────────────────────────── │
│                             │
│ ╔═════════════════════════╗ │ Primary CTA
│ ║   ♥ GUARDAR ESTE LOOK   ║ │ Heart icon + text
│ ╚═════════════════════════╝ │ Blush Rose
│                             │
│ ╔═════════════════════════╗ │ Secondary CTA
│ ║  COMPARTIR / VER EN AR  ║ │ Ghost button
│ ╚═════════════════════════╝ │
│                             │
│                             │
└─────────────────────────────┘
```

### Color breakdown:
- **Card background:** Elevated white card with shadow 0 8px 24px rgba(232, 180, 196, 0.15)
- **Tags:** Lavender Calm at 40% opacity background
- **Mood/Season tags:** Use Honey Warm for season, Sky Soft for mood
- **Button:** Blush Rose (primary), Lavender border (secondary)

### Interactive elements:
- **Item names:** Clickable, navigate to wardrobe detail screen
- **Color circles:** Hover to show hex code
- **Emoji buttons:** Visual feedback (scale 1.1x on hover, bg tint on click)
- **Heart button:** Filled when saved, animated pulse on click

### Animation specs:
- **Page load:** Outfit card scale-in from bottom (300ms ease-out)
- **Item list:** Stagger fade-in (200ms each)
- **Color circles:** Reveal with bounce animation (400ms)
- **Save button:** Checkmark animation on save (300ms) + confetti (500ms optional)

### Copy tone:
> "MÍRАТЕ. Completa. Segura. Hermosa."
> "¿Cómo se siente este look?" (Never ask "Do you like this?")
> "Este look celebra tu estilo" (Empowerment, not just recommendation)

### Accessibility notes:
- Emoji buttons have proper label text: "Adoré este look", "Indeciso", "Guardarlo para después"
- Color information not conveyed by color alone (mood/season with text)
- Focus indicators visible on all buttons
- Item names are links with proper :focus states

---

## MOCKUP 3: WARDROBE INVENTORY + CAROUSEL OF LOOKS
### "Tu armario, organizado y listo"

### Layout (Mobile 375px width)

```
┌─────────────────────────────┐
│ [<] WARDROBE INVENTORY  [⋯] │ Header
│                             │
│ ─────────────────────────── │
│                             │
│ RESUMEN DE MI ARMARIO:      │ Section title
│                             │
│ Total de items: 47          │ Summary stats
│ Colores preferidos:         │ Cards with data
│ ┌─────────────────────────┐ │
│ │ Pastel Blue: 12         │ │ Pie chart or list
│ │ Blush: 10               │ │ with color circles
│ │ White/Neutral: 15       │ │
│ │ Otros: 10               │ │
│ └─────────────────────────┘ │
│                             │
│ ─────────────────────────── │
│                             │
│ FILTRAR Y ORDENAR:          │ Filter bar
│                             │
│ [Color ▼] [Tipo ▼]          │ Compact dropdown buttons
│ [Estación ▼] [Mood ▼]       │ Height: 40px
│                             │
│ ─────────────────────────── │
│                             │
│ GRID DE MI ARMARIO:         │
│                             │
│ ┌──────────┐ ┌──────────┐  │ 2-column grid
│ │ [Photo]  │ │ [Photo]  │  │ Mobile
│ │ Blusa    │ │ Pantalón │  │ Cards: 160x200px
│ │ Blanco   │ │ Azul     │  │ 8px gap
│ │ Verano   │ │ Primaver │  │
│ └──────────┘ └──────────┘  │ Hover: Slight shadow
│                             │ increase, opacity
│ ┌──────────┐ ┌──────────┐  │ increase
│ │ [Photo]  │ │ [Photo]  │  │
│ │ Falda    │ │ Cardigan │  │
│ │ Rosa     │ │ Beige    │  │
│ │ Primaver │ │ Otoño    │  │
│ └──────────┘ └──────────┘  │
│                             │
│ [Load more] or infinite     │
│                             │
│ ─────────────────────────── │
│                             │
│ SUGERENCIAS DE OUTFITS      │ Carousel section
│ Usando [Selected Item]      │ Headline
│                             │
│  ◄  ┌──────────────────┐ ► │ Swipeable cards
│     │   [Outfit 1]     │   │ 280x280px
│     │                  │   │ Snap scrolling
│     │  "Casual Chic"   │   │
│     │   ♥ 0  📤 0      │   │ Like & share counts
│     └──────────────────┘   │
│                             │
│ ─────────────────────────── │
│                             │
│ ╔═════════════════════════╗ │ Primary CTA
│ ║  + CREAR NUEVO OUTFIT   ║ │ Plus icon + text
│ ║  (Blush Rose)           ║ │ Full width
│ ╚═════════════════════════╝ │ Height: 48px
│                             │
│                             │
└─────────────────────────────┘
```

### Desktop (1024px) variant:

```
┌────────────────────────────────────┐
│ [<] WARDROBE INVENTORY        [⋯]  │
│                                    │
│ ────────────────────────────────── │
│                                    │
│ RESUMEN:    │ FILTRAR:              │ 2-column layout
│             │ [Color ▼][Tipo ▼]     │ Summary left (25%)
│ 47 items    │ [Season ▼][Mood ▼]    │ Main content right (75%)
│ Colors...   │                        │
│             │ 4-COLUMN GRID:         │
│             │                        │
│             │ ┌──────┐ ┌──────┐    │ 4-column on desktop
│             │ │Photo │ │Photo │... │
│             │ └──────┘ └──────┘    │
│             │ ┌──────┐ ┌──────┐    │
│             │ │Photo │ │Photo │... │
│             │ └──────┘ └──────┘    │
│             │                        │
│             │ CAROUSEL:              │
│             │  ◄ ┌────────────┐ ►   │ Full width
│             │    │ [Outfit]   │     │
│             │    │ Casual...  │     │
│             │    └────────────┘     │
│             │                        │
│             │ ╔════════════════════╗ │ CTA button
│             │ ║ + CREAR OUTFIT     ║ │
│             │ ╚════════════════════╝ │
│                                    │
└────────────────────────────────────┘
```

### Color breakdown:
- **Grid cards:** White bg with 1px Light Grey border
- **Hover state:** Shadow 0 8px 20px rgba(0,0,0, 0.1) + opacity increase
- **Summary box:** Lavender Calm at 20% opacity
- **Tags:** Use color circles + text labels
- **CTA button:** Blush Rose with plus icon

### Interactive elements:
- **Grid items:** Clickable to expand or view full item details
- **Carousel:** Touch swipe (mobile) or arrow navigation (desktop)
- **Filter buttons:** Dropdown menus with checkboxes
- **Load more:** Pagination or infinite scroll (with "Load more" button visible)

### Animation specs:
- **Grid load:** Stagger fade-in from top (150ms each)
- **Carousel:** Smooth slide animation (300ms ease-out)
- **Filter change:** Grid re-layout with 200ms transition
- **Hover:** Shadow expand (200ms ease-out)

### Copy tone:
> "47 piezas esperando brillar"
> "Ningún artículo debería estar escondido"
> "¿Usando [Item]? Aquí hay 5 formas de combinarla" (for carousel)

### Accessibility notes:
- Filter buttons have aria-expanded, aria-label attributes
- Carousel has keyboard navigation (Arrow left/right)
- Grid items have proper alt text with item description
- Summary stats are in a proper semantic <table> or list
- Focus visible on all interactive elements

---

## MOCKUP ANNOTATIONS: SPACING & SIZING

### Mockup 1 (Onboarding):

```
Illustration area: 240px height
Vertical spacing between sections: 24px (lg)
Body type cards: 150x150px each, 8px gap
Card padding: 16px
Button height: 48px
Button padding horizontal: 24px (lg)
Step indicator: 8px between dots
```

### Mockup 2 (Outfit Result):

```
Elevated card: 20px padding, 20px border-radius
Item detail cards: 16px padding, 12px border-radius
Color circles: 40px diameter
Emoji buttons: 44x44px tap targets
Primary button: 48px height, full width - 32px margins
Secondary button: 44px height
Vertical rhythm between sections: 24px
```

### Mockup 3 (Inventory):

```
Summary box: 16px padding, 12px border-radius
Filter bar: 40px height buttons, 8px gap
Grid gap: 8px (mobile), 16px (desktop)
Grid item card: 160x200px (mobile), 200x250px (desktop)
Carousel card: 280x280px, centered with 16px margin
```

---

## DESIGN SYSTEM INTEGRATION

All mockups use:
- **Typography:** Inter Tight (headings), Inter (body)
- **Colors:** 5 pastels + 4 neutrals (as defined in system)
- **Spacing:** 8px base unit system
- **Components:** Buttons, cards, tags (from component library)
- **Animations:** 300ms standard duration, ease-out easing
- **Accessibility:** WCAG AA minimum on all screens

---

## FIGMA SETUP RECOMMENDATION

1. **Create artboards:**
   - 375px mobile frame
   - 768px tablet frame
   - 1280px desktop frame

2. **Use auto layout:**
   - Cards with padding and gap
   - Buttons with icon + label spacing
   - Grid layouts responsive

3. **Set up variants:**
   - Button: state (idle, hover, active, disabled)
   - Card: type (standard, elevated, glass)
   - Tag: variant (neutral, color, removable)

4. **Create interactive prototype:**
   - Link onboarding → wardrobe upload → outfit result
   - Show filter interactions in inventory screen

5. **Add notes:**
   - Copy tone annotations on each screen
   - Animation timing notes
   - Accessibility checklist
   - Responsive behavior notes

---

## NEXT STEPS FOR ERIK

1. Create Figma file with these 3 screens
2. Build component library
3. Add interactive prototype for basic user flow
4. Get feedback from potential users (diverse body types)
5. Refine based on feedback
6. Handoff to dev team with specs

