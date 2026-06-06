from core.config import settings

def test_config_defaults():
    assert settings.ENVIRONMENT == "development"
    assert settings.DATABASE_URL is not None
