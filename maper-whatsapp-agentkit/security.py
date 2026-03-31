"""
Seguridad — Verificacion de firma y rate limiting.

Implementa:
- Verificacion de X-Hub-Signature-256 (OWASP A02).
- Rate limiting por IP y por numero de telefono (OWASP A07).
- Validacion de numeros de telefono.
"""

import hashlib
import hmac
import logging
import re
import time
from collections import defaultdict
from typing import Optional

from config import Settings

logger = logging.getLogger("maper.security")


# ---------------------------------------------------------------------------
# Verificacion de firma del webhook (X-Hub-Signature-256)
# ---------------------------------------------------------------------------

def verify_webhook_signature(
    payload_body: bytes,
    signature_header: Optional[str],
    app_secret: str,
) -> bool:
    """
    Verifica que el payload viene realmente de Meta.

    Meta firma cada POST del webhook con HMAC-SHA256 usando el App Secret.
    El header X-Hub-Signature-256 contiene 'sha256=<hex_digest>'.

    CRITICO: Usar hmac.compare_digest para evitar timing attacks.
    CRITICO: Usar el body raw (bytes), no el JSON parseado.
    """
    if not signature_header:
        logger.warning("Webhook recibido sin header X-Hub-Signature-256")
        return False

    if not signature_header.startswith("sha256="):
        logger.warning("Formato de firma invalido: %s", signature_header[:20])
        return False

    expected_signature = (
        "sha256="
        + hmac.new(
            app_secret.encode("utf-8"),
            payload_body,
            hashlib.sha256,
        ).hexdigest()
    )

    is_valid = hmac.compare_digest(signature_header, expected_signature)

    if not is_valid:
        logger.warning("Firma del webhook NO coincide — posible solicitud maliciosa")

    return is_valid


# ---------------------------------------------------------------------------
# Rate limiting en memoria (por IP y por numero de telefono)
# ---------------------------------------------------------------------------

class RateLimiter:
    """
    Rate limiter simple basado en ventana deslizante.

    Para produccion con multiples instancias, usar Redis.
    Para un MVP single-instance, esto es suficiente.
    """

    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        # key -> lista de timestamps
        self._requests: dict[str, list[float]] = defaultdict(list)

    def is_allowed(self, key: str) -> bool:
        """
        Verifica si la key (IP o telefono) tiene permitido hacer otra request.

        Retorna True si esta dentro del limite, False si debe ser rechazado.
        """
        now = time.monotonic()
        window_start = now - self.window_seconds

        # Limpiar requests viejas fuera de la ventana.
        self._requests[key] = [
            t for t in self._requests[key] if t > window_start
        ]

        if len(self._requests[key]) >= self.max_requests:
            logger.warning(
                "Rate limit excedido para key: %s (%d requests en %ds)",
                _sanitize_key(key),
                len(self._requests[key]),
                self.window_seconds,
            )
            return False

        self._requests[key].append(now)
        return True

    def cleanup(self) -> None:
        """Limpia entries expiradas para liberar memoria."""
        now = time.monotonic()
        window_start = now - self.window_seconds
        expired_keys = [
            k for k, timestamps in self._requests.items()
            if all(t <= window_start for t in timestamps)
        ]
        for key in expired_keys:
            del self._requests[key]


# ---------------------------------------------------------------------------
# Validacion de numero de telefono
# ---------------------------------------------------------------------------

# Formato esperado: digitos, minimo 10, maximo 15 (estandar E.164 sin +).
_PHONE_PATTERN = re.compile(r"^\d{10,15}$")


def is_valid_phone_number(phone: str) -> bool:
    """Valida que el numero de telefono tenga formato valido."""
    return bool(_PHONE_PATTERN.match(phone))


def _sanitize_key(key: str) -> str:
    """Anonimiza key para logs."""
    if len(key) > 6:
        return f"{key[:3]}***{key[-3:]}"
    return "***"
