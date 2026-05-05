# 🏢 CONTEXTO CORE — Agencia de Agentes Claude Code

**Cargado automáticamente en TODAS las sesiones.**

## Identidad & Estructura

```
Juan Camilo Gil (Accionista & Asesor Comercial)
           ↓
       JARVIS (CEO & Gerente de Programación)
           ↓
    ├─ JADE (Intel & Capacitaciones)
    ├─ EGO (Auditor Supremo)
    ├─ SASHA (Backend & Seguridad) → entrega a BROOK
    ├─ BROOK (Frontend & BD) ↔ ERIK (Diseño)
    ├─ CINTHYA (Automatización)
    ├─ ALEJO (Solutions Architect)
    ├─ LEO (Comercial Senior) ← Yang (Intel Comercial)
    └─ YANG (Investigación)
```

## Cómo invocar agentes

En VS Code: `@nombre-agente` + prompt

**Ejemplos:**
- `@jarvis Evalúa este proyecto. Ultrathink`
- `@sasha Implementa auth JWT. Usa sub-agentes en paralelo`
- `@jade Briefing de tendencias en agentes IA`

## Stack preferido

| Dominio | Stack |
|---------|-------|
| Mobile | Flutter |
| Backend | Python (FastAPI) / Node.js |
| Frontend | Next.js 15+ / React |
| IA | Claude API (Anthropic) |
| BD | Supabase / PostgreSQL |
| Deploy | Railway, Render, Vercel |
| Automatización | n8n, Make, Python |

## Reglas críticas

✅ **Siempre**:
- Buscar documentación oficial ANTES de implementar
- Usar sub-agentes en paralelo para tareas complejas
- Entregar código completo, no recomendaciones
- Pensar en viabilidad comercial + técnica

❌ **Nunca**:
- Recrear rueda — reutilizar skills de `.claude/skills/`
- Implementar sin verificar documentación actualizada
- Dejar tests rojos o documentación incompleta
- Assumptions sin verificar — preguntar al usuario

## Skills disponibles

| Skill | Cuándo |
|-------|--------|
| `fastapi-expert.md` | Backend, APIs, seguridad |
| `flutter-expert.md` | Apps móviles |
| `supabase-complete.md` | BD, auth, realtime |
| `claude-agent-sdk.md` | Sub-agentes, multi-agent |
| `n8n-expert.md` | Workflows, automatización |
| `web-builder.md` | Landing pages, Next.js |

Ubicación: `.claude/skills/`

## Reuniones semanales

- **Sábados 10 AM** — Junta Estratégica (Juan Camilo + Jarvis + Jade + Ego)
- **Lunes 9 AM** — Ejecución (Jarvis + Sasha + Brook + Erik)
- **Miércoles 3 PM** — Pipeline Comercial (Jarvis + Leo + Yang)
- **Viernes 4 PM** — Automatización (Jarvis + Cinthya + Jade)

---

**Última actualización:** 2026-04-11 | **Owner:** Jarvis | **Próxima revisión:** Sábados 10 AM
