/**
 * ASTECIA Integration Server v1.0
 * Cerebro comercial personal de Juan Camilo Gil
 *
 * Features:
 * - Gmail, Calendar, Drive, Tasks APIs
 * - Firecrawl + Google Custom Search web access
 * - WhatsApp Web integration
 * - Security hardened (OWASP 2025 compliance)
 * - Rate limiting, input validation, error sanitization
 */

const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const { Anthropic } = require('@anthropic-ai/sdk');

require('dotenv').config();

const app = express();

// ============================================
// SECURITY MIDDLEWARE
// ============================================

// Helmet: Add security headers
app.use(helmet());

// CORS: Restrict origins
const allowedOrigins = (process.env.ALLOWED_ORIGINS || 'http://localhost:3000').split(',');
app.use(cors({
  origin: allowedOrigins,
  credentials: true,
  methods: ['GET', 'POST'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

// Body parser with size limit
app.use(express.json({ limit: '1mb' }));

// Rate limiting: 100 requests per 15 minutes per IP
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  message: 'Too many requests from this IP, please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
});
app.use(limiter);

// ============================================
// ENVIRONMENT VALIDATION
// ============================================

const requiredEnvVars = [
  'CLAUDE_API_KEY',
  'GOOGLE_CLIENT_ID',
  'GOOGLE_CLIENT_SECRET',
];

for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    console.error(`❌ Missing required environment variable: ${envVar}`);
    process.exit(1);
  }
}

const client = new Anthropic();

// TODO: Importar tools cuando estén listos
// const { createGmailTool } = require('./agents/tools/gmail');
// const { createCalendarTool } = require('./agents/tools/calendar');
// const { createDriveTool } = require('./agents/tools/drive');
// const { createTasksTool } = require('./agents/tools/tasks');
// const { createWhatsAppTool } = require('./agents/tools/whatsapp');
// const { createLocalFilesTool } = require('./agents/tools/localFiles');

/**
 * Placeholder tools array
 * Se populará en Sprint 1-3
 */
const tools = [
  // Tools irán aquí
];

// ============================================
// INPUT VALIDATION
// ============================================

const MAX_MESSAGE_LENGTH = 10000;

function validateMessage(message) {
  if (!message || typeof message !== 'string') {
    return { valid: false, error: 'Message must be a non-empty string' };
  }

  if (message.length > MAX_MESSAGE_LENGTH) {
    return { valid: false, error: `Message exceeds maximum length of ${MAX_MESSAGE_LENGTH}` };
  }

  return { valid: true };
}

// ============================================
// ASTECIA AGENT
// ============================================

/**
 * ASTECIA Agent - Cerebro comercial
 */
async function astecia(userMessage, conversationHistory = []) {
  try {
    const messages = [
      ...conversationHistory,
      {
        role: 'user',
        content: userMessage,
      },
    ];

    const response = await client.messages.create({
      model: process.env.CLAUDE_MODEL || 'claude-sonnet-4-6-20250514',
      max_tokens: 2048,
      system: `Eres ASTECIA, el cerebro comercial personal de Juan Camilo Gil.

Tu misión: Automatizar la gestión de email, calendario, tareas, documentos y búsqueda web.

Personalidad:
- Directo, sin fluff
- Bilingüe (español/inglés)
- Tono profesional pero amigable
- Proactivo en sugerencias

Datos disponibles:
- Gmail: emails, búsqueda, respuestas
- Google Calendar: eventos, disponibilidad, reuniones
- Google Drive: documentos, cotizaciones, templates
- Google Tasks: notas, TODOs
- WhatsApp Web: mensajes, conversaciones
- Archivos locales: formatos, catálogos, políticas

Capacidades:
1. Leer email → resumir → proponer respuesta
2. Ver calendario → sugerir mejores horarios
3. Buscar documentos → extraer datos
4. Responder WhatsApp automáticamente
5. Crear tareas y recordatorios
6. Acceder a archivos locales → cotizaciones, formatos

IMPORTANTE:
- Si los tools no están disponibles, comunica que estamos en setup
- Mantén contexto de la conversación
- Sé honesto sobre limitaciones
- Confirma antes de acciones críticas`,
      messages: messages,
      tools: tools.length > 0 ? tools : undefined,
    });

    let textResponse = '';
    if (response.content[0].type === 'text') {
      textResponse = response.content[0].text;
    }

    return {
      response: textResponse,
      stop_reason: response.stop_reason,
      usage: {
        input_tokens: response.usage.input_tokens,
        output_tokens: response.usage.output_tokens,
      },
    };
  } catch (error) {
    console.error('Error en ASTECIA:', error.message);
    throw error;
  }
}

// ============================================
// ROUTES
// ============================================

/**
 * POST /astecia - Interfaz principal
 */
app.post('/astecia', async (req, res) => {
  try {
    const { message, history = [] } = req.body;

    const validation = validateMessage(message);
    if (!validation.valid) {
      return res.status(400).json({ error: validation.error });
    }

    const result = await astecia(message, history);
    res.json(result);
  } catch (error) {
    console.error('Error in /astecia route:', error.message);
    res.status(500).json({
      error: 'Internal Server Error',
      ...(process.env.NODE_ENV !== 'production' && { debug: error.message })
    });
  }
});

/**
 * GET /health - Health check
 */
app.get('/health', async (req, res) => {
  try {
    const isClaudeHealthy = process.env.CLAUDE_API_KEY ? true : false;

    res.json({
      status: isClaudeHealthy ? 'healthy' : 'degraded',
      service: 'ASTECIA Integration Server',
      timestamp: new Date().toISOString(),
      tools_configured: tools.length,
      claude_api: isClaudeHealthy ? 'ok' : 'not_configured',
      environment: process.env.NODE_ENV || 'development',
    });
  } catch (error) {
    console.error('Health check error:', error.message);
    res.status(503).json({ status: 'unhealthy', error: 'Health check failed' });
  }
});

/**
 * GET / - Info endpoint
 */
app.get('/', (req, res) => {
  res.json({
    service: 'ASTECIA - Cerebro Comercial Personal',
    version: '1.0.0-alpha',
    owner: 'Juan Camilo Gil',
    status: 'in_development',
    endpoints: {
      health: 'GET /health',
      astecia: 'POST /astecia (body: { message, history? })',
    },
    tools_status: {
      gmail: 'TODO (Sprint 1)',
      calendar: 'TODO (Sprint 1)',
      drive: 'TODO (Sprint 1)',
      tasks: 'TODO (Sprint 1)',
      whatsapp: 'TODO (Sprint 2)',
      localFiles: 'TODO (Sprint 2)',
    },
    timeline: {
      'April 17': 'Setup repo + security',
      'April 18': 'Gmail, Calendar, Drive, Tasks',
      'April 19': 'WhatsApp, Local Files',
      'April 20': 'Deploy to production',
      'April 25': 'Go-live',
    },
  });
});

// ============================================
// ERROR HANDLER
// ============================================

app.use((err, req, res, next) => {
  if (process.env.NODE_ENV !== 'production') {
    console.error('Unhandled error:', err);
  }

  res.status(500).json({
    error: 'Internal Server Error',
    ...(process.env.NODE_ENV !== 'production' && { message: err.message })
  });
});

/**
 * 404 HANDLER
 */
app.use((req, res) => {
  res.status(404).json({
    error: 'Not Found',
    path: req.path,
    method: req.method,
    hint: 'Available endpoints: GET /, GET /health, POST /astecia'
  });
});

// ============================================
// START SERVER
// ============================================

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`
╔══════════════════════════════════════════════════════════╗
║  🚀 ASTECIA Integration Server v1.0                      ║
║  Cerebro Comercial Personal de Juan Camilo Gil          ║
║══════════════════════════════════════════════════════════║
║  ✓ Server running on http://localhost:${PORT}
║  ✓ Security: Helmet + CORS + Rate Limiting              ║
║  ✓ Tools: Ready for integration (Sprint 1)              ║
║  ✓ Status: Development Mode                             ║
║  ✓ Environment: ${process.env.NODE_ENV || 'development'}
╚══════════════════════════════════════════════════════════╝
  `);
});

module.exports = { app, astecia };
