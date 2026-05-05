#!/usr/bin/env node

/**
 * ASTECIA WhatsApp Web Integration
 * Asistente Estratégico Comercial en WhatsApp
 *
 * Usa: Baileys (WhatsApp Web emulation) + Claude API + Node.js
 *
 * Ejecución: npm start (requiere Node.js 18+)
 */

import dotenv from 'dotenv';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import qrcode from 'qrcode-terminal';
import { default as makeWASocket, useMultiFileAuthState, DisconnectReason } from '@whiskeysockets/baileys';
import { Anthropic } from '@anthropic-ai/sdk';
import { ASTECIA_SYSTEM_PROMPT } from './utils/astecia-prompt.js';

// Setup environment
dotenv.config();
const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Constants
const SESSIONS_DIR = path.join(__dirname, 'sessions');
const SESSION_NAME = process.env.WHATSAPP_SESSION_NAME || 'astecia-session';
const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;

// Validate API key
if (!ANTHROPIC_API_KEY) {
  console.error('❌ Error: ANTHROPIC_API_KEY no configurada en .env');
  console.error('Copia .env.example a .env y agrega tu API key de Anthropic');
  process.exit(1);
}

// Initialize Anthropic client
const anthropic = new Anthropic({
  apiKey: ANTHROPIC_API_KEY,
});

// Message queue to prevent rate limiting
const messageQueue = [];
let isProcessingMessage = false;

/**
 * Send message to Claude (ASTECIA)
 */
async function getAsteciaResponse(userMessage) {
  try {
    console.log(`🤖 ASTECIA procesando: "${userMessage}"`);

    const message = await anthropic.messages.create({
      model: process.env.ASTECIA_MODEL || 'claude-haiku-4-5-20251001',
      max_tokens: parseInt(process.env.ASTECIA_MAX_TOKENS || '1024'),
      system: ASTECIA_SYSTEM_PROMPT,
      messages: [
        {
          role: 'user',
          content: userMessage,
        },
      ],
    });

    const response = message.content[0].type === 'text' ? message.content[0].text : '';
    console.log(`✅ ASTECIA responde: "${response}"`);

    return response;
  } catch (error) {
    console.error('❌ Error llamando a Claude API:', error.message);
    return '❌ Error procesando tu solicitud. Intenta de nuevo.';
  }
}

/**
 * Process message queue (prevents rate limiting)
 */
async function processMessageQueue(sock) {
  if (isProcessingMessage || messageQueue.length === 0) return;

  isProcessingMessage = true;
  const { from, text, messageId } = messageQueue.shift();

  try {
    // Get response from ASTECIA
    const response = await getAsteciaResponse(text);

    // Send response back
    await sock.sendMessage(from, { text: response }, { quoted: { key: { id: messageId } } });
    console.log(`✉️  Mensaje enviado a ${from}`);
  } catch (error) {
    console.error('❌ Error enviando mensaje:', error.message);
  } finally {
    isProcessingMessage = false;
    // Process next message in queue
    if (messageQueue.length > 0) {
      setTimeout(() => processMessageQueue(sock), 1000);
    }
  }
}

/**
 * Check if message mentions ASTECIA
 */
function mentionsAstecia(text) {
  // Match: @astecia, astecia, ASTECIA, Astecia (case insensitive)
  const asteciaPattern = /(@?astecia\b)/i;
  return asteciaPattern.test(text);
}

/**
 * Extract message content (remove ASTECIA mention)
 */
function extractMessageContent(text) {
  // Remove @astecia or astecia from the beginning/mention
  return text.replace(/^@?astecia\s*/i, '').trim();
}

/**
 * Handle incoming messages
 */
async function handleMessage(message, sock) {
  // Ignore group messages for now
  if (message.key.remoteJid.includes('@g.us')) {
    console.log('⏭️  Ignorando mensaje de grupo');
    return;
  }

  // Only process text messages
  if (!message.message?.conversation && !message.message?.extendedTextMessage) {
    return;
  }

  const fullText = message.message?.conversation || message.message?.extendedTextMessage?.text || '';
  const from = message.key.remoteJid;
  const messageId = message.key.id;

  if (!fullText.trim()) return;

  console.log(`📨 Mensaje recibido de ${from}: "${fullText}"`);

  // Check if message mentions ASTECIA
  if (!mentionsAstecia(fullText)) {
    console.log('⏭️  Mensaje ignorado (no menciona ASTECIA)');
    return;
  }

  // Extract actual message content (remove ASTECIA mention)
  const messageContent = extractMessageContent(fullText);

  // If empty after removing mention, ask for clarification
  if (!messageContent) {
    const response = '👋 Hola, soy ASTECIA. ¿Qué necesitas? Cuéntame tu duda comercial.';
    messageQueue.push({ from, text: response, messageId, isResponse: true });
    processMessageQueue(sock);
    return;
  }

  console.log(`✅ ASTECIA activado: "${messageContent}"`);

  // Add to queue
  messageQueue.push({ from, text: messageContent, messageId });

  // Process queue
  processMessageQueue(sock);
}

/**
 * Initialize WhatsApp connection
 */
async function startWhatsApp() {
  console.log('🚀 Iniciando ASTECIA WhatsApp...\n');

  // Create sessions directory
  if (!fs.existsSync(SESSIONS_DIR)) {
    fs.mkdirSync(SESSIONS_DIR, { recursive: true });
  }

  const { state, saveCreds } = await useMultiFileAuthState(
    path.join(SESSIONS_DIR, SESSION_NAME)
  );

  const sock = makeWASocket({
    auth: state,
    printQRInTerminal: true,
    browser: ['ASTECIA', 'Safari', '1.0.0'],
    syncFullHistory: false,
  });

  // Handle credentials
  sock.ev.on('creds.update', saveCreds);

  // Handle connection updates
  sock.ev.on('connection.update', async (update) => {
    const { connection, lastDisconnect, qr } = update;

    if (qr) {
      console.log('\n📱 Escanea el QR con tu WhatsApp:\n');
      qrcode.generate(qr, { small: true });
    }

    if (connection === 'open') {
      console.log('\n✅ ASTECIA está activo en WhatsApp Web');
      console.log('📲 Escuchando mensajes...\n');
      console.log('💡 Tip: Envía un mensaje a cualquier contacto que inicie ASTECIA');
      console.log('Para detener: Presiona Ctrl+C\n');
    }

    if (connection === 'close') {
      if (lastDisconnect?.error?.output?.statusCode === DisconnectReason.LoggedOut) {
        console.log('\n⚠️  Sesión cerrada. Escanea el QR de nuevo.');
        process.exit(0);
      }
    }
  });

  // Handle incoming messages
  sock.ev.on('messages.upsert', async (m) => {
    for (const message of m.messages) {
      // Only process if message is not from us
      if (!message.key.fromMe) {
        await handleMessage(message, sock);
      }
    }
  });

  // Keep process running
  process.on('SIGINT', () => {
    console.log('\n\n👋 ASTECIA desconectado.');
    process.exit(0);
  });
}

// Start the bot
startWhatsApp().catch(console.error);
