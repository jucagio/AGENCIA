# Capacidades de la Infraestructura Local de Agentes

## Hardware

- **CPU:** 11th Gen Intel Core i5-1135G7 (4 cores, 2.4-4.2 GHz)
- **RAM:** 16 GB DDR4
- **Storage:** 211 GB disponibles
- **GPU:** Intel Iris Xe (DirectX 12 compatible, no CUDA)
- **OS:** Windows 11 Pro (Build 10.0.26200)

## Agentes Paralelos Recomendados

| Escenario | Max Agentes | Duración | Performance |
|-----------|------------|----------|-------------|
| **Óptimo** | 2-3 paralelos | <600s (10min) | Sin throttle, RAM estable |
| **Máximo** | 3 paralelos | 300-600s | Observable throttle, CPU 80-95% |
| **Crítico** | 4+ paralelos | >600s | OOM risk, sistema inestable |

**Recomendación:** Mantener máximo 3 agentes en ejecución simultánea.

## Asignación de Recursos

```
Sistema Operativo:          4 GB (fixed)
FastAPI + Herramientas:     2 GB
Agentes activos (2-3):      4-5 GB
Cache + Buffer:             3-4 GB
Reserve para OS:            1-2 GB
─────────────────────────────────
Total disponible:          16 GB
```

## Throughput por Modelo

| Modelo | Tiempo promedio | Casos de uso |
|--------|-----------------|--------------|
| **Haiku** | 30-60 seg | Clasificación, enrutamiento, tareas simples |
| **Sonnet** | 2-3 min | Investigación, frontend, diseño, automatización |
| **Opus** | 4-6 min | Backend, arquitectura, auditoría, decisiones críticas |

**Notas:**
- Tiempos incluyen latencia de API (150-200ms promedio)
- Streaming responses más rápidos que esperar respuesta completa
- Parallel execution: 3 Sonnet @ 3min = ~3min total (no 9min)

## APIs Locales

| Servicio | URL | Puerto | Estado |
|----------|-----|--------|--------|
| **FastAPI** | http://localhost:8000 | 8000 | Activo (dev mode) |
| **Obsidian Vault** | agencia-vault/ | N/A | Archivo local (Git sync) |
| **MCP Server** | .claude/mcp-servers/ | N/A | Integration point |

## Endpoints Disponibles

### Públicos (sin autenticación)
- `GET /health` — Health check del servidor
- `GET /config` — Configuración no-sensible
- `POST /auth/login` — Obtener JWT token

### Protegidos (requieren JWT + permisos)
- `GET /agents` — Listar todos los agentes
- `GET /agents/{id}/state` — Estado de un agente
- `POST /agents/{id}/execute` — Ejecutar un agente (requiere agents:execute)

## Sistema de Permisos (Zero-Trust)

```
Role: admin
├─ agents:read
├─ agents:execute
├─ agents:manage
└─ system:audit

Role: agent
├─ agents:read
└─ agents:execute

Role: viewer
└─ agents:read

Role: none
  (sin permisos)
```

**Agentes por rol:**
- **admin:** Jarvis, Ego
- **agent:** Sasha, Brook, Erik, Cinthya, Jade, Alejo, Leo, Yang
- **viewer:** (configurables en login)

## Limitaciones Conocidas

### Performance
- **Sin aceleración GPU:** Modelos Opus pueden ser lentos (4-6 min vs 1-2 min en GPU)
- **RAM limitada:** 4+ agentes → memory pressure, GC pausas visibles
- **CPU:** i5 de 4 cores → bottleneck en parallelización extrema (5+ agentes)

### Conectividad
- **Offline-only:** Sin configuración de Supabase sync, todo es local
- **Git como source of truth:** Obsidian vault sincronizado con Git, no BD remota

### Automatización
- **n8n opcional:** Requiere puerto 5678 libre, no es crítico para MVP

## Optimizaciones Aplicadas

✅ **Obsidian Vault para persistencia:** Sin Docker, sin DB compleja
✅ **JWT para autenticación ligera:** Sin sesiones en Redis
✅ **Rate limiting en memoria:** 30 req/min por IP
✅ **Audit logging JSONL:** Logs compactos, facilita grep
✅ **Agent state JSON:** Lectura/escritura O(1), sin queries

## Monitoreo de Performance

### Señales de problemas

| Señal | Causa | Solución |
|-------|-------|----------|
| CPU > 95% por >30s | 4+ agentes ejecutándose | Esperar a que terminen, max 3 |
| RAM > 14 GB | Memory leak u óptimo en Haiku | Reiniciar FastAPI server |
| API latencia > 5s | OS thrashing | Cerrar otras apps |
| MCP timeout | Obsidian vault corrupted | Verificar .gitignore |

### Comandos útiles

```bash
# Verificar estado de agentes
curl -H "Authorization: Bearer TOKEN" http://localhost:8000/agents

# Ver logs de auditoría (últimas 10 lineas)
tail -n 10 .claude/agent-logs/api_audit.jsonl

# Ver estado de un agente
curl -H "Authorization: Bearer TOKEN" http://localhost:8000/agents/{id}/state

# Revisar estado de Obsidian vault
cd agencia-vault && git log --oneline | head -20
```

## Escalabilidad Futura

Si la Agencia escala a:

- **5-10 agentes:** Migrar a Paperclip local + PostgreSQL Docker
- **10-50 agentes:** Cloud infrastructure (Railway, Render, Vercel)
- **50+ agentes:** Multi-tenancy, kubernetes, distribuido

Arquitectura actual soporta MVP con 11 agentes (máx 3 paralelos).

## Requerimientos para Producción

- [ ] Supabase sync para backup remoto de agencia-vault
- [ ] Monitoreo de performance (Grafana local o cloud)
- [ ] Rate limiting en Redis (vs. en-memoria actual)
- [ ] HTTPS con certificados auto-signed (localhost)
- [ ] Backup automatizado diario (vault + agent-state)
- [ ] Database para users (vs. hardcoded credentials actuales)

## Stack Técnico Completo

```
ORQUESTACIÓN:    Jarvis + Agent SDK (Python + Claude API)
PERSISTENCIA:    Obsidian vault (Markdown + Git)
API:             FastAPI + Pydantic + JWT (Python)
AUTENTICACIÓN:   JWT (HS256, 24h expiration)
LOGGING:         JSONL files (.claude/agent-logs/)
MCP SERVER:      ObsidianBridge (reads/writes vault)
TESTING:         Pytest (security + parallelization)
```

---

**Documento:** CAPABILITIES.md
**Válido para:** Windows 11 Pro, i5-1135G7, 16GB RAM
**Último actualizado:** 2026-04-06
**Owner:** Jarvis (CEO)
