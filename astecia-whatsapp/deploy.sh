#!/bin/bash
# Deploy ASTECIA WhatsApp a Railway
# Uso: ./deploy.sh

set -e

echo "================================"
echo "ASTECIA WhatsApp — Deploy Script"
echo "================================"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "main.py" ]; then
    echo "ERROR: main.py no encontrado. Ejecuta desde astecia-whatsapp/"
    exit 1
fi

# Verificar Railway CLI
if ! command -v railway &> /dev/null; then
    echo "ERROR: Railway CLI no instalado"
    echo "Instala con: npm install -g @railway/cli"
    exit 1
fi

# Verificar Git
if ! command -v git &> /dev/null; then
    echo "ERROR: Git no instalado"
    exit 1
fi

echo "✓ Railway CLI encontrado"
echo "✓ Git encontrado"
echo ""

# Paso 1: Commit y push a GitHub
echo "Paso 1: Commit y push a GitHub..."
git add .
git commit -m "feat: ASTECIA WhatsApp integration" || echo "Sin cambios nuevos"
git push origin main || echo "Fallo al hacer push (puede estar ya actualizado)"
echo "✓ Código actualizado en GitHub"
echo ""

# Paso 2: Verificar Railway login
echo "Paso 2: Verificar Railway login..."
railway whoami || {
    echo "No estás logged en Railway. Ejecutando login..."
    railway login
}
echo "✓ Railway login verificado"
echo ""

# Paso 3: Verificar proyecto Railway
echo "Paso 3: Verificar proyecto Railway..."
railway init --force || true
echo "✓ Proyecto Railway inicializado"
echo ""

# Paso 4: Deploy
echo "Paso 4: Desplegando a Railway..."
echo "Esto puede tomar 2-3 minutos..."
echo ""
railway up --detach

echo ""
echo "================================"
echo "✓ Deploy iniciado!"
echo "================================"
echo ""
echo "Próximos pasos:"
echo "1. Espera 2-3 minutos a que Railway compile e implemente"
echo "2. Obtén la URL:"
echo "   railway logs"
echo "3. Busca 'Application running on:' para ver tu URL"
echo "4. En Meta Dashboard → WhatsApp → Callback URL"
echo "   Pega: https://[tu-url]/webhook"
echo ""
echo "Para monitorear logs:"
echo "   railway logs -f"
echo ""
