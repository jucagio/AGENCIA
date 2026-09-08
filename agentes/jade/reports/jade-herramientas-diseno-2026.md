# Herramientas de Diseño 2026 — Jade Intel
**Preparado por:** Jade, Directora de Intel & Capacitaciones
**Fecha:** 2026-04-20 | **Versión:** 1.0

---

## RESUMEN EJECUTIVO

| Cambio | Impacto | Quién |
|--------|---------|-------|
| Google Stitch + DESIGN.md | Exploración visual 5x más rápida, gratis | Erik |
| Nano Banana 2 (Imagen 3 Flash) | Wireframe → mockup alta fidelidad en segundos | Erik |
| Figma Make + AI Agents (desde mar 2026) | Prototipado desde componentes propios con IA en canvas | Erik |
| v0 con Git integration (desde feb 2026) | Herramienta de producción real (PRs, branches, deploy) | Brook |
| Tailwind v4 @theme CSS-first | Elimina tailwind.config.js, builds 5-100x más rápidos | Brook |
| Cursor + Figma MCP | Cierra gap diseño-código sin handoff manual | Brook |

---

## 1. FIGMA AI / FIGMA MAKE

**Figma Make** es el producto de mayor evolución de Figma en 2026:

- **Make Kits (desde 2 abril 2026):** trae tus propios componentes del design system como contexto. El AI genera prototipos con tus componentes reales, no inventa nuevos.
- **Make Attachments:** adjunta datos y constraints del proyecto al contexto de generación.
- **Embed en Figma Design/FigJam/Slides:** prototipos Make dentro de archivos normales (desde ene 2026).
- **AI Agents en canvas (desde 24 marzo 2026):** agentes que diseñan directamente sobre el canvas con "Skills" para dar contexto del equipo.
- **Design-to-code bidireccional:** push de UI renderizada como frames editables + pull de contexto de diseño al código. Compatible con Cursor, Warp, Factory, Firebender y Augment.
- **Herramientas de imagen:** Expand, Erase, Isolate — disponibles en FigJam, Slides y Buzz.

---

## 2. GOOGLE STITCH + DESIGN.MD

Google adquirió Galileo AI (inicios 2025) → relanzó como **Google Stitch** con Gemini detrás. Disponible gratis en Google Labs (350 gen estándar + 200 experimentales/mes).

**Capacidades clave:**
- **5 pantallas simultáneas** (antes: 1 a la vez)
- **Voice design:** hablas directamente al canvas para diseño conversacional
- **AI design critique** en tiempo real
- **Export a Figma** directo
- **Generación de código** HTML/CSS/React desde el diseño

### DESIGN.MD — la función más poderosa

Archivo de texto plano que defines una vez y adjuntas al workspace de Stitch. Funciona como "design system en prosa":

```markdown
# Design System — Data Reporting Agents
## Colors
- Primary: #6366F1 (Indigo 500) — CTAs, active states
- Background: #0F172A — dark canvas
- Surface: #1E293B — cards, panels
## Typography
- Headings: Inter, 700
- Body: Inter, 400, 16px/24px
- Code: JetBrains Mono
## Components
- Buttons: rounded-lg, no outline, primary fill only
- Cards: border border-slate-700, rounded-xl, p-6
## Don'ts
- No gradients on backgrounds
- No serif fonts
```

Cada pantalla generada respeta estas reglas automáticamente — sin repetir el contexto en cada prompt.

---

## 3. NANO BANANA 2 (Imagen 3 Flash / Gemini 3.1 Flash Image)

"Nano Banana 2" es el nombre en clave del modelo de imagen más avanzado de Google disponible en abril 2026.

**Por qué importa para diseño UI:**
- **99% de precisión en texto:** labels, botones, menús, titulares legibles y bien posicionados
- **Entendimiento espacial:** comprende layouts, jerarquías, proporciones
- **Consistencia:** hasta 5 personajes y 14 objetos con consistency entre pantallas
- **Output 4K nativo**
- **In-image localization:** edita partes específicas sin destruir el resto
- **Aspect ratios nativos:** mobile (9:16), desktop (16:9), square (1:1)

**Cómo lo usa Erik:**
1. Boceto o wireframe rough
2. Nano Banana 2 → mockup alta fidelidad con texto real, colores y componentes
3. Export a Figma para refinamiento
4. O referencia visual directa para v0/Stitch

**Disponibilidad:** Google AI Studio (gratis), API Google (producción), plugin Figma Community.

---

## 4. DESIGN-TO-CODE WORKFLOWS COMPARADOS

### Tres rutas principales

**Ruta A — Diseño primero → código (tradicional evolucionada)**
```
Figma → Dev Mode / Figma Make → React/Tailwind
```
Herramientas: Figma + Anima / Locofy / Builder.io / Cursor + Figma MCP
- Control: alto | Velocidad: media | Código: media-alta

**Ruta B — Texto/imagen → código directo (AI-first)**
```
Prompt/screenshot → v0 / Emergent / Framer → código production-ready
```
- Control: medio | Velocidad: muy alta | Código: alta (v0), variable (otros)

**Ruta C — AI canvas → Figma → código (RECOMENDADA para la Agencia)**
```
Google Stitch → Figma (refinamiento) → v0 + Cursor (código)
```
- Control: alto | Velocidad: alta | Código: alta

### Tabla comparativa herramientas

| Herramienta | Input | Output | Git | MCP |
|---|---|---|---|---|
| v0 by Vercel | Texto + imagen | Next.js + shadcn | ✅ (feb 2026) | ✅ |
| Figma Make | Diseño + prompt | Prototipo + código | ❌ directo | ✅ Dev Mode |
| Emergent | Texto | React/Next.js/Expo | ❌ | ❌ |
| Google Stitch | Texto + voz + DESIGN.md | HTML/CSS/React | ❌ | ❌ |
| Builder.io | Figma frame | React/Vue/Angular | ✅ | ✅ |
| Framer | Texto + visual editor | Live website | ❌ | ❌ |
| Cursor + Figma MCP | Figma design | Cualquier stack | ✅ | ✅ |
| Banani | Screenshot → Figma | Figma editable + código | ❌ | ❌ |
| Relume | Texto | Sitemap + wireframes Figma | ❌ | ❌ |

---

## 5. TAILWIND CSS v4 — CAMBIOS CRÍTICOS

**Cambio central: CSS-first con `@theme`**

```css
/* v4 — globals.css */
@import "tailwindcss";

@theme {
  --color-brand: #6366F1;
  --font-sans: 'Inter', sans-serif;
  --spacing-section: 4rem;
  --radius-card: 0.75rem;
}
```
Cada token genera automáticamente: `bg-brand`, `text-brand`, `border-brand`, etc.

**Otros cambios:**
- Motor Rust (Oxide + Lightning CSS): builds 5x (completo) a 100x (incremental) más rápidos
- Zero-config content detection: no más `content: ['./src/**/*.tsx']`
- Sin PostCSS plugin requerido
- Container queries nativas: `@sm`, `@lg`, `@min-*`, `@max-*` (antes: plugin externo)
- Cascade layers nativas CSS
- Nuevas variantes: `not-*`, `in-*`, `nth-*`

**Para Brook:** NO iniciar proyectos con `tailwind.config.js`. Usar `@theme` desde el inicio.

---

## 6. TENDENCIAS UI/UX 2026

1. **Liquid Glass** (Apple iOS 26 → web): superficies translúcidas con profundidad y movimiento. Para dashboards premium y apps SaaS de alto valor.
2. **Motion como guía cognitiva**: animaciones como parte de lógica UX, no decoración. Herramientas: Rive, Framer Motion 11+.
3. **Tipografía oversized**: titulares vw-based como elemento visual principal en hero sections y landings.
4. **Bento Grid layouts**: tarjetas modulares redondeadas estándar para dashboards. Brook debe dominar esto.
5. **IA como capa ambiental invisible**: sugerencias contextuales, autocompletado, UI adaptativa — sin botón explícito "Usar IA".
6. **Dark mode como default**: especialmente en dashboards, herramientas dev y apps de productividad.
7. **Accesibilidad como estándar** (WCAG 2.2 vigente): riesgo legal real en Europa y EE.UU.
8. **Bold, saturated colors** (dopamine design): paletas brillantes — reacción al minimalismo gris 2020-2023.
9. **3D e interactividad WebGL**: React Three Fiber, Spline — democratizados en 2026.
10. **Calm design** (contra-tendencia B2B): patrones predecibles sin sorpresas en fintech/SaaS.

---

## 7. RECOMENDACIONES POR AGENTE

### Para Erik

**Herramientas a dominar ahora:**
1. **Google Stitch + DESIGN.md**: crear DESIGN.md una sola vez por proyecto. Costo: gratis.
2. **Nano Banana 2 vía Google AI Studio**: boceto → mockup alta fidelidad antes de Figma.
3. **Figma AI Agents en canvas**: configurar Skills con contexto del proyecto antes de empezar.
4. **Relume**: cuando llegue proyecto nuevo → sitemap + wireframes en <10 minutos.

**Principios para Data Reporting Agents:**
- Dark mode first: `#0F172A` base, `#1E293B` surface
- Bento grid para pantalla principal del dashboard
- Tipografía: Inter para UI, JetBrains Mono para datos/código
- Motion funcional en transiciones de datos
- Liquid Glass para modales y overlays premium

### Para Brook

**Cambios técnicos críticos:**
1. **Tailwind v4 `@theme`**: migrar de `tailwind.config.js`. No iniciar proyectos con config v3.
2. **shadcn/ui como base**: es el output nativo de v0. Sin shadcn/ui, integración con v0 es más costosa.
3. **Cursor + Figma MCP**: leer directamente el diseño de Erik desde el IDE. Reduce gap drásticamente.
4. **Container queries nativas v4**: `@sm`, `@lg` en lugar de media queries para componentes responsive.

**Workflow recomendado para Brook:**
```
Erik termina pantalla en Figma
→ Brook usa Cursor + Figma MCP para leer diseño
→ Genera código base con v0 (si hay componentes nuevos)
→ Refina en Cursor con contexto Figma MCP
→ Aplica tokens Tailwind v4 @theme
→ Review con Erik antes de merge
```

---

## 8. WORKFLOW COMPLETO DE LA AGENCIA (Recomendado)

### Fase 1 — Exploración (1-2h por feature)
```
Erik crea DESIGN.md del proyecto (una vez)
  → Google Stitch + DESIGN.md → 5 variaciones de pantalla
  → Elige dirección → descarga a Figma
```

### Fase 2 — Diseño en Figma
```
Erik construye design system formal (Auto Layout, Variables, Components)
  → Figma Make + AI Agents para prototipado interactivo
  → Entrega frames a Brook con annotations en Dev Mode
```

### Fase 3 — Código (Brook)
```
Cursor + Figma MCP → contexto del diseño en el IDE
  → v0 para componentes nuevos (prompt + imagen del frame de Figma)
  → Tailwind v4 @theme tokens
  → Review cruzado con Erik
```

### Fase 4 — Validación
```
Ego: ¿el código respeta el diseño?
Cyber Neo: ¿vulnerabilidades en nuevas dependencias?
Erik: QA visual (contraste, espaciado, tipografía, motion)
Brook: QA técnico (performance, Core Web Vitals, WCAG 2.2)
```

---

## Fuentes

- Figma Make — figma.com/make
- Figma Release Notes abril 2026 — releasebot.io
- Google Stitch — blog.google, developers.googleblog.com
- Nano Banana 2 — blog.google, Figma Community plugin
- v0 by Vercel — vercel.com/blog
- Tailwind v4 Migration Guide — dev.to, maviklabs.com
- Emergent, Banani, Relume — emergent.sh, banani.co, relume.io
- UI/UX Trends 2026 — orizon.co, raw.studio, tubikstudio.com

---

*Jade — 20 abril 2026 | Próxima actualización: mayo 2026*
