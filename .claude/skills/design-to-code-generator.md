# Design-to-Code Generator — Screenshot to React + Tailwind

## Descripcion
Skill para convertir screenshots, mockups o sitios web existentes en codigo React + Tailwind automaticamente. Usa Firecrawl para scraping visual, Claude Vision para analisis, y genera componentes production-ready. Optimizada para Erik (lead) y Sasha (backend integration).

## Instrucciones

Cuando el usuario pida convertir un diseno visual a codigo, sigue estas directrices:

### Que resuelve esta skill

Convierte cualquier fuente visual en codigo funcional:
- Screenshot de un sitio web → React + Tailwind
- Mockup en imagen (PNG/JPG) → Componentes React
- Sitio web existente (URL) → Clon funcional en React
- Wireframe dibujado a mano → Estructura HTML/React basica

### Stack Tecnologico

| Herramienta | Funcion | Costo |
|-------------|---------|-------|
| **Firecrawl** | Web scraping + screenshots de URLs | Free tier: 500 credits/mes, Pro: $19/mes |
| **Claude Vision** (Opus/Sonnet) | Analisis visual de screenshots | Incluido en API |
| **screenshot-to-code** (open source) | Pipeline completo screenshot → HTML/React | Gratis (self-hosted) |
| **Open Lovable** | Clone de sitios web a React apps | Gratis (open source) |

### Opcion 1: Firecrawl API — URL a Codigo

**Setup:**
```bash
npm install firecrawl
# O usar directamente via API
```

**API Key:**
- Registrarse en https://www.firecrawl.dev
- Obtener API key del dashboard
- Guardar en `.env`: `FIRECRAWL_API_KEY=fc-xxxxx`

**Workflow: URL → Screenshot → Codigo:**

```python
# 1. Capturar screenshot de un sitio web
import requests

FIRECRAWL_API_KEY = "fc-xxxxx"

# Scrape con screenshot
response = requests.post(
    "https://api.firecrawl.dev/v1/scrape",
    headers={
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "url": "https://example.com",
        "formats": ["markdown", "screenshot"],
        "actions": [
            {"type": "wait", "milliseconds": 3000},
            {"type": "screenshot", "fullPage": True}
        ]
    }
)

data = response.json()
screenshot_url = data["data"]["screenshot"]
markdown_content = data["data"]["markdown"]

# 2. Enviar a Claude Vision para analisis
import anthropic

client = anthropic.Anthropic()

analysis = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {"type": "url", "url": screenshot_url}
            },
            {
                "type": "text",
                "text": """Analyze this screenshot and generate:
1. A complete React component using Tailwind CSS
2. Responsive design (mobile-first)
3. All visual elements faithfully reproduced
4. Semantic HTML structure
5. Accessibility attributes (aria-labels, alt text)

Output ONLY the React component code, no explanations."""
            }
        ]
    }]
)

react_code = analysis.content[0].text
```

### Opcion 2: screenshot-to-code (Open Source)

Repositorio: https://github.com/abi/screenshot-to-code

**Setup local:**
```bash
git clone https://github.com/abi/screenshot-to-code.git
cd screenshot-to-code

# Backend
cd backend
pip install -r requirements.txt
echo "ANTHROPIC_API_KEY=sk-ant-xxxxx" > .env
python main.py

# Frontend
cd ../frontend
npm install
npm run dev
```

**Uso:**
1. Abrir http://localhost:5173
2. Subir screenshot o pegar URL
3. Seleccionar stack: HTML/Tailwind, React/Tailwind, Vue/Tailwind
4. El sistema genera codigo automaticamente
5. Iterar con instrucciones en lenguaje natural

**Precision tipica:**
- Sitios estaticos: 85-95% fidelidad
- Sitios con animaciones: 70-85%
- Apps complejas con estado: 60-75%

### Opcion 3: Open Lovable — URL a React App Completa

```bash
# Clonar cualquier sitio web como React app
git clone https://github.com/raidendotai/openlovable.git
cd openlovable
npm install

# Configurar
echo "FIRECRAWL_API_KEY=fc-xxxxx" > .env
echo "ANTHROPIC_API_KEY=sk-ant-xxxxx" >> .env

# Ejecutar
npm run clone -- --url "https://example.com"
```

Output: React app completa con TypeScript, Tailwind CSS y componentes organizados.

### Opcion 4: Claude Code Directo — Screenshot Local

Sin herramientas externas, usando Claude Code con una imagen local:

```
# En Claude Code, con la imagen en el proyecto:
"Mira este screenshot (./mockup.png) y genera un componente React con Tailwind CSS 
que reproduzca fielmente el diseno. Incluye responsive breakpoints y accesibilidad."
```

Claude Vision analiza la imagen y genera el codigo directamente.

### Integracion con FastAPI Backend

Para monetizar como servicio SaaS:

```python
# app/api/v1/endpoints/design.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.design_service import DesignService

router = APIRouter(prefix="/design", tags=["design"])

@router.post("/screenshot-to-code")
async def screenshot_to_code(
    file: UploadFile = File(...),
    framework: str = "react",  # react, vue, html
    css_framework: str = "tailwind",  # tailwind, css, styled-components
):
    """Convierte un screenshot en codigo React/Vue/HTML + CSS."""
    if file.content_type not in ["image/png", "image/jpeg", "image/webp"]:
        raise HTTPException(400, "Only PNG, JPEG, and WebP images are supported")
    
    if file.size > 10 * 1024 * 1024:  # 10MB max
        raise HTTPException(400, "Image size must be under 10MB")
    
    service = DesignService()
    result = await service.convert_screenshot(
        image=await file.read(),
        content_type=file.content_type,
        framework=framework,
        css_framework=css_framework,
    )
    
    return {
        "code": result.code,
        "components": result.components,
        "design_tokens": result.design_tokens,
        "fidelity_score": result.fidelity_score,
    }

@router.post("/url-to-code")
async def url_to_code(
    url: str,
    framework: str = "react",
    css_framework: str = "tailwind",
):
    """Convierte un sitio web (URL) en codigo React/Vue/HTML + CSS."""
    service = DesignService()
    result = await service.convert_url(
        url=url,
        framework=framework,
        css_framework=css_framework,
    )
    
    return {
        "code": result.code,
        "components": result.components,
        "design_tokens": result.design_tokens,
        "original_screenshot": result.screenshot_url,
        "fidelity_score": result.fidelity_score,
    }
```

### POC Decision Gate

**Criterios para continuar despues del spike (5 dias):**

| Criterio | Threshold | Metodo de validacion |
|----------|-----------|---------------------|
| Fidelidad visual | >= 80% | Comparacion manual screenshot vs output |
| Tiempo de generacion | < 60 segundos | Benchmark con 10 screenshots |
| Calidad del codigo | Componentes reutilizables, sin CSS inline | Code review por Sasha |
| Responsive | Funciona en 375px, 768px, 1440px | Test manual en 3 viewports |
| Costo por conversion | < $0.50 (API costs) | Calcular tokens consumidos |

**Decision matrix:**
- 5/5 criterios pass → Full implementation como feature SaaS
- 3-4/5 pass → Implementation limitada, iterar en areas debiles
- < 3/5 pass → Archivar, revisitar en Q3 2026

### Prompt Engineering para Alta Fidelidad

**Prompt optimizado para Claude Vision:**

```
You are an expert frontend developer. Analyze this UI screenshot and generate 
production-ready React + Tailwind CSS code.

RULES:
1. Match colors EXACTLY using hex values extracted from the image
2. Match spacing proportionally using Tailwind's spacing scale
3. Match typography: font sizes, weights, line heights
4. Include ALL visible text content exactly as shown
5. Make it responsive: works on 375px, 768px, and 1440px
6. Use semantic HTML: header, main, section, nav, footer
7. Add aria-labels to interactive elements
8. Use Tailwind CSS classes ONLY (no custom CSS)
9. Export as a single React functional component with TypeScript
10. Include comments marking each visual section

OUTPUT FORMAT:
- One complete .tsx file
- Import statements at top
- Component with props interface
- Export default at bottom
```

### Mejores Practicas

1. **Siempre comparar output vs original**: No confiar ciegamente. Abrir ambos lado a lado.
2. **Iterar en Claude Code**: Despues de la primera generacion, pedir ajustes especificos ("el boton es mas grande", "el spacing entre cards es 24px").
3. **Extraer design tokens**: Antes de generar codigo, pedir a Claude que extraiga colores, tipografia y spacing como variables Tailwind.
4. **Componentes atomicos**: Pedir componentes pequenos (Button, Card, Navbar) en lugar de paginas completas.
5. **Screenshot de alta calidad**: Usar capturas a 2x resolution para mejor analisis visual.
6. **Full page screenshots**: Para sitios largos, usar Firecrawl con `fullPage: true`.

### Cuando usar esta skill vs otras

| Situacion | Herramienta |
|-----------|-------------|
| Tengo un diseno en Stitch/Figma | Usar **Stitch MCP** skill |
| Tengo un screenshot o mockup | Usar **esta skill** |
| Quiero clonar un sitio existente | Usar **esta skill** (Firecrawl + Open Lovable) |
| Quiero disenar desde cero con IA | Usar **Stitch** primero, luego exportar |
| Landing page desde zero | Usar **Web Builder** skill |

### Monetizacion como Feature SaaS

Si el POC es exitoso, integrar al producto Data Reporting Agents:

**Pricing sugerido:**
- Free: 5 conversiones/mes
- Pro ($29/mes): 100 conversiones/mes
- Business ($99/mes): Unlimited + API access + priority
- Enterprise ($299/mes): Unlimited + custom models + SLA

**Metricas de exito:**
- Conversion rate de free → paid: > 5%
- NPS del feature: > 40
- Tiempo promedio de generacion: < 45 segundos
