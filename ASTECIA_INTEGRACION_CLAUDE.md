# ASTECIA — Integración de Herramientas con Claude Platform

**Versión:** v1  
**Fecha:** 2026-04-17  
**Responsable:** Jarvis (CEO)  
**Stack:** FastAPI + Supabase + Claude SDK

---

## 🎯 Objetivo

Integrar las 6 herramientas especificadas en `ASTECIA_HERRAMIENTAS_ESPECIFICACION.md` con el agente ASTECIA en Claude Platform, permitiendo:

✅ Consultas dinámicas de precios (sin hardcodeo)  
✅ Búsquedas de clientes en tiempo real  
✅ Cálculos automáticos de ROI  
✅ Generación de propuestas  
✅ Inteligencia de mercado  
✅ Validación de oportunidades  

---

## 📐 Arquitectura de Integración

```
┌─────────────────────────────────────────────────┐
│        ASTECIA Agent (Claude Sonnet 4.6)       │
│          - v3 en Claude Platform               │
│          - System Prompt optimizado            │
└────────────┬────────────────────────────────────┘
             │
      ┌──────┴──────────────────────┐
      │   Tools / MCP Servers        │
      └──────┬───────────────────────┘
             │
      ┌──────┴─────────────────────────────────────┐
      │                                            │
      ▼                                            ▼
┌──────────────────────┐              ┌──────────────────────┐
│   FastAPI Backend    │              │  MCP Servers         │
│  (Juan Camilo)       │              │  (Open Source)       │
│                      │              │                      │
│  - /api/precios      │              │  - Web Search (RAG)  │
│  - /api/clientes     │              │  - Custom MCPs       │
│  - /api/roi          │              │                      │
│  - /api/propuestas   │              │                      │
│  - /api/oportunidades│              │                      │
└──────────┬───────────┘              └──────────┬───────────┘
           │                                      │
           ▼                                      ▼
      ┌─────────────────────────────────────────────────┐
      │        Supabase PostgreSQL + Storage             │
      │  ├─ tablas: precios, clientes, historiales       │
      │  ├─ Storage: propuestas PDF, documentos          │
      │  └─ Real-time: Suscripciones a cambios           │
      └─────────────────────────────────────────────────┘
```

---

## 🔧 Paso 1: Crear FastAPI Backend

### 1.1 Estructura de Proyecto

```bash
~/astecia-backend/
├── main.py                    # FastAPI app
├── config.py                  # Supabase credentials
├── requirements.txt           # Dependencies
├── routers/
│   ├── precios.py            # Price Lookup
│   ├── clientes.py           # Customer Search
│   ├── roi.py                # ROI Calculator
│   ├── propuestas.py         # Proposal Generator
│   └── oportunidades.py      # Opportunity Validator
├── models/
│   ├── schemas.py            # Pydantic models
│   └── database.py           # Supabase client
└── utils/
    ├── auth.py               # API key validation
    └── helpers.py            # Utility functions
```

### 1.2 Dependencias

```txt
fastapi==0.104.1
uvicorn==0.24.0
python-dotenv==1.0.0
supabase==2.0.0
pydantic==2.5.0
requests==2.31.0
weasyprint==59.3  # Para generar PDFs
jinja2==3.1.2     # Para templates
```

### 1.3 main.py

```python
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from routers import precios, clientes, roi, propuestas, oportunidades
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="ASTECIA Backend",
    description="API para herramientas de ASTECIA",
    version="1.0.0"
)

# CORS para Claude Platform
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(precios.router, prefix="/api/precios", tags=["precios"])
app.include_router(clientes.router, prefix="/api/clientes", tags=["clientes"])
app.include_router(roi.router, prefix="/api/roi", tags=["roi"])
app.include_router(propuestas.router, prefix="/api/propuestas", tags=["propuestas"])
app.include_router(oportunidades.router, prefix="/api/oportunidades", tags=["oportunidades"])

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ASTECIA Backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 1.4 Configuración de Supabase

```python
# config.py
import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Verificar conexión
def check_db():
    try:
        response = supabase.table("precios").select("COUNT").execute()
        return {"status": "connected", "count": response.count}
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

---

## 🔧 Paso 2: Implementar Cada Tool

### 2.1 Tool: Price Lookup

```python
# routers/precios.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config import supabase

router = APIRouter()

class PrecioRequest(BaseModel):
    codigo_equipo: str
    cantidad: int = 1
    cliente_id: str = None

@router.get("/{codigo_equipo}")
def get_precio(codigo_equipo: str, cantidad: int = 1, cliente_id: str = None):
    """Obtener precio actual de un equipo Videojet"""
    try:
        # Buscar en tabla precios
        response = supabase.table("precios")\
            .select("*")\
            .eq("codigo", codigo_equipo)\
            .execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail=f"Equipo {codigo_equipo} no encontrado")
        
        equipo = response.data[0]
        precio_base = equipo["precio_base"]
        
        # Aplicar descuentos
        descuento = 0
        
        # Descuento corporativo si existe
        if cliente_id:
            desc_response = supabase.table("descuentos_corporativos")\
                .select("descuento_porcentaje")\
                .eq("cliente_id", cliente_id)\
                .execute()
            
            if desc_response.data:
                descuento = desc_response.data[0]["descuento_porcentaje"] / 100
        
        # Descuento por volumen
        if cantidad >= 5:
            descuento = max(descuento, 0.10)
        
        precio_final = precio_base * (1 - descuento)
        
        return {
            "codigo": codigo_equipo,
            "modelo": equipo["modelo"],
            "precio_base": precio_base,
            "descuento_aplicable": descuento * 100,
            "precio_final": precio_final,
            "cantidad": cantidad,
            "total": precio_final * cantidad,
            "moneda": "COP",
            "vigencia": equipo["vigencia"],
            "especificaciones": equipo.get("especificaciones", {}),
            "plazo_entrega": equipo.get("plazo_entrega", "5-7 días"),
            "stock": equipo.get("stock", True)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
def get_precio_post(request: PrecioRequest):
    """POST version del price lookup"""
    return get_precio(
        request.codigo_equipo,
        request.cantidad,
        request.cliente_id
    )
```

### 2.2 Tool: Customer Intelligence

```python
# routers/clientes.py
from fastapi import APIRouter, HTTPException
from config import supabase

router = APIRouter()

@router.get("/{cliente_id}")
def get_cliente(cliente_id: str, incluir_historial: bool = True, incluir_oportunidades: bool = True):
    """Obtener información completa de un cliente"""
    try:
        # Datos del cliente
        cliente_response = supabase.table("clientes")\
            .select("*")\
            .eq("cliente_id", cliente_id)\
            .execute()
        
        if not cliente_response.data:
            raise HTTPException(status_code=404, detail=f"Cliente {cliente_id} no encontrado")
        
        cliente = cliente_response.data[0]
        
        # Historial
        historial = []
        if incluir_historial:
            hist_response = supabase.table("historiales")\
                .select("*")\
                .eq("cliente_id", cliente_id)\
                .order("fecha", desc=True)\
                .limit(5)\
                .execute()
            historial = hist_response.data or []
        
        # Oportunidades
        oportunidades = []
        if incluir_oportunidades:
            opp_response = supabase.table("oportunidades_pot")\
                .select("*")\
                .eq("cliente_id", cliente_id)\
                .eq("estado", "activo")\
                .execute()
            oportunidades = opp_response.data or []
        
        # Descuentos
        desc_response = supabase.table("descuentos_corporativos")\
            .select("*")\
            .eq("cliente_id", cliente_id)\
            .execute()
        
        descuentos = desc_response.data[0] if desc_response.data else {}
        
        return {
            "cliente_id": cliente_id,
            "nombre": cliente.get("nombre"),
            "rubro": cliente.get("rubro"),
            "ubicacion": cliente.get("ubicacion"),
            "contacto_principal": cliente.get("contacto_principal"),
            "representante_maper": cliente.get("representante_maper"),
            "historial": historial,
            "oportunidades_activas": oportunidades,
            "descuentos_corporativos": {
                "categoria": descuentos.get("categoria", "N/A"),
                "descuento_porcentaje": descuentos.get("descuento_porcentaje", 0),
                "condiciones_pago": descuentos.get("condiciones_pago", "NET 30")
            },
            "momento_verdad": cliente.get("momento_verdad"),
            "dolores_identificados": cliente.get("dolores_identificados", [])
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 2.3 Tool: ROI Calculator

```python
# routers/roi.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import math

router = APIRouter()

class ROIRequest(BaseModel):
    precio_equipo: float
    produccion_diaria_botellas: float
    precio_botella_vendida: float
    ahorros_merma: float
    ahorros_mano_obra: float
    vida_util_anos: int = 10
    tasa_descuento: float = 0.15

@router.post("/calcular")
def calcular_roi(request: ROIRequest):
    """Calcular ROI automáticamente"""
    try:
        # Beneficio mensual
        beneficio_produccion = (request.produccion_diaria_botellas * 30 * request.precio_botella_vendida)
        beneficio_mensual = beneficio_produccion + request.ahorros_merma + request.ahorros_mano_obra
        beneficio_anual = beneficio_mensual * 12
        
        # Payback period (en meses)
        payback_meses = request.precio_equipo / beneficio_mensual
        
        # ROI porcentaje
        beneficio_total_vida_util = beneficio_anual * request.vida_util_anos
        roi_porcentaje = ((beneficio_total_vida_util - request.precio_equipo) / request.precio_equipo) * 100
        
        # VPN (Valor Presente Neto)
        vpn = -request.precio_equipo
        for ano in range(1, request.vida_util_anos + 1):
            vpn += beneficio_anual / math.pow(1 + request.tasa_descuento, ano)
        
        # TIR (aproximado con búsqueda binaria)
        tir = calcular_tir(request.precio_equipo, beneficio_anual, request.vida_util_anos)
        
        # Análisis de sensibilidad
        mejor_caso = roi_porcentaje * 1.5  # +50%
        peor_caso = roi_porcentaje * 0.7   # -30%
        
        return {
            "roi_porcentaje": round(roi_porcentaje, 2),
            "payback_period_meses": round(payback_meses, 1),
            "vpn_neto": round(vpn, 0),
            "tir": round(tir, 2),
            "beneficio_anual": round(beneficio_anual, 0),
            "beneficio_cinco_anos": round(beneficio_anual * 5, 0),
            "analisis_sensibilidad": {
                "mejor_caso": round(mejor_caso, 2),
                "peor_caso": round(peor_caso, 2),
                "escenario_probable": round(roi_porcentaje, 2)
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def calcular_tir(inversion, beneficio_anual, anos):
    """Calcular TIR usando búsqueda binaria"""
    def vpn_tir(tir):
        vpn = -inversion
        for ano in range(1, anos + 1):
            vpn += beneficio_anual / math.pow(1 + tir, ano)
        return vpn
    
    low, high = 0.0, 2.0
    for _ in range(100):
        mid = (low + high) / 2
        if vpn_tir(mid) > 0:
            low = mid
        else:
            high = mid
    
    return low
```

---

## 🔧 Paso 3: Registrar Tools en Claude Platform

### 3.1 Actualizar Agent ASTECIA (YAML)

Después de que FastAPI esté corriendo en producción, agregar a la configuración:

```yaml
tools:
  - name: price_lookup
    description: Consultar precio actual de equipos Videojet
    type: http
    url: https://astecia-api.onrender.com/api/precios/{codigo_equipo}
    method: GET
    input:
      codigo_equipo: string
      cantidad: integer
      cliente_id: string (optional)

  - name: customer_search
    description: Obtener información completa de un cliente
    type: http
    url: https://astecia-api.onrender.com/api/clientes/{cliente_id}
    method: GET
    input:
      cliente_id: string

  - name: roi_calculate
    description: Calcular ROI automáticamente
    type: http
    url: https://astecia-api.onrender.com/api/roi/calcular
    method: POST
    input:
      precio_equipo: number
      produccion_diaria_botellas: number
      precio_botella_vendida: number
      ahorros_merma: number
      ahorros_mano_obra: number

  - name: proposal_generate
    description: Generar propuesta comercial automáticamente
    type: http
    url: https://astecia-api.onrender.com/api/propuestas/generar
    method: POST
```

### 3.2 Actualizar System Prompt (Sección)

Agregar a `system:` en ASTECIA:

```yaml
system: |
  ## HERRAMIENTAS DISPONIBLES
  
  Tienes acceso a estas herramientas automáticamente. Úsalas cuando:
  
  1. **price_lookup** - Cuando pregunten por precios
     Ejemplo: "¿Cuánto cuesta el VJ1240?" → llamar tool
  
  2. **customer_search** - Cuando necesites contexto de cliente
     Ejemplo: "¿Quién es el decision maker en Cargill?" → llamar tool
  
  3. **roi_calculate** - Cuando necesites justificar inversión
     Ejemplo: "¿Vale la pena invertir en esto?" → llamar tool
  
  4. **proposal_generate** - Cuando debas generar propuesta
     Ejemplo: "Redacta propuesta para Omnilife" → llamar tool
  
  ## INSTRUCCIONES IMPORTANTES
  
  ✓ NUNCA digas "precios son entre X y Y" (impreciso)
  ✓ SIEMPRE llama price_lookup para obtener precio exacto
  ✓ NUNCA estimes ROI manualmente (impreciso)
  ✓ SIEMPRE llama roi_calculate para cálculos reales
  ✓ Si un tool falla, mantén el contexto y propón alternativa
```

---

## 🚀 Paso 4: Deployment

### 4.1 Opción A: Render (Recomendado)

```bash
# 1. Conectar GitHub con Render
# 2. Crear nuevo Web Service
# 3. Seleccionar rama y build command

Build command: pip install -r requirements.txt
Start command: uvicorn main:app --host 0.0.0.0 --port 8000

Environment variables:
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=your-key-here
```

**Costo:** $7/mes (Starter) → $25/mes (Production)

### 4.2 Opción B: Railway

Similar a Render, setup en 5 minutos.

---

## ✅ Checklist de Validación

- [ ] FastAPI corriendo localmente
- [ ] Supabase tablas creadas y populadas
- [ ] Todos los endpoints respondiendo
- [ ] CORS habilitado para Claude Platform
- [ ] API desplegada en producción (Render o Railway)
- [ ] Tools registrados en Claude Platform
- [ ] System prompt actualizado
- [ ] Testing end-to-end con ASTECIA
- [ ] Juan Camilo validó resultados

---

## 📞 Soporte y Debugging

### Si price_lookup falla:
```
→ Verificar que tabla "precios" existe en Supabase
→ Verificar formato de respuesta JSON
→ Check logs: Render → Logs tab
```

### Si tools no aparecen en ASTECIA:
```
→ Guardar nueva versión del agent (v4)
→ Esperar 30 segundos
→ Recargar página Claude Platform
```

---

**Owner:** Jarvis  
**Estado:** 🟢 Listo para desarrollo  
**Timeline:** 2-3 semanas para go-live completo  
**Prioridad:** P0 (Crítica)
