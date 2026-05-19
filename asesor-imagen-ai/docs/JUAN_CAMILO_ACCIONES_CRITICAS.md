# ACCIONES CRÍTICAS — Juan Camilo Gil

**Owner:** Juan Camilo Gil (Accionista)  
**Deadline:** HOY y MAÑANA (2026-05-18/19)  
**Impact:** Sprint 0.4 + 0.5 execution  
**Status:** ⏳ AWAITING YOUR INPUT

---

## 🚨 RESUMEN URGENTE

El proyecto está 100% especificado pero **requiere TUS decisiones** para continuar.

**Sin esto, todo se bloquea:**
1. Erik no puede diseñar 6 screens (S05-S11)
2. Antigravity no puede iniciar Sprint 0.5
3. Timeline a launch entra en RIESGO

**Tiempo requerido de ti: 2-3 horas hoy/mañana.**

---

## ✅ ACCIÓN 1: DECISIONES UX (D1-D5)

**Documento:** `docs/DECISIONES_CRITICAS_UX.md`

**5 decisiones binarias** con opciones recomendadas por Leo + Jarvis:

### D1 — App Name
```
A) "AI Fit Check" (tech-forward)
B) "Asesor de Imagen" (local friendly)
C) Dual approach
```
**Recomendación:** A (mejor para SaaS B2B LATAM premium)

### D2 — Try-On Flow
```
A) Upload prenda directo (ágil)
B) Seleccionar de Wardrobe (requiere closet)
C) Ambos (hybrid)
```
**Recomendación:** C (A por defecto, B como opción)

### D3 — Body Analysis Onboarding
```
A) Obligatorio al registrar (higher LTV, -40% DAU)
B) Opcional en Settings (higher DAU, -20% adoption)
C) Triggered en behavior (balance)
```
**Recomendación:** C (triggered on use, no friction upfront)

### D4 — Free Tier Limits
```
A) 3 try-ons/mes (strong paywall)
B) Unlimited preview (lower quality)
C) 1/día limit (psychology-friendly)
D) Hybrid: 1/día free + preview quality
```
**Recomendación:** D (balance revenue + growth)

### D5 — Social Sharing
```
A) Instagram/WhatsApp native sharing (viral)
B) No built-in (manual screenshot)
C) Instagram-only (temporal Stories)
```
**Recomendación:** A (mandatory for viral growth, competitors use it)

---

## ✅ ACCIÓN 2: ENTREGA CREDENCIALES

**Two API keys required for Sprint 0.5:**

### Google Cloud Vision API Key
```
Location: Google Cloud Console
Project: asesor-imagen-ai (o tu proyecto)
API: Vision API (enable si no está)
Service Account: genera private key JSON
Variable: GOOGLE_CLOUD_VISION_API_KEY
```

**Action:** 
1. Go to console.cloud.google.com
2. Enable Vision API
3. Create Service Account (o usar existente)
4. Generate JSON key
5. Send to Jarvis: `{email, key}`

**Timeline:** 10 minutos

### Replicate API Token
```
Location: replicate.com/account
Token: Get API token from account settings
Variable: REPLICATE_API_TOKEN
```

**Action:**
1. Go to replicate.com/account
2. Copy API token
3. Send to Jarvis in DM

**Timeline:** 2 minutos

---

## 📅 TIMELINE CRÍTICA

### HOY (SAB 2026-05-18)
- [ ] **10:00 AM** — Junta Estratégica (Jarvis, Jade, Ego)
  - Presenta tus respuestas D1-D5 en formato simple:
    ```
    D1: [X] A / [ ] B / [ ] C
    D2: [X] A / [ ] B / [ ] C
    D3: [ ] A / [X] B / [ ] C
    D4: [ ] A / [ ] B / [ ] C / [X] Hybrid
    D5: [X] A / [ ] B / [ ] C
    ```
  - Confirma credenciales timeline
  
- [ ] **Antes de las 6 PM** — Envía:
  - D1-D5 respuestas a Jarvis
  - GCV API key (JSON) a Jarvis
  - Replicate token a Jarvis

### MAÑANA (DOM 2026-05-19)
- [ ] Reunión comercial con Leo + Yang (30 min)
  - Leo te presenta impacto comercial de D1-D5
  - Validar decisiones desde revenue perspective
  - Finalizar cualquier cambio

### SIN ESTO
→ Erik bloqueado esperando D1-D5 (pierde 5-7 días)  
→ Antigravity no puede iniciar Sprint 0.5  
→ Launch 2026-07-31 en RIESGO

---

## 🎯 TUS RESPONSABILIDADES

| Tarea | Deadline | Owner |
|-------|----------|-------|
| D1-D5 decisiones | Hoy | Tú |
| GCV API key | Hoy | Tú |
| Replicate token | Hoy | Tú |
| Validar con Leo (comercial) | Mañana | Tú + Leo |

**Total time:** 2-3 horas HOY + 30 min MAÑANA.

---

## 📞 NEXT STEPS

1. **Lee:** `docs/DECISIONES_CRITICAS_UX.md` (15 min)
2. **Decide:** Marca tus respuestas en formato simple (5 min)
3. **Gather:** GCV key + Replicate token (10 min)
4. **Send:** DM a Jarvis con decisiones + credenciales (1 min)
5. **Reunión:** Leo te explica impacto comercial (30 min mañana)

**Mensaje a Jarvis template:**
```
Decisiones UX:
D1: A (AI Fit Check)
D2: C (both hybrid)
D3: C (triggered)
D4: Hybrid (1/día free + preview)
D5: A (native sharing)

Credenciales:
GCV API key: [paste JSON]
Replicate token: [paste token]

Leo me explica impacto mañana.
```

---

## 🚀 IMPACT IF YOU DELIVER TODAY

✅ Erik can design 6 screens starting tomorrow  
✅ Brook can implement S01-S04 by Thursday  
✅ Antigravity can start Sprint 0.5 next week (post-rate-limiting)  
✅ Timeline to launch STAYS on track (2026-07-31)  
✅ All 3 parallel tracks (backend, frontend, design) UNBLOCKED  

---

**No secrets. No BS. You hold the key. Let's ship.** 🚀

