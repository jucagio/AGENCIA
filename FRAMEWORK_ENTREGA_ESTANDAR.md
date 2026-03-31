# FRAMEWORK DE ENTREGA ESTÁNDAR — Agencia IA

**Versión:** 1.0 | **Fecha:** 31 Mar 2026 | **Propósito:** Ciclo de entrega consistente (4-8 semanas) | **Dueño:** Sasha (Tech Lead)

---

## 1. ENTRADA (KICK-OFF) — Semana 0

### Información requerida del cliente
- **Scope:** Descripción ejecutiva del problema / oportunidad
- **Usuarios:** Perfiles, volúmenes, geografía, idiomas
- **KPIs:** Métricas de éxito (conversión, tiempo, ahorros, automatización)
- **Restricciones:** Budget, timeline, integraciones existentes, compliance, data sensitivity
- **Acceso:** Credenciales, APIs, bases de datos, contacto técnico cliente

### Validaciones previas (Sasha + Jarvis)
- ✅ Viabilidad técnica: stack, complejidad estimada, dependencies
- ✅ Viabilidad comercial: margen, recursos, riesgo
- ✅ Contrato firmado: scope, SLAs, pagos, IP ownership

### Participantes — Kick-off Meeting (1h)
**Cliente side:** Product Owner, Technical Contact, Sponsor comercial
**Nuestro side:** Jarvis (CEO), Sasha (Tech Lead), Leo (CSM), Brook o Erik (si aplica)

### Entregables
- [ ] Documento de Scope firmado
- [ ] Calendario de entregas confirmado
- [ ] Roles y comunicación establecida (daily standup time, escalation path)
- [ ] Acceso a sistemas cliente validado

---

## 2. FASE 1: DESCUBRIMIENTO — Semana 1 (4 días)

**Objetivo:** Entender el negocio, diseñar solución de alto nivel, validar supuestos

| Tarea | Dueño | Output |
|-------|-------|--------|
| User Research & Entrevistas | Brook + Leo | User personas, jobs-to-be-done, pain points |
| Análisis de Competencia | Yang (si aplica) | Benchmarking, diferenciadores únicos |
| Arquitectura de Alto Nivel | Sasha | Tech architecture diagram, stack decisions |
| Propuesta de Diseño (wireframes) | Erik | Low-fidelity mockups, user flows |
| **Checkpoint 1: Discovery Review** | Jarvis (aprueba) | Acuerdo en solución propuesta |

---

## 3. FASE 2: DISEÑO & ARQUITECTURA — Semanas 1-2 (8 días)

**Objetivo:** Planos técnicos finales, diseño de alta fidelidad, BD diseñada

| Tarea | Dueño | Output |
|-------|-------|--------|
| Arquitectura Detallada (APIs, BD, infra) | Sasha | Architecture docs, ER diagram, API specs, security plan |
| Diseño de Alta Fidelidad | Erik + Brook | Figma design system, component library, prototypes |
| Plan de Datos | Sasha | DB schema, migration strategy, backups |
| Plan de Testing | Brook | QA strategy, test cases, automation plan |
| **Checkpoint 2: Design Review** | Jarvis + cliente | Aprobación de diseños finales antes de code |

---

## 4. FASE 3: DESARROLLO — Semanas 2-6 (4 semanas)

**Objetivo:** Código en producción listo para testing

**Dailies:** 15min standup (Sasha + Brook + Erik + QA)

| Semana | Hito | Tarea | Owner |
|--------|------|-------|-------|
| **Week 2** | Sprint 1 | Backend APIs base + Auth + DB migrations | Sasha |
| **Week 3** | Sprint 2 | Backend features + Frontend foundation + Designs finales | Sasha + Brook + Erik |
| **Week 4** | Sprint 3 | Feature completion + QA integration | Sasha + Brook |
| **Week 5** | Sprint 4 | Performance optimization + Security hardening | Sasha + QA |
| **Week 6** | Sprint 5 | Bug fixes + Documentation + Handoff prep | Sasha + Brook |
| **Checkpoint 3: Dev Complete** | Jarvis | Código en staging, QA ready |

---

## 5. FASE 4: TESTING & OPTIMIZACIÓN — Semanas 6-7 (6 días)

**Objetivo:** Sistema production-ready, documentado, optimizado

| Tarea | Dueño | Output |
|-------|-------|--------|
| QA & Testing (manual + automation) | Brook (QA) | Test report, bug log, fixes verified |
| Performance Testing & Tuning | Sasha + Brook | Load test report, optimization done, SLA validated |
| Security Audit (OWASP compliance) | Sasha (Ego reviews) | Security report, fixes applied, penetration test if needed |
| User Acceptance Testing (UAT) | Cliente side | Signoff on functionality, edge cases, tweaks |
| **Checkpoint 4: Ready for Deploy** | Jarvis + cliente | UAT approved, all blockers resolved |

---

## 6. FASE 5: DEPLOYMENT & HANDOFF — Semana 7-8 (5 días)

**Objetivo:** Producto live, cliente capacitado, soporte en place

| Tarea | Dueño | Output |
|-------|-------|--------|
| Production Deployment | Sasha (infra) | Live, monitoring enabled, backups verified |
| Capacitación Cliente | Leo (CSM) | Training session, docs, knowledge base, support handoff |
| Documentación Final | Brook + Sasha | API docs, deployment runbook, troubleshooting guide, runbooks |
| Transición a Soporte | Leo (CSM) | Support SLA defined, escalation path, response times |
| **Checkpoint 5: Go-Live** | Jarvis | Sistemas monitoreados, cliente autónomo |

---

## 7. ROLES & RESPONSABILIDADES

| Rol | Reporta a | Responsabilidad |
|-----|-----------|-----------------|
| **Tech Lead (Sasha)** | Jarvis | Arquitectura, backend, security, timeline técnico, escalaciones |
| **Product Manager (Brook)** | Sasha | Features, UX, testing, QA, frontend code quality |
| **Designer (Erik)** | Brook | Design system, visuals, prototypes, handoff to developers |
| **Client Success Manager (CSM/Leo)** | Jarvis | Comunicación cliente, alignment, capacitación, post-launch soporte |
| **QA Lead (Brook)** | Sasha | Testing strategy, automation, bug triage, UAT coordination |
| **DevOps/Infra** | Sasha | Deployment, monitoring, CI/CD, backups, SLAs |

---

## 8. CHECKPOINTS & APROBACIONES

| Checkpoint | Aprobado por | Si hay bloques |
|------------|--------------|----------------|
| **Kick-off:** Scope confirmado | Jarvis + Cliente | Reschedule o redefinir scope |
| **Discovery:** Solución validada | Jarvis + Cliente | Backtrack a descubrimiento |
| **Design:** Planos aprobados | Jarvis + Cliente | Design revisions antes de dev |
| **Dev Complete:** Código en staging | Jarvis | Extensión de timeline si deficiencias críticas |
| **Ready for Deploy:** QA + UAT pasado | Jarvis + Cliente | Bug fixes o rollback |
| **Go-Live:** Sistema en producción | Jarvis | Post-mortem si issues, plan de correcciones |

**Escalación:** Cualquier bloqueante = daily standup + Jarvis + Cliente en 24h máximo.

---

## 9. CADENCIA DE COMUNICACIÓN

- **Dailies:** 15min standup (equipo interno) — M-V 9:00 AM
- **Weekly Reviews:** 1h (cliente + Jarvis + CSM) — Viernes 10:00 AM
- **Blockers:** Comunicación inmediata (Slack → Jarvis → Cliente)
- **Post-Launch:** Weekly check-ins semana 1-2, luego mensual

---

## 10. ENTREGABLES FINALES (HANDOFF)

✅ **Código:** Repositorio con README, setup instructions, deploy docs
✅ **Documentación:** API specs, database schema, architecture diagrams, runbooks
✅ **Capacitación:** Video tutorials, user manual, FAQ, support ticketing system
✅ **Monitoreo:** Dashboards configurados, alertas activas, logs centralizados
✅ **Soporte:** 30 días de bug fixes gratis, post-launch SLA (4h response, 24h fix para críticos)

---

## 11. POST-LAUNCH SUPPORT (30 DÍAS)

- **Bug Fixes:** Gratis si es defecto de entrega. Mejoras/cambios = horas adicionales facturables.
- **Performance Monitoring:** Sasha monitorea 24h primera semana, luego transición a cliente.
- **Escalation:** Crítico = 4h response, Fix 24h. Normal = 24h response.
- **Día 30:** Retrospectiva + handoff final a cliente o plan de mantenimiento ongoing.

---

## 12. VARIANTES POR TIPO DE PROYECTO

| Tipo | Duración | Nota |
|------|----------|------|
| **MVP Simple** (CRUD + Auth) | 4 semanas | Omitir security audit exhaustivo si low-risk |
| **App Estándar** | 6 semanas | 2 sprints feature, 1 sprint optimization/hardening |
| **Sistema Crítico** (finanzas, health) | 8 semanas | Security audit + penetration test + compliance + SLA strict |
| **Integraciones Complejas** | +2 semanas | Per integration type (SAP, Salesforce, legacy systems) |

---

**Aprobado por:** Jarvis (CEO)
**Auditoría por:** Ego (Auditor)
**Efectivo desde:** 2 de abril 2026

