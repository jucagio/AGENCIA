# CAFETEROS GLOBALES — Plataforma de Marketplace Café

## Identidad del Proyecto
**Nombre comercial:** Cafeteros Globales (TBD con marketing)

**Descripción:** Marketplace especializado que conecta cafeteros colombianos con compradores distribuidores globales. Logística 100% integrada vía DHL. Modelo B2B2C (cafeteros → buyers internacionales).

**Visión:** Convertir a pequeños cafeteros colombianos en exportadores directos. Reducir intermediarios. Transacciones de lotes (bultos de ~1 tonelada).

---

## Timeline Crítico
- **HOY:** 27 mayo 2026
- **BETA:** Agosto 2026 (3 meses) — 3-5 cafeteros test + 1-2 buyers test, transacciones reales
- **MVP COMPLETO:** Q4 2026 / Q1 2027 — Lanzamiento público
- **ESCALA:** 100 transacciones/mes durante año 1

---

## Métricas de Éxito Fase 1

| Métrica | Target | Timeline |
|---------|--------|----------|
| Cafeteros activos | 10 (año 1) | Q4 2026 |
| Transacciones/mes | 100 (año 1) | Q4 2026 |
| Volumen/mes | ~100 toneladas | Q4 2026 |
| Conversión (leads → sellers) | >30% | Beta + Q4 2026 |
| NPS cafeteros | >40 | Q4 2026 |
| NPS buyers | >50 | Q4 2026 |

---

## Features MVP (Beta + Año 1)

### Beta (Agosto 2026)
- [ ] Sign up cafeteros (manual FNC validation)
- [ ] Sign up buyers (manual admin approval)
- [ ] Crear catálogo café (variedad, volumen, precio, cupo)
- [ ] Browse & filtrar catálogo (buyers)
- [ ] Crear orden (buyer selecciona café + cantidad)
- [ ] Checkout + pago internacional (Stripe?)
- [ ] DHL logistics: creación label, tracking basic
- [ ] Dashboard cafetero: mis órdenes, ganancias
- [ ] Dashboard buyer: mis órdenes, tracking
- [ ] Email notificaciones (orders, shipments)

### MVP Completo (Q4 2026)
- Lo anterior +
- [ ] Chat cafetero ↔ buyer (negociación precios)
- [ ] Ratings & reviews
- [ ] Batch management (bundlear múltiples órdenes a DHL)
- [ ] Invoice generation + tax compliance
- [ ] Analytics: trending cafés, buyers by region, export volumes
- [ ] Onboarding FNC (automático, si aplica regulación)
- [ ] API para integraciones (buyers ERP)
- [ ] Mobile app (iOS/Android) MVP

---

## Stack Técnico (Propuesto)

| Capa | Tech | Justificación |
|------|------|---------------|
| Frontend | Next.js 15 + Tailwind 4 | Web + rápido, SEO para buyers |
| Mobile | Flutter | iOS + Android con mismo código |
| Backend | Python FastAPI | APIs escalables, pagos + DHL |
| Base de datos | PostgreSQL (Supabase) | Relacional (órdenes, inventario), RLS para multi-tenant |
| Pagos | Stripe (internacional) + Wise (payouts) | Pagos cross-border simples |
| Logistics API | DHL Express API | Integración directa (labels, tracking) |
| Storage | Supabase Storage | Documentos (invoices, certificates) |
| Hosting | Railway (backend) + Vercel (frontend) | Escalable, pay-as-you-go |
| Auth | Supabase Auth + JWT | Multi-tenant (cafeteros ≠ buyers) |

---

## Arquitectura de Alto Nivel

```
┌─────────────────────────────────────────────────────────────────┐
│                      BUYERS GLOBALES (Web + App)                │
│                    (Distribuidores, Roasters, etc)              │
└─────────────────────┬───────────────────────────────────────────┘
                      │ HTTPS/REST
┌─────────────────────┴───────────────────────────────────────────┐
│                     CAFETEROS GLOBALES API                      │
│         (FastAPI, Supabase Auth, PostgreSQL)                    │
├─────────────┬────────────────┬────────────────┬─────────────────┤
│   Orders    │   Catalog      │   Payments     │   Logistics     │
│   Service   │   Service      │   Service      │   Service       │
│             │                │                │   (DHL API)     │
└─────────────┴────────────────┴────────────────┴─────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
   PostgreSQL    Supabase      Stripe +
   (data)        Storage       Wise APIs
                 (docs)        (pagos)
```

---

## Equipo Asignado

| Rol | Agente | Dedicación | Notas |
|-----|--------|-----------|-------|
| **CEO Proyecto** | Jarvis | Full-time | Coordina, decisiones estratégicas |
| **Backend** | Sasha | Full-time | APIs, pagos, integración DHL |
| **Frontend Web** | Brook | Full-time | Marketplace UI, dashboards |
| **Mobile** | Brook (sub-agente) | Híbrido | Flutter app |
| **Diseño** | Erik | Híbrido | Sistema diseño cafeteros-globales |
| **Automatización** | Cinthya | Híbrido | Workflows DHL, notificaciones, reportes |
| **Intel & Comercial** | Jade + Yang | As-needed | Investigación FNC, regulación, benchmarking |
| **Arquitectura** | Alejo | Híbrido | Review decisiones técnicas críticas |
| **Auditoría** | Ego | As-needed | Auditorías de seguridad, compliance |

---

## Riesgos Críticos (para Alejo + Ego)

1. **Regulación FNC** — ¿Qué autorización necesita café para marketplace?
2. **Pagos internacionales** — Compliance OFAC, AML, tax per país
3. **Logistics** — ¿DHL puede manejar 100 toneladas/mes? ¿Qué pasa si falla un envío?
4. **Trust** — Cafeteros + buyers van a necesitar garantías (escrow, insurance)
5. **Competencia** — ¿Alibaba está haciendo algo similar?

---

## Presupuesto (TO BE CALCULATED)

Jalvis + Alejo armarán estimado detallado en el PLAN.md con:
- Horas/agente
- Infraestructura
- Integraciones (Stripe, DHL, Wise)
- Testing & QA

---

## Próximos pasos
1. ✅ Crear PLAN.md detallado (Jarvis + Alejo)
2. ⏳ JADE investiga: FNC, regulación, mercado, competitors
3. ⏳ EGO audita riesgos
4. ⏳ Presentar plan a Juan Camilo con presupuesto
5. ⏳ Kickoff oficial con equipo

---

**Owner:** Jarvis (CEO Agencia)
**Creado:** 27 mayo 2026
**Estado:** Fase de planeamiento estratégico
