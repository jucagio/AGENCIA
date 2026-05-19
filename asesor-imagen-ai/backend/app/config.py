"""
Configuration settings for Asesor de Imagen AI.

Loaded from environment variables (.env file in development, secrets in prod).
Uses pydantic-settings v2 with field validation.

Naming convention:
    - Environment variables are SCREAMING_SNAKE_CASE (e.g. SECRET_KEY).
    - Python attributes are SCREAMING_SNAKE_CASE to match env var names exactly.
      pydantic-settings is case-insensitive by default but explicit names avoid confusion.

ADR-001 (Alejo): Supabase Auth nativo es la auth de producción.
    Custom JWT (SECRET_KEY/HS256) se mantiene SOLO durante migración 0.1 -> 0.2.
    En Entrega 0.2 se elimina y se usa exclusivamente JWKS de Supabase (ES256).
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings sourced from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="forbid",
    )

    # -------------------------------------------------------------------------
    # Environment
    # -------------------------------------------------------------------------
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = True
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    # -------------------------------------------------------------------------
    # FastAPI app
    # -------------------------------------------------------------------------
    APP_NAME: str = "Asesor de Imagen AI"
    APP_VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"

    # -------------------------------------------------------------------------
    # CORS
    # -------------------------------------------------------------------------
    # Comma-separated list of allowed origins. Empty in dev -> sane defaults applied.
    ALLOWED_ORIGINS: str = ""
    # Placeholder. Implementación real en 0.3 con slowapi+Redis
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, ge=1, le=10000)

    # -------------------------------------------------------------------------
    # Custom JWT (LEGACY - to be removed in Entrega 0.2 per ADR-001)
    # -------------------------------------------------------------------------
    SECRET_KEY: str = Field(
        default="dev-only-change-me-min-32-chars-1234567890",
        description="Symmetric key for legacy custom JWT (HS256). LEGACY.",
    )
    JWT_ALGORITHM: Literal["HS256"] = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # -------------------------------------------------------------------------
    # Supabase (ADR-001 — auth source of truth)
    # -------------------------------------------------------------------------
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""
    # JWKS endpoint for ES256 token validation (Entrega 0.2 wire-up).
    # Auto-derived from SUPABASE_URL via computed field.
    SUPABASE_JWT_AUDIENCE: str = "authenticated"
    SUPABASE_JWKS_CACHE_TTL_SECONDS: int = 600  # 10 min — see Supabase guidance

    # -------------------------------------------------------------------------
    # Async worker (ADR-002 — ARQ + Redis)
    # -------------------------------------------------------------------------
    REDIS_URL: str = "redis://localhost:6379/0"
    ARQ_QUEUE_NAME: str = "asesor_imagen_jobs"

    # -------------------------------------------------------------------------
    # Idempotency (ADR-003)
    # -------------------------------------------------------------------------
    IDEMPOTENCY_TTL_SECONDS: int = 86400  # 24h

    # -------------------------------------------------------------------------
    # Storage (ADR-005 — Supabase Storage + Cloudflare R2)
    # -------------------------------------------------------------------------
    SUPABASE_STORAGE_BUCKET: str = "user-uploads"
    R2_ACCOUNT_ID: str = ""
    R2_ACCESS_KEY_ID: str = ""
    R2_SECRET_ACCESS_KEY: str = ""
    R2_BUCKET: str = ""
    R2_PUBLIC_URL: str = ""

    # -------------------------------------------------------------------------
    # External AI APIs
    # -------------------------------------------------------------------------
    GOOGLE_CLOUD_VISION_API_KEY: str | None = None
    GOOGLE_VISION_CREDENTIALS: str | None = None
    VISION_BATCH_SIZE: int = 5
    REPLICATE_API_TOKEN: str = ""
    REPLICATE_MODEL_VERSION: str = "replicate/replicate/tryon"  # pinned per ADR-004
    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-opus-4-7"

    # -------------------------------------------------------------------------
    # Payments
    # -------------------------------------------------------------------------
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    MERCADO_PAGO_ACCESS_TOKEN: str = ""
    MERCADO_PAGO_WEBHOOK_SECRET: str = ""

    # -------------------------------------------------------------------------
    # Validators
    # -------------------------------------------------------------------------
    @field_validator("SECRET_KEY")
    @classmethod
    def _secret_key_strength(cls, v: str) -> str:
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v

    @field_validator("SUPABASE_URL")
    @classmethod
    def _supabase_url_format(cls, v: str) -> str:
        if v and not v.startswith(("http://", "https://")):
            raise ValueError("SUPABASE_URL must start with http:// or https://")
        return v.rstrip("/")

    # -------------------------------------------------------------------------
    # Computed properties
    # -------------------------------------------------------------------------
    @computed_field  # type: ignore[prop-decorator]
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def allowed_origins_list(self) -> list[str]:
        """Parse ALLOWED_ORIGINS env var into a clean list."""
        if not self.ALLOWED_ORIGINS:
            return []
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",") if o.strip()]

    @computed_field  # type: ignore[prop-decorator]
    @property
    def supabase_jwks_url(self) -> str:
        """JWKS endpoint URL derived from SUPABASE_URL.

        Used by Entrega 0.2 for ES256 token validation per Supabase docs.
        Reference: https://<project>.supabase.co/auth/v1/.well-known/jwks.json
        """
        if not self.SUPABASE_URL:
            return ""
        return f"{self.SUPABASE_URL}/auth/v1/.well-known/jwks.json"

    def assert_production_ready(self) -> None:
        """Fail fast on misconfigured production deploys.

        Called from main.py lifespan when ENVIRONMENT=production.
        """
        missing: list[str] = []
        required_in_prod = {
            "SUPABASE_URL": self.SUPABASE_URL,
            "SUPABASE_ANON_KEY": self.SUPABASE_ANON_KEY,
            "SUPABASE_SERVICE_ROLE_KEY": self.SUPABASE_SERVICE_ROLE_KEY,
            "ALLOWED_ORIGINS": self.ALLOWED_ORIGINS,
            "REDIS_URL": self.REDIS_URL,
        }
        for key, value in required_in_prod.items():
            if not value:
                missing.append(key)
        if self.SECRET_KEY.startswith("dev-only-"):
            missing.append("SECRET_KEY (still using dev placeholder)")
        if self.STRIPE_SECRET_KEY and not self.STRIPE_WEBHOOK_SECRET:
            missing.append("STRIPE_WEBHOOK_SECRET (required if STRIPE_SECRET_KEY set)")
        if self.MERCADO_PAGO_ACCESS_TOKEN and not self.MERCADO_PAGO_WEBHOOK_SECRET:
            missing.append("MERCADO_PAGO_WEBHOOK_SECRET (required if MP token set)")
        if missing:
            raise RuntimeError(
                f"Production env missing critical settings: {', '.join(missing)}"
            )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached singleton Settings instance.

    Use dependency injection in FastAPI:
        from fastapi import Depends
        def my_endpoint(settings: Settings = Depends(get_settings)): ...
    """
    return Settings()


# Backwards-compatible module-level instance.
# Prefer get_settings() in new code (testable, lru-cached).
settings = get_settings()
