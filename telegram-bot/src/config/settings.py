from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, model_validator


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    TELEGRAM_TOKEN: str
    ANTHROPIC_API_KEY: str
    ALLOWED_USER_IDS: list[int] = Field(default_factory=list)
    MAX_HISTORY_MESSAGES: int = 20
    RATE_LIMIT_MESSAGES: int = 10
    RATE_LIMIT_WINDOW_SECONDS: int = 60
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "development"

    @model_validator(mode="after")
    def _validate_allowed_users(self) -> "Settings":
        if not self.ALLOWED_USER_IDS:
            raise ValueError(
                "ALLOWED_USER_IDS esta vacio. "
                "Configura al menos un Telegram user ID autorizado."
            )
        return self


settings = Settings()
