# IMAGE ADVISOR AI + VIRTUAL TRY-ON
## Complete Design System v1.0

**Designer:** Erik
**Date:** March 29, 2026
**Status:** Ready for Implementation

---

## OVERVIEW

This is a **complete, production-ready design system** for an AI-powered fashion app that:
- Analyzes user body type
- Generates personalized outfit recommendations
- Shows outfits on the user's specific body type (virtual try-on)
- Organizes wardrobe with smart suggestions

**Target users:** Gen Z & Millennials (all genders)
**Key requirement:** Pastel colors, inclusive, never judgmental
**Platform:** Mobile-first (85% usage)

---

## WHAT'S INCLUDED

### 1. **Complete Design System** (70 pages)
File: `design-system-image-advisor-ai.md`

✅ Color palette (5 pastels + 4 neutrals, all WCAG AA+)
✅ Typography system (3 fonts, 13 text styles, complete scale)
✅ Component library (buttons, cards, inputs, tags, icons, etc.)
✅ Spacing system (8px base unit)
✅ Animation specifications (timing, easing, purpose)
✅ Layout & grid system (mobile → tablet → desktop)
✅ Accessibility checklist (WCAG 2.1 AA)
✅ States & microinteractions (hover, active, disabled, loading, error)

**Use this for:** Design implementation, component development, consistency checks

---

### 2. **Three Key Mockups** (45 pages)
File: `mockups-detailed-specs.md`

✅ **Screen 1: Onboarding & Body Analysis**
   - Step-by-step process, never judgmental
   - Copy: "Esto no define tu belleza"
   - Responsive layouts (mobile, tablet, desktop)

✅ **Screen 2: Outfit with Virtual Try-On**
   - Hero elevated card showing outfit on user's body
   - Item details, color palette, mood tags
   - Empowerment moment: "MÍRАТЕ. Completa. Hermosa."

✅ **Screen 3: Wardrobe Inventory + Carousel**
   - Organized inventory with summary stats
   - Smart filters (color, type, season, mood)
   - Carousel: "5 outfits using this item"

Each mockup includes:
- ASCII wireframes with detailed spacing
- Color breakdown
- Interactive element specifications
- Animation timing
- Accessibility notes
- Copy tone guidance

**Use this for:** UI implementation, developer specs, user testing prototypes

---

### 3. **Tone & Voice Guide** (60 pages)
File: `tone-voice-copywriting-guide.md`

✅ **5 Core Tone Pillars:**
1. Empowering, not directive
2. Inclusive, not exclusive
3. Genuine, not performative
4. Conversational, not corporate
5. Body-neutral, not body-obsessed

✅ **Comprehensive Copy Library:**
- 50+ example phrases organized by screen
- Phrases to ALWAYS use (empowerment, celebration)
- Phrases to NEVER use (judgment, corporate speak)
- Copy by feature (onboarding, upload, outfit creation, etc.)
- Writing style rules (short sentences, contractions, exclamation marks)
- Examples for all user states (first-time, returning, power user)
- Push notification & email templates

✅ **Complete Example Flows:**
- Full onboarding flow with all copy
- Error messaging (constructive, helpful)
- Empty states (inviting, not depressing)
- Celebration moments (genuine joy)

**Use this for:** Copywriting, user messaging, brand training, QA copy review

---

### 4. **Illustration & Photography Guide** (50 pages)
File: `illustration-photography-style-guide.md`

✅ **Part 1: Character Illustration (Adora)**
- Brand character profile (warm, approachable, body-positive)
- Visual style specification (flat + soft shadows, not hyper-realistic)
- Reference artists to study (Bumble, Headspace, Calm, Coolors)
- 6 illustration scenarios (welcome, onboarding, loading, success, error, empty)
- Color palette for illustrations
- Technical specifications (hi-res PNG, SVG, animation-ready)

✅ **Part 2: Virtual Try-On Photography**
- **Option A:** AI-Generated (Runway ML, Stable Diffusion) — Recommended
  - Cost: $3,600-9,300 for 3 months
  - Speed: 2-3 weeks
  - Scalability: Infinite outfits

- **Option B:** Real Model Photography
  - Cost: $8,500-20,500
  - Speed: 4-5 weeks
  - Quality: High-end, luxury feel

✅ **Photography Style Direction**
- Body diversity requirements (10+ body types per outfit)
- Skin tone diversity (8+ tones)
- Lighting & posture specifications
- What to AVOID (over-retouching, pose that's too model-like)
- What to INCLUDE (natural skin, genuine expressions)

✅ **Reference Photographers**
- ASOS Design, Outfittery, Vestiaire Collective, Stitch Fix, The Outnet

**Use this for:** Illustrator RFP, photography vendor selection, quality assurance

---

### 5. **Executive Summary** (30 pages)
File: `EXECUTIVE-SUMMARY.md`

✅ High-level overview of entire system
✅ Design decisions explained
✅ Accessibility compliance details
✅ Files delivered & what's ready
✅ Cost estimates ($43,600-66,300 for MVP)
✅ Timeline (4-5 months)
✅ Success metrics
✅ Key differentiators vs. competitors
✅ Questions for Jarvis & Juan Camilo

**Use this for:** Leadership presentations, investor decks, project kickoffs

---

### 6. **Technical Handoff to Jarvis** (50 pages)
File: `HANDOFF-TO-JARVIS.md`

✅ **Design System → Code** (CSS/Tailwind examples)
- Color tokens implementation
- Typography system in code
- Component library structure

✅ **Frontend Stack Recommendations**
- Mobile: Flutter or React Native
- Web: Next.js 15 + Tailwind 4
- Code examples for buttons, inputs, spacing

✅ **Backend Requirements**
- User profile schema (TypeScript)
- Wardrobe management API
- Outfit generation algorithm
- Virtual try-on integration
- Analytics & tracking

✅ **Mobile Considerations**
- Flutter implementation details
- Camera & image upload specs
- Performance targets

✅ **Accessibility Checklist** (for implementation)

✅ **Questions for Jarvis** (architecture, features, timeline)

**Use this for:** Developer briefs, architecture planning, code review

---

### 7. **Quick Reference Guide** (10 pages)
File: `QUICK-REFERENCE.md`

✅ Color palette at a glance
✅ Typography sizes (quick lookup)
✅ Component quick specs
✅ Spacing system
✅ Animation timings
✅ Accessibility checklist (one page)
✅ Tone & voice rules (DO's and DON'Ts)
✅ Key phrases (copy templates)
✅ Mockup overview
✅ File locations & who needs what
✅ Quick decision trees (color, size, spacing)

**Use this for:** Daily reference, printing, bookmarking, team training

---

### 8. **This Document**
File: `README.md`

Navigation guide for all files.

---

## QUICK START GUIDE

### For Jarvis (Gerente de Programación)
1. Read: **EXECUTIVE-SUMMARY.md** (30 min)
2. Skim: **HANDOFF-TO-JARVIS.md** (20 min)
3. Bookmark: **QUICK-REFERENCE.md**
4. Share all files with team

### For Sasha (Backend Developer)
1. Read: **HANDOFF-TO-JARVIS.md** (sections 1-5)
2. Reference: **design-system-image-advisor-ai.md** (accessibility section)
3. Use code examples from HANDOFF-TO-JARVIS.md

### For Brook (Frontend Developer)
1. Read: **HANDOFF-TO-JARVIS.md** (sections 2-3)
2. Deep dive: **design-system-image-advisor-ai.md** (complete)
3. Reference: **mockups-detailed-specs.md** (spacing & sizing)
4. Create Figma component library from specs

### For Copywriters/Cinthya
1. Read: **tone-voice-copywriting-guide.md** (complete)
2. Use: Copy library for all screens
3. Reference: **QUICK-REFERENCE.md** (copy templates)

### For Jade (Training)
1. Read: **tone-voice-copywriting-guide.md**
2. Train team on 5 tone pillars
3. Review all copy before shipping

### For Illustration Vendor
1. Read: **illustration-photography-style-guide.md** (Part 1)
2. Study: Reference artists provided
3. Create character design brief

### For Virtual Try-On Vendor
1. Read: **illustration-photography-style-guide.md** (Part 2)
2. Analyze: Cost/benefit of AI vs. real photography
3. Propose platform & timeline

---

## FILE STRUCTURE

```
/erik/
  ├── README.md (you are here)
  ├── design-system-image-advisor-ai.md (70KB)
  ├── mockups-detailed-specs.md (45KB)
  ├── tone-voice-copywriting-guide.md (60KB)
  ├── illustration-photography-style-guide.md (50KB)
  ├── EXECUTIVE-SUMMARY.md (30KB)
  ├── HANDOFF-TO-JARVIS.md (50KB)
  └── QUICK-REFERENCE.md (10KB)

Total: ~315KB of design documentation
```

---

## KEY STATISTICS

### Colors
- 5 primary pastels (all WCAG AA+)
- 4 neutral colors
- 4 functional colors (error, success, warning, disabled)
- 4 gradient combinations

### Typography
- 3 font families
- 13 text styles
- Scale from 11px → 36px

### Components
- 4 button variants
- 3 card types
- 4 input types
- 6 component categories

### Spacing
- 8px base unit system
- 7 spacing values (xs → 3xl)

### Mockups
- 3 complete screens
- 6 variations (mobile, tablet, desktop)
- ASCII diagrams for all

### Copy
- 50+ example phrases
- 10+ complete flows
- 100+ specific copy recommendations

### Illustrations
- 6 character scenarios
- Character style guide
- 5 reference artists

### Try-on Options
- 2 platforms recommended (Runway, Stable Diffusion)
- 2 real photography strategies
- Budget estimates for both
- Timeline estimates

---

## DESIGN PRINCIPLES

Every decision in this system is guided by:

1. **Empowerment** — Users feel capable, not judged
2. **Inclusion** — All body types celebrated equally
3. **Accessibility** — WCAG AA from day one
4. **Warmth** — Pastels + conversational tone
5. **Simplicity** — Beautiful but not complicated
6. **Data-driven** — Colors, fonts, components researched
7. **Scalability** — Every component documented for devs

---

## SUCCESS DEFINITION

✅ **Technical success:** Zero design debt, all specs documented, developers have clear implementation path

✅ **User success:** Users feel empowered, safe, celebrated. They trust the brand.

✅ **Business success:** Users complete onboarding >70%, save outfits >50%, return week 1→4 >40%

**Not:** "How many users?" but "Do users feel better about themselves after using this?"

---

## TIMELINE & NEXT STEPS

### This Week
- [ ] Jarvis reviews design system
- [ ] Jarvis reviews technical handoff
- [ ] Align on architecture & vendors

### Week 2-3
- [ ] Send illustration brief to vendors
- [ ] Select AI/photography platform for try-on
- [ ] Sasha starts backend design
- [ ] Brook prepares Figma setup

### Week 4-5
- [ ] Illustrator starts character design
- [ ] Virtual try-on platform training
- [ ] Sasha builds APIs
- [ ] Brook builds component library

### Week 6-8
- [ ] Integration testing
- [ ] User testing with diverse participants
- [ ] Refinement based on feedback
- [ ] Final QA

---

## QUESTIONS & SUPPORT

### I have a question about...

**...the color system?**
→ See QUICK-REFERENCE.md (color section) or design-system-image-advisor-ai.md (section 2)

**...typography or spacing?**
→ See QUICK-REFERENCE.md (typography/spacing) or design-system-image-advisor-ai.md (sections 3-5)

**...how to implement this?**
→ See HANDOFF-TO-JARVIS.md (complete technical guide)

**...the copy/voice?**
→ See tone-voice-copywriting-guide.md (complete library)

**...the mockups?**
→ See mockups-detailed-specs.md (3 complete screens)

**...illustrations or try-on?**
→ See illustration-photography-style-guide.md

**...high-level overview?**
→ See EXECUTIVE-SUMMARY.md

**...quick lookup?**
→ See QUICK-REFERENCE.md

---

## CONTACT & COLLABORATION

**Questions or feedback?** → Reach out to Erik

**Ready to implement?** → Share HANDOFF-TO-JARVIS.md with dev team

**Need Figma file?** → Erik can set up component library in Figma

**Need illustrated mockups?** → Erik can create high-fidelity designs in Figma

---

## VERSION & UPDATES

| Version | Date | Status |
|---------|------|--------|
| 1.0 | March 29, 2026 | Complete, ready for implementation |
| 1.1 | TBD | Dark mode variant (requested by Jade?) |
| 1.2 | TBD | Tablet-specific layouts |
| 2.0 | TBD | Additional features, expanded component library |

---

## FINAL NOTE

This design system is **beautiful because it's kind.**

Every color, every word, every interaction is designed to make users feel:
- **Safe** — Your body type won't be judged
- **Empowered** — You'll find outfits that make you feel incredible
- **Seen** — Your body is celebrated, not hidden
- **Inspired** — Technology works for you, not against you

That's the real value: **It's not just pretty. It's kind.**

---

## HOW TO USE THIS DOCUMENT

1. **First time?** → Read this (README.md) + EXECUTIVE-SUMMARY.md
2. **Need implementation?** → Read HANDOFF-TO-JARVIS.md
3. **Daily reference?** → Bookmark QUICK-REFERENCE.md
4. **Deep dive on component?** → Go to design-system-image-advisor-ai.md (sections 1-7)
5. **Copy everything?** → Use tone-voice-copywriting-guide.md

---

**Ready to build something beautiful. 💙**

*Created by Erik, Senior Designer*
*For Image Advisor AI + Virtual Try-On*
*March 29, 2026*

