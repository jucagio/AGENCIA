# Lecciones Aprendidas — Infraestructura Local de Agentes IA

**Proyecto:** FASE 0-5 Infraestructura Local
**Fecha:** 2026-04-06
**Equipo:** Jarvis (CEO), Jade (Intel), Ego (Auditor)

---

## Lo que salio bien

### 1. Obsidian vault en vez de PostgreSQL Docker
**Decision:** Usar archivos Markdown + Git en vez de base de datos relacional
**Resultado:** Setup en minutos en vez de horas. Sin Docker, sin migraciones, sin connection pooling.
**Leccion:** Para MVPs locales, la solucion mas simple que funcione es la mejor. Git ya nos da versionado y auditoria gratis.

### 2. Velocidad de entrega
**Plan:** 14-21 horas en 3-4 dias
**Real:** ~8 horas en 1 sesion extendida
**Leccion:** Cuando la arquitectura es simple (sin Docker, sin DB externa), la implementacion es dramaticamente mas rapida.

### 3. Deteccion de credenciales por Ego
**Hallazgo:** GROQ API key expuesta en settings.local.json (commit publico)
**Accion:** Remediada con git filter-branch + .gitignore
**Leccion:** La auditoria automatica de Ego detecta cosas que el desarrollador no ve. El auditor siempre debe revisar DESPUES de implementar.

### 4. Test suite como red de seguridad
**Resultado:** 39 tests pasando en 1.58 segundos
**Leccion:** Tests automatizados detectan regresiones inmediatamente. El rate limiter acumulando estado entre tests fue un bug real que solo los tests encontraron.

---

## Lo que salio mal (y como se arreglo)

### 1. Emojis en Windows cp1252
**Problema:** Python logging en Windows usa codepage 1252, que no soporta emojis Unicode.
**Efecto:** Cada linea de log del agent-runner generaba un UnicodeEncodeError (aunque no crasheaba).
**Fix:** Reemplazar emojis con [LABELS] ASCII: [OK], [START], [RUN], [ERROR], [STATUS].
**Leccion:** En Windows, NUNCA usar emojis en logs de Python. Usar text labels.

### 2. FastAPI BaseHTTPMiddleware import
**Problema:** FastAPI 0.135+ movio `BaseHTTPMiddleware` a `starlette.middleware.base`.
**Efecto:** El servidor arrancaba con una version vieja del codigo (sin auth endpoints) porque el import fallaba silenciosamente.
**Fix:** Cambiar `from fastapi.middleware.base` a `from starlette.middleware.base`.
**Leccion:** Siempre verificar que el servidor carga la version actual del codigo. FastAPI evoluciona rapido — imports cambian entre versiones.

### 3. Puerto 8000 zombie
**Problema:** Un proceso previo de uvicorn quedo escuchando en puerto 8000 y no se podia matar.
**Efecto:** El nuevo servidor con auth no podia usar ese puerto.
**Fix:** Usar puerto 8001 como alternativa.
**Leccion:** En Windows, procesos zombie son comunes con servidores async. Tener un puerto backup (8001) o usar `netstat -ano | grep :PORT` para diagnosticar.

### 4. Rate limiter acumulando entre tests
**Problema:** Todos los tests comparten el mismo `TestClient` y `app`. El rate limiter (30 req/min por IP) se acumula.
**Efecto:** Tests posteriores reciben 429 (rate limited) en vez de 401 o 200.
**Fix:** Fixture `autouse` que resetea el rate limiter antes de cada test class.
**Leccion:** Middleware con estado (rate limiting, caching) DEBE resetearse entre tests. Usar fixtures de pytest.

### 5. datetime.utcnow() deprecado
**Problema:** Python 3.12+ depreca `datetime.utcnow()` en favor de `datetime.now(timezone.utc)`.
**Efecto:** Warnings en test suite.
**Fix:** Actualizar jwt.py a usar `datetime.now(timezone.utc)`.
**Leccion:** Mantener dependencias actualizadas. Deprecation warnings son bugs futuros.

### 6. requirements-api.txt con versiones exactas inexistentes
**Problema:** `pyjwt==2.8.1` no existe (maximo disponible era 2.12.1).
**Efecto:** `pip install` falla.
**Fix:** Usar version constraints flexibles: `pyjwt>=2.8.0`.
**Leccion:** NUNCA usar versiones exactas en requirements a menos que sea absolutamente necesario. Usar `>=` con version minima.

---

## Patrones que repetir

1. **Auditoria post-implementacion** — Ego siempre revisa despues de cada fase. Detecta lo que el desarrollador no ve.
2. **Zero-trust desde el principio** — Todos empiezan sin permisos. Es mas facil dar acceso que quitar.
3. **Obsidian vault para MVPs** — Simple, versionado, legible. Escalar a DB cuando sea necesario.
4. **39 tests antes de produccion** — No hay deployment sin suite de tests verde.
5. **Fix immediato de credenciales** — Si se expone un secret, revocar + limpiar historial en <1 hora.

---

## Patrones que evitar

1. **Emojis en codigo Python para Windows** — Usar [LABELS] ASCII.
2. **Versiones exactas en requirements** — Usar `>=` constraints.
3. **Compartir estado de middleware entre tests** — Resetear antes de cada test.
4. **Confiar en que el servidor cargo la version actual** — Verificar endpoints con `/openapi.json`.
5. **Matar procesos con `taskkill` en Windows** — A veces no funciona. Tener puerto backup.

---

## Metricas del proyecto

| Metrica | Valor |
|---------|-------|
| Lineas de codigo | ~4,500 |
| Tests | 39/39 (100%) |
| Tiempo de ejecucion (tests) | 1.58 segundos |
| Agentes configurados | 11 |
| Paralelismo maximo | 3 simultaneos |
| Bugs encontrados por tests | 3 (rate limiter, JSON corrupto, timing) |
| Bugs encontrados por auditoria | 1 critico (credencial expuesta) |
| Tiempo plan vs real | 14-21h plan vs ~8h real |

---

## Proximos pasos basados en lecciones

1. **Pre-commit hook** para detectar secrets antes de commit (Ego recomendacion)
2. **PYTHONIOENCODOING=utf-8** como variable de entorno global en Windows
3. **Supabase sync** para backup remoto del vault
4. **CI/CD pipeline** con GitHub Actions (ejecutar 39 tests en cada push)
5. **CLAUDE_API_KEY** real para conectar agentes a la API de Anthropic

---

**Documentado por:** Jarvis (CEO)
**Revisado por:** Ego (Auditor), Jade (Intel)
**Fecha:** 2026-04-06
