# Setup Local de la Infraestructura de Agentes

Guía step-by-step para ejecutar la Agencia localmente en Windows 11.

## Requisitos Previos

- Python 3.10+ (`python --version`)
- Git (`git --version`)
- ~2.5 GB espacio en disco para dependencias
- Terminal (CMD, PowerShell, o WSL2 Bash)

Opcionalmente recomendado:
- VS Code con Claude Code extension
- Obsidian (para trabajar con agencia-vault/)
- GitHub Desktop (para sincronizar vault)

## 1. Clonar el Repositorio

```bash
git clone <REPO_URL> agencia
cd agencia
```

## 2. Crear Archivo .env

Copiar credenciales desde .env.example:

```bash
# Windows CMD
copy .env.example .env

# Windows PowerShell
Copy-Item .env.example .env

# WSL2/Bash
cp .env.example .env
```

Editar `.env` con credenciales reales:

```env
CLAUDE_API_KEY=sk-...        # Tu API key de Anthropic
JWT_SECRET=your-secret-key   # Secreto para firmar JWTs (cualquier string largo)
VAULT_PATH=agencia-vault     # Path al vault (relativo o absoluto)
ENVIRONMENT=development
DEBUG=true
```

**IMPORTANTE:** `.env` no se versionará en Git (excepto `.env.example`).

## 3. Instalar Dependencias Python

```bash
# Crear virtual environment (recomendado)
python -m venv venv

# Activar venv
# Windows CMD
venv\Scripts\activate
# Windows PowerShell
venv\Scripts\Activate.ps1
# WSL2/Bash
source venv/bin/activate

# Instalar dependencias
pip install -r requirements-api.txt
pip install pytest pytest-asyncio  # Para tests

# Verificar instalación
pip list | grep -E "fastapi|pydantic|PyJWT"
```

## 4. Crear Estructura de Directorios

```bash
# Ya debería existir desde clone, pero verificar:
mkdir -p .claude/agent-state
mkdir -p .claude/agent-logs
mkdir -p tests
```

## 5. Verificar Configuración

```bash
# Testear que settings carga correctamente
python -c "from api.config import settings; print(settings.vault_path)"
```

Si sale error, revisar:
- `.env` existe en raíz del proyecto
- Variables están correctamente nombradas
- No hay caracteres especiales en valores

## 6. Ejecutar FastAPI Server

### Opción A: Usando launch.json de Claude Code (recomendado)

1. Abrir proyecto en VS Code
2. Click en "Run & Debug" (Ctrl+Shift+D)
3. Seleccionar "FastAPI Server" de dropdown
4. Click play verde

VS Code levantará servidor en http://localhost:8000

### Opción B: Línea de comandos

```bash
# Con reload automático (desarrollo)
py -m uvicorn api.main:app --reload --port 8000

# Sin reload (producción)
py -m uvicorn api.main:app --port 8000 --workers 4
```

### Verificar que está corriendo

```bash
curl http://localhost:8000/health
# Debería retornar: {"status":"ok","environment":"development","vault":"..."}
```

## 7. Test de Autenticación

```bash
# 1. Login y obtener token
curl -X POST "http://localhost:8000/auth/login?username=jarvis&password=agencia"
# Respuesta:
# {"access_token":"eyJ0...","token_type":"bearer","user":"jarvis","role":"admin"}

# 2. Copiar el token completo (sin comillas)
TOKEN="eyJ0..."

# 3. Usar token para acceder a endpoint protegido
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/agents
# Debería retornar lista de agentes
```

## 8. Ejecutar Tests

```bash
# Test de seguridad
pytest tests/test_security.py -v

# Test de paralelización
pytest tests/test_parallelization.py -v

# Todos los tests
pytest tests/ -v
```

## 9. Ejecutar Agent-Runner (Opcional)

```bash
# Ver agentes disponibles
python .claude/agent-runner.py --list

# Ejecutar un agente (requiere CLAUDE_API_KEY funcional)
python .claude/agent-runner.py --execute sasha --prompt "Tu prompt aquí"

# Ejecutar múltiples agentes en paralelo
python .claude/agent-runner.py --parallel sasha,brook --prompt "Prompt para ambos"
```

## 10. Ver Obsidian Vault

```bash
# Abrir Obsidian (cliente de escritorio)
# File > Open Vault > Seleccionar carpeta "agencia-vault"

# O explorar en terminal
ls -la agencia-vault/01_Projects/
ls -la agencia-vault/06_Metadata/
```

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'api'"

**Causa:** PYTHONPATH no incluye directorio raíz del proyecto
**Solución:**
```bash
# Windows CMD
set PYTHONPATH=%cd%

# Windows PowerShell
$env:PYTHONPATH = (Get-Location).Path

# Bash
export PYTHONPATH="$(pwd)"

# Luego ejecutar de nuevo
py -m uvicorn api.main:app --reload
```

### Error: "jwt.exceptions.DecodeError: Signature verification failed"

**Causa:** JWT_SECRET en .env no coincide con el usado para crear token
**Solución:** Verificar que JWT_SECRET sea idéntico en .env

### Error: "LF will be replaced by CRLF" en git

**Causa:** Diferencias entre Windows (CRLF) y Unix (LF)
**Solución:** No es error, solo warning. Git automáticamente convierte.

### Port 8000 ya está en uso

**Causa:** Otro proceso usa puerto 8000
**Solución:**
```bash
# Cambiar puerto
py -m uvicorn api.main:app --reload --port 8001

# O matar proceso que usa 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### .env no se carga

**Causa:** Archivo no existe o está en carpeta equivocada
**Verificar:**
```bash
# Debería estar en raíz del proyecto
ls -la .env

# Si no existe, crear desde template
cp .env.example .env
# Y editar con credenciales reales
```

### Rate limiting bloquea tus requests

**Causa:** Más de 30 requests/minuto desde tu IP
**Solución:** Esperar 1 minuto o ejecutar desde IP diferente

### Audit logs llenan disco

**Causa:** .claude/agent-logs/api_audit.jsonl crece sin límite
**Solución:**
```bash
# Limpiar logs viejos (mantener últimos 10k líneas)
tail -n 10000 .claude/agent-logs/api_audit.jsonl > .claude/agent-logs/api_audit.jsonl.tmp
mv .claude/agent-logs/api_audit.jsonl.tmp .claude/agent-logs/api_audit.jsonl
```

## Comandos Útiles Diarios

```bash
# Ver estado de todos los agentes
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/agents | python -m json.tool

# Ver último cambio en vault
cd agencia-vault && git log --oneline -5 && cd ..

# Ejecutar un agente y guardar resultado
python .claude/agent-runner.py --execute sasha --prompt "Tu prompt" | tee output.txt

# Limpiar estado de agentes
rm -rf .claude/agent-state/*

# Reiniciar el servidor (mata y levanta)
pkill -f "uvicorn api.main"
py -m uvicorn api.main:app --reload
```

## Estructura de Carpetas

```
agencia/
├── api/
│   ├── main.py                  # FastAPI app
│   ├── config.py                # Settings (pydantic)
│   ├── dependencies.py          # JWT dependency injection
│   └── security/
│       ├── jwt.py               # JWTHandler
│       └── permissions.py       # PermissionChecker
├── .claude/
│   ├── agent-runner.py          # Orquestador de agentes
│   ├── agent-state/             # Estado persistente (JSON)
│   ├── agent-logs/              # Logs de ejecución
│   ├── mcp-servers/
│   │   └── obsidian-bridge.py   # MCP server para vault
│   ├── launch.json              # Configuración de VS Code
│   └── agents.json              # Config de los 11 agentes
├── tests/
│   ├── test_security.py         # Tests de auth y permissions
│   └── test_parallelization.py  # Tests de paralelización
├── agencia-vault/               # Obsidian vault (Git sync)
│   ├── 01_Projects/
│   ├── 02_Areas/
│   ├── 03_Resources/
│   ├── 06_Metadata/
│   └── README.md
├── .env                         # Credenciales (NO VERSIONED)
├── .env.example                 # Template de .env
├── .gitignore                   # Excluye .env, logs, etc
├── requirements-api.txt         # Dependencias Python
├── CAPABILITIES.md              # Hardware + capacidades
├── README_LOCAL_SETUP.md        # Este archivo
└── IMPLEMENTATION_COMPLETE.md   # Validación final
```

## Próximos Pasos

1. ✅ Setup local completado
2. Ejecutar `pytest tests/ -v` para validar todo
3. Probar login: `curl -X POST "http://localhost:8000/auth/login?username=jarvis&password=agencia"`
4. Explorar endpoints con Postman o curl
5. Leer `CAPABILITIES.md` para entender límites de hardware
6. Abrir `agencia-vault/` en Obsidian para ver estructura

## Soporte

Si algo no funciona:
1. Verificar que `.env` existe y tiene CLAUDE_API_KEY válido
2. Ejecutar `python api/config.py` para validar settings
3. Verificar que `pip list` incluye fastapi, pydantic, pyjwt
4. Revisar sección "Troubleshooting" arriba
5. Leer logs: `.claude/agent-logs/api_audit.jsonl` (últimas líneas)

---

**Documento:** README_LOCAL_SETUP.md
**Válido para:** Windows 11 Pro + Python 3.10+
**Último actualizado:** 2026-04-06
**Mantenedor:** Jarvis (CEO)
