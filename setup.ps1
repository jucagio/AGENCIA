# Setup FASE 1 Simplificada — FastAPI + Obsidian Vault
# Windows PowerShell script

Write-Host "🔧 Setup FASE 1 Simplificada — Infraestructura de Agentes Locales" -ForegroundColor Green

# 1. Verificar prerrequisitos
Write-Host "`n📋 Verificando prerrequisitos..."
$checks = @(
    @{ cmd = "python --version"; desc = "Python 3.12+" },
    @{ cmd = "git --version"; desc = "Git" },
    @{ cmd = "pip --version"; desc = "pip" }
)

foreach ($check in $checks) {
    try {
        $result = Invoke-Expression $check.cmd 2>&1
        Write-Host "✅ $($check.desc): $($result | Select-Object -First 1)" -ForegroundColor Green
    } catch {
        Write-Host "❌ $($check.desc) NO encontrado" -ForegroundColor Red
        exit 1
    }
}

# 2. Crear .env si no existe
Write-Host "`n📝 Configurando .env..."
if (!(Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "⚠️  Archivo .env creado. Edítalo con tus credenciales:" -ForegroundColor Yellow
    Write-Host "   - CLAUDE_API_KEY=sk-ant-..."
    Write-Host "   - JWT_SECRET=tu_secreto_aqui"
} else {
    Write-Host "✅ .env ya existe" -ForegroundColor Green
}

# 3. Crear directorios necesarios
Write-Host "`n📂 Creando directorios..."
$dirs = @(
    ".claude/agent-state",
    ".claude/agent-logs",
    "api/models",
    "api/routes",
    "api/security",
    "tests"
)

foreach ($dir in $dirs) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✅ Directorio creado: $dir" -ForegroundColor Green
    }
}

# 4. Instalar dependencias Python
Write-Host "`n📦 Instalando dependencias Python..."
pip install -r requirements-api.txt

# 5. Crear .gitkeep en directorios
Write-Host "`n🔐 Creando .gitkeep..."
@(".claude/agent-state/.gitkeep", ".claude/agent-logs/.gitkeep") | ForEach-Object {
    if (!(Test-Path $_)) {
        New-Item -Path $_ -ItemType File -Force | Out-Null
    }
}

Write-Host "`n✅ Setup COMPLETO" -ForegroundColor Green
Write-Host "`n📚 Próximos pasos:" -ForegroundColor Cyan
Write-Host "   1. Edita .env con tus credenciales (CLAUDE_API_KEY, JWT_SECRET)"
Write-Host "   2. Ejecuta: python -m uvicorn api.main:app --reload --port 8000"
Write-Host "   3. Accede a: http://localhost:8000/docs (Swagger UI)"
Write-Host "   4. Agentes en FASE 2"
