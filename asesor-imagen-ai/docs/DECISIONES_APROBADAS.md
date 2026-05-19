# DECISIONES APROBADAS — D1-D5 FINALES

**Aprobado por:** Juan Camilo Gil  
**Fecha:** 2026-05-18 (SAB)  
**Status:** 🟢 OFICIAL — Válido para toda ejecución  
**Owner:** Jarvis (CEO)

---

## ✅ DECISION RECORD

### D1: APP NAME
**Decisión:** DUAL APPROACH ✅
```
Marca Global: "AI Fit Check"
Tagline/Claim: "Tu Asesor de Imagen Confiable"

En UI:
  • Logo: "AI Fit Check" (pequeño, premium)
  • Subtítulo: "AI Fit Check — Asesor de Imagen" (contexto local)
  • Messaging: "Premium accesible, confiable"

Aplicar en:
  • Splash screens (S01)
  • Header de toda la app
  • App store (Google Play, Apple App Store)
  • Landing page / marketing
```

**Rationale:** Global reach + local trust + premium positioning

---

### D2: TRY-ON FLOW
**Decisión:** HYBRID (upload directo como default) ✅
```
Default Path (Quick Win):
  1. User llega a Virtual Try-On
  2. "Sube tu foto" → prominent CTA
  3. Toma/sube foto de persona
  4. "Elige prendas" (max 5, o sugiere defaults)
  5. "Generar Outfit Ideal" → result en 20-30 seg
  
Secondary Path (With Analysis):
  • Si user tiene body_analysis previo:
    - Offer: "Usar mi análisis de cuerpo para mejores recomendaciones?"
    - Filter: pre-filtered wardrobe items (body-type appropriate)
  
  • Si user es NEW:
    - Wardrobe selection visible pero no required
    - CTA: "Analizar mi cuerpo para mejores combos?" (soft, in-flow)
    - Skip: allow skip, learn from behavior
```

**Rationale:** Minimiza fricción (upload) pero ofrece confianza (análisis) a quien quiera.

---

### D3: BODY ANALYSIS ONBOARDING
**Decisión:** TRIGGERED (gamified escalation) ✅
```
Day 0 (Signup):
  ✗ NO pedir análisis
  ✓ Cero fricción
  → Mensaje: "Empezamos con try-on, luego análisis"

Day 1 (Post 1st try-on):
  Soft offer: "¿Quieres análisis de tu cuerpo para combos aún mejores?"
  CTA: "Sí, analizar" (secondary, soft pill button)
  Alt: "Saltarse por ahora"
  
Day 3 (Post 3rd try-on):
  Gamified: "🎯 Desbloquea tu asesor personal con análisis"
  Progress badge: "3/5 intentos gratis — próximo: análisis"
  
Day 7 (Post 5th try-on):
  Strong push: "Tu análisis de color season = combos perfectos"
  Positioning: "Professional stylists use this"
  CTA: "Iniciar análisis completo" (primary)
```

**Rationale:** Cero fricción upfront, but gamified upgrade feels like feature not barrier.

---

### D4: FREE TIER LIMITS
**Decisión:** HYBRID (1 try-on/día + preview quality) ✅
```
FREE TIER:
  • 1 try-on/día (30/mes equivalent)
  • Preview quality (480p, watermarked)
  • NO share button (preview only)
  • Body analysis available (but limited)
  • Saved collections: 1 max
  • Ads: gentle (contextual, not intrusive)

ESTILO TIER ($9.99/month):
  • 5 try-ons/día
  • 1080p quality (full HD)
  • Share to Instagram Stories + WhatsApp (with watermark)
  • Body analysis unlimited
  • Saved collections: 10 max
  • Priority support: 24h response

IMAGEN TIER ($19.99/month):
  • Unlimited try-ons/día
  • 2K quality (premium)
  • All sharing features (no watermark on Stories)
  • Body analysis unlimited + export
  • Saved collections: unlimited
  • Export templates (for StyleKit integrations)
  • Priority support: 2h response
  • Ad-free experience

Projected MRR (Mes 12):
  • 5K free users × $0 = $0
  • 10K Estilo users × $10 (ARPU) = $100K
  • 5K Imagen users × $20 (ARPU) = $100K
  • Total: $200K+ (target $350-500K = adjust pricing or user volume)
```

**Rationale:** 
- 1/día = sticky (daily habit)
- Preview quality = psychological incentive to upgrade
- Hybrid hits churn, conversion, and scalability concerns

---

### D5: SOCIAL SHARING
**Decisión:** NATIVE SHARING (A) ✅
```
Feature Implementation:
  • Post-result: Big [Share] button below outfit image
  • Platforms supported:
    1. Instagram Stories (PRIMARY: temporary, less spam, high engagement)
    2. WhatsApp (SECONDARY: personal network, high trust)
    3. Instagram Feed (TERTIARY: permanent, lower engagement)
  
  • Watermark: "Created with AI Fit Check — Your Personal Image Advisor"
    - On free tier: watermark visible
    - On Estilo+: watermark on Stories only
    - On Imagen: no watermark
  
  • Referral mechanics:
    - Sharer gets: +1 free try-on (credited to account)
    - Friend who clicks link gets: +1 free try-on (after signup)
    - Trackable via referral code in link
  
  • Analytics:
    - Track: clicks, shares, referral conversions
    - Dashboard: "You've shared X times, recruited Y users"
```

**Rationale:** 
- Required for 1M user target (can't buy all with ads)
- Evangelists share because feature works (not because incentivized)
- Network effect: early users → friends → exponential

---

## 🎯 IMPACT SUMMARY

| Dimension | Impact | Why |
|-----------|--------|-----|
| **Brand** | Premium + Accesible | Dual name, both markets |
| **DAY 1 UX** | Quick win (upload) | Hybrid: result fast, analysis optional |
| **Retention** | +30% (sticky DAU) | 1 try-on/día = daily habit |
| **Conversion** | ~5-8% free→paid | Preview quality incentivizes upgrade |
| **Virality** | Network effect enabled | Native sharing + referrals |
| **MRR Target** | $200K+ path to $350K-500K | Volume + ARPU optimization |

---

## 📋 IMPLEMENTATION CHECKLIST

### For Erik (Design S05-S11)
- [ ] D1: Logo + branding in S01-S11 (all screens show "AI Fit Check — Asesor de Imagen")
- [ ] D2: S04 Virtual Try-On shows upload prominence + optional wardrobe selection
- [ ] D3: S04 result has soft CTA for body analysis (not mandatory, soft)
- [ ] D4: S10 Paywall shows 3 tiers: Free (1/día preview), Estilo ($9.99), Imagen ($19.99)
- [ ] D5: S04 result has [Share] button → Instagram Stories + WhatsApp options

### For Brook (Implementation S01-S04)
- [ ] D1: MaterialApp theme shows branding (logo, tagline)
- [ ] D2: S04 default shows UploadZone prominent, wardrobe as secondary
- [ ] D3: Body analysis as CTA after 1st try-on (can skip)
- [ ] D4: Free tier shows "1/30 try-ons used" counter
- [ ] D5: Share button wired to native intent (Instagram, WhatsApp)

### For Antigravity (Sprint 0.5 Workers)
- [ ] D4: Free tier counter → check usage in body_analysis, try_on tables
- [ ] D5: Track shares → log to try_on.shared, increment referral counter

### For Backend Config
- [ ] Add to `.env`:
  ```
  APP_NAME=AI Fit Check
  APP_TAGLINE=Tu Asesor de Imagen Confiable
  FREE_TIER_LIMIT=1  # try-ons per day
  ESTILO_PRICE_USD=9.99
  IMAGEN_PRICE_USD=19.99
  PREVIEW_QUALITY=480  # pixels
  FULL_QUALITY=1080
  PREMIUM_QUALITY=2048
  ```

---

## 🚀 NEXT STEPS

1. ✅ **Erik:** Unlock para diseñar S05-S11 (ahora tienes todo)
2. ✅ **Brook:** Unlock para S01-S04 (once Flutter issues resolved)
3. ✅ **Antigravity:** Worker integration (S0.5) considera free tier limiting
4. ✅ **Update SPRINT_TRACKER:** Mark D1-D5 as APPROVED

---

## 📝 DECISION AUTHORITY

**Approved by:** Juan Camilo Gil (Founder/Accionista)  
**Validated by:** Jarvis (CEO) — comercial + técnico aligned  
**Date approved:** 2026-05-18  
**Validity:** Permanent unless explicitly changed (with Jarvis + Juan Camilo alignment)

**This is the SINGLE SOURCE OF TRUTH for D1-D5 going forward.**

---

**Status:** 🟢 READY FOR EXECUTION

Erik, you're unblocked. Design S05-S11. Go. 🎨

