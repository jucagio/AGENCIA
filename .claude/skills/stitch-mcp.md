# Stitch MCP — Google Design System Integration

## Descripcion
Skill para integrar Google Stitch con Claude Code via MCP (Model Context Protocol). Permite disenar UI con IA en Stitch y exportar automaticamente a codigo React + Tailwind. Elimina la desincronizacion entre diseno y codigo. Optimizada para Erik (diseno) y Brook (implementacion).

## Instrucciones

Cuando el usuario pida ayuda con Stitch, design-to-code, o integracion Figma/Stitch, sigue estas directrices:

### Que es Google Stitch

Google Stitch es la herramienta gratuita de Google Labs para disenar UI con IA. Features principales:
- **Vibe Design**: Describe tu negocio y la sensacion deseada, Stitch genera layout, spacing y componentes
- **Voice Canvas**: Habla directamente al canvas, el agente escucha, critica y modifica en tiempo real
- **Multi-screen**: Genera hasta 5 pantallas interconectadas con design system consistente
- **DESIGN.md Export**: Exporta un archivo plain-text con todas las decisiones de diseno (colores, tipografia, spacing, componentes)
- **MCP Server**: Conexion directa con Claude Code, Cursor y otros AI coding tools
- **350 generaciones gratis/mes**

URL: https://stitch.withgoogle.com

### Instalacion del MCP Server

**Paso 1 — Configurar en Claude Code (VS Code):**

Agregar al archivo `.claude/settings.json` o al settings global de Claude Code:

```json
{
  "mcpServers": {
    "stitch": {
      "command": "npx",
      "args": ["@_davideast/stitch-mcp", "proxy"]
    }
  }
}
```

**Paso 2 — Autenticacion con Google:**

La primera vez que ejecutes el MCP, se abrira un flujo OAuth de Google. Acepta los permisos para que Claude Code pueda leer tus proyectos de Stitch.

Si ya tienes `gcloud` instalado y autenticado, el proceso es automatico.

**Paso 3 — Verificar conexion:**

En Claude Code, escribe:
```
Fetch my Stitch projects
```
Si el MCP esta bien configurado, Claude listara tus proyectos de Stitch.

### Alternativa: CLI Standalone

```bash
npx @_davideast/stitch-mcp init
```

El wizard maneja: instalacion de gcloud, OAuth, credenciales y setup del proyecto.

### Workflow Completo: Stitch → Codigo

```
1. DISENAR en Stitch
   - Abrir https://stitch.withgoogle.com
   - Crear proyecto nuevo
   - Usar Vibe Design: describir el negocio y la sensacion deseada
   - Stitch genera hasta 5 pantallas con design system consistente
   - Iterar con Voice Canvas si es necesario
   
2. EXPORTAR desde Stitch
   - Click en "Export" → seleccionar "DESIGN.md"
   - Stitch genera un archivo plain-text con:
     * Paleta de colores (hex codes)
     * Tipografia (font families, sizes, weights)
     * Spacing rules
     * Componentes descritos (botones, cards, navbars, etc.)
     * Layout specifications
   
3. IMPORTAR a Claude Code via MCP
   - En Claude Code: "Fetch screens from my Stitch project [nombre]"
   - Claude lee el design metadata via MCP
   - O: copiar DESIGN.md al root del proyecto y Claude lo lee automaticamente
   
4. GENERAR CODIGO
   - "Generate a React app with Tailwind CSS from the Stitch design"
   - Claude genera componentes production-ready siguiendo el DESIGN.md
   - Output: JSX/TSX + Tailwind classes + responsive breakpoints
   
5. ITERAR
   - Cambiar algo en Stitch → re-exportar → Claude actualiza el codigo
   - O: pedir cambios directamente a Claude y luego sincronizar a Stitch
```

### Formato DESIGN.md

El archivo DESIGN.md que exporta Stitch tiene esta estructura:

```markdown
# Design System — [Nombre del Proyecto]

## Colors
- Primary: #2563EB
- Secondary: #1E293B
- Accent: #F59E0B
- Background: #FFFFFF
- Surface: #F8FAFC
- Text Primary: #0F172A
- Text Secondary: #64748B

## Typography
- Heading: Inter, sans-serif
- Body: Inter, sans-serif
- Scale: 14/16/18/20/24/30/36/48px
- Line Height: 1.5 (body), 1.2 (headings)

## Spacing
- Base unit: 4px
- Scale: 4/8/12/16/24/32/48/64/96px

## Components
### Button
- Primary: bg-blue-600, text-white, rounded-lg, px-6 py-3
- Secondary: border border-gray-300, text-gray-700, rounded-lg
- Hover: opacity 90%, shadow-sm

### Card
- bg-white, rounded-xl, shadow-sm, p-6
- Hover: shadow-md transition

[...mas componentes]

## Screens
### Screen 1 — Dashboard
- Layout: sidebar (240px) + main content
- Header: fixed top, 64px height
- Content: 3-column grid, gap-6

[...mas screens]
```

### Integracion con CI/CD

Para automatizar el flujo design → code:

```
Workflow propuesto:

1. Erik diseña en Stitch
2. Erik exporta DESIGN.md al repo (branch: design-sync)
3. CI detecta cambio en DESIGN.md
4. CI ejecuta Claude Code: "Update components based on new DESIGN.md"
5. Claude genera/actualiza codigo
6. PR automatico con los cambios
7. Brook revisa y aprueba
8. Merge a main

Ciclo completo: ~15 min (vs 4h manual)
```

**GitHub Action ejemplo:**

```yaml
name: Design Sync
on:
  push:
    branches: [design-sync]
    paths: ['DESIGN.md']

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Generate code from design
        run: |
          npx claude-code "Read DESIGN.md and update all React components to match the new design system. Generate Tailwind CSS classes. Keep existing business logic intact."
      - name: Create PR
        uses: peter-evans/create-pull-request@v6
        with:
          title: "design: sync components with Stitch DESIGN.md"
          branch: design-sync-auto
          body: "Auto-generated from Stitch DESIGN.md update"
```

### Best Practices

1. **DESIGN.md como fuente de verdad**: Siempre mantener el DESIGN.md actualizado en el root del repo. Claude Code lo lee automaticamente.
2. **Un proyecto Stitch por producto**: No mezclar diseños de distintos productos en un mismo proyecto.
3. **Vibe Design para MVP**: Para prototipos rapidos, describir el negocio y dejar que Stitch genere. Para produccion, refinar manualmente.
4. **Voice Canvas para iteraciones**: Mas rapido que escribir instrucciones detalladas.
5. **Export frecuente**: Cada vez que cambies algo significativo en Stitch, re-exportar DESIGN.md.
6. **No editar DESIGN.md manualmente**: Siempre editar en Stitch y re-exportar. Si editas a mano, la sincronizacion se pierde.
7. **Componentes atomicos**: Pedir a Claude que genere componentes pequenos y reutilizables, no paginas monoliticas.

### Troubleshooting

| Problema | Solucion |
|----------|----------|
| MCP no conecta | Verificar que `npx @_davideast/stitch-mcp proxy` funciona standalone. Revisar OAuth. |
| DESIGN.md vacio | Asegurar que el proyecto en Stitch tiene screens generados antes de exportar. |
| Codigo no respeta colores | Verificar que DESIGN.md esta en el root del repo. Pedir a Claude: "Read DESIGN.md and list the color palette". |
| OAuth expira | Re-ejecutar `npx @_davideast/stitch-mcp init` para refrescar credenciales. |
| 350 limit alcanzado | Crear cuenta Google adicional, o esperar al reset mensual. Para produccion, considerar Google Workspace. |

### Cuando usar Stitch vs otras herramientas

| Herramienta | Cuando usarla |
|-------------|---------------|
| **Stitch** | Prototipado rapido de UI, design systems nuevos, MVP, iteraciones con IA |
| **Figma** | Diseños detallados que requieren control pixel-perfect, colaboracion con clientes que ya usan Figma |
| **DESIGN.md manual** | Cuando ya tienes un design system definido y solo necesitas documentarlo para Claude |
| **Web Builder skill** | Landing pages rapidas con shadcn/ui donde no necesitas Stitch |

### Ejemplo End-to-End: Teclado de Senas

```
1. Abrir Stitch → Nuevo proyecto "Teclado de Senas"
2. Vibe Design: "App educativa para personas sordomudas. 
   Tono: calido, accesible, inclusivo. 
   Paleta: azules suaves + amarillo accesibilidad.
   Pantallas: Home, Teclado de signos, Lecciones, Progreso, Settings"
3. Stitch genera 5 pantallas con design system
4. Exportar DESIGN.md al repo teclado-senas/
5. En Claude Code: "Fetch screens from Stitch project 'Teclado de Senas' 
   and generate Flutter widgets following the DESIGN.md"
6. Claude genera widgets de Flutter con los colores, tipografia y layout
7. Brook integra los widgets en la app existente
```

### Colaboracion Erik ↔ Brook

- **Erik** es dueno del diseño en Stitch (crea, itera, exporta DESIGN.md)
- **Brook** consume el DESIGN.md y genera/implementa codigo
- **Regla**: Erik NO edita codigo, Brook NO edita Stitch
- **Sync meeting**: 15 min diarios durante sprint activo
