# 🏗️ Infraestructura de Agentes IA Locales — FASE 1 + 2

**Estado:** ✅ Operativo (placeholder sin CLAUDE_API_KEY)

---

## 📋 Resumen

Infraestructura simplificada para ejecutar **2-3 agentes IA en paralelo** localmente:

```
FastAPI Server          Agent Runner              Obsidian Vault
(localhost:8000)    (.claude/agent-runner.py)  (persistencia de estado)
     |                      |                         |
     +----------+----------+----------+
                |
         11 agentes configurados
         (Jarvis, Sasha, Brook, etc.)
```

---

## 🚀 Instalación Rápida

### 1. Edita `.env` con credenciales

```bash
# .env (crear desde .env.example)
CLAUDE_API_KEY=sk-ant-...  # Agrega cuando tengas disponible
JWT_SECRET=tu_secreto_seguro_aqui
```

### 2. Instala dependencias (Windows PowerShell)

```powershell
.\setup.ps1
```

O manual:
```bash
pip install -r requirements-api.txt
```

### 3. Crea directorios

```bash
mkdir -p .claude/agent-state .claude/agent-logs api/models api/routes api/security tests
```

---

## 📖 Cómo Usar

### A) FastAPI Server (API local)

```bash
# Levanta servidor en localhost:8000
python -m uvicorn api.main:app --reload --port 8000
```

**Endpoints disponibles:**

```
GET  /health              → Health check
GET  /agents              → Lista todos los agentes
GET  /agents/{id}/state   → Estado actual del agente
POST /agents/{id}/execute → Ejecutar agente con prompt
GET  /config              → Config (no-sensitive)
```

**Testing con curl:**

```bash
# Health check
curl http://localhost:8000/health

# Listar agentes
curl http://localhost:8000/agents

# Estado de Jarvis
curl http://localhost:8000/agents/jarvis/state

# Swagger UI (documentación interactiva)
open http://localhost:8000/docs
```

---

### B) Agent Runner (orquestación)

```bash
# Listar agentes configurados
python .claude/agent-runner.py --list

# Ver estado actual de un agente
python .claude/agent-runner.py --state jarvis

# Ejecutar un agente
python .claude/agent-runner.py --execute sasha --prompt "Diseña schema PostgreSQL"

# Ejecutar 2-3 agentes EN PARALELO
python .claude/agent-runner.py --execute sasha,brook,erik --prompt "Hola"

# Ejecutar con prompt personalizado
python .claude/agent-runner.py --execute jarvis --prompt "Planifica FASE 3"
```

**Output:**
- Estado se guarda en `.claude/agent-state/{agent_name}.json` ✅
- Logs en `.claude/agent-logs/{agent_name}_executions.log` ✅
- Todo versionado automáticamente en Git ✅

---

## 🏗️ Estructura de Carpetas

```
.
├── .env.example                    # Template (copy to .env)
├── .env                            # Credenciales (no versionado)
├── .gitignore                      # Excluye .env, agent-state, logs
│
├── agents.json                     # Config 11 agentes
├── requirements-api.txt            # Dependencias Python
├── setup.ps1                       # Script instalación Windows
│
├── .claude/
│   ├── launch.json                 # Config servidores (FastAPI + Agent Runner)
│   ├── agent-runner.py             # Orquestador de agentes (FASE 2)
│   ├── agent-state/                # Estado persistente (no versionado)
│   │   ├── jarvis.json
│   │   ├── sasha.json
│   │   └── ...
│   └── agent-logs/                 # Logs de ejecución (no versionado)
│       └── {agent_name}_executions.log
│
├── api/
│   ├── __init__.py
│   ├── main.py                     # FastAPI app
│   ├── config.py                   # Pydantic Settings
│   ├── models/                     # ORM models (vacío)
│   ├── routes/                     # API endpoints (vacío)
│   └── security/                   # JWT, permissions (vacío)
│
├── agencia-vault/                  # Obsidian vault (YA EXISTE)
│   ├── 01_Projects/
│   ├── 02_Areas/
│   ├── 03_Resources/
│   └── ...
│
└── tests/                          # Test suite (vacío)
```

---

## 🔌 Integración Claude API (CUANDO TENGAS KEY)

**Archivo:** `.claude/agent-runner.py` líneas ~180-195

Descomenta este código:

```python
# === INTEGRATION POINT: Claude API ===
from anthropic import Anthropic

client = Anthropic(api_key=settings.claude_api_key)
agent_config = self.get_agent_config(agent_name)

response = client.messages.create(
    model=agent_config["model"],  # "opus" or "sonnet"
    max_tokens=agent_config.get("max_tokens", 4096),
    system=f"You are {agent_config['role']}.",
    messages=[{"role": "user", "content": prompt}]
)

result.output = response.content[0].text
```

Luego:
```bash
pip install anthropic
# Agrega CLAUDE_API_KEY a .env
python .claude/agent-runner.py --execute sasha --prompt "..."
```

---

## 📊 Agentes Disponibles

```
Jarvis      → CEO & Orchestrator (Opus)
Sasha       → Backend & Security (Opus)
Brook       → Frontend & BD (Sonnet)
Erik        → Design (Sonnet)
Cinthya     → Automation (Sonnet)
Jade        → Intel & Capacitaciones (Sonnet)
Alejo       → Solutions Architect (Opus)
Ego         → Auditor (Opus)
Leo         → Sales Agent (Opus)
Yang        → Commercial Intel (Sonnet)
Prospect    → Prospecting Agent (Sonnet)
```

**Max paralelos:** 3 agentes simultáneos (recomendado para 16GB RAM)

---

## 🔒 Seguridad

- ✅ `.env` excluido de Git (credenciales seguras)
- ✅ JWT en `api/main.py` (pendiente implementación completa)
- ✅ CORS restringido a `localhost` only
- ✅ Estado persistente en archivos JSON (Obsidian vault)
- ✅ Auditoría vía Git commits

---

## 📝 Próximos Pasos

**FASE 3:** MCP server para Obsidian
- Agentes escriben ADRs automáticamente
- Actualizar progreso del proyecto
- Sincronización automática con vault

**FASE 4:** Seguridad en APIs
- JWT completo
- Rate limiting
- Autenticación

**FASE 5:** Testing & Validación
- Test de paralelización
- Documentación de capacidades
- E2E testing

---

## 🐛 Troubleshooting

### FastAPI no levanta
```bash
# Verifica que Python esté en PATH
python --version

# Verifica dependencias
pip list | grep -i fastapi

# Instala manualmente
pip install fastapi uvicorn
```

### Agent Runner falla
```bash
# Verifica agents.json existe
ls agents.json

# Ejecuta con --list para debug
python .claude/agent-runner.py --list
```

### Estado no persiste
```bash
# Verifica directorios existen
mkdir -p .claude/agent-state .claude/agent-logs

# Verifica permisos de escritura
ls -la .claude/agent-state/
```

---

## 📞 Referencias

- **Agents Config:** `agents.json`
- **FastAPI App:** `api/main.py`
- **Agent Runner:** `.claude/agent-runner.py`
- **Settings:** `api/config.py`
- **Vault:** `agencia-vault/`

---

**Versión:** 0.1.0 (FASE 1 + 2)
**Última actualización:** 2026-04-06
**Estado:** ✅ Operativo (placeholder, sin API KEY)
