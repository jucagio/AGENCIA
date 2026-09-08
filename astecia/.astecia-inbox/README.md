# .astecia-inbox — Consultas de ASTECIA a Jarvis

**.astecia-inbox** — canal asíncrono donde ASTECIA deja las consultas que exceden su scope comercial para que Jarvis las resuelva.

Esta carpeta es el **canal asíncrono entrante** para Jarvis (CEO). ASTECIA (corriendo en Haiku, vía OpenClaw + WhatsApp) escribe aquí cuando necesita:

- Análisis estratégico profundo (>15 min de thinking)
- Investigación de mercado compleja
- Decisiones arquitectónicas (producto, proceso, sistemas)
- Soporte técnico / programación / automatización
- Decisiones que comprometan >$200M COP
- Cualquier cosa que exceda su scope comercial táctico

---

## Protocolo para Jarvis

Cuando Juan Camilo te active en Claude Code, **SIEMPRE al inicio de sesión** revisa esta carpeta:

```bash
ls -lt "C:\Users\PCC\Documents\JUAN CAMILO GIL\PERSONAL\PROGRAMACIÓN\AGENCIA\.astecia-inbox\"
```

Si hay archivos `.md` nuevos (no es README.md), léelos en orden de urgencia. Formato de nombre:

```
YYYY-MM-DD_HHMM_<tema-kebab-case>.md
```

Ejemplo: `2026-04-22_1530_cargill-propuesta-40M.md`

## Cómo responder

1. **Lee la consulta completa** — contexto, pregunta, lo que ASTECIA ya pensó, decisiones bloqueadas
2. **Piensa profundo** (Ultrathink si aplica) — aprovecha que corres en Opus
3. **Responde en `.jarvis-inbox/<mismo-nombre-de-archivo>.md`** con este template:

```markdown
# Respuesta de Jarvis — <tema>

**De:** Jarvis (CEO)
**Para:** ASTECIA
**Fecha:** <ISO timestamp>
**Re:** <nombre del archivo de consulta>

## Recomendación directa
<1-2 frases — qué hacer, claro y accionable>

## Razonamiento
<por qué esa es la mejor opción, qué trade-offs evaluaste>

## Cómo ejecutarlo (táctico, para ASTECIA)
<pasos concretos que ASTECIA le transmita a Juan Camilo por WhatsApp>

## Si sale mal (plan B)
<alternativa si la recomendación falla>
```

4. **Notifica a Juan Camilo por WhatsApp** (vía ASTECIA o directamente): *"Respondí la consulta sobre `<tema>` en `.jarvis-inbox/`. ASTECIA la leerá."*

5. **Después de responder, archiva la consulta original** moviendo el archivo de `.astecia-inbox/` a `.astecia-inbox/archive/<YYYY-MM>/`.

---

## Principios del canal

- **Asíncrono por diseño:** ASTECIA no te bloquea. Da su mejor respuesta táctica y abre la consulta en paralelo.
- **Jarvis = profundidad, ASTECIA = velocidad.** No dupliques pensamiento que ASTECIA ya puede hacer.
- **Todo queda archivado.** Es la memoria organizacional de decisiones estratégicas.
- **No hay consulta tonta.** Si ASTECIA escaló, es porque lo necesita.

---

*Última actualización: 2026-04-22 por Jarvis (CEO)*
