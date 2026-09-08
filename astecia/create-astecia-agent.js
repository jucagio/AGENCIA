#!/usr/bin/env node

import fs from 'fs';

// Leer API Key del .env
const envPath = './whatsapp-astecia/.env';
let API_KEY = null;

try {
  const envContent = fs.readFileSync(envPath, 'utf-8');
  const match = envContent.match(/ANTHROPIC_API_KEY=(.+)/);
  if (match) {
    API_KEY = match[1].trim().replace(/^['"]|['"]$/g, '');
  }
} catch (e) {
  console.error('❌ No se pudo leer el archivo .env');
  console.error('Asegúrate de tener configurado whatsapp-astecia/.env con tu API Key');
  process.exit(1);
}

if (!API_KEY) {
  console.error('❌ ANTHROPIC_API_KEY no encontrada en .env');
  process.exit(1);
}

const API_BASE = 'https://api.anthropic.com/v1';

const ASTECIA_CONFIG = {
  name: 'ASTECIA',
  description: 'Asistente Estratégico Comercial de Juan Camilo Gil. Especialista en ventas B2B industriales (CIJ, TIJ, Laser). Domina PNL, AIDA, SPIN Selling, Modelo DISC.',
  model: 'claude-opus-4-6',
  system_prompt: `Eres ASTECIA, el cerebro comercial personal de Juan Camilo Gil.

IDENTIDAD:
- LEO (vendedor élite), YANG (investigadora), JARVIS (estratega)
- Especialista en ventas B2B industriales (CIJ, TIJ, Laser, Inspección, Automatización)
- Distribuidor exclusivo Videojet en Suroccidente Colombia

METODOLOGÍAS:
- PNL: lenguaje persuasivo, metáforas, reencuadre
- AIDA: Atención → Interés → Deseo → Acción
- SPIN Selling: Situación → Problema → Implicación → Necesidad
- Modelo DISC: adaptas discurso por perfil (D, I, S, C)

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

Estoy listo. ¿Cuál es tu pregunta comercial?`
};

async function createAgent() {
  console.log('\n🚀 Creando ASTECIA en la Consola Claude...\n');

  try {
    const response = await fetch(`${API_BASE}/agents`, {
      method: 'POST',
      headers: {
        'x-api-key': API_KEY,
        'content-type': 'application/json'
      },
      body: JSON.stringify(ASTECIA_CONFIG)
    });

    const data = await response.json();

    if (!response.ok) {
      console.error('❌ Error creando agente:', data);
      process.exit(1);
    }

    console.log('✅ ¡ASTECIA creado exitosamente!\n');
    console.log('📊 Información:');
    console.log(`   • ID: ${data.id}`);
    console.log(`   • Nombre: ${data.name}`);
    console.log(`   • Modelo: ${data.model}\n`);

    console.log('🔗 Accede aquí:');
    console.log(`   https://platform.claude.com/workspaces/default/agents/${data.id}\n`);

    console.log('💡 Próximos pasos:');
    console.log('   1. Abre el link arriba');
    console.log('   2. Prueba ASTECIA con una pregunta comercial');
    console.log('   3. ¡Disfruta!\n');

  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

createAgent();
