---
name: alejo-project-flowchart
description: |
  Metodología obligatoria de Alejo ANTES de escribir software. Para CADA proyecto nuevo Alejo
  produce TRES entregables que cumplen normativa ISO 5807 / ANSI: (1) documento Markdown con
  flujograma Mermaid ISO-compliant, (2) IMAGEN PNG del flujograma renderizada (vía higgsfield
  o Mermaid CLI) para uso en presentaciones, (3) MAPA CONCEPTUAL en formato Obsidian Canvas
  (.canvas) mostrando relaciones entre conceptos del proyecto. Cada paso del proceso debe ser
  CLARO, ESPECÍFICO y con verbo de acción — nunca etiquetas truncadas tipo "Buscar informaci..."
  El objetivo: cero ambigüedad, cero consultas durante ejecución, cumplimiento normativo.
trigger:
  - Proyecto nuevo aprobado por Juan Camilo
  - Pivot mayor en proyecto existente
  - Cliente nuevo con scope no definido
  - Antes de cualquier kickoff de Sprint 0
owner: Alejo (Solutions Architect)
deliverables:
  - 00_FLUJOGRAMA.md (documento con Mermaid ISO 5807)
  - 00_FLUJOGRAMA.png (imagen renderizada del diagrama)
  - 00_MAPA_CONCEPTUAL.canvas (Obsidian Canvas)
normativa:
  - ISO 5807:1985 — Information processing — Documentation symbols and conventions for data, program and system flowcharts
  - ANSI X3.5 — Flowchart Symbols and their Usage in Information Processing
estimated_effort: 2-3 horas
---

# Skill: Project Flowchart ISO 5807 (Alejo)

> **Regla de oro:** *No hay una línea de código antes de que existan los 3 entregables firmados por Juan Camilo.*

Esta habilidad enseña a Alejo a producir el arranque de cualquier proyecto cumpliendo normativa internacional ISO 5807. Antes esta habilidad producía solo Mermaid plano sin respetar simbología — ya no. Ahora cada símbolo tiene significado normativo y hay validación de cumplimiento.

---

## I. CUÁNDO SE INVOCA

Alejo activa este skill automáticamente cuando detecta:

1. Juan Camilo dice: *"vamos a hacer X"*, *"nuevo proyecto"*, *"cliente nuevo"*, *"propuesta para…"*
2. Jarvis convoca un kickoff de proyecto
3. Un proyecto existente pivota de arquitectura
4. Un cliente cambia el scope >30%

---

## II. SIMBOLOGÍA OBLIGATORIA ISO 5807 (TABLA NORMATIVA)

**Alejo DEBE usar exactamente estos símbolos. Cualquier desviación = retrabajo.**

| Símbolo ISO | Nombre | Uso | Sintaxis Mermaid |
|------------|--------|-----|------------------|
| ⬭ Elipse / Óvalo | **Terminal (Inicio/Fin)** | Marca el inicio o fin del proceso. Reservado a la primera y última actividad. Contenido: "INICIO" o "FIN". | `id([INICIO])` o `id([FIN])` |
| ▭ Rectángulo | **Operación / Proceso** | Cualquier actividad o tarea. Debe iniciar con **verbo de acción en infinitivo** (Validar, Generar, Enviar, Calcular). | `id[Verbo + objeto + complemento]` |
| ◇ Rombo | **Punto de decisión** | Decisión SÍ/NO únicamente. Contenido: pregunta cerrada que termina en "?". Siempre 2 salidas etiquetadas SI/NO. | `id{¿Pregunta cerrada?}` |
| ▱ Paralelogramo | **Entrada / Salida de datos** | Input externo del usuario o output al usuario. | `id[/Datos entrada/]` o `id[\Salida\]` |
| 🗎 Documento | **Documento / Registro** | Reporte, factura, manual, contrato — cualquier artefacto en papel/PDF. | `id[(Documento)]` |
| 🗇 Multidocumento | **Listados acumulados** | Conjunto de documentos o notas de trabajo. | `id[[Listado]]` |
| ⏣ Cilindro | **Base de datos** | Almacenamiento persistente. Especificar tabla/colección. | `id[(Tabla DB)]` |
| ◯ Círculo pequeño con letra | **Conector en página** | Une partes del flujograma en la misma página cuando hay solapamiento. Letra A, B, C… | `id((A))` |
| ⬠ Pentágono inferior | **Conector fuera de página** | Une con otra página del flujograma. | `id>Página 2\]` |
| → Flecha | **Dirección de flujo** | Sentido del proceso. Siempre arriba→abajo o izquierda→derecha. | `-->` o `-- texto -->` |

**Reglas adicionales ISO 5807:**
1. Cada rombo de decisión DEBE tener exactamente 2 salidas etiquetadas `SI` y `NO`
2. Todo proceso tiene 1 INICIO y al menos 1 FIN (puede tener varios FIN)
3. Las flechas NO se cruzan; si deben cruzarse, usa conectores ◯
4. Cada caja debe poder leerse sola (no abreviaturas, no truncados como "Buscar informaci...")
5. Máximo 15 nodos por diagrama; si excede, fragmenta en subprocesos referenciados
6. Numera las cajas si el proceso tiene >8 pasos: `[1. Validar pedido]`

---

## III. ESTRUCTURA OBLIGATORIA DEL DOCUMENTO

Output: **3 archivos** en `agencia-vault/01_Projects/<NOMBRE_PROYECTO>/`:

```
00_FLUJOGRAMA.md         ← Documento principal con 7 secciones
00_FLUJOGRAMA.png        ← Imagen renderizada del diagrama TO-BE
00_MAPA_CONCEPTUAL.canvas ← Mapa conceptual Obsidian
```

### Sección 1 — Problema + Causa Raíz (5 Whys)

```markdown
## 1. Problema

**Síntoma observable:** <qué ve el usuario / cliente>

**5 Whys:**
1. ¿Por qué ocurre X? → …
2. ¿Por qué Y? → …
3. ¿Por qué Z? → …
4. ¿Por qué W? → …
5. ¿Por qué V? → **CAUSA RAÍZ**

**Costo de no resolverlo:** <USD/mes, horas/semana, % churn, etc.>
```

**Criterio:** Si la causa raíz es "no tenemos la herramienta" → vuelve a empezar.

---

### Sección 2 — Actores y Stakeholders

```markdown
## 2. Actores

| Actor | Rol | Dolor específico | Métrica que le importa |
|-------|-----|------------------|------------------------|
| Usuario final | … | … | … |
| Cliente que paga | … | … | … |
| Decisor técnico | … | … | … |
| Equipo interno | … | … | … |
```

---

### Sección 3 — Flujo AS-IS (proceso actual) — ISO 5807

```markdown
## 3. Flujo AS-IS

\`\`\`mermaid
flowchart TD
    INICIO([INICIO: Usuario quiere X])
    P1[1. Acción específica con verbo]
    D1{¿Decisión cerrada?}
    P2[2. Otra acción específica]
    DOC1[(Documento generado)]
    FIN([FIN: Resultado actual])

    INICIO --> P1
    P1 --> D1
    D1 -- SI --> P2
    D1 -- NO --> DOC1
    P2 --> FIN
    DOC1 --> FIN
\`\`\`

**Puntos de dolor en el flujo actual:**
- 🔴 Paso P1: <tiempo/costo>
- 🔴 Decisión D1: <fricción>
```

**REGLAS para este diagrama:**
- Inicio y fin obligatorios con elipse `([texto])`
- Cada proceso con verbo en infinitivo
- Decisiones siempre cerradas (SI/NO)
- Numera pasos si hay >8

---

### Sección 4 — Flujo TO-BE (estado deseado) — ISO 5807

```markdown
## 4. Flujo TO-BE

\`\`\`mermaid
flowchart TD
    INICIO([INICIO: Usuario abre la app])
    E1[/Entrada: Foto del usuario/]
    P1[1. Validar calidad de imagen]
    DB1[(users.profiles)]
    D1{¿Cumple resolución mínima?}
    P2[2. Solicitar nueva foto]
    P3[3. Procesar análisis corporal con Vision API]
    DOC1[(Reporte de medidas)]
    P4[4. Generar recomendación con Claude]
    S1[\Salida: 5 outfits sugeridos\]
    FIN([FIN: Outfit seleccionado])

    INICIO --> E1
    E1 --> P1
    P1 --> D1
    D1 -- NO --> P2
    P2 --> E1
    D1 -- SI --> P3
    P3 --> DB1
    P3 --> DOC1
    DOC1 --> P4
    P4 --> S1
    S1 --> FIN

    style P3 fill:#90EE90
    style P4 fill:#90EE90
    style S1 fill:#90EE90
\`\`\`

**Ganancia esperada:**
- Tiempo total: <antes> → <después> (Nx)
- Pasos manuales eliminados: <#>
- Trazabilidad: <antes vs después>
```

---

### Sección 5 — Decisiones Arquitectónicas (mini-ADRs)

```markdown
## 5. Decisiones Arquitectónicas

### ADR-001: <Decisión>
- **Contexto:** …
- **Opciones evaluadas:**
  - A) … → Pro: … Con: … Costo: …
  - B) … → Pro: … Con: … Costo: …
- **Decisión:** A
- **Razón:** …
- **Trade-off aceptado:** …
- **Kill-switch / revisar en:** <umbral medible>
```

**Mínimo 3 ADRs.**

---

### Sección 6 — Criterios de Éxito (KPIs medibles)

```markdown
## 6. Criterios de Éxito

| KPI | Baseline (AS-IS) | Meta (TO-BE) | Cómo se mide | Cadencia |
|-----|------------------|--------------|--------------|----------|
| … | … | … | … | … |

**Definition of Done:** Los KPIs alcanzan meta durante 2 meses consecutivos.
```

---

### Sección 7 — Riesgos y Mitigación

```markdown
## 7. Riesgos

| # | Riesgo | Probabilidad | Impacto | Mitigación | Owner |
|---|--------|--------------|---------|------------|-------|
| R1 | … | Alta/Media/Baja | Alto/Medio/Bajo | … | Nombre |
```

---

## IV. ENTREGABLE 2 — IMAGEN PNG DEL FLUJOGRAMA

**Obligatorio.** El diagrama TO-BE debe existir también como imagen PNG para presentaciones.

### Opción A — Mermaid CLI (preferido, determinista)
```powershell
# Requiere: npm install -g @mermaid-js/mermaid-cli
mmdc -i 00_FLUJOGRAMA.md -o 00_FLUJOGRAMA.png -t default -b white -w 1920
```

### Opción B — higgsfield MCP (cuando se requiera estilo visual ejecutivo)
Usar `mcp__higgsfield__generate_image` con prompt detallado:
- Estilo: "ISO 5807 standard flowchart, clean professional corporate style, white background, blue boxes for processes, diamonds for decisions, ovals for start/end, arrows showing flow direction, top-down layout, readable Spanish labels"
- Incluir lista explícita de nodos y conexiones en el prompt
- Resolución: 1920×1080 mínimo

### Opción C — Excalidraw (cuando se requiera edición posterior)
Generar archivo `.excalidraw` con la estructura ISO. Solo si los stakeholders lo van a editar.

**Validación de la imagen:**
- [ ] Todos los símbolos respetan ISO 5807
- [ ] Texto legible al 100% de zoom
- [ ] No hay nodos truncados ("Buscar informaci...") — texto completo
- [ ] Flechas no se cruzan
- [ ] Decisiones con etiquetas SI/NO visibles
- [ ] Inicio (elipse) y Fin (elipse) presentes

---

## V. ENTREGABLE 3 — MAPA CONCEPTUAL (Obsidian Canvas)

**Obligatorio.** Diferente del flujograma — un mapa conceptual muestra **relaciones entre conceptos**, no el flujo de un proceso.

Usar el skill `json-canvas` para producir `00_MAPA_CONCEPTUAL.canvas`.

**Estructura del mapa conceptual:**

```
                    [PROYECTO]
                        |
        ┌───────────────┼───────────────┐
        |               |               |
   [Problema]      [Solución]      [Stakeholders]
        |               |               |
   ┌────┴────┐     ┌────┴────┐     ┌────┴────┐
   |         |     |         |     |         |
 [Dolor1] [Dolor2] [Tech]  [UX]  [Usuario] [Cliente]
```

**Reglas:**
- Nodo central = nombre del proyecto
- 3-5 ramas principales: Problema, Solución, Stakeholders, Tecnología, Riesgos
- Cada rama con 2-4 sub-nodos máximo
- Aristas con etiquetas que describen la relación ("causa", "resuelve", "depende de", "mide")
- Colores por categoría (problema=rojo, solución=verde, tech=azul)
- Cada nodo puede enlazar a la sección correspondiente en `00_FLUJOGRAMA.md` con `[[wikilink]]`

---

## VI. CHECKLIST DE CIERRE (obligatorio antes de entregar)

### Documento Markdown
- [ ] Las 7 secciones completas
- [ ] Mínimo 3 ADRs con trade-offs medibles
- [ ] KPIs con baseline, meta, método, cadencia
- [ ] Riesgos con owner

### Diagrama ISO 5807
- [ ] INICIO y FIN con elipse `([texto])`
- [ ] Cada proceso con verbo en infinitivo
- [ ] Decisiones con `{?}` y salidas SI/NO etiquetadas
- [ ] Documentos con `[(texto)]`, bases de datos con cilindro
- [ ] I/O con paralelogramo `[/texto/]` o `[\texto\]`
- [ ] Máx 15 nodos por diagrama, sin flechas cruzadas
- [ ] CERO texto truncado o con "..."
- [ ] Numeración si >8 pasos

### Imagen PNG
- [ ] Archivo `00_FLUJOGRAMA.png` existe en la carpeta del proyecto
- [ ] Resolución ≥1920×1080
- [ ] Texto 100% legible
- [ ] Símbolos ISO correctos

### Mapa conceptual
- [ ] Archivo `00_MAPA_CONCEPTUAL.canvas` existe
- [ ] Nodo central = proyecto
- [ ] 3-5 ramas principales
- [ ] Aristas etiquetadas con tipo de relación
- [ ] Colores por categoría

### Test de las 10 preguntas
El documento responde solo, sin preguntar a Alejo:
1. ¿Qué problema resolvemos?
2. ¿Para quién?
3. ¿Cómo se hace hoy?
4. ¿Cómo va a quedar?
5. ¿Qué stack usamos y por qué?
6. ¿Dónde se despliega?
7. ¿Cómo medimos éxito?
8. ¿Qué puede salir mal?
9. ¿Quién es responsable de qué?
10. ¿Cuándo sabemos que terminó?

---

## VII. ANTI-PATRONES (lo que Alejo NUNCA hace)

- ❌ Cajas con texto truncado: "Buscar informaci...", "Asignación del...", "Desarrollo de la lógica de control en coordin..."
- ❌ Procesos sin verbo de acción ("Información del cliente" → mal; "Recopilar información del cliente" → bien)
- ❌ Rombos con más de 2 salidas o salidas sin etiquetar
- ❌ Mezclar símbolos arbitrariamente (todo como rectángulo es violación ISO)
- ❌ Flechas cruzadas sin conectores
- ❌ Diagramas con >15 nodos (fragmenta en subprocesos)
- ❌ Causa raíz = "no tenemos la herramienta"
- ❌ ADRs sin trade-off explícito
- ❌ KPIs vagos ("mejorar performance")
- ❌ Entregar PDF en lugar de Markdown editable
- ❌ Saltar el mapa conceptual o la imagen PNG "por tiempo"

---

## VIII. HANDOFF

1. Guardar los 3 archivos en `agencia-vault/01_Projects/<PROYECTO>/`
2. Commit: `feat(<proyecto>): flujograma ISO 5807 + imagen + mapa conceptual`
3. TL;DR de 5 líneas a Jarvis
4. Jarvis presenta a Juan Camilo (sábado 10 AM)
5. Solo después de firma → Sasha/Brook arrancan Sprint 0

---

**Mantra de Alejo:** *"Un símbolo mal usado vale por una semana de retrabajo."*
