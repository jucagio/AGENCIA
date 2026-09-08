"""Configuration management using Pydantic Settings."""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from .env file."""

    # Claude API
    claude_api_key: str = ""

    # JWT Security
    jwt_secret: str = "default_jwt_secret_change_in_env"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24

    # Application
    environment: str = "development"
    debug: bool = True
    app_name: str = "Agencia Agent Orchestrator"

    # Paths
    vault_path: str = "agencia-vault"
    agent_state_path: str = ".claude/agent-state"
    agent_logs_path: str = ".claude/agent-logs"

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
