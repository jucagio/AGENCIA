# DESIGN HANDOFF TO JARVIS
## Technical Recommendations for Implementation

**From:** Erik, Senior Designer
**To:** Jarvis, Gerente de Programación
**Date:** March 29, 2026
**Purpose:** Bridge design system → technical architecture

---

## OVERVIEW

I've completed a comprehensive design system for the Image Advisor AI app. This document explains how to translate it into technical requirements for your backend, frontend, and AI integration teams.

---

## 1. DESIGN SYSTEM → CODE

### What You're Getting (From Erik)

✅ **1 Color Palette** (Figma variables + CSS custom properties ready)
✅ **1 Typography System** (Inter Tight + Inter fonts, complete scale)
✅ **1 Component Library** (Buttons, cards, inputs, etc. — all specified)
✅ **3 Mockup Flows** (Onboarding, outfit creation, inventory)
✅ **1 Animation Spec** (Timing, easing, purpose for each interaction)
✅ **1 Tone & Voice Guide** (Copy library for all screens)

### What Sasha & Brook Need to Build

**Sasha (Backend):**
1. User profile schema (body type, preferences, color palette)
2. Wardrobe management API (upload, organize, retrieve items)
3. Outfit generation algorithm (color matching, silhouette logic)
4. Virtual try-on integration (call to Runway/Stable Diffusion API)
5. Saved outfits & favorites system
6. Analytics (which outfits were saved, what body types preferred, etc.)

**Brook (Frontend):**
1. React Native or Flutter UI (all components from design system)
2. Camera integration (for wardrobe uploads)
3. Outfit display (high-res image rendering)
4. Interactive flows (step-by-step onboarding, outfit creation)
5. Responsive design (mobile 375px → desktop 1280px)
6. Accessibility features (keyboard nav, screen reader labels)

---

## 2. TECHNICAL REQUIREMENTS FROM DESIGN SYSTEM

### Frontend Stack Recommendation

Based on the design system, here's what works best:

**Mobile (Recommended: Flutter or React Native)**
- Why: Cross-platform, design system transfers easily, animations smooth
- Color system: Easy to implement with MaterialColor + ThemeData (Flutter) or StyleSheet (React Native)
- Components: Use design system for Buttons, Cards, TextFields, Tags
- Typography: Inter Tight (Google Fonts) available on both
- Animations: Flutter has superior animation capabilities (Lottie support)

**Web (Recommended: Next.js 15 + Tailwind 4)**
- Why: Full-stack flexibility, Tailwind matches design token system
- Colors: Define as Tailwind theme (see example below)
- Components: shadcn/ui has good base components to customize
- Typography: Google Fonts (Inter Tight, Inter, Crimson Text)
- Animations: Framer Motion for microinteractions

### Colors → Code (CSS/Tailwind Example)

```css
/* CSS Custom Properties */
:root {
  /* Primary Pastels */
  --color-blush-rose: #E8B4C4;
  --color-lavender-calm: #D8C9E8;
  --color-mint-fresh: #B8E6D9;
  --color-honey-warm: #F0D49A;
  --color-sky-soft: #C8DFE8;

  /* Neutrals */
  --color-charcoal: #2A2A2A;
  --color-slate-grey: #5F6B7A;
  --color-off-white: #F8F7F6;
  --color-white: #FFFFFF;
  --color-light-grey: #E8E6E4;

  /* Functional */
  --color-error: #D65D5D;
  --color-success: #6FB889;
  --color-warning: #E8A747;
  --color-disabled: #ABABAB;
}
```

```javascript
// Tailwind theme configuration
module.exports = {
  theme: {
    colors: {
      blush: '#E8B4C4',
      lavender: '#D8C9E8',
      mint: '#B8E6D9',
      honey: '#F0D49A',
      sky: '#C8DFE8',
      charcoal: '#2A2A2A',
      slate: '#5F6B7A',
      // ... etc
    },
    spacing: {
      xs: '4px',
      sm: '8px',
      md: '16px',
      lg: '24px',
      xl: '32px',
      '2xl': '48px',
      '3xl': '64px',
    },
    borderRadius: {
      sm: '8px',
      md: '12px',
      lg: '16px',
      xl: '20px',
      full: '24px', // for pill shapes
    },
  },
};
```

### Typography → Code

```javascript
// Next.js font configuration (Font Optimization)
import { Inter_Tight, Inter, Crimson_Text } from 'next/font/google'

const interTight = Inter_Tight({
  variable: '--font-inter-tight',
  subsets: ['latin'],
  weight: ['400', '500', '600', '700'],
})

const inter = Inter({
  variable: '--font-inter',
  subsets: ['latin'],
  weight: ['400', '500', '600'],
})

const crimsonText = Crimson_Text({
  variable: '--font-crimson-text',
  subsets: ['latin'],
  weight: ['400'],
  style: ['italic'],
})
```

```css
/* Typography system */
.heading-1 {
  font-family: var(--font-inter-tight);
  font-size: 36px;
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.5px;
}

.heading-2 {
  font-family: var(--font-inter-tight);
  font-size: 28px;
  font-weight: 700;
  line-height: 1.25;
  letter-spacing: -0.3px;
}

.body-regular {
  font-family: var(--font-inter);
  font-size: 16px;
  font-weight: 400;
  line-height: 1.5;
  letter-spacing: 0.3px;
}

/* ... etc for all 13 text styles */
```

---

## 3. COMPONENT LIBRARY IMPLEMENTATION

### Button Component (Example)

**Design spec:**
- Primary: Blush Rose bg, Charcoal text, 12px border-radius, 48px height, 24px h-padding
- States: idle (shadow 0 4px 12px rgba(232,180,196,0.3)), hover (+5% darker), active (scale 0.98)

**React implementation:**
```jsx
export const Button = ({
  variant = 'primary', // 'primary' | 'secondary' | 'tertiary' | 'ghost'
  size = 'md', // 'sm' | 'md' | 'lg'
  disabled = false,
  children,
  ...props
}) => {
  const baseStyles = 'font-semibold rounded-lg transition-all duration-300'

  const variantStyles = {
    primary: 'bg-blush-rose text-charcoal hover:bg-blush-rose-dark shadow-lg hover:shadow-xl active:scale-98',
    secondary: 'border-2 border-lavender text-charcoal hover:bg-lavender/20',
    tertiary: 'text-blush-rose hover:underline',
    ghost: 'border border-light-grey bg-white hover:shadow-md',
  }

  const sizeStyles = {
    sm: 'px-4 py-2 text-sm h-10',
    md: 'px-6 py-3 text-base h-12',
    lg: 'px-6 py-3 text-lg h-[48px] w-full',
  }

  return (
    <button
      disabled={disabled}
      className={`
        ${baseStyles}
        ${variantStyles[variant]}
        ${sizeStyles[size]}
        ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
      `}
      {...props}
    >
      {children}
    </button>
  )
}
```

### All Components Need Similar Treatment

For each component in the design system:
1. Extract visual specs (size, color, spacing, shadow, border-radius)
2. Extract interactive specs (hover, active, disabled states)
3. Extract animation specs (duration, easing, when to trigger)
4. Implement as reusable component
5. Document prop interface
6. Test accessibility (keyboard nav, ARIA labels, contrast)

---

## 4. BACKEND REQUIREMENTS

### User Profile Schema (Sasha needs this)

```typescript
interface UserProfile {
  userId: string
  bodyType: 'pear' | 'rectangle' | 'hourglass' | 'apple' | 'triangle' | 'inverted-triangle' | 'plus-size' | 'petite'
  skinTone: string // for outfit color recommendations
  stylePreferences: string[] // ['casual', 'elegant', 'creative', 'professional']
  colorPreferences: string[] // ['blush', 'lavender', 'mint', 'honey', 'sky']
  favorites: OutfitID[]
  savedOutfits: OutfitID[]
  generatedOutfits: OutfitID[]
  createdAt: timestamp
  lastAnalyzed: timestamp
}

interface WardrobeItem {
  itemId: string
  userId: string
  photoUrl: string
  autoDetected: {
    color: string
    category: 'tops' | 'bottoms' | 'dresses' | 'outerwear' | 'shoes' | 'accessories'
    fabric: string
    season: 'spring' | 'summer' | 'fall' | 'winter' | 'all'
  }
  manualTags: string[]
  timesWorn: number
  lastWorn: timestamp
  createdAt: timestamp
}

interface Outfit {
  outfitId: string
  userId: string
  items: WardrobeItem[]
  generatedImage: string // URL from virtual try-on
  metadata: {
    mood: string
    occasion: string
    colorPalette: string[]
    season: string
    generatedAt: timestamp
  }
  userRating: 'loved' | 'undecided' | 'save-for-later' | null
  saved: boolean
}
```

### API Endpoints Needed

```
POST /api/user/profile
  → Create user profile with body type + preferences

POST /api/wardrobe/upload
  → Upload clothing photo
  → Returns: auto-detected category, color, etc.

POST /api/wardrobe/items
  → Get all user's wardrobe items
  → Params: filter (color, category, season)

POST /api/outfit/generate
  → Generate outfit based on user profile + wardrobe
  → Calls virtual try-on service (Runway/Stable Diffusion)
  → Returns: Outfit object with image

POST /api/outfit/save
  → Save outfit to user's favorites

GET /api/outfit/suggestions/{itemId}
  → Get 5 outfit suggestions using specific item
```

### Virtual Try-On Integration

```typescript
// If using Runway ML or Stable Diffusion
async function generateOutfitImage(
  userBodyType: string,
  clothingItems: WardrobeItem[],
  userProfile: UserProfile
): Promise<string> {
  const prompt = buildPrompt(userBodyType, clothingItems, userProfile)

  const image = await callAIService(prompt, {
    platform: 'runway-ml', // or 'stable-diffusion'
    outputSize: '1080x1440',
    quality: 'high',
  })

  return image.url
}

// Prompt template (important for consistency)
function buildPrompt(bodyType, items, profile): string {
  return `
    A fashion outfit photo showing:
    - Model body type: ${bodyType}
    - Skin tone: ${profile.skinTone}
    - Clothing: ${items.map(i => i.description).join(', ')}
    - Style: ${profile.stylePreferences.join(', ')}
    - Lighting: Natural, flattering, golden hour
    - Background: Clean white or light grey
    - Photography: Professional fashion photography
    - Mood: Confident, comfortable, beautiful

    Important:
    - Show full body head to feet
    - Clothing details must be visible
    - Model should have natural, relaxed posture
    - No retouching artifacts
  `
}
```

---

## 5. MOBILE-SPECIFIC CONSIDERATIONS

### Flutter Implementation (Recommended)

**Why Flutter?**
- Beautiful animations out of the box
- Pastel colors render smoothly
- Single codebase for iOS + Android
- Easy to implement design tokens

```dart
// Color tokens in Flutter
class AppColors {
  static const Color blushRose = Color(0xFFE8B4C4);
  static const Color lavenderCalm = Color(0xFFD8C9E8);
  static const Color mintFresh = Color(0xFFB8E6D9);
  // ... etc
}

// Typography tokens
class AppTypography {
  static const TextStyle heading1 = TextStyle(
    fontFamily: 'InterTight',
    fontSize: 28,
    fontWeight: FontWeight.w700,
    height: 1.2,
    letterSpacing: -0.5,
  );

  static const TextStyle bodyRegular = TextStyle(
    fontFamily: 'Inter',
    fontSize: 14,
    fontWeight: FontWeight.w400,
    height: 1.5,
    letterSpacing: 0.3,
  );
}

// Component example
class PrimaryButton extends StatelessWidget {
  final String label;
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 48,
      width: double.infinity,
      child: ElevatedButton(
        onPressed: onPressed,
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.blushRose,
          foregroundColor: AppColors.charcoal,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          elevation: 4,
          shadowColor: AppColors.blushRose.withOpacity(0.3),
        ),
        child: Text(
          label,
          style: AppTypography.buttonText,
        ),
      ),
    );
  }
}
```

### Camera & Image Upload (Important for onboarding)

```dart
// Using image_picker package
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;

Future<void> uploadClothingPhoto() async {
  final ImagePicker _picker = ImagePicker();
  final XFile? image = await _picker.pickImage(
    source: ImageSource.camera,
  );

  if (image != null) {
    // Compress image
    final File compressed = await _compressImage(File(image.path));

    // Upload to backend
    final response = await http.post(
      Uri.parse('/api/wardrobe/upload'),
      headers: {'Authorization': 'Bearer $token'},
      body: {
        'file': await MultipartFile.fromPath('file', compressed.path),
      },
    );

    // Backend auto-detects color, category, etc.
    final wardrobeItem = WardrobeItem.fromJson(jsonDecode(response.body));

    // Show result to user
    showOutfitGenerationUI(wardrobeItem);
  }
}
```

---

## 6. ACCESSIBILITY IMPLEMENTATION CHECKLIST

### For Sasha (Backend)

- [ ] All text fields have `aria-label` or `aria-labelledby`
- [ ] All color information has redundant text/icon
- [ ] API returns error messages (not just status codes)
- [ ] Keyboard navigation possible for all workflows
- [ ] Images have descriptive alt text
- [ ] No reliance on color alone to convey information

### For Brook (Frontend)

- [ ] Button focus visible (2px ring or outline)
- [ ] Minimum font size 16px for body text
- [ ] Line height minimum 1.4x
- [ ] Link text descriptive (not "click here")
- [ ] Form errors clear and actionable
- [ ] Motion can be disabled (prefers-reduced-motion)
- [ ] Tested with screen reader (NVDA, VoiceOver)
- [ ] Tested keyboard-only navigation
- [ ] Contrast ratios verified (axe, Lighthouse, WAVE tools)

---

## 7. DEPLOYMENT & PERFORMANCE

### Frontend Performance Targets

- **First Contentful Paint (FCP):** <1.5s
- **Largest Contentful Paint (LCP):** <2.5s
- **Cumulative Layout Shift (CLS):** <0.1
- **Time to Interactive (TTI):** <3s
- **Lighthouse score:** >85

### Image Optimization

```javascript
// Outfit images should be:
// - Format: WebP (with JPEG fallback)
// - Size: 1080x1440px max
// - Compression: 85-90% quality
// - CDN delivery: Cloudflare, AWS CloudFront, Vercel Edge
// - Progressive loading: LQIP + blur-up animation

// Example Next.js Image component
<Image
  src={outfit.generatedImage}
  alt="Outfit on your body"
  width={1080}
  height={1440}
  priority={true}
  placeholder="blur"
  blurDataURL={blurHash}
  loading="eager"
/>
```

---

## 8. ANALYTICS & TRACKING

### Events to Track (For insights on user behavior)

```typescript
// Important: Track WITHOUT being creepy
// Privacy-first: No detailed body measurements, no photos stored unnecessarily

trackEvent('onboarding_started', {
  timestamp: now(),
  user_id: anonymized,
  device: 'ios' | 'android' | 'web',
})

trackEvent('body_type_selected', {
  body_type: 'pear' | 'rectangle' | ...,
  step: 1,
})

trackEvent('wardrobe_item_uploaded', {
  item_count: 5, // cumulative
  auto_detected_category: 'tops',
})

trackEvent('outfit_generated', {
  generation_time: 2400, // milliseconds
  success: true,
})

trackEvent('outfit_saved', {
  outfit_id: 'uuid',
  user_rating: 'loved' | 'undecided' | 'save-for-later',
})

trackEvent('outfit_shared', {
  platform: 'instagram' | 'whatsapp' | 'email',
})
```

### DO NOT Track
- Detailed body measurements (privacy)
- Raw face images (privacy + ethics)
- Specific clothing costs (privacy)
- User's real name with data (unless consented)

---

## 9. QUESTIONS FOR YOU (JARVIS)

Before you start implementation, I need answers:

### Architecture Questions:
1. **Database:** PostgreSQL + Supabase? Firebase? Custom?
2. **Backend:** FastAPI, Node.js, or other?
3. **Frontend:** Flutter, React Native, or web-first?
4. **Hosting:** Railway, Render, AWS?
5. **AI integration:** Which platform (Runway, Stable Diffusion, partnership)?

### Feature Questions:
1. **MVP scope:** Just onboarding + 1 outfit? Or full inventory?
2. **Social features:** Share outfits? Follow other users? Community?
3. **E-commerce:** Direct shopping integration? Or just recommendations?
4. **Subscription:** Freemium model? How do you monetize?

### Timeline Questions:
1. **Launch target:** 4 months, 6 months, or flexible?
2. **Sprints:** 2-week sprints? 1-week?
3. **Team size:** How many devs on this? (Sasha only, or larger team?)

---

## 10. HANDOFF NEXT STEPS

### This Week:
- [ ] Jarvis reviews this handoff document
- [ ] Erik + Jarvis align on tech stack
- [ ] Sasha gets backend requirements

### Next Week:
- [ ] Brook gets Figma file with component specs
- [ ] Start illustration RFP (using Erik's brief)
- [ ] Select AI platform for try-on

### Week 3-4:
- [ ] Sasha starts backend architecture
- [ ] Brook builds component library
- [ ] Illustrator starts Adora character design

### Week 5+:
- [ ] Sasha builds APIs
- [ ] Brook builds UI components
- [ ] Integration testing

---

## FILES I'M HANDING OFF

Location: `/erik/`

1. **design-system-image-advisor-ai.md** (Complete system)
2. **mockups-detailed-specs.md** (3 screens with spacing)
3. **tone-voice-copywriting-guide.md** (All copy)
4. **illustration-photography-style-guide.md** (Character brief)
5. **EXECUTIVE-SUMMARY.md** (High-level overview)
6. **HANDOFF-TO-JARVIS.md** (This file)

### Additional Files I Can Create:
- Figma file (component library + mockups) — Ask and I'll set it up
- CSS framework starter — Can provide Tailwind config
- Storybook setup — For component documentation
- Accessibility audit checklist — For QA

---

## FINAL NOTES

### Design System Principles:
Every component, every color, every word is designed to make users feel **empowered, not judged.**

This means:
- When something fails, the error message is helpful, not blaming
- When something succeeds, we celebrate, not minimize
- When showing outfits, they're on REAL body types, not generic models
- When collecting data, we're transparent about privacy

### Technical Implications:
- Backend must be secure (body analysis data is sensitive)
- Frontend must be accessible (different abilities, different devices)
- Images must render beautifully (outfit photos are hero content)
- Animations must perform well (frame drops destroy the feeling)

### Success Definition:
Not "How many users?" but "Do users feel better about themselves after using this app?"

If we nail that, the business metrics will follow.

---

## CONTACT & SUPPORT

**Questions about design system?** → Reach out to Erik
**Questions about implementation?** → Let's sync (Erik + Jarvis + Sasha + Brook)
**Need clarification on spec?** → File is detailed, but happy to explain

---

**Ready to build. Let's make something beautiful.** 💙

