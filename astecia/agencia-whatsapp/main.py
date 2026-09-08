"""
AGENCIA — WhatsApp Gateway
Sasha @ Programadora Senior

Recibe mensajes de WhatsApp de Juan Camilo,
enruta al agente correcto y responde en tiempo real.
"""

import os
import hmac
import hashlib
from fastapi import FastAPI, Request, Response, HTTPException
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator
from dotenv import load_dotenv
from router import route_message

load_dotenv()

app = FastAPI(title="Agencia WhatsApp Gateway", version="1.0.0")

# ── Seguridad ──────────────────────────────────────────────────────────────────
ALLOWED_NUMBER   = os.getenv("JUAN_CAMILO_PHONE")   # e.g. "whatsapp:+573001234567"
TWILIO_TOKEN     = os.getenv("TWILIO_AUTH_TOKEN")
VALIDATE_TWILIO  = os.getenv("VALIDATE_TWILIO_SIGNATURE", "true").lower() == "true"


def validate_twilio_request(request: Request, form: dict) -> bool:
    """Verifica que la petición venga realmente de Twilio."""
    if not VALIDATE_TWILIO:
        return True
    validator = RequestValidator(TWILIO_TOKEN)
    url = str(request.url)
    signature = request.headers.get("X-Twilio-Signature", "")
    return validator.validate(url, dict(form), signature)


# ── Webhook principal ──────────────────────────────────────────────────────────
@app.post("/webhook")
async def webhook(request: Request):
    form = await request.form()

    # 1. Validar que viene de Twilio
    if not validate_twilio_request(request, form):
        raise HTTPException(status_code=403, detail="Firma Twilio inválida")

    from_number  = form.get("From", "")
    body         = form.get("Body", "").strip()
    media_url    = form.get("MediaUrl0", None)

    # 2. Solo Juan Camilo puede dar órdenes
    if from_number != ALLOWED_NUMBER:
        resp = MessagingResponse()
        resp.message(
            "🔒 Acceso denegado.\n"
            "Esta Agencia responde únicamente a su director."
        )
        return Response(content=str(resp), media_type="application/xml")

    # 3. Mensaje vacío
    if not body and not media_url:
        resp = MessagingResponse()
        resp.message("Recibí tu mensaje pero estaba vacío. ¿Qué necesitas?")
        return Response(content=str(resp), media_type="application/xml")

    # 4. Enrutar al agente correcto y obtener respuesta
    response_text = await route_message(body, media_url)

    # 5. Responder por WhatsApp
    resp = MessagingResponse()
    resp.message(response_text)
    return Response(content=str(resp), media_type="application/xml")


# ── Health check ───────────────────────────────────────────────────────────────
@app.get("/")
def health():
    return {"status": "Agencia operativa", "agentes": [
        "Jarvis", "Jade", "Ego", "Sasha", "Brook", "Erik", "Cinthya"
    ]}
