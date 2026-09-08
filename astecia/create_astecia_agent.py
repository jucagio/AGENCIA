#!/usr/bin/env python3
"""
Script para crear ASTECIA como agente en la Consola Claude
Usa la API de Anthropic
"""

import os
import json
import sys
from pathlib import Path

# Leer API Key del .env
env_path = Path('./whatsapp-astecia/.env')
api_key = None

if env_path.exists():
    with open(env_path, 'r') as f:
        for line in f:
            if line.startswith('ANTHROPIC_API_KEY='):
                api_key = line.split('=', 1)[1].strip().strip('"').strip("'")
                break

if not api_key:
    print('❌ ANTHROPIC_API_KEY no encontrada en whatsapp-astecia/.env')
    sys.exit(1)

# Configuración de ASTECIA
astecia_config = {
    'name': 'ASTECIA',
    'description': 'Asistente Estratégico Comercial de Juan Camilo Gil. Especialista en ventas B2B industriales (CIJ, TIJ, Laser). Domina PNL, AIDA, SPIN Selling, Modelo DISC.',
    'model': 'claude-opus-4-6',
    'instructions': '''Eres ASTECIA, el cerebro comercial personal de Juan Camilo Gil.

IDENTIDAD:
- LEO (vendedor élite), YANG (investigadora), JARVIS (estratega)
- Especialista en ventas B2B industriales (CIJ, TIJ, Laser, Inspección, Automatización)
- Distribuidor exclusivo Videojet en Suroccidente Colombia

METODOLOGÍAS:
- PNL: lenguaje persuasivo, metáforas, reencuadre
- AIDA: Atención → Interés → Deseo → Acción
- SPIN Selling: Situación → Problema → Implicación → Necesidad
- Modelo DISC: adaptas discurso por perfil (Dominante, Influyente, Estable, Concienzudo)

HABILIDADES:
✓ Analizar propuestas y evaluar viabilidad real
✓ Estructurar ofertas con margen y términos estratégicos
✓ Construir argumentarios persuasivos
✓ Identificar dolores y objeciones antes de que surjan
✓ Redactar emails persuasivos y guiones de llamada
✓ Manejo de objeciones basado en valor
✓ Priorización estratégica del portfolio

ESTILO:
- Natural, humano, estratégico (sin jargón)
- Rápido, sin demora, sin teoría, sin relleno
- Siempre accionable: propone siguiente paso concreto
- Sincero contigo
- Máximo 3 párrafos
- Primer párrafo = respuesta + decisión
- Lenguaje: español únicamente

CONTEXTO MAPER:
- Clientes: Cargill, Omnilife, Colombina, Kimberly Clark, Papeles del Cauca, Tecnosur
- Equipos: CIJ, TTO, Laser, LCM, LPA
- Territory: Suroccidente Colombia

Estoy listo. ¿Cuál es tu pregunta comercial?'''
}

print('\n🚀 Creando ASTECIA en la Consola Claude...\n')

try:
    import urllib.request
    import urllib.error

    url = 'https://api.anthropic.com/v1/agents'
    headers = {
        'x-api-key': api_key,
        'content-type': 'application/json',
    }

    data = json.dumps(astecia_config).encode('utf-8')

    req = urllib.request.Request(url, data=data, headers=headers, method='POST')

    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())

    print('✅ ¡ASTECIA creado exitosamente!\n')
    print('📊 Información:')
    print(f"   • ID: {result.get('id', 'N/A')}")
    print(f"   • Nombre: {result.get('name', 'N/A')}")
    print(f"   • Modelo: {result.get('model', 'N/A')}\n")

    agent_id = result.get('id')
    if agent_id:
        print('🔗 Accede aquí:')
        print(f'   https://platform.claude.com/workspaces/default/agents/{agent_id}\n')

    print('💡 Próximos pasos:')
    print('   1. Abre el link arriba')
    print('   2. Prueba ASTECIA con una pregunta comercial')
    print('   3. ¡Disfruta!\n')

except urllib.error.HTTPError as e:
    error_data = json.loads(e.read().decode())
    print(f'❌ Error: {error_data}')
    sys.exit(1)
except Exception as e:
    print(f'❌ Error: {str(e)}')
    sys.exit(1)
