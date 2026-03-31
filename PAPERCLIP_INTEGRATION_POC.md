# Paperclip + Claude Agent SDK — Prueba de Concepto (POC)

**Fecha:** 31 de Marzo 2026
**Responsable:** Jarvis (CEO)
**Objetivo:** Validar integración de Paperclip como plataforma de orquestación empresarial para la Agencia
**Stack:** Paperclip (Node.js + PostgreSQL) + Claude Agent SDK + Supabase

---

## 1. Visión Estratégica

Paperclip es el "sistema nervioso" de la Agencia:
- **Antes**: Agentes IA trabajando en paralelo sin orquestación clara
- **Después**: Agencia operando como empresa autónoma gestionada por Jarvis (CEO) con visibilidad total, control de presupuestos y ejecución programada

### Capacidades que se ganan con Paperclip:
✅ Organigramas dinámicos → Jarvis → Sasha, Brook, Erik, Cinthya, Leo, Yang
✅ Presupuestos por agente → Control de costos de ejecución
✅ Tareas vinculadas a objetivos → Trazabilidad total de decisiones
✅ Heartbeats (ejecución programada) → Agentes trabajando sin intervención humana
✅ Sistema de tickets → Auditoría completa de quién hizo qué y cuándo
✅ Gobernanza → Control editorial sobre estrategia de la Agencia

---

## 2. Arquitectura Propuesta

```
┌─────────────────────────────────────────────────────┐
│         JUAN CAMILO GIL (Accionista)                │
│              Dashboard de Paperclip                  │
│         Ve: objetivos, presupuestos, tickets        │
└────────────────┬────────────────────────────────────┘
                 │
         ┌───────▼─────────┐
         │   JARVIS (CEO)  │
         │   Paperclip UI  │
         │ Asigna tareas   │
         │ Ve estado real   │
         └───────┬─────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
┌───▼──┐  ┌──────▼──┐  ┌────▼────┐
│SASHA │  │ BROOK   │  │   ERIK  │
│      │  │ CINTHYA │  │   LEO   │
│      │  │ YANG    │  │         │
└──┬───┘  └────┬────┘  └────┬────┘
   │           │           │
   │    Paperclip API      │
   │  (Node.js + PostgreSQL)
   │           │           │
   └───────────┼───────────┘
               │
      ┌────────▼─────────┐
      │ Claude Agent SDK │
      │ (Routing haiku/  │
      │  sonnet/opus)    │
      └──────────────────┘
```

### Flujo de ejecución

1. **Juan Camilo** crea tarea en Paperclip: "Auditar seguridad de FastAPI"
2. **Jarvis** la ve, evalúa y asigna a **Sasha** con presupuesto máximo
3. **Sasha** recibe la tarea vía Paperclip API + Claude Agent SDK
4. **Sasha** ejecuta, documenta en sistema de tickets
5. **Paperclip** registra: quién trabajó, cuánto costó, cuánto tiempo tardó
6. **Ego** audita automáticamente los entregables
7. **Jarvis** reporta a Juan Camilo: "Auditoría completa, 3 CVEs críticas identificadas"

---

## 3. Requisitos Técnicos de Integración

### 3.1 Instalar Paperclip

```bash
# En raíz de la Agencia
cd /Users/PCC/Documents/JUAN\ CAMILO\ GIL/PERSONAL/PROGRAMACIÓN/AGENCIA

# Instalación automática
npx paperclipai onboard --yes

# O instalación manual
git clone https://github.com/paperclipai/paperclip.git
cd paperclip
pnpm install
pnpm dev
```

**Resultado esperado:** Paperclip API en `http://localhost:3100`

### 3.2 Crear estructura organizacional en Paperclip

```json
{
  "company": "Agencia de Agentes IA",
  "owner": "Juan Camilo Gil",
  "ceo": "Jarvis",
  "departments": [
    {
      "name": "Ejecución Técnica",
      "head": "Sasha",
      "agents": ["Sasha", "Brook", "Erik", "Cinthya"],
      "budget_monthly_usd": 5000
    },
    {
      "name": "Comercial",
      "head": "Leo",
      "agents": ["Leo", "Yang"],
      "budget_monthly_usd": 3000
    },
    {
      "name": "Dirección & Auditoría",
      "head": "Jade",
      "agents": ["Jade", "Ego"],
      "budget_monthly_usd": 2000
    }
  ]
}
```

### 3.3 Conectar Claude Agent SDK con Paperclip API

**Archivo:** `.claude/paperclip-connector.ts`

```typescript
import { Anthropic } from "@anthropic-ai/sdk";

const client = new Anthropic();
const PAPERCLIP_API = "http://localhost:3100";

export async function assignTaskToAgent(
  agentName: string,
  taskDescription: string,
  priority: "high" | "medium" | "low",
  estimatedTokens: number
) {
  // 1. Crear ticket en Paperclip
  const ticketResponse = await fetch(`${PAPERCLIP_API}/api/tickets`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      title: taskDescription,
      assigned_to: agentName,
      priority,
      estimated_cost_tokens: estimatedTokens,
      created_by: "jarvis",
      created_at: new Date().toISOString(),
    }),
  });

  const ticket = await ticketResponse.json();

  // 2. Enviar instrucción al agente vía Claude API
  const response = await client.messages.create({
    model: "claude-opus-4-6",
    max_tokens: estimatedTokens,
    messages: [
      {
        role: "user",
        content: `[PAPERCLIP TICKET #${ticket.id}]\n\n${taskDescription}\n\nDocumenta el resultado en el ticket cuando termines.`,
      },
    ],
  });

  // 3. Registrar resultado en Paperclip
  await fetch(`${PAPERCLIP_API}/api/tickets/${ticket.id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      status: "completed",
      result: response.content[0].type === "text" ? response.content[0].text : "",
      tokens_used: response.usage.output_tokens,
      completed_at: new Date().toISOString(),
    }),
  });

  return ticket;
}
```

---

## 4. Fase 1 — POC (Esta semana)

### Hito 1: Instalar y configurar Paperclip
**Responsable:** Sasha (con asistencia de Cinthya)
**Tiempo estimado:** 2 horas
**Entregable:** Paperclip corriendo localmente con estructura organizacional mapeada

### Hito 2: Crear connector Claude Agent SDK ↔ Paperclip
**Responsable:** Sasha
**Tiempo estimado:** 4 horas
**Entregable:** Código en TypeScript que:
- Crea tickets en Paperclip vía API
- Envía instrucciones a agentes vía Claude API
- Registra resultados automáticamente

### Hito 3: Prueba funcional end-to-end
**Responsable:** Jarvis + Sasha
**Tiempo estimado:** 2 horas
**Prueba:**
```
1. Jarvis crea tarea en Paperclip: "Sasha, audita el código del Teclado de Señas"
2. Sistema enruta automáticamente a Sasha vía Claude Agent SDK
3. Sasha recibe, trabaja, entrega resultado
4. Sistema registra en Paperclip: ticket completado, costos, tiempo
5. Jarvis ve en dashboard de Paperclip el estado real
```

**Criterios de éxito:**
- ✅ Tarea fluye automáticamente de Paperclip → Claude Agent SDK → Sasha
- ✅ Resultado se registra automáticamente en Paperclip
- ✅ Dashboard de Jarvis muestra estado actualizado
- ✅ Presupuesto se deduce del banco de horas

---

## 5. Riesgos y Mitigación

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|--------|-----------|
| Paperclip API no es compatible con Claude SDK | Media | Alto | Mantener wrapper de integración flexible; plan B es HTTP polling |
| Latencia en comunicación API | Media | Medio | Usar colas (Bull/RabbitMQ) para desacoplar |
| Datos de organizacional no sincronizados | Baja | Medio | Sincronización manual semanal + validación automática |
| Presupuestos se agotan | Media | Alto | Alertas automáticas a Jarvis cuando presupuesto < 20% |

---

## 6. Plan de Despliegue

**Fase 1 (POC — Esta semana):** Validar integración localmente
**Fase 2 (Alfa — Próxima semana):** Sasha, Brook, Erik usan Paperclip para sus tareas
**Fase 3 (Beta — 2 semanas):** Todos los agentes usando Paperclip, Jarvis reporta a Juan Camilo vía dashboard
**Fase 4 (Producción):** Paperclip como plataforma oficial de orquestación + deploy en Railway o Render

---

## 7. Próximos Pasos

- [ ] **Lunes 8:00 AM:** Sasha comienza instalación de Paperclip
- [ ] **Miércoles 3:00 PM:** Revisión de progreso (Jarvis + Sasha)
- [ ] **Viernes 5:00 PM:** Prueba funcional end-to-end
- [ ] **Sábado 10:00 AM:** Reporte a Juan Camilo en Junta Directiva

---

**Documento creado:** 31 de Marzo 2026
**Próxima revisión:** 4 de Abril 2026 (después de POC)
