# Claude SEO — Skill para Brook y Erik

## Descripcion
Skill con 13 comandos especializados que convierte a Claude en un especialista SEO completo. Vive dentro del proyecto para acceder al codebase, sitemap y archivos reales. Instalable en un solo comando.

## Instrucciones

Cuando el usuario pida auditoria SEO, optimizacion de contenido, o mejoras de posicionamiento, sigue estas directrices:

### Instalacion

```bash
# Opcion A — npx (recomendado)
npx skills.sh install claude-seo

# Opcion B — manual
git clone https://github.com/skills-sh/claude-seo .claude/skills/claude-seo
```

### Los 13 comandos

#### Auditoria Tecnica (5 comandos)

| Comando | Que hace |
|---------|----------|
| `/seo-audit` | Auditoria completa: meta tags, headings, imagenes sin alt, links rotos, duplicados |
| `/seo-speed` | Performance: bundle size, imagenes sin optimizar, tiempo de carga estimado |
| `/seo-structure` | Arquitectura del sitio: jerarquia de URLs, linking interno, profundidad de paginas |
| `/seo-crawl` | Vista del crawler: robots.txt, directivas noindex, canonicals, sitemap.xml |
| `/seo-schema` | Datos estructurados: Schema.org, rich snippets, validacion de JSON-LD |

#### Contenido y Keywords (5 comandos)

| Comando | Que hace |
|---------|----------|
| `/seo-keywords` | Densidad de keywords, ubicacion en headings, variaciones semanticas |
| `/seo-meta` | Genera meta titles (50-60 chars) y descriptions (150-160 chars) optimizados |
| `/seo-headings` | Jerarquia H1-H6, keyword placement, estructura logica del contenido |
| `/seo-content` | Longitud, legibilidad Flesch, contenido delgado, duplicados internos |
| `/seo-images` | Alt text, nombres de archivo, formatos modernos (WebP/AVIF), lazy loading |

#### Reportes y Automatizacion (3 comandos)

| Comando | Que hace |
|---------|----------|
| `/seo-report` | Reporte markdown completo combinando todos los audits con prioridad de issues |
| `/seo-compare` | Compara metricas SEO entre dos paginas o con un competidor |
| `/seo-fix` | Agente autonomo: auditoria → prioriza por impacto → corrige automaticamente |

### Flujo de trabajo recomendado

```
1. /seo-audit      → visión general de todos los problemas
2. /seo-speed      → impacto en Core Web Vitals
3. /seo-keywords   → oportunidades de contenido
4. /seo-fix        → correccion automatica de los issues de mayor impacto
5. /seo-report     → reporte final para el cliente
```

### Integracion con Web Builder (claude-webkit)

Usar en combinacion con el skill `web-builder.md`:

| Fase Web Builder | Comando SEO a ejecutar |
|-----------------|----------------------|
| Fase 2 — Design | `/seo-structure` para planificar arquitectura de URLs |
| Fase 3 — Build | `/seo-schema` para agregar Schema.org desde el inicio |
| Fase 5 — Refine | `/seo-keywords` y `/seo-meta` antes de publicar |
| Fase 6 — Deploy | `/seo-audit` completo post-deploy |

### Metricas objetivo

| Metrica | Objetivo minimo | Objetivo ideal |
|---------|----------------|----------------|
| Lighthouse SEO score | > 90 | 100 |
| Meta title length | 50-60 chars | 55 chars |
| Meta description | 150-160 chars | 155 chars |
| H1 por pagina | 1 exactamente | 1 con keyword principal |
| Imagenes con alt text | 100% | 100% descriptivas |
| Core Web Vitals LCP | < 4s | < 2.5s |

### Casos de uso en la Agencia

- Auditoria SEO de sitios de clientes de Juan Camilo
- Optimizacion de landing pages generadas con Web Builder
- Analisis competitivo de proyectos en evaluacion
- Reporte SEO mensual para clientes en retainer
- Checklist pre-lanzamiento de cualquier sitio nuevo
