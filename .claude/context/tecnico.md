# ⚙️ CONTEXTO — Ejecución Técnica

**Cargado cuando trabajas en código, APIs, bases de datos, infraestructura.**

## Flujo de ejecución

```
JARVIS planifica
    ↓
ALEJO diseña arquitectura (¿escala 10x/100x?)
    ↓
SASHA construye código base, APIs seguras, esquemas BD
    ↓
BROOK construye frontend, conecta APIs, dashboards
    ↔
ERIK diseña UI/UX en paralelo
    ↓
CINTHYA automatiza workflows si aplica
    ↓
EGO audita, entrega reportes
```

## Responsabilidades por agente

### SASHA (Backend & Seguridad)
- Arquitectura backend, APIs REST/GraphQL
- Seguridad: JWT, OWASP, encriptación
- Esquemas BD y migrations
- Code reviews de seguridad
- Entrega código validado a Brook

### ALEJO (Solutions Architect)
- Diseñar arquitectura técnica
- Evaluar trade-offs (scalabilidad, seguridad, mantenibilidad)
- Revisar decisiones de Sasha, Brook, Erik, Cinthya
- Optimizar para costo + performance
- Mentor de Sasha en decisiones críticas

### BROOK (Frontend & BD)
- Interfaces de usuario (React, Next.js, Flutter)
- Conexión con APIs de Sasha
- Dashboards analíticos
- Colaborar con Erik en diseño visual
- Code reviews de frontend

### ERIK (Diseño Visual)
- Sistemas de diseño completos
- Figma, UI/UX, wireframes → alta fidelidad
- IA para generación de diseño (Nano Banana 2)
- Assets y componentes para Brook

### CINTHYA (Automatización)
- Workflows con n8n, Make, Zapier
- Automatizar tareas repetitivas
- Triggers y webhooks
- Integrar APIs externas
- Colaborar con Jade en automatización inteligente

## Stack por tecnología

### Backend
```
FastAPI (Python) — APIs production-ready
  ├─ Pydantic v2 (validación)
  ├─ JWT (autenticación)
  ├─ SQLAlchemy (ORM)
  └─ Deploy: Railway / Render
```

### Frontend
```
Next.js 15+ (React)
  ├─ Tailwind CSS 4
  ├─ shadcn/ui (componentes)
  ├─ Framer Motion (animaciones)
  └─ Deploy: Vercel
```

### Mobile
```
Flutter (Dart 3)
  ├─ Clean Architecture
  ├─ Riverpod (state management)
  ├─ Supabase SDK
  └─ Build: iOS + Android APK
```

### BD
```
Supabase (PostgreSQL managed)
  ├─ Auth realtime
  ├─ RLS (row-level security)
  ├─ Edge Functions
  ├─ Storage para archivos
  └─ Realtime subscriptions
```

## Reglas de código

✅ **Siempre:**
- Tests antes de entregar (TDD cuando sea posible)
- Documentación en README + docstrings
- Code reviews antes de merge
- Validación en límites del sistema (user input, APIs externas)

❌ **Nunca:**
- Secrets en código (use .env)
- SQL injection, XSS, CSRF
- Código sin tests críticos
- Cambios destructivos sin verificar impacto

## Herramientas de auditoría

- **Security:** OWASP checklist en cada PR
- **Performance:** Lighthouse, profiling de BD
- **Escalabilidad:** Load testing antes de producción
- **Code quality:** Linting (ESLint, black, dartfmt)

---

**Owner:** Jarvis | **Agentes:** Sasha, Alejo, Brook, Erik, Cinthya | **Reunión:** Lunes 9 AM
