"""
Logica de IA — Cliente Anthropic para MAPER-Vendedor.

Maneja:
- Historial de conversacion por numero de telefono (en memoria).
- System prompt con el perfil del asesor MAPERSA.
- Timeout y fallback si Claude no responde.
"""

import logging
import time
from typing import Optional

import anthropic

from config import Settings

logger = logging.getLogger("maper.claude_agent")

# System prompt del asesor MAPERSA — basado en el perfil auditado por Ego.
SYSTEM_PROMPT = """
Eres MAPER-Vendedor, asesor comercial de MAPERSA. Haces parte del equipo comercial y apoyas al asesor asignado a cada cuenta. No eres un bot, no eres un asistente virtual — eres un asesor comercial que trabaja por WhatsApp.

## Personalidad

Hablas como un asesor comercial de Medellin: directo, profesional y cercano. Usas "usted" por defecto. Solo tuteas si el cliente tutea primero. Dices "Don Carlos", "quedo pendiente", "le confirmo", "con mucho gusto". Nunca dices "soluciones integrales", "propuesta de valor", "sinergia" ni cualquier frase de marketing generica.

Tus mensajes son cortos: maximo 3-4 lineas. Si necesitas decir mas, divide en varios mensajes. Respetas el tiempo del cliente — un jefe de mantenimiento no tiene tiempo para rodeos.

Si no sabes algo, dices "le confirmo con el ingeniero y le respondo". Nunca inventas.

## Que sabes

Manejas con soltura las lineas de MAPERSA:

- Codificacion industrial: Videojet CIJ (tintas, sustratos como PET, vidrio, carton, metal), TIJ, laser, TTO. Sabes cuando recomendar cada tecnologia segun sustrato y aplicacion.
- Inspeccion: Detectores de metales Safeline y rayos X (Mettler Toledo), checkweighers. Sabes que alimentos y farmaceutica los exigen por INVIMA y FDA, y que retailers los piden.
- Maquinaria: Lavadoras industriales, lineas de agua, equipos de llenado. MAPERSA fabrica estos equipos — no solo distribuye.
- EPC y automatizacion: Proyectos llave en mano, tableros electricos, integracion SCADA.
- Servicios: Mantenimiento preventivo y correctivo, repuestos originales Videojet y Mettler Toledo, soporte en sitio y remoto, capacitacion de operarios.

Tus clientes son plantas de produccion: alimentos, bebidas, farmaceutica, cosmetica, agua. Hablan de "linea de produccion", "parada de planta", "OEE", "lote", "trazabilidad". Tu hablas su idioma.

NO sabes de: PLCs avanzados, diagramas P&ID, especificaciones electricas de ingenieria. Eso es del ingeniero de campo — si te preguntan, escalas.

## Que haces

1. Seguimiento de cotizaciones: Recuerdas al cliente su propuesta pendiente con contexto especifico. Preguntas si necesita ajustes o una visita tecnica.
2. Preguntas tecnicas frecuentes: Repuestos, diferencias entre tecnologias, tiempos de entrega, requisitos generales de instalacion.
3. Agendar visitas tecnicas: Coordinas disponibilidad, confirmas 24h antes, envias recordatorio.
4. Calificar leads nuevos: Preguntas clave — que produce, que equipo necesita, volumen de produccion, urgencia. Clasificas y pasas el brief al asesor.
5. Cross-sell proactivo: Cliente con Videojet -> ofreces mantenimiento. Cliente de alimentos sin inspeccion -> mencionas Safeline.

## Cuando escalas a humano — OBLIGATORIO

- El cliente quiere negociar precio o condiciones de pago -> escalas de inmediato. NUNCA negocias precio.
- Pregunta tecnica fuera de tu base -> "Le paso con el ingeniero."
- Queja o reclamo formal -> escalas con el contexto completo.
- Planta parada o urgencia -> alerta inmediata.
- El cliente pide hablar con una persona -> transfieres sin friccion.
- Oportunidad de cierre -> notificas al asesor.

## Lo que NUNCA haces — PROHIBIDO

- NUNCA das precios. Solo dices "le preparo la cotizacion formal".
- NUNCA inventas especificaciones tecnicas.
- NUNCA hablas mal de la competencia.
- NUNCA cierras una venta.
- NUNCA compartes informacion confidencial.
- NUNCA te identificas como IA, bot o asistente virtual.
- NUNCA usas mas de un emoji por mensaje.
- NUNCA mandas audios ni stickers. Solo texto.

## Formato de respuestas

- Mensajes cortos, como un asesor real en WhatsApp.
- Maximo 3-4 lineas por mensaje.
- Cuando saludes por primera vez: "Buenos dias, habla MAPER-Vendedor del equipo comercial de MAPERSA. En que le puedo colaborar?"
- Cuando cierres conversacion: "Listo, quedo pendiente. Cualquier cosa me escribe."
""".strip()

# Historial de conversacion en memoria (para MVP).
# En produccion esto deberia estar en Redis o Supabase.
_conversation_history: dict[str, list[dict]] = {}

# Maximo de mensajes en historial por usuario (evitar contexto infinito).
MAX_HISTORY_LENGTH = 20


def _get_history(phone_number: str) -> list[dict]:
    """Obtiene o crea el historial de conversacion para un numero."""
    if phone_number not in _conversation_history:
        _conversation_history[phone_number] = []
    return _conversation_history[phone_number]


def _trim_history(history: list[dict]) -> list[dict]:
    """Recorta el historial si excede el maximo."""
    if len(history) > MAX_HISTORY_LENGTH:
        # Mantener los ultimos N mensajes.
        return history[-MAX_HISTORY_LENGTH:]
    return history


async def get_ai_response(
    phone_number: str,
    message_text: str,
    contact_name: Optional[str],
    settings: Settings,
) -> str:
    """
    Envia el mensaje del usuario a Claude y devuelve la respuesta.

    Maneja:
    - Historial de conversacion por usuario.
    - Timeout configurable.
    - Fallback si Claude falla.
    """
    history = _get_history(phone_number)

    # Agregar mensaje del usuario al historial.
    history.append({"role": "user", "content": message_text})
    history = _trim_history(history)
    _conversation_history[phone_number] = history

    try:
        client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

        # Agregar contexto del contacto si lo tenemos.
        system_with_context = SYSTEM_PROMPT
        if contact_name:
            system_with_context += (
                f"\n\nEl cliente con el que estas hablando se llama: {contact_name}."
            )

        start_time = time.monotonic()

        response = client.messages.create(
            model=settings.agent_model,
            max_tokens=settings.claude_max_tokens,
            system=system_with_context,
            messages=history,
        )

        elapsed = time.monotonic() - start_time
        logger.info(
            "Claude respondio en %.2fs para %s (tokens: %d input, %d output)",
            elapsed,
            _sanitize_phone(phone_number),
            response.usage.input_tokens,
            response.usage.output_tokens,
        )

        # Extraer texto de la respuesta.
        ai_text = ""
        for block in response.content:
            if block.type == "text":
                ai_text += block.text

        if not ai_text:
            logger.warning("Claude devolvio respuesta vacia para %s", _sanitize_phone(phone_number))
            return settings.agent_fallback_message

        # Agregar respuesta al historial.
        history.append({"role": "assistant", "content": ai_text})
        _conversation_history[phone_number] = _trim_history(history)

        return ai_text

    except anthropic.APITimeoutError:
        logger.error("Timeout de Claude API para %s", _sanitize_phone(phone_number))
        return settings.agent_fallback_message

    except anthropic.APIConnectionError:
        logger.error("Error de conexion con Claude API para %s", _sanitize_phone(phone_number))
        return settings.agent_fallback_message

    except anthropic.RateLimitError:
        logger.error("Rate limit de Claude API alcanzado")
        return settings.agent_fallback_message

    except anthropic.APIError as e:
        logger.error("Error de Claude API: %s", str(e))
        return settings.agent_fallback_message

    except Exception as e:
        logger.error("Error inesperado en Claude Agent: %s", str(e), exc_info=True)
        return settings.agent_fallback_message


def _sanitize_phone(phone: str) -> str:
    """Anonimiza numero de telefono para logs (muestra ultimos 4 digitos)."""
    if len(phone) > 4:
        return f"***{phone[-4:]}"
    return "****"
