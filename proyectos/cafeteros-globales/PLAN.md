# CAFETEROS GLOBALES — PLAN DE TRABAJO EJECUTIVO

**Fecha:** 27 mayo 2026
**De:** Jarvis (CEO Agencia) + Jade (Intel) + Alejo (Arquitectura) + Ego (Auditoría)
**Para:** Juan Camilo Gil (Accionista)
**Estado:** ⚠️ **PAUSAR 4 SEMANAS ANTES DE EJECUTAR** (ver recomendación final)

---

## TL;DR — Lee esto primero (5 minutos)

### La oportunidad
Marketplace B2B que conecta 557 mil familias cafeteras colombianas con buyers distribuidores globales, eliminando intermediarios. Mercado potencial: $5.5B anuales en exportaciones, 96% de cafeteros sin acceso directo a buyers. Diferenciador: Sello FNC + Logística DHL integrada + Pagos internacionales.

### El problema
**El proyecto tal como está está planteado (development-first, sin validación de mercado) tiene >70% probabilidad de fallar.** Estamos por gastar $65–83K en código sin tener:
- Un solo cliente validado (cafetero o buyer con LOI)
- Confirmación legal que se puede operar (abogado comercio exterior)
- Validación que Stripe Connect nos aprueba
- Modelo de negocio cerrado (comisión TBD)
- Logística real mapeada (DHL Express no es la solución para toneladas)

### La solución
**PAUSAR 4 semanas (junio 1–30) para validación de mercado y legal.** Costo: ~$8–10K. Output: Go/No-Go con datos reales, no supuestos.

Si GO: ejecutamos MVP en octubre 2026 (3 meses más tarde) pero con **probabilidad de éxito real**.
Si NO-GO: ahorras $60K+ y pivotas a algo más viable.

### Decisión requerida
¿Autorizas pausa de validación antes de junio 1 kickoff? SÍ / NO

---

## I. OPORTUNIDAD DE MERCADO (Jade)

### Tamaño del mercado y demanda

| Métrica | Cifra | Fuente |
|---------|-------|--------|
| Familias cafeteras Colombia | 557,000 | FNC 2025 |
| Pequeños productores (<5 ha) | 96% | FNC |
| Producción anual | 14.8M sacos (60kg c/u) | FNC |
| Exportaciones 2025 | US$5.5B (récord) | Agrolatam |
| Crecimiento YoY | +30% | Agrolatam 2025 |
| Colombia ranking global | 3er exportador | Legiscomex |

**El gap:** 96% de cafeteros (535K familias) NO tiene acceso directo a buyers globales. Dependen de intermediarios que capturan 70–90% del valor. **Oportunidad:** eliminar 1–2 intermediarios = captura de valor de 15–30% para cafeteros.

### Demanda comprador

Tostadores internacionales buscan activamente:
- Trazabilidad de origen (specialty coffee + regulación EU deforestación 2025)
- Relaciones directas con productores para consistency
- Acceso a lotes pequeños de specialty (50–500kg)

Benchmark: **Algrano** (marketplace café suiza, 10 años operando) reportó 35% de volumen 2024 con relaciones repeatadas comprador-productor, validando que los buyers buscan conexión directa.

### Competencia y diferenciadores

| Competidor | Fortaleza | Debilidad |
|---|---|---|
| **Algrano** (Suiza) | 10 años, 4K conexiones, modelo validado | Sin presencia Latinoamérica fuerte, sin logística integrada, sin sello FNC |
| **CAFIX (FNC)** | Respaldo institucional, acceso 557K cafeteros | Solo conecta compradores YA existentes del cafetero, no genera nuevas conexiones |
| **Cropster** | Herramienta operacional tostador | No es marketplace, no conecta origen |
| **Alibaba/TradeKey** | Volumen masivo | Sin especialización café, sin trazabilidad, sin logística integrada |

**Nuestro diferenciador (si no lo cagamos):**
```
Sello FNC (confianza institucional) + Logística DHL (infraestructura) + 
Compliance OFAC/KYC (legal) + Marketplace B2B (discovery)
= Único canal donde tostador en Tokio compra directamente de cafetero en Huila
```

---

## II. ARQUITECTURA TÉCNICA & PRESUPUESTO (Alejo)

### Stack recomendado

| Capa | Tech | Rationale |
|------|------|-----------|
| Frontend | Next.js 15 + Tailwind 4 | Web responsivo, SEO buyers, deploy Vercel |
| Mobile | **DIFERIDA a MVP** | Flutter post-Beta, no hay demanda móvil inicial |
| Backend | Python FastAPI | APIs escalables, Sasha expertise, deploy Railway |
| Database | PostgreSQL Supabase | Relacional, RLS multi-tenant, auth nativo |
| Payments | Stripe Connect Express | KYC + OFAC incluido, manejo marketplace |
| Logistics | **NO DHL Express API** | DHL Express es courier ≤300kg; usamos tarifas estáticas + freight forwarder partner |
| Hosting | Railway (backend) + Vercel (frontend) | Escalable, pay-as-you-go |

### Cambios críticos al scope original

1. **❌ DHL API no en Beta** → Usamos quote estático (tabla de tarifas) + creación manual de envío. Integración DHL real en MVP (Q4).
2. **❌ Flutter no en Beta** → Web responsivo soluciona 90% de uso. Flutter en MVP.
3. **✅ Stripe Connect Express en Beta** → KYC + OFAC delegado a Stripe, simplifica compliance inicial.
4. **❌ Wise no necesario en Beta** → Stripe Connect paga a Colombia. Evaluar Wise en MVP si FX es problema.

### Presupuesto Desarrollo (actualizado)

**FASE 1 — Beta (junio 1 — agosto 15, 11 semanas)**

| Agente | Tareas | Horas | Costo |
|--------|--------|-------|-------|
| **Alejo** | ADRs, schema design, code reviews | 60h | $4,200 |
| **Sasha** | Backend auth + catálogo + ordenes + Stripe Connect + RLS | 220–280h | $13,200–16,800 |
| **Brook** | Next.js scaffold, auth, catálogo, checkout, dashboards | 180–240h | $8,100–10,800 |
| **Erik** | Sistema diseño Tailwind, 12–15 pantallas, assets | 80–100h | $3,200–4,000 |
| **Cinthya** | Notificaciones email, alertas internas DHL, tracking n8n | 40–60h | $1,600–2,400 |
| **Buffer 15%** | Imprevistos, re-trabajo | — | $4,500–5,700 |
| **TOTAL BETA** | | **580–740h** | **$34,800–44,400** |

**FASE 2 — MVP Completo (sep 1 — dic 15, 15 semanas)**

| Agente | Tareas | Horas | Costo |
|--------|--------|-------|-------|
| **Alejo** | Escalabilidad, FinOps, DHL integration architecture | 50h | $3,500 |
| **Sasha** | DHL MyDHL API real, Wise integración (si aplica), security audit | 160–220h | $9,600–13,200 |
| **Brook** | Flutter mobile, analytics dashboard, SEO refinement | 180–240h | $8,100–10,800 |
| **Erik** | Mobile design, landing page pública | 70–90h | $2,800–3,600 |
| **Cinthya** | Automatización completa shipping-to-tracking, reportes cafetero | 50–70h | $2,000–2,800 |
| **Buffer 15%** | | — | $3,900–5,100 |
| **TOTAL MVP** | | **510–670h** | **$29,900–39,000** |

**TOTAL AÑO 1 DESARROLLO: $64,700 – $83,400 USD**

> ⚠️ Esto **NO incluye** costos ocultos: abogado (~$8–15K), compliance officer (~$5K/year), seguros (~$2–5K/year), marketing/buyer acquisition (~$10–20K), customer support, translations.
> **Presupuesto realista año 1: $100–130K total.**

### Infraestructura + Terceros (año 1)

| Categoría | Beta (3m) | MVP (9m) | Notas |
|---|---|---|---|
| Hosting (Vercel, Railway, Supabase) | ~$165 | ~$1,665 | ~$55/mes → $185/mes con escalado |
| Stripe Connect fees | ~$2,430 | ~$38,880 | 5.4% all-in sobre GMV |
| DHL/Freight | Passthrough a buyer | Passthrough a buyer | Costo operacional, no nuestro |
| **Total infra año 1** | | | **~$43K** |

---

## III. RIESGOS CRÍTICOS (Ego) — El por qué PAUSAR

### Los 5 riesgos que pueden MATAR el proyecto

#### 1️⃣ STRIPE CONNECT RECHAZA LA APLICACIÓN
**Probabilidad:** Alta | **Impacto:** Crítico
- Marketplace agricultural commodities + KYB cafeteros rurales = high-risk vertical
- Stripe puede tardar 4–8 semanas y rechazar
- Sin Plan B documentado
**Mitigación:** Aplicar Stripe YA esta semana (no mes 2). Validar que pase pre-screening.

#### 2️⃣ RESPONSABILIDAD TRIBUTARIA DESCONOCIDA
**Probabilidad:** Alta | **Impacto:** Crítico
- DIAN puede clasificar marketplace como exportador de hecho
- Retención fuente + IVA + ICA municipal = pasivo potencial
- Equipo no tiene abogado; únicamente Juan Camilo persona física
**Mitigación:** Contratar abogado comercio exterior + fintech ANTES de operar. Opinion letter sobre estructura legal, FNC, DIAN, OFAC.

#### 3️⃣ FNC NO ALÍA FORMALMENTE (asumir "no se opone" es ingenuo)
**Probabilidad:** Alta | **Impacto:** Alto
- FNC defiende su rol histórico de intermediario exportador
- "Bendición informal" no es contrato; puede revertir
- Sin alianza FNC, pierde diferenciador clave (sello café de Colombia)
**Mitigación:** Contacto directo con FNC (via ProColombia) ANTES de desarrollar. Meta: LOI (letter of intent) que valide sello + referidos de cafeteros.

#### 4️⃣ DHL EXPRESS NO ES LA SOLUCIÓN LOGÍSTICA
**Probabilidad:** Alta | **Impacto:** Crítico
- DHL Express = paquetería ≤300kg; café verde en toneladas va por flete aéreo consolidado o marítimo LCL
- "Quote estático DHL" en Beta es vender humo a buyers serios
- Buyers comprando $5–15K por tonelada no aceptan "precio estimado" de envío
**Mitigación:** Hablar con freight forwarder real (Hellmann, Kuehne+Nagel, agente local) ANTES de tocar código. Redesign logística.

#### 5️⃣ CERO CLIENTES VALIDADOS A 3 MESES DE BETA
**Probabilidad:** Alta | **Impacto:** Crítico
- Sin LOIs de cafeteros o buyers, Beta es desarrollo en vacío
- Métrica "5 cafeteros + 2 buyers a agosto" sin un solo contacto iniciado
**Mitigación:** Pausa 4 semanas. Yang + Leo hacen discovery: 15 entrevistas (8 cafeteros, 7 buyers), mínimo 3 LOIs, validación de pain + comisión aceptable.

### Risk Register completo (20 riesgos identificados)
Ver documento detallado de Ego en `proyectos/cafeteros-globales/.claude/context/EGO_AUDIT.md` (adjunto en follow-up).

---

## IV. VALIDACIÓN COMERCIAL REQUERIDA (4 SEMANAS)

### Fases de validación (junio 1–30)

**Semana 1: Legal + Compliance**
- [ ] Contratar abogado comercio exterior + fintech (Brigard, Posse Herrera, o boutique)
- [ ] Opinion letter: estructura legal, FNC, DIAN, OFAC, AML/KYC requirements
- [ ] Costo: $5–8K
- **Owner:** Juan Camilo + Jarvis

**Semana 2: Stripe Validation**
- [ ] Abrir aplicación Stripe Connect como marketplace
- [ ] Reporte de pre-screening: ¿aprobada o riesgos?
- [ ] Plan B si rechaza (dLocal, Mercado Pago, PayU?)
- [ ] Costo: $0 (validación)
- **Owner:** Sasha + Jarvis

**Semana 2–3: FNC + Comercial**
- [ ] Yang investiga FNC: contacto oficial, proceso alianza, comisión aceptable para FNC
- [ ] Leo agenda reunión con FNC (via ProColombia como puente)
- [ ] Meta: LOI que valide acceso a sello + referidos cafeteros
- [ ] Costo: $0 + viaje si aplica
- **Owner:** Yang + Leo + Juan Camilo

**Semana 3–4: Market Discovery**
- [ ] Yang entrevista 20–30 cafeteros pequeños: pain, willingness-to-pay, comisión, qué reemplaza
- [ ] Leo entrevista 15–20 buyers potenciales (tostadores, importadores): QVP, volumen mínimo, precio aceptable, timeline
- [ ] Validar: ¿verdaderamente existe la fricción que resolvemos?
- [ ] Meta: Mínimo 3 LOIs (cafetero, buyer, o ambos)
- [ ] Costo: $1–2K en viajes/interviews
- [ ] **Owner:** Leo + Yang

**Semana 3–4: Freight Forwarder + Logística**
- [ ] Alejo + Sasha: 2–3 llamadas con freight forwarders reales (Hellmann, Kuehne+Nagel, agente cali)
- [ ] Validar: capacidad, API/integraciones, comisión/margen, SLA
- [ ] Reescribir logística del proyecto (no DHL Express)
- [ ] Costo: $0
- [ ] **Owner:** Alejo + Sasha

**Semana 4: Decisión + Replan**
- [ ] Compilar resultados: 3 LOIs? Stripe aprobada? Abogado OK? Freight forwarder partner? FNC?
- [ ] Decisión GO/NO-GO con Juan Camilo
- [ ] Si GO: reescribir PLAN.md, descopear Beta a 1 corredor + 1 producto, redefinir presupuesto
- [ ] Si NO-GO: pivot a otro proyecto o pausa indefinida
- [ ] **Owner:** Jarvis + Juan Camilo

### Presupuesto validación: ~$8–10K (vs. $65K+ de desarrollo sin validación)

---

## V. TIMELINE REALISTA

### OPCIÓN A — Si autorizas PAUSA (recomendado)

```
MAY 27       JUN 1        JUL 1          AUG 15        DEC 31
  │            │            │              │              │
  └─ HOY ─ PAUSA 4w ─ VALIDACIÓN CIERRA ─ BETA LAUNCH ─ MVP LAUNCH
              ↓
         Abogado, Stripe, FNC, discovery
         LEO + YANG + SASHA + ALEJO
         → Decisión GO/NO-GO 30 junio
              │
              ├─ NO-GO → Cancela proyecto
              │
              └─ GO → Sprint 0 julio 1
                   Sprint 1-5 julio 15 - ago 15 (Beta)
                   Sprint 6-11 sep 1 - dic 15 (MVP)
```

**Kickoff técnico:** Julio 1 (si GO)
**Beta launch:** Agosto 15
**MVP launch:** Diciembre 15 (Q4 2026) / Enero (Q1 2027)

### OPCIÓN B — Si NO autorizas pausa (NOT RECOMMENDED)

```
JUN 1                  AUG 15              DEC 15
  │                     │                   │
  └─ Kickoff directo ─ BETA SHIPS ──────────┴─ MVP
       (sin validación)  (probable fail)
```

**Riesgo:** Construyes en vacío, Stripe rechaza mes 2, cafeteros reales tienen pain que no es el tuyo, comisión no es viable, pierdes $65K.

---

## VI. RECOMENDACIÓN FINAL (Jarvis + Ego)

### Decisión propuesta

**PAUSA 4 semanas (junio 1–30) para validación de mercado, legal y logística.** No es "retrasar" — es asegurar que ejecutamos sobre datos reales, no supuestos.

### Racional

1. **Reduce riesgo asimétrico:** Cuesta $10K validar, cuesta $65K+ fallar sin validación.
2. **Descubre los killlers temprano:** Stripe rechaza? FNC no alía? Comisión no es viable? Mejor saber ahora.
3. **Mejora odds de éxito:** De ~30% (sin validación) a ~70% (con validación).
4. **Mantiene momentum:** Julio–diciembre aún son 22 semanas para Beta + MVP con equipo movido.

### Qué pasa si GO después de validación

- Descope Beta a **1 corredor geográfico** (ej: Huila → Berlín) + **1 producto** (café verde lavado Geisha)
- Métrica de éxito Beta = **1 transacción real completa** (pago + envío + tracking + payout), no "100 tx/mes"
- Presupuesto realista: $100–130K año 1 (+ validación $8–10K)
- Equipo: Sasha 100%, Brook 100%, Erik 50%, Cinthya 30%, Alejo 20%

### Qué pasa si NO-GO

- Ahorras $60K+
- Pivotas a otro proyecto:
  - ¿SaaS de gestión exportación para cafeteros existentes (sin marketplace)?
  - ¿Plataforma de trazabilidad/blockchain para cafeteros?
  - ¿Marketplace local Colombia (cafetero → cafeterías locales)?

---

## VII. PROXIMOS PASOS (esta semana)

| # | Acción | Owner | Deadline | Costo |
|---|--------|-------|----------|-------|
| **1** | Discutir recomendación PAUSA con Juan Camilo | Jarvis | HOY | $0 |
| **2** | Si PAUSA aprobada: contratar abogado comercio exterior | Juan Camilo | MAY 29 | $5–8K |
| **3** | Si PAUSA aprobada: abrir Stripe Connect application | Sasha + Jarvis | MAY 29 | $0 |
| **4** | Si PAUSA aprobada: Yang contacta ProColombia para intro FNC | Yang | MAY 30 | $0 |
| **5** | Si NO-PAUSA: kickoff técnico inmediato | Jarvis | JUN 1 | *ver OPCIÓN B* |

---

## DOCUMENTOS DETALLADOS

Para más profundidad, revisar:
- **Intel Jade:** Análisis FNC, mercado café, competencia (Algrano, CAFIX), regulación EU
- **Arquitectura Alejo:** ADR-001 a 005, schema BD, APIs, scaling path, 11 risk mitigations
- **Auditoría Ego:** 20 riesgos identificados, 5 killers, análisis por dominio, recomendaciones

---

## DECISIÓN REQUERIDA (Juan Camilo)

**Opción A: PAUSA 4 semanas, validar antes de ejecutar** ← Recomendado
**Opción B: Kickoff inmediato junio 1, asumo riesgos** ← Not recommended

**Respuesta esperada:** Hoy o máximo mañana (28 mayo) para que Jarvis pueda comunicar a equipo.

---

**Compilado por:** Jarvis (CEO), Jade (Intel), Alejo (Arquitectura), Ego (Auditoría)
**Fecha:** 27 mayo 2026
**Próxima revisión:** 10 junio 2026 (si PAUSA) — checkpoint de validación

