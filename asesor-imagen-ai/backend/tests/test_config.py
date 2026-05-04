"""
Tests for application configuration.
"""

from app.config import Settings, get_settings


def test_default_settings():
    """Settings should load with sensible defaults."""
    settings = Settings()
    assert settings.APP_NAME == "Asesor de Imagen AI"
    assert settings.APP_VERSION == "0.1.0"
    assert settings.ENVIRONMENT == "development"
    assert settings.JWT_ALGORITHM == "HS256"
    assert settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES == 30
    assert settings.RATE_LIMIT_PER_MINUTE == 60


def test_allowed_origins_list():
    """allowed_origins_list should split comma-separated string."""
    settings = Settings(ALLOWED_ORIGINS="http://a.com, http://b.com")
    assert settings.allowed_origins_list == ["http://a.com", "http://b.com"]


def test_is_production():
    """is_production should return True only in production environment."""
    dev = Settings(ENVIRONMENT="development")
    prod = Settings(ENVIRONMENT="production")
    assert dev.is_production is False
    assert prod.is_production is True


def test_get_settings_is_cached():
    """get_settings should return the same instance (cached)."""
    s1 = get_settings()
    s2 = get_settings()
    assert s1 is s2
