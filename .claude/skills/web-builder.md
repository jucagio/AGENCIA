# Web Builder — Skill para Brook y Erik

## Descripcion
Skill para construir landing pages y sitios completos usando Claude Code + claude-webkit. Claude pregunta sobre el negocio, diseña, construye y despliega en Vercel automaticamente. Stack: Next.js 15+, Tailwind CSS 4, shadcn/ui, TypeScript, Framer Motion.

## Instrucciones

Cuando el usuario pida construir un sitio web o landing page, sigue estas directrices:

### Setup inicial (una sola vez)

```bash
git clone https://github.com/Hainrixz/claude-webkit.git
cd claude-webkit
node -v && git --version && claude --version  # verificar requisitos
claude
```

Requisitos: Node.js 18+, Git, Claude Code instalado.

### Las 6 fases del proceso

**Fase 1 — Discovery**
Hacer preguntas al cliente sobre:
- Nombre y descripcion del negocio
- Publico objetivo
- Paleta de colores preferida (o dejar que Claude proponga)
- Tono (formal, amigable, tecnico, creativo)
- Secciones necesarias (hero, servicios, testimonios, precios, contacto)

**Fase 2 — Design Approval**
Presentar plan visual con:
- Colores primario/secundario/acento con codigos hex
- Tipografia (heading font + body font)
- Estilo general (minimalista, corporativo, creativo, etc.)
- Layout propuesto por secciones
→ Esperar aprobacion antes de construir

**Fase 3 — Construccion automatizada**
Generar en orden:
1. Layout base y configuracion de Tailwind
2. Header con navegacion
3. Hero section con animacion Framer Motion
4. Seccion de servicios/features
5. Testimonios
6. Seccion de precios (si aplica)
7. Footer con CTA y datos de contacto

**Fase 4 — Preview local**
```bash
npm run dev
# Abrir http://localhost:3000
```
Mostrar al cliente antes de publicar.

**Fase 5 — Refinamiento iterativo**
Ajustar via lenguaje natural:
- "Cambia el color primario a #2563EB"
- "Agrega una seccion de FAQ"
- "Hace el hero mas grande con imagen de fondo"

**Fase 6 — Deploy en Vercel**
```bash
npx vercel --prod
```
Vercel genera URL automaticamente. Conectar dominio custom si el cliente lo tiene.

### Los 13 sub-skills incluidos en claude-webkit

| Sub-skill | Que hace |
|-----------|----------|
| design-methodology | Principios de diseno aplicados a cada decision |
| component-architecture | Estructura de componentes React reutilizables |
| performance-optimization | Core Web Vitals, lazy loading, bundle size |
| deployment-automation | CI/CD con Vercel, preview branches |
| humanizer | Textos naturales, no genericos |
| seo-fundamentals | Meta tags, OG tags, sitemap basico |
| accessibility | ARIA labels, contraste, navegacion por teclado |
| responsive-design | Mobile-first, breakpoints consistentes |
| animation-systems | Framer Motion: fade, slide, stagger effects |
| content-strategy | Jerarquia de informacion, CTAs efectivos |
| color-theory | Paletas armonicas, contraste WCAG |
| typography-systems | Escala tipografica, line-height, legibilidad |
| code-quality | TypeScript estricto, componentes limpios |

### Checklist de calidad antes de entregar

- [ ] Lighthouse score > 90 en Performance, Accessibility, SEO
- [ ] Responsive en mobile (375px), tablet (768px), desktop (1440px)
- [ ] Todas las imagenes con alt text descriptivo
- [ ] Meta title y description unicos por pagina
- [ ] Sin errores en consola del navegador
- [ ] CTA visible above the fold en mobile
- [ ] Formulario de contacto funcional

### Casos de uso en la Agencia

- Landing page de proyecto nuevo para presentar a inversores
- Sitio web de cliente de Juan Camilo (MAPER)
- Portfolio o pagina de servicios de la Agencia
- MVP visual de un producto en evaluacion

### Colaboracion Brook ↔ Erik

- **Erik** define el sistema de diseno en Fase 2 (colores, tipografia, estilo)
- **Brook** implementa en Fase 3-5 usando los assets de Erik
- **Brook** hace el deploy en Fase 6
