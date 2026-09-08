"""
ASTECIA WhatsApp Integration
============================
Agent comercial exclusivo de Juan Camilo Gil integrado con WhatsApp Business API.

Recibe mensajes de WhatsApp → invoca ASTECIA → responde via WhatsApp
Corre 24/7 en Railway sin que Juan Camilo tenga máquina encendida.
"""

import os
import json
import logging
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
import httpx
from anthropic import Anthropic

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Variables de entorno (configuradas en Railway)
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE = os.getenv("WHATSAPP_PHONE")  # Ej: "573222340376"
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "astecia_secret_2026")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Validar credenciales críticas
if not WHATSAPP_TOKEN:
    logger.error("WHATSAPP_TOKEN no configurado en Railway")
if not ANTHROPIC_API_KEY:
    logger.error("ANTHROPIC_API_KEY no configurado en Railway")

# URLs
WHATSAPP_API_URL = "https://graph.instagram.com/v18.0"
PHONE_ID = os.getenv("WHATSAPP_PHONE_ID", "")  # Configurar en Railway si aplica

# Cliente Anthropic
client = Anthropic()

# Contexto base de ASTECIA
ASTECIA_SYSTEM_PROMPT = """Eres ASTECIA, el asistente comercial estratégico de Juan Camilo Gil de MAPER S.A.

Combinas:
- LEO: vendedor que cierra deals con argumentos basados en valor
- YANG: investigadora que entiende el contexto de cada cliente
- JARVIS: estratega que piensa en ROI y portfolio

## Tu Rol
Responde preguntas comerciales de Juan Camilo en tiempo real:
- Análisis de oportunidades
- Investigación de empresas y decision makers
- Argumentarios de venta personalizados
- Estructuración de propuestas
- Manejo de objeciones
- Priorización del portfolio

## Reglas
1. Respuestas en ESPAÑOL únicamente
2. Máximo 200 palabras (WhatsApp-friendly)
3. Accionable hoy, no teoría
4. Sincero: di si algo no va a cerrar
5. Si necesitas más contexto, pregunta
6. Confidencial: todo entre tú y Juan Camilo

## Contexto MAPER S.A.
- Distribuidor exclusivo Videojet en Suroccidente Colombia (Valle, Cauca, Nariño)
- Equipos: CIJ, TTO, Laser, LCM, LPA
- Principales clientes: Cargill, Omnilife, Colombina, Tecnosur, Papeles del Cauca, Kimberly Clark

## Portfolio Actual (13-Abr-2026)
CRÍTICOS:
- POT 28546 (Cargill, 40M, negociación)
- POT 26108 (Omnilife, 52.2M, demo)
- POT 25641 (Colombina, 80M, cierre esperado)
- POT 27985 (Colombina, 126M, multi-equipo)
- KC-S2O (Kimberly Clark, 44eq, post-venta)

TIER 1 (80% feeling):
- Papeles del Cauca (168M, licitación)
- Belleza Express (48M+56M)
- O Tafur (180M, avícola)
- Tecnosur (36M, guerra competitiva)

Responde como lo haría Leo (vendedor), Yang (investigadora), o Jarvis (estratega) según la pregunta.
"""

# =============================================================================
# ASTECIA AGENT
# =============================================================================

class ASTECIAAgent:
    """Agente ASTECIA integrado con Claude API."""

    def __init__(self):
        self.model = "claude-haiku-4-5-20251001"  # Haiku para respuestas rápidas
        self.conversation_history = {}  # {phone_number: [messages]}

    def get_conversation_history(self, phone_number: str):
        """Obtiene el historial de conversación del usuario."""
        if phone_number not in self.conversation_history:
            self.conversation_history[phone_number] = []
        return self.conversation_history[phone_number]

    def add_to_history(self, phone_number: str, role: str, content: str):
        """Añade un mensaje al historial."""
        self.get_conversation_history(phone_number).append({
            "role": role,
            "content": content
        })
        # Mantener solo últimos 20 mensajes para no sobrecargar contexto
        if len(self.conversation_history[phone_number]) > 20:
            self.conversation_history[phone_number] = self.conversation_history[phone_number][-20:]

    def process_message(self, phone_number: str, user_message: str) -> str:
        """
        Procesa un mensaje de WhatsApp e invoca ASTECIA.

        Args:
            phone_number: Número de WhatsApp del usuario
            user_message: Contenido del mensaje

        Returns:
            Respuesta de ASTECIA
        """
        try:
            # Añadir mensaje del usuario al historial
            self.add_to_history(phone_number, "user", user_message)

            # Log
            logger.info(f"Mensaje de {phone_number}: {user_message[:50]}...")

            # Invocar Claude Haiku con ASTECIA prompt
            response = client.messages.create(
                model=self.model,
                max_tokens=500,  # Suficiente para WhatsApp
                system=ASTECIA_SYSTEM_PROMPT,
                messages=self.get_conversation_history(phone_number)
            )

            # Extraer respuesta
            astecia_response = response.content[0].text

            # Añadir respuesta al historial
            self.add_to_history(phone_number, "assistant", astecia_response)

            logger.info(f"Respuesta ASTECIA: {astecia_response[:50]}...")

            return astecia_response

        except Exception as e:
            logger.error(f"Error procesando mensaje de {phone_number}: {str(e)}")
            return "Disculpa, hubo un error procesando tu solicitud. Intenta de nuevo."


# Instancia global
astecia = ASTECIAAgent()

# =============================================================================
# FASTAPI APP
# =============================================================================

app = FastAPI(
    title="ASTECIA WhatsApp",
    description="Agente comercial de Juan Camilo Gil vía WhatsApp Business API",
    version="1.0.0"
)

# =============================================================================
# WEBHOOKS
# =============================================================================

@app.get("/webhook")
async def webhook_verify(request: Request):
    """
    Verifica el webhook con Meta WhatsApp Business API.

    Meta envía:
    - hub.mode = "subscribe"
    - hub.challenge = token
    - hub.verify_token = verify_token configurado
    """
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == WHATSAPP_VERIFY_TOKEN:
        logger.info("Webhook verificado correctamente")
        return PlainTextResponse(challenge)
    else:
        logger.warning(f"Webhook verification falló: mode={mode}, token={token}")
        raise HTTPException(status_code=403, detail="Forbidden")


@app.post("/webhook")
async def webhook_messages(request: Request):
    """
    Recibe mensajes de WhatsApp Business API.

    Estructura esperada:
    {
        "object": "whatsapp_business_account",
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": "573222340376",
                        "text": {"body": "Tu mensaje aquí"},
                        "type": "text"
                    }]
                }
            }]
        }]
    }
    """
    try:
        data = await request.json()
        logger.info(f"Webhook recibido: {json.dumps(data, indent=2)}")

        # Validar estructura
        if data.get("object") != "whatsapp_business_account":
            return {"status": "ok"}

        # Procesar cambios
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})

                # Procesar mensajes
                for message in value.get("messages", []):
                    await process_incoming_message(message)

                # Procesar cambios de status (entregas, vistas)
                for status in value.get("statuses", []):
                    logger.info(f"Status update: {status}")

        return {"status": "ok"}

    except Exception as e:
        logger.error(f"Error procesando webhook: {str(e)}", exc_info=True)
        return {"status": "error", "message": str(e)}


# =============================================================================
# PROCESAMIENTO DE MENSAJES
# =============================================================================

async def process_incoming_message(message: dict):
    """Procesa un mensaje entrante de WhatsApp."""
    try:
        phone_number = message.get("from")
        message_type = message.get("type")

        if not phone_number:
            logger.warning("Mensaje sin número de teléfono")
            return

        # Solo procesar mensajes de texto por ahora
        if message_type != "text":
            logger.info(f"Tipo de mensaje no soportado: {message_type}")
            await send_whatsapp_message(
                phone_number,
                "Por ahora solo puedo procesar mensajes de texto. Escribe tu pregunta!"
            )
            return

        # Extraer texto
        text_body = message.get("text", {}).get("body", "").strip()
        if not text_body:
            logger.warning("Mensaje de texto vacío")
            return

        logger.info(f"Mensaje de {phone_number}: {text_body}")

        # Procesar con ASTECIA
        response = astecia.process_message(phone_number, text_body)

        # Enviar respuesta
        await send_whatsapp_message(phone_number, response)

    except Exception as e:
        logger.error(f"Error procesando mensaje: {str(e)}", exc_info=True)


async def send_whatsapp_message(phone_number: str, message_text: str):
    """
    Envía un mensaje via WhatsApp Business API.

    Args:
        phone_number: Número destino (ej: "573222340376")
        message_text: Contenido del mensaje
    """
    try:
        if not WHATSAPP_TOKEN or not PHONE_ID:
            logger.warning("WHATSAPP_TOKEN o PHONE_ID no configurados, no se puede enviar")
            return

        # Preparar payload
        payload = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "text",
            "text": {
                "body": message_text
            }
        }

        # URL del endpoint
        url = f"{WHATSAPP_API_URL}/{PHONE_ID}/messages"

        # Enviar
        async with httpx.AsyncClient() as client_http:
            response = await client_http.post(
                url,
                json=payload,
                headers={
                    "Authorization": f"Bearer {WHATSAPP_TOKEN}",
                    "Content-Type": "application/json"
                }
            )

            if response.status_code == 200:
                result = response.json()
                logger.info(f"Mensaje enviado a {phone_number}: {result.get('messages', [{}])[0].get('id')}")
            else:
                logger.error(f"Error enviando mensaje: {response.status_code} - {response.text}")

    except Exception as e:
        logger.error(f"Error en send_whatsapp_message: {str(e)}", exc_info=True)


# =============================================================================
# HEALTH CHECKS
# =============================================================================

@app.get("/health")
async def health_check():
    """Health check para Railway."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "astecia": "online",
        "whatsapp": "connected" if WHATSAPP_TOKEN else "disconnected"
    }


@app.get("/")
async def root():
    """Root endpoint con info del servicio."""
    return {
        "service": "ASTECIA WhatsApp",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "webhook": "/webhook"
        }
    }


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))

    logger.info(f"ASTECIA WhatsApp iniciando en puerto {port}...")
    logger.info(f"WhatsApp Token: {'configurado' if WHATSAPP_TOKEN else 'NO configurado'}")
    logger.info(f"Anthropic API Key: {'configurado' if ANTHROPIC_API_KEY else 'NO configurado'}")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
