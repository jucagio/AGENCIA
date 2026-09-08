# BRIEF — Flux Schnell Rechazada / Replicate + 3 Optimizaciones (Opción F)
**Fecha:** 2026-05-19
**Estado:** PREPARADO — pendiente envío tras confirmación de Juan Camilo
**Para:** Sasha, Brook, Erik, Ego, Cinthya
**De:** Jade (Directora Intel & Capacitaciones)
**Cc:** Jarvis (CEO)

---

## Qué pasó

Flux Schnell no pasó el umbral de calidad del equipo.

Erik evaluó los outputs: **6.4/10** sobre un threshold de **8.0 mínimo**. El problema de fondo: Flux genera ropa genérica. No hace clothing transfer real. Para nuestro producto eso no es aceptable. Detectarlo antes de producción es exactamente para lo que existe el proceso de evaluación — funcionó.

---

## Decisión

Retornamos a **Replicate FASHN** — ya validado en **8.4/10** — y aprovechamos el momento para ejecutar tres optimizaciones que estaban en el backlog. No volvemos igual. Volvemos mejor.

---

## Las 3 optimizaciones que ejecutamos ahora (Opción F)

### Optimización 1 — Cache SHA256 (ADR-004)
- **Qué hace:** Antes de llamar a Replicate, verifica si ya procesamos esa combinación exacta de imagen de usuario + prenda (hash SHA256). Si existe en cache, devuelve el resultado sin costo de API.
- **Impacto:** -45% en llamadas a Replicate
- **Quien implementa:** Sasha — Sprint T2 a T6
- **Referencia:** ADR-004 (decisión de arquitectura ya documentada)

### Optimización 2 — FASHN Base Free Tier
- **Qué hace:** Usar el tier gratuito de FASHN base para el volumen de pruebas del cap de 3/semana, reservando el tier de pago solo para usuarios convertidos.
- **Impacto:** -50% en costo de API para usuarios free
- **Quien implementa:** Sasha — configuración de credenciales + routing por tier

### Optimización 3 — Cap de 3/semana como palanca de conversión
- **Qué hace:** Mantener el cap, pero optimizar el mensaje de upgrade en el momento exacto del bloqueo (copy + CTA).
- **Impacto:** Mayor conversión en el punto de fricción
- **Quien implementa:** Brook (frontend), Erik (copy y diseño del CTA)

---

## Resultado combinado de las 3 optimizaciones

| Parámetro | Baseline | Con Opción F |
|-----------|----------|--------------|
| Proveedor | Replicate FASHN | Replicate FASHN |
| Cap/usuario | 3/sem | 3/sem |
| Calidad | 8.4/10 | 8.4/10 |
| Llamadas a API | 100% | ~55% (cache SHA256) |
| Costo API usuarios free | 100% | ~50% (free tier FASHN) |
| Margen vs baseline | — | **+37%** |

---

## Plan de ejecución de Sasha — Sprints T2 a T6

```
T2 — Implementar cache SHA256
     - Hash de (user_image_id + garment_id)
     - Storage en Redis o equivalente
     - TTL: 7 días (dentro del ciclo semanal del cap)

T3 — Routing por tier FASHN
     - Usuario free → FASHN base free tier
     - Usuario pago → FASHN pro tier
     - Fallback automático si free tier tiene latencia >X

T4 — Tests de integración cache + routing
     - Verificar que cache no produce falsos positivos
     - Validar que el tier correcto se activa por tipo de usuario

T5 — Brook: optimizar CTA de upgrade en pantalla de cap
     - Mostrar resultado de la prueba Y luego el bloqueo (no antes)
     - Copiar con Erik el texto del CTA

T6 — Ego: auditar implementación completa antes de release
     - Cache funciona: hits/misses correctos
     - Tier routing: sin mezcla de usuarios free/pago
     - Margen real vs proyectado
```

---

## Qué hace cada agente

**Sasha:** Lidera T2 a T4. Cache SHA256 + routing de tier FASHN. Documentar en ADR cualquier decisión de implementación nueva.

**Brook:** T5 — Pantalla de cap optimizada. Trigger en el momento correcto (post-resultado, no pre).

**Erik:** T5 — Copy y diseño del CTA de upgrade. El cap es el momento de mayor intención de compra del usuario. El mensaje debe estar a la altura.

**Cinthya:** Monitoreo de cache hit rate desde T4. Alerta si hit rate cae por debajo de 30% en primeras 72h post-release.

**Ego:** T6 — Auditoría completa antes de release a producción. Valida margen real vs +37% proyectado. Reporta a Jarvis.

**Jade:** Disponible para capacitar a Sasha en patrones de cache con hash para APIs de imagen si hay dudas de implementación.

---

## Tono de equipo

Flux no pasó. No es un retroceso — es información. Ahora sabemos exactamente dónde está nuestro piso de calidad y qué proveedor lo supera.

Volvemos a Replicate, pero no volvemos igual. Tres optimizaciones que estaban pendientes se ejecutan ahora. El margen sube de +26% a +37%. El cap de 3/semana sigue siendo el diferenciador.

Margen viable. Calidad validada. Cap activo. Seguimos.

---

**Proxima accion:** Jade envía este brief al equipo en el momento que Juan Camilo confirme Opción F. Sasha inicia T2 el mismo dia.
