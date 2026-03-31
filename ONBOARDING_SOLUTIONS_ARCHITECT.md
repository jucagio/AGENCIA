# Onboarding — Arquitecto de Soluciones

**Para:** Nuevo Arquitecto contratado
**De:** Jarvis (CEO)
**Duración:** 2 semanas intensas
**Objetivo:** Estar listo para liderar decisiones arquitectónicas en Week 3

---

## Semana 1 — Context & Induction

### Día 1 (Lunes)
**Duración:** 4 horas

#### 1. Welcome + Paperwork (30 min)
- Juan Camilo: Bienvenida + contexto comercial
- Firma contratos, acceso a sistemas, credenciales

#### 2. CEO Briefing con Jarvis (90 min)
**Temas:**
- Visión de la Agencia: "Empresa autónoma gestionada por agentes IA"
- Proyectos activos: Teclado de Señas, automatizaciones, API services
- Stack actual: FastAPI, React, Flutter, Supabase, n8n, Claude API
- Riesgos conocidos: escalabilidad, deuda técnica, costos cloud
- Próximas 90 días: integración de Paperclip, contratación de 2 engineers
- Tu rol exacto: "Eres mi brazo derecho técnico, ayúdame a tomar decisiones"

#### 3. Arquitectura Actual con Sasha (90 min)
**Con:** Sasha (Programadora Senior)
**Temas:**
- Tour de repos (FastAPI backend, React frontend, Flutter app)
- Decisiones arquitectónicas pasadas: por qué esas, qué salió bien/mal
- Código base quality assessment: deuda técnica, seguridad OWASP, testing
- Problemas actuales: rendimiento, scaling, mantenibilidad
- Planes futuros: migración de BD, refactor de APIs, optimización

#### 4. Acesso a Información Crítica (60 min)
- GitHub repos (acceso SSH)
- Figma: sistemas de diseño
- Documentación técnica: ADRs, runbooks
- Presupuesto/costos: Railway, Vercel, Supabase bills
- Slack: canales #arquitectura, #tech, #random

---

### Día 2 (Martes)
**Duración:** 5 horas

#### 1. Infraestructura & Operaciones con Cinthya (90 min)
**Con:** Cinthya (Automatización)
**Temas:**
- n8n: workflows actuales, triggers, integraciones
- Deployment pipeline: cómo se deploya código
- Monitoreo: qué alertas existen, cómo responder
- CI/CD: GitHub Actions, qué se testea, qué se debería
- Automatización de la Agencia: procesos repetitivos que podrían optimizarse

#### 2. Base de Datos Profundo con Brook (90 min)
**Con:** Brook (Frontend & BD)
**Temas:**
- Esquema PostgreSQL actual: relaciones, constraints, índices
- Queries lentas: qué debería optimizarse
- RLS (Row Level Security) en Supabase: cómo está implementado
- Migraciones: historia de cambios, cómo se hacen
- Escalabilidad BD: cuál es el plan cuando crezca 10x?

#### 3. Producto & Métricas (90 min)
**Con:** Leo + Yang
**Temas:**
- Qué están vendiendo: productos/servicios de la Agencia
- Métricas de éxito: revenue, users, retention, NPS
- Feedback de clientes: qué les duele, qué aman
- Roadmap comercial: qué construir en los próximos 3 meses
- Cómo la arquitectura afecta al negocio (costo, velocity, quality)

#### 4. Auditoría & Mejora Continua con Ego + Jade (60 min)
**Con:** Ego + Jade
**Temas:**
- Hallazgos de auditoría: qué issues encontró Ego
- Capacitación: qué está enseñando Jade al equipo
- Tendencias: qué nuevo está surgiendo en el mercado
- Gaps: dónde necesita reforzarse el equipo

---

### Día 3 (Miércoles)
**Duración:** 4 horas

#### 1. Código Deep-Dive: Backend (120 min)
**Solo:** Review de FastAPI codebase
- Estructura del proyecto
- Endpoints principales
- Autenticación (JWT)
- Validación (Pydantic v2)
- Testing
- Seguridad OWASP

**Deliverable:** Notas de observaciones (issues encontrados)

#### 2. Código Deep-Dive: Frontend (120 min)
**Solo:** Review de React codebase
- Estructura del proyecto
- State management
- API calls
- Performance: bundle size, rendering
- Responsive design
- Testing

**Deliverable:** Notas de observaciones

---

### Día 4 (Jueves)
**Duración:** 4 horas

#### 1. Paperclip + Claude Agent SDK (120 min)
**Con:** Sasha + Cinthya
**Temas:**
- Estado actual del POC de Paperclip
- Integración con Claude API
- Diseño de routing (haiku/sonnet/opus)
- Presupuesto tracking
- Qué falta para producción

#### 2. Sesión de Preguntas Abiertas con Jarvis (120 min)
**Con:** Jarvis (CEO)
**Formato:** Q&A libre
- Clarificar lo que no entendiste
- Plantear preocupaciones
- Proponer mejoras iniciales
- Alinear expectativas

---

### Día 5 (Viernes)
**Duración:** 3 horas

#### 1. Reporte de Primera Semana (120 min)
**Formato:** Presentación a Jarvis
**Estructura:**
- 3 fortalezas técnicas encontradas
- 3 riesgos o puntos de mejora identificados
- 1 recomendación rápida (implementable en semana 1)
- Preguntas pendientes

**Entregable:** Slide deck con hallazgos

#### 2. Plan de Acción de Semana 2 (60 min)
**Con:** Jarvis
**Define:**
- Qué vas a estudiar/hacer semana 2
- Reuniones que necesitas (con quién, cuándo)
- Deliverables esperados al final de semana 2

---

## Semana 2 — Deep Technical Work

### Lunes 8 AM
**Reunión:** Ejecución Técnica (tu primera)
- Presenta hallazgos de semana 1
- Identifica bloqueos del equipo
- Propone soluciones

### Martes
**Proyecto:** Arquitectura de Scaling para Paperclip + Claude Agent SDK

**Entregable:** Documento "Arquitectura Propuesta"
- Diagrama de componentes
- Flujo de tareas (Jarvis → agente → resultado)
- Routing inteligente (haiku/sonnet/opus)
- Cost modeling (presupuesto/mes)
- Risk assessment
- Timeline de implementación

**Duración:** 6 horas de trabajo concentrado

### Miércoles 3 PM
**Reunión:** Comercial (opcional, para entender context)

### Jueves
**Proyecto:** Code Review profundo
- Selecciona 1 componente crítico (ej: authentication en FastAPI)
- Escribe ADR (Architecture Decision Record)
- Propone refactor si es necesario
- Documenta standards

### Viernes 4 PM
**Reunión:** Automatización + Mejora (observador)

---

## Fin de Semana (Sábado 10 AM)
**Junta Directiva:** Primera participación como observador
- Escucha dinámica de liderazgo
- Entiende cómo se toman decisiones
- Prepárate para tu input técnico en próximas juntas

---

## Checklist de Accesos (IT)

- [ ] GitHub: acceso a repos
- [ ] Slack: canales técnicos
- [ ] Figma: documentos de diseño
- [ ] Railway/Render: acceso a deployment
- [ ] Supabase: acceso a consola
- [ ] Notion/Docs: documentación interna
- [ ] Google Workspace: mail, calendar
- [ ] 1password: credenciales compartidas
- [ ] Paperclip: acceso a plataforma

---

## Reuniones Fijas para el Arquitecto

| Día | Hora | Reunión | Duración | Con quién |
|-----|------|---------|----------|-----------|
| Lunes | 9 AM | Ejecución Técnica | 45 min | Sasha, Brook, Erik, Cinthya |
| Martes | 11 AM | 1-on-1 con Jarvis | 30 min | Jarvis |
| Jueves | 10 AM | Code Review Session | 60 min | Sasha (rotating) |
| Sábado | 10 AM | Junta Directiva | 60 min | Juan Camilo, Jarvis, Jade, Ego |

**Otras reuniones:** 1-on-1 con cada agente técnico (Sasha, Brook, Erik, Cinthya) en semanas 1-2

---

## Deliverables Esperados — End of Week 2

### Técnicos
1. ✅ Documento "Assessment Arquitectura Actual" (hallazgos, riesgos, oportunidades)
2. ✅ Documento "Paperclip Integration Architecture" (detallado, listo para implementar)
3. ✅ 1-2 ADRs (Architecture Decision Records) sobre decisiones clave
4. ✅ Code Review report: 1 componente crítico estudiado

### Soft
1. ✅ Rapport establecido con Sasha, Brook, Erik, Cinthya
2. ✅ Preguntas claras resueltas con Jarvis
3. ✅ Expectativas alineadas: ¿qué espera Jarvis? ¿qué esperas tú?

### Comercial
1. ✅ Entiendo mercado, productos, financial model básico

---

## Success Criteria — End of Month 1

- ✅ Participas en decisiones arquitectónicas de 2+ features nuevas
- ✅ Has mentorado a Sasha en mínimo 1 decisión crítica
- ✅ Paperclip está en beta, Arquitecto validó su escalabilidad
- ✅ Equipo técnico te ve como referencia (piden tu input)
- ✅ Jarvis confía en delegarte decisiones sin su supervisión

---

## Preguntas Frecuentes

**¿Qué hago si no entiendo algo?**
Pregunta inmediatamente. Mejor que tengas claridad que esperes.

**¿A quién recurro si tengo un problema?**
Jerarquía: Sasha (técnico) → Jarvis (decisiones) → Juan Camilo (comercial)

**¿Puedo proponer cambios grandes?**
Sí, pero primero documenta el problema y propuesta en un ADR. Luego discute con Jarvis.

**¿Cuál es el horario exacto?**
40 horas/semana, flexible. Reuniones core: lunes 9 AM, martes 11 AM, jueves 10 AM, sábado 10 AM

**¿Hay mentoring de mi parte?**
Sí, después de mes 1, empezarás a mentorizar engineers junior (cuando contratemos)

---

## Recursos Útiles (Bookmarks)

**Documentación:**
- `/docs` en repos GitHub
- Notion workspace: arquitectura + decisiones
- tododeia.com: tendencias diarias (actualizado por Yang)

**Comunidades:**
- Slack #arquitectura: preguntas técnicas
- Slack #random: cultura, chismes, memes

**Libros recomendados:**
- "Designing Data-Intensive Applications" — Martin Kleppmann
- "Building Microservices" — Sam Newman
- "The Art of Scalability" — Martin Kimbell

---

## Tu Rol en 30 Segundos

**Eres el "guardia técnico" de decisiones escalables:**
- ¿Construimos o compramos?
- ¿Qué arquitectura aguanta 100x crecimiento?
- ¿Cómo mentorizamos al equipo en pensamiento arquitectónico?

**Reportas a Jarvis.**
**Colaboras con todos.**
**La decisión correcta > la tecnología que te gusta.**

---

**Bienvenido a la Agencia.**

*Estamos construyendo el futuro de la automatización empresarial con agentes IA. Tú eres pieza crítica en el siguiente nivel de escalabilidad.*

— Jarvis + Juan Camilo

---

**Documento creado:** 31 de Marzo 2026
**Próxima actualización:** Después de entrevistar y contratar al Arquitecto
