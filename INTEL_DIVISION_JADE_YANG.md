# División de Responsabilidades Intel — Jade vs Yang

**Fecha:** 31 de Marzo 2026
**Cambio:** Reorientación estratégica de funciones de investigación

---

## Antes (Situación Anterior)

```
YANG (solo):
├─ Monitorea tododeia.com (skills nuevas)
├─ Investigación comercial ad-hoc
└─ Inteligencia de empresas (inconsistente)

JADE:
├─ Capacitación
├─ Investigación de tendencias (ad-hoc)
└─ Otros
```

**Problema:** YANG dividida, sin enfoque claro. Tendencias tech no monitoreadas constantemente.

---

## Ahora (Nuevo Modelo)

### 🧠 JADE — Intel Técnica & Tendencias
**Tarea programada:** `jade-estudio-tendencias-diario` (8:05 AM, lunes-viernes)

**Responsabilidades:**
1. ✅ **Monitoreo de tododeia.com** (tomó de Yang)
   - Skills nuevas que el equipo debería aprender
   - Categorización por agente

2. ✅ **Búsqueda en GitHub**
   - Repos de agentes, frameworks, soluciones
   - Best practices en multi-agent systems
   - Vulnerabilidades de seguridad
   - Code reutilizable

3. ✅ **Comunidades de Agentes IA**
   - Discord: LangChain, Anthropic, CrewAI
   - Slack communities
   - X/Twitter trending
   - Papers académicos (arxiv)
   - Product Hunt (nuevas herramientas)

4. ✅ **Cost Optimization**
   - Cómo ahorrar en Claude API
   - Nuevas features que reduzcan costos
   - Alternativas emergentes

5. ✅ **Seguridad & Vulnerabilidades**
   - CVEs críticos
   - OWASP updates
   - Security research

6. ✅ **Beneficio Directo para Agencia**
   - ¿Qué implementamos YA?
   - ¿Qué investigamos próximas 2 semanas?
   - ¿Qué observamos a largo plazo?

**Entrega:**
- 9 AM en Slack #intel: brief diario
- reports/jade-intel-diaria-{fecha}.md: archivo detallado
- Recomendaciones accionables por agente

---

### 💼 YANG — Intel Comercial & Mercado
**Tarea programada:** `yang-monitor-tododeia` → ahora `yang-intel-comercial` (9:03 PM)

**Responsabilidades:**
1. ✅ **Pipeline Comercial**
   - Top 5 oportunidades cada semana
   - Tomadores de decisión, dolores, timing
   - Contactos y next steps

2. ✅ **Competitive Intelligence**
   - Qué hacen otras agencias de agentes IA
   - Startups emergentes en nuestro espacio
   - Diferenciadores nuestros vs competencia
   - Benchmarking de precios

3. ✅ **Market Intelligence**
   - Tendencias de DEMANDA (no tech, mercado)
   - Quién está contratando agencias
   - TAM (Total Addressable Market)
   - Dónde está el dinero

4. ✅ **Hiring Intelligence**
   - Sueldos de mercado para Arquitecto
   - Benchmarks de posiciones similares
   - Referencias posibles

5. ✅ **Opportunistic Intelligence**
   - Noticias de empresas (posibles clientes)
   - Funding rounds
   - Leadership changes en target market
   - Momentos de contacto óptimos

**Entrega:**
- 9:15 PM en Slack a Jarvis + Leo: brief comercial
- Accionable: top 3 empresas para contactar esta semana
- Argumentario actualizado para Leo

---

## Matriz de Responsabilidades

| Área | Jade | Yang |
|------|------|------|
| **Tendencias Tech** | ✅ Estudia diariamente | ❌ No |
| **GitHub & Repos** | ✅ Monitorea | ❌ No |
| **Comunidades Agentes** | ✅ Participa | ❌ No |
| **tododeia.com** | ✅ Ahora (antes Yang) | ❌ No |
| **Vulnerabilidades** | ✅ Identifica | ❌ No |
| **Empresas Específicas** | ❌ No | ✅ Investigación profunda |
| **Competencia** | ❌ No | ✅ Análisis detallado |
| **Market TAM** | ❌ No | ✅ Research |
| **Oportunidades Comerciales** | ❌ No | ✅ Pipelines |
| **Hiring Intel** | ❌ No | ✅ Sueldos, benchmarks |

---

## Sinergia Jade + Yang

```
JADE (Lunes-Viernes 8 AM):
"El stack emergente es LangGraph para multi-agent"
    ↓
YANG (Viernes/Lunes 9 PM):
"Y X company usa LangGraph → oportunidad para vender"
    ↓
JARVIS:
Entiende tendencia técnica + oportunidad comercial
    ↓
LEO:
"Contacta a X company, aquí está cómo les vendemos nuestro stack"
```

---

## Cambio en Tareas Programadas

### Jade — ACTUALIZADA
```
taskId: jade-estudio-tendencias-diario
Cuándo: 8:05 AM, lunes-viernes
Qué: Monitoreo completo (tododeia + GitHub + comunidades + seguridad)
Entrega: Slack #intel + archivo de reporte
```

### Yang — ACTUALIZADA
```
taskId: yang-monitor-tododeia → (name actualizado conceptualmente)
Cuándo: 9:03 PM, diariamente (ó 3 veces/semana)
Qué: Intel comercial, pipeline, competencia, market
Entrega: Slack a Jarvis + Leo + archivo de reporte
```

---

## Cómo Funciona en Práctica

### Escenario 1 — Nuevas Tendencias
```
LUNES 8 AM (Jade en tododeia):
Jade descubre: "LangGraph 0.2 con state management mejorado"
→ Investigación profunda
→ Reporta: "Sasha debería aprender LangGraph, podría optimizar Paperclip routing"
→ Slack: @sasha LangGraph 0.2 está aquí, primer prototipo en 1 semana?

VIERNES 9 PM (Yang):
Yang ve empresa X usando LangGraph en su blog
→ Identifica: "Esa company probablemente quiere mejorar su arquitectura"
→ Agrega a pipeline
→ Reporta: "Company X es oportunidad ahora, timing perfecto"
→ Slack a Leo: "Contacta a Company X esta semana, ellos usan LangGraph"

SÁBADO 10 AM (Junta Directiva):
Jarvis + Juan Camilo ven:
- Tendencia: LangGraph está ganando
- Acción Sasha: prototipo en 1 semana
- Oportunidad: Company X ahora
- Resultado: Vendemos solución a medida usando LangGraph
```

### Escenario 2 — Vulnerabilidad Crítica
```
MARTES 8 AM (Jade en GitHub):
Jade encuentra CVE crítico en PostgreSQL usado por Supabase
→ Reporta inmediatamente
→ Slack critical: @sasha CVE-XXX afecta Supabase, parchar ASAP

MISMO DÍA:
Sasha parchea en 2 horas
Ego audita
Cinthya deploya

JUEVES 9 PM (Yang):
Yang ve que clientes usan PostgreSQL
→ Toma nota: "Nosotros parche rapido, eso es diferenciador"
```

### Escenario 3 — Oportunidad Comercial
```
VIERNES 9 PM (Yang):
Yang lee: "Startup X recibió $10M funding, van a hacer agentes IA"
→ Identifica: "Oportunidad: venderles servicios de agencia"
→ Reporta a Leo + Jarvis

LUNES 8 AM (Jade):
Jade busca Company X en GitHub
→ Ve su stack (Python, FastAPI)
→ Reporta: "Usan FastAPI, podemos hacer partnership"

MIÉRCOLES 3 PM (Reunión Comercial Jarvis + Leo + Yang):
Leo arma pitch basado en:
- Intel de Yang: oportunidad + timing
- Intel de Jade: su stack tech + cómo encajamos
- Resultado: propuesta técnica + comercial completa
```

---

## Expectativas de Output

### Jade (Diario)
```
Tiempo: 30-45 minutos
Output: 1 brief en Slack + 1 archivo de reporte
Formato: 3-5 descubrimientos clave accionables
Ejemplo:
"📊 INTEL TÉCNICA - 31 Marzo:
🔴 CRÍTICO: CVE-2026-XXXX en PostgreSQL — @sasha urgente
🟡 IMPORTANTE: LangGraph 0.2 lanzado — @sasha investigar
🟢 INTERESANTE: Paperclip gains 500 stars GitHub — arquitectura validada
Acción: Sasha hace prototipo LangGraph, Ego audita CVE, Jarvis prepara para Arquitecto"
```

### Yang (Diario/3x semana)
```
Tiempo: 30-45 minutos
Output: 1 brief a Jarvis + Leo + 1 archivo
Formato: Empresas + momentum + acción
Ejemplo:
"💼 INTEL COMERCIAL - 31 Marzo:
🎯 TOP 3 OPORTUNIDADES:
1. Company X ($10M funding) — CEO @linkedin — contactar esta semana
2. Company Y (hiring CTO) — timing perfecto — Leo hace pitch
3. Company Z (shift a AI) — problema + solución = nuestra

🏢 COMPETITIVE: AgenciaA bajó precios 20%, respuesta: diferenciador técnico
📊 MARKET: Demand de agentes IA creció 40% YoY — TAM expandiendo"
```

---

## Success Criteria

**Jade:**
- ✅ 1 descubrimiento crítico/semana que beneficie directamente a la Agencia
- ✅ 3-5 items accionables diarios
- ✅ Equipo implementa mínimo 1 recomendación/semana
- ✅ Brief impacta decisiones arquitectónicas

**Yang:**
- ✅ Pipeline comercial actualizado diariamente
- ✅ 3-5 oportunidades nuevas/semana identificadas
- ✅ Leo usa intel para pitch más efectivos
- ✅ Timing de contacto optimizado

**Sinergia:**
- ✅ Jade + Yang proporcionan contexto completo a Jarvis
- ✅ Propuestas técnicas + comerciales alineadas
- ✅ Equipo 3 pasos adelante del mercado

---

**Documento creado:** 31 de Marzo 2026
**Implementación:** Inmediata (tareas programadas actualizadas)
**Próxima revisión:** 30 de Abril (primer mes de operación)
