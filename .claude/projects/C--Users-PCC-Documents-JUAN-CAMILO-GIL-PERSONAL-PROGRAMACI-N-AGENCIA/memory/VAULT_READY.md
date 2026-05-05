---
name: VAULT LISTA — Próximos Pasos por Agente
description: Qué puede hacer cada agente AHORA que agencia-vault está lista y estructurada
type: project
---

# ✅ VAULT LISTA — Estructura Completada

**Fecha:** 2026-04-05
**Status:** ✅ Estructura creada, versionada, lista para uso
**Commit:** `a2b7141` — setup: estructura PARA personalizada para Agencia IA

---

## 📁 Lo que Existe Ahora

```
✅ agencia-vault/
  ├─ 01_Projects/Teclado_de_Senias/
  │  ├─ Proyecto.md         (definición)
  │  ├─ Arquitectura.md     (decisiones tech)
  │  ├─ Progreso.md         (status diario)
  │  └─ (pendiente: Financiero.md)
  │
  ├─ 02_Areas/ (7 carpetas por agente)
  │  ├─ Dirección_Jarvis/               → index.md
  │  ├─ Intel_Comercial_Jade_Yang/      → index.md
  │  ├─ Técnica_Sasha_Alejo/            → index.md
  │  ├─ Ejecución_Brook_Erik/           → index.md
  │  ├─ Auditoría_Ego/                  → index.md
  │  ├─ Comercial_Leo/                  → index.md
  │  └─ Automatización_Cinthya/         → index.md
  │
  ├─ 03_Resources/                    (vacío, lista para Jade)
  │  └─ (pendiente: Tendencias_IA.md, Stack_Tech/, etc)
  │
  ├─ 06_Metadata/
  │  ├─ Decisiones_ADR/               (historial de decisiones)
  │  ├─ Templates/                    (plantillas reutilizables)
  │  ├─ Auditorías/                   (vacío, lista para Ego)
  │  └─ Agentes/
  │     ├─ Instrucciones_Jade.md      ✅
  │     ├─ Instrucciones_Ego.md       ✅
  │     └─ (pendiente: Instrucciones_Jarvis.md, etc)
  │
  ├─ .claude/
  │  └─ CLAUDE.md                     ✅ (instrucciones de uso)
  │
  └─ README_AGENCIA.md                ✅ (guía de inicio)
```

---

## 🚀 Próximos Pasos por Agente

### 1️⃣ **Jade** — Inteligencia & Capacitaciones (INICIO: Mañana 8 AM)

**Acciones inmediatas:**
- [ ] Abre agencia-vault en Obsidian
- [ ] Lee: `.claude/Agentes/Instrucciones_Jade.md`
- [ ] Investiga tema: tendencias en agentes IA, frameworks, mercado
- [ ] Crea: `03_Resources/Tendencias_IA_Semana_04-08.md`
- [ ] Taguea: `#tendencia-ia`, `#framework-nuevo`
- [ ] Git commit: `intel: tendencias agentes IA semana 04`

**Por qué ahora:**
Tu rol es alimentar a Jarvis + Leo + equipo con inteligencia fresca.
El vault te permite:
- Capturar hallazgos dónde quieras
- Que toda la Agencia encuentre tu research al instante
- Historial versionado de qué sabías cuándo

**Resultado esperado:**
Viernes → síntesis semanal → brief para Jarvis

---

### 2️⃣ **Jarvis** — CEO (INICIO: Cuando tengas decisión importante)

**Acciones inmediatas:**
- [ ] Abre agencia-vault
- [ ] Lee: `06_Metadata/Templates/Plantilla_ADR.md`
- [ ] Cuando tomes decisión arquitectónica importante → crea ADR

**Ejemplo real:**
Supongamos decides: "Usamos PostgreSQL + Supabase RLS para auth del Teclado"

Haces:
1. Copias `06_Metadata/Templates/Plantilla_ADR.md`
2. Renombras: `06_Metadata/Decisiones_ADR/adr-001-auth-supabase-rls.md`
3. Documentas:
   - **Contexto:** Por qué se necesita decisión
   - **Decisión:** PostgreSQL + Supabase RLS
   - **Alternativas:** Firebase, JWT + custom db, etc
   - **Por qué:** Trade-offs de seguridad, escalabilidad
4. Git commit: `adr: decisión auth con Supabase RLS — trade-offs considerados`

**Resultado:**
- Próxima semana, Sasha implementa sabiendo POR QUÉ
- Año que viene, Alejo busca "¿Qué decidimos en auth?" y ve historial completo
- Auditable: quién, cuándo, por qué

---

### 3️⃣ **Sasha, Brook, Erik** — Ejecución (INICIO: Próximo sprint)

**Acciones inmediatas:**
- [ ] Abre agencia-vault
- [ ] Familiarízate con: `01_Projects/Teclado_de_Senias/`
- [ ] Próximo sprint, actualiza diariamente: `01_Projects/Teclado_de_Senias/Progreso.md`

**Ejemplo de actualización diaria:**
```markdown
### Semana 2026-04-12

**Sasha:**
- ✅ Completé: Scaffold de proyecto FastAPI + Supabase SDK
- ⏳ En progreso: Implementación de auth endpoints
- 🚫 Bloqueado por: Nada en este momento

**Brook:**
- ✅ Completé: Revisión de Figma con Erik
- ⏳ En progreso: Setup inicial Flutter + estructura de carpetas
- 🚫 Bloqueado por: Esperando APIs de Sasha para conectar

**Erik:**
- ✅ Completé: Design system inicial en Figma
- ⏳ En progreso: Componentes base (botones, inputs, etc)
```

**Beneficio:**
- Junta semanal tiene contexto → más rápido
- Próxima semana, nuevo developer se onboarda leyendo historial
- No se pierde información entre sprints

---

### 4️⃣ **Ego** — Auditoría (INICIO: Este viernes)

**Acciones inmediatas:**
- [ ] Abre agencia-vault
- [ ] Lee: `.claude/Agentes/Instrucciones_Ego.md`
- [ ] Este viernes, audita: código (si existe), arquitectura (ADRs), seguridad
- [ ] Crea: `02_Areas/Auditoría_Ego/Reporte_2026-04-05.md`
- [ ] Filtra: 🔴 críticos, 🟠 mayores, 🟡 menores
- [ ] Git commit: `audit: 2026-04-05 — [resumen hallazgos]`

**Por qué ahora:**
- Establece baseline de calidad
- Próximas auditorías pueden comparar progreso
- Documentas qué se fijó vs qué sigue abierto

---

### 5️⃣ **Leo + Yang** — Comercial (INICIO: Después de próxima reunión)

**Acciones inmediatas:**
- [ ] Abre agencia-vault
- [ ] Lee: `02_Areas/Comercial_Leo/index.md`
- [ ] Después de conversación importante con cliente:
  - Yang crea: `02_Areas/Intel_Comercial_Jade_Yang/Análisis_[Empresa].md`
  - Leo crea: `02_Areas/Comercial_Leo/Deal_[Empresa].md`

**Ejemplo:**
Yang investiga "Acme Corp" antes de reunión
→ Crea: `Análisis_Acme_Corp.md` (estructura, tomadores de decisión, dolores)
→ Leo documenta: `Deal_Acme_Corp.md` (conversación, siguiente paso, valor propuesto)
→ Próxima reunión, contexto completo en vault

---

### 6️⃣ **Cinthya** — Automatización (INICIO: Cuando crees workflow)

**Acciones inmediatas:**
- [ ] Abre agencia-vault
- [ ] Lee: `02_Areas/Automatización_Cinthya/index.md`
- [ ] Cuando crees workflow importante → documenta en vault

**Ejemplo:**
Cinthya crea workflow: "Notificar a Sasha si hay CVE crítico en FastAPI"
→ Crea: `02_Areas/Automatización_Cinthya/Workflows_n8n_Security.md`
→ Documenta: trigger, pasos, outputs
→ Git commit: `automation: alerta CVE crítica en FastAPI`
→ Próximo mes, Jade busca "¿Qué alertas tenemos?" → encuentra automático

---

### 7️⃣ **Alejo** — Solutions Architect (INICIO: Cuando revisa arquitectura)

**Acciones inmediatas:**
- [ ] Abre agencia-vault
- [ ] Lee: `02_Areas/Técnica_Sasha_Alejo/index.md`
- [ ] Cuando Sasha completa decisión arquitectónica importante → revisa + comenta

**Ejemplo:**
Sasha implementa auth → Alejo revisa `01_Projects/Teclado_de_Senias/Arquitectura.md`
→ Alejo añade comentario: "Buena decisión RLS. Considerar índices en user_id para P95."
→ Git commit: "review: arquitectura auth — scalability notes"

---

## 📋 Integración con Memory

**Tu memory (sesión actual):**
- `.claude/projects/.../memory/claudesidian_plan.md` ← cómo implementar
- `.claude/projects/.../memory/QUICKSTART.md` ← pasos iniciales

**Vault (persistente):**
- `agencia-vault/` ← donde viven todas las decisiones/intel/progreso
- Versionado con Git (historial auditable)

**CLAUDE.md (permanente):**
- `agencia-vault/.claude/CLAUDE.md` ← instrucciones de trabajo para todos

---

## ⚡ Acciones de Hoy

1. **Tú (mañana):** Abre agencia-vault en Obsidian + Claude Code
2. **Jade (mañana 8 AM):** Comienza investigación, crea primer documento
3. **Jarvis (cuando necesite):** Documentar decisiones como ADRs
4. **Ejecutores:** Familiarizarse con estructura, próximo sprint actualizar diario
5. **Ego (viernes):** Primer reporte de auditoría
6. **Leo/Yang:** Documentar próxima oportunidad comercial

---

## 🎯 Métrica de Éxito

**Semana 1:** ✅ Estructura creada
**Semana 2:** Jade publica intel, Jarvis documenta 1 ADR
**Semana 3:** Todos actualizando diariamente (Sasha/Brook/Erik + Ego)
**Semana 4:** Junta de prueba: generar briefing ejecutivo desde vault

---

**Propuesto por:** Jarvis
**Status:** ✅ LISTA PARA USAR
**Next:** Convocar a @jade para que empiece a publicar intel mañana

**Comandos útiles:**
```bash
cd agencia-vault
code .                    # Abre en VS Code
# Luego abre en Obsidian: File → Open Vault → selecciona esta carpeta
```

---

**¿LISTO?** Sí. El vault está estructurado, versionado y documentado.

**Próximo:** Convocar a **@jade** para que empiece a usar vault mañana. 🚀
