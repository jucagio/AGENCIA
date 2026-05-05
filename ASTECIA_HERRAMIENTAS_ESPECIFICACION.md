# ASTECIA — Especificación de Herramientas

**Versión:** v1  
**Fecha:** 2026-04-17  
**Owner:** Jarvis (CEO)  
**Status:** 🟢 En diseño

---

## Resumen Ejecutivo

ASTECIA necesita 6 herramientas integradas para ser completamente autónomo como asesor comercial de Juan Camilo. Estas herramientas permiten:
- Consultas dinámicas de precios (sin hardcodear)
- Inteligencia de clientes en tiempo real
- Cálculos automáticos de ROI
- Generación de propuestas
- Investigación de mercado

**Stack sugerido:**
- Backend: FastAPI (Python) con Supabase
- Integración: Anthropic Tools API
- Datos: Supabase PostgreSQL + API REST

---

## 1️⃣ CONSULTA DE PRECIOS (Price Lookup)

**Propósito:** Obtener precios dinámicos de equipos Videojet sin hardcodear rangos

**Tipo:** Tool / MCP Server  
**Endpoint:** `GET /api/precios/{codigo_equipo}`  
**Modelo:** Sonnet 4.6 lo llamará automáticamente

### Input Schema
```json
{
  "codigo_equipo": "VJ1240",
  "cantidad": 1,
  "cliente_id": "cargill-001"  // opcional, para precios especiales
}
```

### Output Schema
```json
{
  "codigo": "VJ1240",
  "modelo": "CIJ VJ1240 Standard",
  "precio_base": 6500000,
  "precio_vigente": 6500000,
  "moneda": "COP",
  "descuento_aplicable": 0.05,
  "precio_final": 6175000,
  "vigencia": "2026-04-30",
  "especificaciones": {
    "tipo": "CIJ",
    "velocidad": "50-300m/min",
    "altura_fuente": "2-12mm",
    "consumo": "750W"
  },
  "plazo_entrega": "5-7 días",
  "stock": true
}
```

### Lógica
- Si `cliente_id` existe y tiene descuento corporativo → aplicar descuento
- Si `cantidad > 5` → aplicar descuento por volumen
- Retornar `precio_base` + especificaciones técnicas
- NUNCA retornar precios estimados o rangos (siempre valores exactos)

### Tabla de Precios (Actualizar en Supabase)
| Código | Modelo | Precio Base COP | Tipo | Status |
|--------|--------|-----------------|------|--------|
| VJ1240 | CIJ 1240 | 6,500,000 | CIJ | Activo |
| VJ1280 | CIJ 1280 | 7,500,000 | CIJ | Activo |
| VJ1580 | CIJ 1580 | 8,500,000 | CIJ | Activo |
| VJ1580IP | CIJ 1580 IP65 | 10,000,000 | CIJ | Activo |
| VJ1620FG | CIJ 1620FG | 10,000,000 | CIJ | Activo |
| VJ1880 | CIJ 1880 | 24,000,000 | CIJ | Activo |
| VJ6230 | TTO 6230 | 5,500,000 | TTO | Activo |
| VJ6330 | TTO 6330 | 9,000,000 | TTO | Activo |
| VJ6530 | TTO 6530 | 15,000,000 | TTO | Activo |
| VJ7210 | Laser 7210 | 90,000,000 | Laser | Activo |
| VJ7920 | Laser 7920 | 120,000,000 | Laser | Activo |
| VJ2380 | LCM 2380 | 30,000,000 | LCM | Activo |
| VJ9550 | LPA 9550 | 168,000,000 | LPA | Activo |
| VJ9560 | LPA 9560 | 40,000,000 | LPA | Activo |

---

## 2️⃣ BÚSQUEDA DE CLIENTE (Customer Intelligence)

**Propósito:** Obtener contexto completo de un cliente desde el CRM

**Tipo:** Tool / MCP Server  
**Endpoint:** `GET /api/clientes/{cliente_id}`

### Input Schema
```json
{
  "cliente_id": "cargill-001",
  "incluir_historial": true,
  "incluir_oportunidades": true
}
```

### Output Schema
```json
{
  "cliente_id": "cargill-001",
  "nombre": "Cargill Colombia",
  "rubro": "Alimentos / Proteínas",
  "ubicacion": "Villagorgona, Valle",
  "contacto_principal": {
    "nombre": "Santiago Pérez",
    "cargo": "Gerente de Producción",
    "email": "sperez@cargill.com.co",
    "telefono": "+57 2 5551234"
  },
  "representante_maper": "Juan Camilo Gil",
  "historial": [
    {
      "fecha": "2026-04-10",
      "tipo": "visita",
      "nota": "Demo VJ1240, interesado en 2 equipos",
      "siguiente_paso": "Propuesta económica"
    }
  ],
  "oportunidades_activas": [
    {
      "pot": "28546",
      "equipo": "VJ1240",
      "valor": 40000000,
      "etapa": "Negociación",
      "probabilidad": 0.85
    }
  ],
  "descuentos_corporativos": {
    "categoria": "Tier 1",
    "descuento_porcentaje": 5,
    "condiciones_pago": "NET 30"
  },
  "momento_verdad": "EOQ (fin de trimestre - dentro de 15 días)",
  "dolores_identificados": [
    "Baja velocidad de codificación actual",
    "Falta de trazabilidad en producción",
    "Requisitos de compliance nuevo"
  ]
}
```

### Fuente de Datos
- Supabase table: `clientes`
- Supabase table: `historiales`
- Supabase table: `oportunidades_pot`
- Supabase table: `descuentos_corporativos`

---

## 3️⃣ CÁLCULO DE ROI (ROI Calculator)

**Propósito:** Calcular automáticamente retorno sobre inversión

**Tipo:** Tool / Cloud Function  
**Endpoint:** `POST /api/roi/calcular`

### Input Schema
```json
{
  "precio_equipo": 6500000,
  "produccion_diaria_botellas": 500000,
  "precio_botella_vendida": 0.08,
  "ahorros_merma": 200000,
  "ahorros_mano_obra": 1500000,
  "vida_util_anos": 10,
  "tasa_descuento": 0.15
}
```

### Output Schema
```json
{
  "roi_porcentaje": 145,
  "payback_period_meses": 3.2,
  "vpn_neto": 42500000,
  "tir": 0.68,
  "beneficio_anual": 2100000,
  "beneficio_cinco_anos": 10500000,
  "analisis_sensibilidad": {
    "mejor_caso": 250,
    "peor_caso": 85,
    "escenario_probable": 145
  }
}
```

### Fórmulas
- **Payback Period:** Precio Equipo / Beneficio Mensual
- **ROI:** (Beneficio Total - Precio) / Precio * 100
- **VPN:** Sumatoria de flujos descontados a tasa
- **TIR:** Tasa que hace VPN = 0

---

## 4️⃣ BÚSQUEDA WEB (Web Intelligence)

**Propósito:** Investigar empresas, noticias, inteligencia competitiva

**Tipo:** MCP Server / Apify Integration  
**Endpoint:** Apify `rag-web-browser` o similar

### Casos de Uso
1. **Investigar empresa antes de reunión**
   - Noticias recientes
   - Cambios de leadership
   - Momentos de verdad (expansión, lanzamiento)
   - Dolores identificados

2. **Inteligencia competitiva**
   - Qué está haciendo la competencia
   - Precios competidores
   - Nuevas soluciones en mercado

3. **Validación de datos**
   - Confirmar información de cliente
   - Verificar contactos

### Input
```json
{
  "query": "Cargill Colombia noticias 2026",
  "tipo": "empresa",
  "idioma": "es"
}
```

### Output
```json
{
  "resultados": [
    {
      "titulo": "Cargill invierte en nueva planta en Valle",
      "fecha": "2026-04-10",
      "fuente": "El País",
      "resumen": "Cargill anuncia expansión de capacidad...",
      "relevancia": "ALTA",
      "implicacion": "Nuevo proyecto = oportunidad de equipos"
    }
  ],
  "momento": "AHORA es buen momento",
  "oportunidad": "Expansión en curso"
}
```

**Proveedor sugerido:** Apify `rag-web-browser` (ya integrado con Claude)

---

## 5️⃣ GENERADOR DE PROPUESTAS (Proposal Generator)

**Propósito:** Generar propuestas comerciales automáticamente

**Tipo:** Cloud Function / n8n Workflow  
**Endpoint:** `POST /api/propuestas/generar`

### Input Schema
```json
{
  "cliente_id": "cargill-001",
  "equipos": [
    {
      "codigo": "VJ1240",
      "cantidad": 2,
      "precio_unitario": 6175000
    }
  ],
  "condiciones": {
    "descuento_comercial": 0.05,
    "plazo_pago": "NET 30",
    "garantia_meses": 24,
    "entrega_dias": 7
  },
  "incluir_casos_exito": true,
  "tono": "consultivo"  // vs "agresivo"
}
```

### Output
```json
{
  "propuesta_id": "PROP-2026-0417-001",
  "archivo_url": "https://storage.supabase.io/...propuesta_001.pdf",
  "fecha_generacion": "2026-04-17T14:30:00Z",
  "fecha_vencimiento": "2026-05-17",
  "componentes": {
    "portada": "Cargill Colombia - Solución CIJ",
    "ejecutivo": "Resumen de beneficios",
    "solucion": "Especificaciones técnicas",
    "roi_analysis": "Retorno sobre inversión",
    "casos_exito": "Referencias Videojet",
    "terminos": "Condiciones comerciales",
    "anexos": "Fichas técnicas"
  }
}
```

**Tecnología:** 
- Template: Jinja2 + Markdown
- PDF generation: WeasyPrint o similar
- Storage: Supabase Storage

---

## 6️⃣ VALIDADOR DE OPORTUNIDADES (Opportunity Validator)

**Propósito:** Evaluar si una oportunidad realmente vale la pena

**Tipo:** Tool / ML Scoring Engine  
**Endpoint:** `POST /api/oportunidades/validar`

### Input Schema
```json
{
  "pot_id": "28546",
  "cliente_id": "cargill-001",
  "valor_oportunidad": 40000000,
  "etapa": "Negociación",
  "probabilidad_estimada": 0.85,
  "tiempo_disponible_dias": 20,
  "recursos_necesarios": 2
}
```

### Output Schema
```json
{
  "score_viabilidad": 85,  // 0-100
  "recomendacion": "INSISTIR",  // INSISTIR | MANTENER | CANCELAR
  "analisis": {
    "probabilidad_realista": 0.70,
    "esfuerzo_requerido": "BAJO",
    "roi_tiempo": "ALTO",
    "competencia": "BAJA"
  },
  "factores_positivos": [
    "Cliente Tier 1",
    "Problema identificado claro",
    "Presupuesto disponible",
    "Decision maker receptivo"
  ],
  "factores_negativos": [
    "Plazo corto (20 días)",
    "Requiere 2 personas del equipo"
  ],
  "siguiente_paso": "Enviar propuesta hoy, follow-up miércoles",
  "fecha_cierre_probable": "2026-05-10"
}
```

### Algoritmo de Scoring
```
Score = (
  (Probabilidad * 30) +
  (Valor / 10M * 25) +
  (Capacidad del equipo * 20) +
  (Momento del cliente * 15) +
  (Relación con competencia * 10)
)
```

**Datos de entrada:**
- Histórico de deals cerrados (para calibración)
- Win/loss analysis
- Sales velocity del equipo

---

## 🛠️ Stack de Implementación Sugerido

### Backend
```
FastAPI (Python 3.11)
├── /api/precios/* (Price Lookup)
├── /api/clientes/* (Customer Intelligence)
├── /api/roi/* (ROI Calculator)
├── /api/propuestas/* (Proposal Generator)
└── /api/oportunidades/* (Opportunity Validator)

Database: Supabase PostgreSQL
├── tablas: clientes, historiales, pot, precios
├── RLS: Habilitado para seguridad
└── Real-time: Habilitado para actualizaciones

Storage: Supabase Storage
└── propuestas/ (Documentos PDF)
```

### Integración con ASTECIA
```
Claude Agent (Sonnet 4.6)
├── Tool: price_lookup → /api/precios/
├── Tool: customer_search → /api/clientes/
├── Tool: roi_calculate → /api/roi/
├── MCP: web_search → Apify
├── Tool: proposal_generate → /api/propuestas/
└── Tool: validate_opportunity → /api/oportunidades/
```

### n8n Workflows (Automatización)
```
Workflow 1: Propuestas automáticas
Trigger: POT entra en "Negociación"
Action: Generar propuesta, enviar a cliente, reminder a Juan Camilo

Workflow 2: Inteligencia diaria
Trigger: 8:00 AM
Action: Web search de clientes Tier 1, resumen por email

Workflow 3: Validación de deals
Trigger: POT creado
Action: Calcular score, si es < 50 alertar a Juan Camilo
```

---

## 📋 Checklist de Implementación

**Fase 1 — Infraestructura (Semana 1)**
- [ ] Configurar base de datos Supabase
- [ ] Crear tablas (precios, clientes, historiales)
- [ ] Diseñar esquema de seguridad (RLS)
- [ ] Documentar API contracts

**Fase 2 — Herramientas Core (Semana 2-3)**
- [ ] Tool 1: Price Lookup (3 días)
- [ ] Tool 2: Customer Search (3 días)
- [ ] Tool 3: ROI Calculator (2 días)

**Fase 3 — Herramientas Avanzadas (Semana 4)**
- [ ] Tool 4: Web Search (1 día - usa Apify)
- [ ] Tool 5: Proposal Generator (3 días)
- [ ] Tool 6: Opportunity Validator (2 días)

**Fase 4 — Integración con ASTECIA (Semana 5)**
- [ ] Registrar Tools en Claude Platform
- [ ] Testing end-to-end
- [ ] Training de Juan Camilo
- [ ] Go-live

---

## 💬 Próximos Pasos

1. **Aprobación de arquitectura** — ¿Te gusta este enfoque?
2. **Seleccionar herramienta #1 para comenzar** — Cuál es la más urgente?
3. **Definir fuente de datos** — ¿Dónde están los precios actuales? ¿En Excel, sistema ERP, etc.?
4. **Timeline** — ¿Cuándo necesitas esto listo?

---

**Owner:** Jarvis (CEO)  
**Última actualización:** 2026-04-17  
**Estado:** 🟢 Listo para desarrollo
