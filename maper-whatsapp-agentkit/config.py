"""
Configuracion centralizada — MAPER WhatsApp AgentKit.

Todas las variables de entorno se validan al arrancar.
Si falta alguna variable critica, la app no arranca.
"""

import os
import secrets
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Configuracion inmutable de la aplicacion."""

    # --- Anthropic ---
    anthropic_api_key: str

    # --- WhatsApp / Meta Cloud API ---
    whatsapp_phone_number_id: str
    whatsapp_api_token: str
    webhook_verify_token: str
    meta_app_secret: str  # Para verificar firma X-Hub-Signature-256

    # --- Agente ---
    agent_name: str
    agent_model: str
    agent_fallback_message: str
    agent_greeting: str

    # --- Servidor ---
    host: str
    port: int
    log_level: str

    # --- Rate limiting ---
    rate_limit_max_requests: int
    rate_limit_window_seconds: int

    # --- Claude API ---
    claude_timeout_seconds: int
    claude_max_tokens: int


def load_settings() -> Settings:
    """
    Carga y valida todas las variables de entorno.

    Falla rapido si falta alguna variable critica.
    """

    def _require(name: str) -> str:
        value = os.environ.get(name)
        if not value:
            raise EnvironmentError(
                f"Variable de entorno requerida no encontrada: {name}. "
                f"Revisa el archivo .env.example para la lista completa."
            )
        return value

    def _optional(name: str, default: str) -> str:
        return os.environ.get(name, default)

    return Settings(
        # Criticas — sin estas la app no puede funcionar
        anthropic_api_key=_require("ANTHROPIC_API_KEY"),
        whatsapp_phone_number_id=_require("WHATSAPP_PHONE_NUMBER_ID"),
        whatsapp_api_token=_require("WHATSAPP_API_TOKEN"),
        webhook_verify_token=_require("WEBHOOK_VERIFY_TOKEN"),
        meta_app_secret=_require("META_APP_SECRET"),
        # Agente — personalizables
        agent_name=_optional("AGENT_NAME", "MAPER-Vendedor"),
        agent_model=_optional("AGENT_MODEL", "claude-opus-4-0"),
        agent_fallback_message=_optional(
            "AGENT_FALLBACK_MESSAGE",
            "No entendi tu pregunta. Puedes intentar nuevamente?",
        ),
        agent_greeting=_optional(
            "AGENT_GREETING",
            "Hola, soy el asistente MAPER. En que te puedo ayudar hoy?",
        ),
        # Servidor
        host=_optional("HOST", "0.0.0.0"),
        port=int(_optional("PORT", "8000")),
        log_level=_optional("LOG_LEVEL", "info"),
        # Rate limiting
        rate_limit_max_requests=int(_optional("RATE_LIMIT_MAX_REQUESTS", "20")),
        rate_limit_window_seconds=int(_optional("RATE_LIMIT_WINDOW_SECONDS", "60")),
        # Claude
        claude_timeout_seconds=int(_optional("CLAUDE_TIMEOUT_SECONDS", "30")),
        claude_max_tokens=int(_optional("CLAUDE_MAX_TOKENS", "1024")),
    )
