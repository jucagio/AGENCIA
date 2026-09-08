import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    SUPABASE_PASSWORD: str = os.getenv("SUPABASE_PASSWORD", "")
    
    REPLICATE_API_KEY: str = os.getenv("REPLICATE_API_KEY", "")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev-secret-key-change-in-production")
    
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    API_TITLE: str = "Asesor Imagen AI"
    API_VERSION: str = "0.1.0"

    class Config:
        env_file = ".env.local"
        case_sensitive = True

settings = Settings()
