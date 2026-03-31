---
name: claude-ads
description: >
  Framework de 190+ verificaciones para auditar y optimizar campañas publicitarias
  en Google Ads, Meta Ads, TikTok Ads, LinkedIn Ads y YouTube Ads usando IA.
  Usar cuando se audite una campaña existente, se cree una nueva, se optimice el
  rendimiento o se prepare un reporte de resultados para el cliente.
  Agentes: Leo, Cinthya, Sasha.
---

# Claude Ads — Gestión Multi-Plataforma con IA

## Qué hace este skill

Audita y optimiza campañas publicitarias en 5 plataformas usando 190+ puntos de verificación. El resultado es un diagnóstico con hallazgos clasificados por severidad y un plan de optimización priorizado.

---

## Estructura de Auditoría (190+ checks)

### NIVEL 1 — Configuración de Cuenta (35 checks)

```
GOOGLE ADS — Configuración:
[ ] Seguimiento de conversiones configurado y verificado
[ ] Objetivos de conversión alineados con la meta del negocio
[ ] Audiencias de remarketing creadas (visitantes web, compradores)
[ ] Listas de palabras clave negativas a nivel cuenta
[ ] Configuración de ubicación geográfica correcta
[ ] Extensiones de anuncio activas (sitelinks, llamada, precio, promoción)
[ ] Enlace con Google Analytics 4 activo
[ ] Alertas de rendimiento configuradas
[ ] Presupuesto compartido vs por campaña — decisión documentada
[ ] Configuración de conversiones post-click y post-view

META ADS — Configuración:
[ ] Píxel de Meta instalado y verificado en todas las páginas
[ ] Eventos estándar configurados (ViewContent, AddToCart, Purchase)
[ ] API de Conversiones (server-side) activa
[ ] Catálogo de productos conectado (si aplica)
[ ] Custom Audiences creadas (visitantes, compradores, videos)
[ ] Lookalike Audiences generadas desde las mejores custom audiences
[ ] Cuenta verificada para categorías especiales (si aplica)
[ ] Límite de gasto diario y de cuenta configurado
```

### NIVEL 2 — Estructura de Campañas (45 checks)

```
ESTRUCTURA:
[ ] Campañas organizadas por objetivo (awareness/consideration/conversion)
[ ] Grupos de anuncios/ad sets con temática coherente
[ ] Máximo 1 objetivo por campaña
[ ] Segmentación de audiencias sin solapamiento entre ad sets
[ ] Presupuesto distribuido según el embudo (awareness < conversión)
[ ] CBO (Campaign Budget Optimization) vs ABO — decisión documentada

PALABRAS CLAVE (Google):
[ ] Match types correctos por etapa del embudo
  - Broad match solo con Smart Bidding activo
  - Phrase match para términos de intención media
  - Exact match para términos de alta conversión
[ ] Quality Score > 7/10 en keywords principales
[ ] Términos de búsqueda revisados semanalmente
[ ] Palabras clave negativas añadidas desde search terms
[ ] Grupos de anuncios con 10-20 keywords máximo
```

### NIVEL 3 — Creatividades y Copy (55 checks)

```
GOOGLE ADS — Anuncios:
[ ] Responsive Search Ads con mínimo 5 títulos y 5 descripciones
[ ] Títulos incluyen la keyword principal (al menos 1)
[ ] Al menos 1 título con CTA claro
[ ] Descripciones resaltan beneficio único (no solo features)
[ ] Ad Strength: "Excelente" en los anuncios principales
[ ] URL de destino específica para la keyword/tema del grupo
[ ] Display paths con keywords relevantes

META ADS — Creatividades:
[ ] Test de al menos 3 formatos por ad set (imagen, carrusel, video)
[ ] Video con caption/subtítulos (85% se ve sin audio)
[ ] Primeros 3 segundos del video capturan atención (hook)
[ ] Texto principal < 125 caracteres (preview completo en mobile)
[ ] CTA button alineado con el objetivo del ad set
[ ] Creatividades adaptadas a cada placement (feed, stories, reels)
[ ] Test A/B activo entre creatividades
[ ] Frecuencia < 3 en audiencias frías, < 5 en remarketing
```

### NIVEL 4 — Bidding y Presupuesto (30 checks)

```
ESTRATEGIAS DE PUJA:
[ ] Smart Bidding activo con suficientes conversiones (mínimo 30/mes)
[ ] Target CPA o Target ROAS basado en datos históricos reales
[ ] Período de aprendizaje respetado (no cambiar configuración en 7 días)
[ ] Ajustes de puja por dispositivo justificados con datos
[ ] Ajustes por horario basados en datos de conversión
[ ] Presupuesto diario = objetivo mensual / 30.4

ANÁLISIS DE EFICIENCIA:
[ ] CPC vs benchmark de la industria
[ ] CTR vs benchmark (Google Search > 3%, Meta Feed > 1%)
[ ] CPM tendencia (si sube → saturación de audiencia)
[ ] ROAS >= objetivo mínimo de rentabilidad
[ ] CAC (Customer Acquisition Cost) vs LTV del cliente
```

### NIVEL 5 — Landing Pages (25 checks)

```
[ ] Mensaje de la landing = mensaje del anuncio (message match)
[ ] CTA visible above the fold
[ ] Velocidad de carga < 3 segundos (PageSpeed > 70)
[ ] Mobile-first: diseño optimizado para móvil
[ ] Formulario con mínimos campos necesarios (< 5 campos)
[ ] Social proof visible (testimonios, casos de éxito, logos)
[ ] Sin distracciones (sin menú de navegación completo)
[ ] Pixel/tag de conversión disparando correctamente
[ ] HTTPS activo
[ ] Heatmap instalado (Hotjar/Clarity) para optimización continua
```

---

## Formato de Reporte de Auditoría

```markdown
# Auditoría de Campañas — [Cliente] — [Fecha]

## Resumen Ejecutivo
- Presupuesto mensual auditado: $X
- Plataformas: [Google/Meta/TikTok/LinkedIn]
- Checks completados: X/190
- Score general: X/100

## Hallazgos por Severidad
| # | Hallazgo | Plataforma | Severidad | Impacto estimado | Acción |
|---|----------|-----------|-----------|-----------------|--------|
| 1 | Sin seguimiento de conversiones | Google | 🔴 Crítico | Sin datos para optimizar | Configurar GA4 + Google Tag |

## KPIs Actuales vs Benchmark
| Métrica | Actual | Benchmark industria | Diferencia |
|---------|--------|---------------------|------------|
| CTR | 0.8% | 3.5% | -2.7% ⚠️ |
| CPC | $2.50 | $1.80 | +$0.70 |
| ROAS | 1.8x | 4x | -2.2x 🔴 |

## Plan de Optimización (priorizado por impacto)
1. [Acción] → [Impacto esperado] → [Responsable] → [Fecha]
```

---

## Cómo usa este skill Leo

Cuando un cliente pide gestión o auditoría de campañas:
1. Leo solicita acceso de solo lectura a las cuentas publicitarias
2. Aplica los 190 checks del framework
3. Genera el reporte de auditoría
4. Presenta: "La Agencia encontró X oportunidades de mejora. Con estas optimizaciones proyectamos mejorar el ROAS de X a Y."
5. Cotiza el servicio de gestión como retención mensual

*Fuente: tododeia.com — Claude Ads + Meta Ads Best Practices 2026*
