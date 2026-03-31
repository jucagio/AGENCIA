"""
MAPER WhatsApp AgentKit — FastAPI + Anthropic + Meta Cloud API.

Endpoints:
  GET  /webhook/whatsapp  — Verificacion del webhook (Meta envia challenge).
  POST /webhook/whatsapp  — Recepcion de mensajes entrantes.
  GET  /health            — Health check para Railway.

Seguridad:
  - Verificacion de firma X-Hub-Signature-256 en cada POST.
  - Rate limiting por IP y por numero de telefono.
  - Validacion de input en el borde del sistema.
  - Logs estructurados sin PII.
"""

import logging
import sys

from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, Request, Response, HTTPException, Query
from fastapi.responses import PlainTextResponse, JSONResponse

from config import load_settings, Settings
from security import verify_webhook_signature, RateLimiter, is_valid_phone_number
from claude_agent import get_ai_response
from whatsapp_client import send_text_message, mark_message_read

# ---------------------------------------------------------------------------
# Logging estructurado
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format='{"time":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","msg":"%(message)s"}',
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("maper.main")

# ---------------------------------------------------------------------------
# Startup / Shutdown
# ---------------------------------------------------------------------------

settings: Optional[Settings] = None
rate_limiter_ip: Optional[RateLimiter] = None
rate_limiter_phone: Optional[RateLimiter] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inicializa configuracion y rate limiters al arrancar."""
    global settings, rate_limiter_ip, rate_limiter_phone

    logger.info("Arrancando MAPER WhatsApp AgentKit...")

    try:
        settings = load_settings()
    except EnvironmentError as e:
        logger.critical("Error de configuracion: %s", str(e))
        sys.exit(1)

    rate_limiter_ip = RateLimiter(
        max_requests=settings.rate_limit_max_requests * 3,  # IPs tienen mas margen
        window_seconds=settings.rate_limit_window_seconds,
    )
    rate_limiter_phone = RateLimiter(
        max_requests=settings.rate_limit_max_requests,
        window_seconds=settings.rate_limit_window_seconds,
    )

    logger.info(
        "MAPER WhatsApp AgentKit listo — modelo: %s, rate_limit: %d req/%ds",
        settings.agent_model,
        settings.rate_limit_max_requests,
        settings.rate_limit_window_seconds,
    )

    yield

    logger.info("Apagando MAPER WhatsApp AgentKit...")


# ---------------------------------------------------------------------------
# App FastAPI
# ---------------------------------------------------------------------------

app = FastAPI(
    title="MAPER WhatsApp AgentKit",
    description="Agente de WhatsApp para MAPERSA — powered by Claude",
    version="1.0.0",
    docs_url=None,   # Deshabilitado en produccion (seguridad)
    redoc_url=None,   # Deshabilitado en produccion (seguridad)
    lifespan=lifespan,
)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/health")
async def health_check():
    """Health check para Railway y monitoreo."""
    return {"status": "ok", "agent": "MAPER-Vendedor", "version": "1.0.0"}


# ---------------------------------------------------------------------------
# Webhook GET — Verificacion de Meta
# ---------------------------------------------------------------------------

@app.get("/webhook/whatsapp")
async def verify_webhook(
    request: Request,
):
    """
    Meta envia un GET con hub.mode, hub.verify_token y hub.challenge.
    Si el verify_token coincide, respondemos con el challenge (int).
    """
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == settings.webhook_verify_token:
        logger.info("Webhook verificado exitosamente por Meta")
        return PlainTextResponse(content=challenge, status_code=200)

    logger.warning(
        "Intento de verificacion de webhook fallido — mode=%s, token_match=%s",
        mode,
        token == settings.webhook_verify_token if token else "no_token",
    )
    raise HTTPException(status_code=403, detail="Verification failed")


# ---------------------------------------------------------------------------
# Webhook POST — Mensajes entrantes
# ---------------------------------------------------------------------------

@app.post("/webhook/whatsapp")
async def receive_message(request: Request):
    """
    Recibe mensajes de WhatsApp via Meta Cloud API.

    Flujo:
    1. Verificar firma X-Hub-Signature-256.
    2. Rate limit por IP.
    3. Parsear payload y extraer mensaje.
    4. Rate limit por numero de telefono.
    5. Validar numero de telefono.
    6. Marcar mensaje como leido.
    7. Obtener respuesta de Claude.
    8. Enviar respuesta via WhatsApp.
    """
    # -----------------------------------------------------------------------
    # 1. Verificar firma del webhook
    # -----------------------------------------------------------------------
    raw_body = await request.body()
    signature = request.headers.get("X-Hub-Signature-256")

    if not verify_webhook_signature(raw_body, signature, settings.meta_app_secret):
        logger.warning("Firma invalida — request rechazada desde IP %s", _get_client_ip(request))
        raise HTTPException(status_code=403, detail="Invalid signature")

    # -----------------------------------------------------------------------
    # 2. Rate limit por IP
    # -----------------------------------------------------------------------
    client_ip = _get_client_ip(request)
    if not rate_limiter_ip.is_allowed(client_ip):
        logger.warning("Rate limit IP excedido: %s", client_ip)
        return JSONResponse(status_code=429, content={"error": "Too many requests"})

    # -----------------------------------------------------------------------
    # 3. Parsear payload
    # -----------------------------------------------------------------------
    try:
        body = await request.json()
    except Exception:
        logger.warning("Payload JSON invalido")
        return JSONResponse(status_code=400, content={"error": "Invalid JSON"})

    # Meta espera siempre 200 OK, incluso si no procesamos el mensaje.
    # Si respondemos con error, Meta reintenta y genera loops.
    # Por eso retornamos 200 en la mayoria de casos de "no procesamiento".

    # Verificar que es un evento de WhatsApp.
    if body.get("object") != "whatsapp_business_account":
        return JSONResponse(status_code=200, content={"status": "ignored"})

    # Extraer mensajes del payload.
    messages = _extract_messages(body)
    if not messages:
        # Evento de status (delivered, read, sent) — ignorar.
        return JSONResponse(status_code=200, content={"status": "no_messages"})

    # Procesar cada mensaje (normalmente es 1, pero Meta puede enviar batch).
    for msg_data in messages:
        phone_from = msg_data.get("from", "")
        message_id = msg_data.get("id", "")
        message_type = msg_data.get("type", "")
        contact_name = msg_data.get("_contact_name")

        # Solo procesamos mensajes de texto por ahora.
        if message_type != "text":
            logger.info(
                "Mensaje tipo '%s' de %s — ignorado (solo texto soportado)",
                message_type,
                _sanitize_phone(phone_from),
            )
            continue

        message_text = msg_data.get("text", {}).get("body", "")
        if not message_text:
            continue

        # -------------------------------------------------------------------
        # 4. Rate limit por numero de telefono
        # -------------------------------------------------------------------
        if not rate_limiter_phone.is_allowed(phone_from):
            logger.warning("Rate limit telefono excedido: %s", _sanitize_phone(phone_from))
            await send_text_message(
                to=phone_from,
                text="Estamos recibiendo muchos mensajes. Por favor espera un momento.",
                settings=settings,
            )
            continue

        # -------------------------------------------------------------------
        # 5. Validar numero de telefono
        # -------------------------------------------------------------------
        if not is_valid_phone_number(phone_from):
            logger.warning("Numero de telefono invalido: %s", phone_from[:6])
            continue

        logger.info(
            "Mensaje recibido de %s: [%d chars] tipo=%s",
            _sanitize_phone(phone_from),
            len(message_text),
            message_type,
        )

        # -------------------------------------------------------------------
        # 6. Marcar como leido (doble check azul)
        # -------------------------------------------------------------------
        if message_id:
            await mark_message_read(message_id, settings)

        # -------------------------------------------------------------------
        # 7. Obtener respuesta de Claude
        # -------------------------------------------------------------------
        ai_response = await get_ai_response(
            phone_number=phone_from,
            message_text=message_text,
            contact_name=contact_name,
            settings=settings,
        )

        # -------------------------------------------------------------------
        # 8. Enviar respuesta via WhatsApp
        # -------------------------------------------------------------------
        success = await send_text_message(
            to=phone_from,
            text=ai_response,
            settings=settings,
        )

        if success:
            logger.info("Respuesta enviada a %s [%d chars]", _sanitize_phone(phone_from), len(ai_response))
        else:
            logger.error("Fallo al enviar respuesta a %s", _sanitize_phone(phone_from))

    return JSONResponse(status_code=200, content={"status": "processed"})


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _extract_messages(body: dict) -> list[dict]:
    """
    Extrae mensajes del payload de WhatsApp.

    Estructura esperada:
    body.entry[].changes[].value.messages[]

    Tambien extrae el nombre del contacto si esta disponible.
    """
    messages = []

    for entry in body.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})

            if "messages" not in value:
                continue

            # Extraer nombre del contacto.
            contacts = value.get("contacts", [])
            contact_name = None
            if contacts:
                contact_name = contacts[0].get("profile", {}).get("name")

            for msg in value["messages"]:
                msg["_contact_name"] = contact_name
                messages.append(msg)

    return messages


def _get_client_ip(request: Request) -> str:
    """Obtiene IP del cliente (considera X-Forwarded-For de Railway)."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _sanitize_phone(phone: str) -> str:
    """Anonimiza numero de telefono para logs."""
    if len(phone) > 4:
        return f"***{phone[-4:]}"
    return "****"


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    # Cargar settings para obtener host/port.
    _settings = load_settings()
    uvicorn.run(
        "main:app",
        host=_settings.host,
        port=_settings.port,
        log_level=_settings.log_level,
    )
