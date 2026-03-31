"""
Cliente de WhatsApp — Meta Cloud API.

Maneja el envio de mensajes via Graph API v21.0.
Endpoint: POST /{phone_number_id}/messages

Referencia:
https://developers.facebook.com/docs/whatsapp/cloud-api/reference/messages/
"""

import logging
from typing import Optional

import httpx

from config import Settings

logger = logging.getLogger("maper.whatsapp_client")

GRAPH_API_VERSION = "v21.0"
GRAPH_API_BASE = f"https://graph.facebook.com/{GRAPH_API_VERSION}"


async def send_text_message(
    to: str,
    text: str,
    settings: Settings,
) -> bool:
    """
    Envia un mensaje de texto via WhatsApp Cloud API.

    Args:
        to: Numero de telefono del destinatario (formato internacional, ej: 573107735189).
        text: Texto del mensaje.
        settings: Configuracion de la app.

    Returns:
        True si el mensaje se envio con exito, False si fallo.
    """
    url = f"{GRAPH_API_BASE}/{settings.whatsapp_phone_number_id}/messages"

    headers = {
        "Authorization": f"Bearer {settings.whatsapp_api_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text": {"preview_url": False, "body": text},
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(url, headers=headers, json=payload)

            if response.status_code == 200:
                data = response.json()
                message_id = data.get("messages", [{}])[0].get("id", "unknown")
                logger.info(
                    "Mensaje enviado a %s (wa_msg_id: %s)",
                    _sanitize_phone(to),
                    message_id,
                )
                return True

            else:
                error_data = response.text
                logger.error(
                    "Error al enviar mensaje a %s — HTTP %d: %s",
                    _sanitize_phone(to),
                    response.status_code,
                    error_data,
                )
                return False

    except httpx.TimeoutException:
        logger.error("Timeout al enviar mensaje a %s", _sanitize_phone(to))
        return False

    except httpx.ConnectError:
        logger.error("Error de conexion al enviar mensaje a %s", _sanitize_phone(to))
        return False

    except Exception as e:
        logger.error("Error inesperado al enviar mensaje: %s", str(e), exc_info=True)
        return False


async def mark_message_read(
    message_id: str,
    settings: Settings,
) -> bool:
    """
    Marca un mensaje como leido (doble check azul).

    Buena practica para que el usuario sepa que el bot
    recibio su mensaje mientras Claude procesa la respuesta.
    """
    url = f"{GRAPH_API_BASE}/{settings.whatsapp_phone_number_id}/messages"

    headers = {
        "Authorization": f"Bearer {settings.whatsapp_api_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": message_id,
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                return True
            logger.warning(
                "No se pudo marcar mensaje como leido: HTTP %d",
                response.status_code,
            )
            return False
    except Exception as e:
        logger.warning("Error al marcar mensaje como leido: %s", str(e))
        return False


def _sanitize_phone(phone: str) -> str:
    """Anonimiza numero de telefono para logs."""
    if len(phone) > 4:
        return f"***{phone[-4:]}"
    return "****"
