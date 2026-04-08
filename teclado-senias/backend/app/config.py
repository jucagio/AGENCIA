"""Configuration management for Teclado de Senas backend.

Loads settings from environment variables with sensible defaults
for local development. In production, all secrets MUST be set via
environment variables -- never hardcoded.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from .env file."""

    # Supabase
    supabase_url: str = ""
    supabase_key: str = ""
    supabase_service_role_key: str = ""

    # JWT
    jwt_secret: str = "CHANGE_ME_IN_PRODUCTION"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7

    # Application
    environment: str = "development"
    debug: bool = True
    app_name: str = "Teclado de Senas API"
    app_version: str = "0.1.0"

    # CORS -- Flutter app origins
    cors_origins: str = "http://localhost:3000,http://localhost:8080,http://127.0.0.1:3000"

    # Rate limiting
    rate_limit_per_minute: int = 30

    # Logging
    log_level: str = "INFO"

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
    }

    def get_cors_origins(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
