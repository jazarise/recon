from reconx.config.settings import settings
from reconx.core.errors import ConfigurationError
from reconx.config.secrets import validate_secrets


def run_startup_checks():
    if not settings.database.url:
        raise ConfigurationError("DATABASE_URL must be configured.")

    if not settings.security.jwt_secret or settings.security.jwt_secret == "CHANGE_ME":  # nosec B105
        raise ConfigurationError("JWT_SECRET must be securely configured.")

    valid_envs = {"development", "testing", "staging", "production"}
    if settings.app.env not in valid_envs:
        raise ConfigurationError(f"APP_ENV invalid. Allowed: {valid_envs}")

    if settings.logging.level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
        raise ConfigurationError("LOG_LEVEL must be a valid logging level.")

    validate_secrets(settings)
