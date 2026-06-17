from reconx.core.errors import ConfigurationError

WEAK_SECRETS = {"password123", "secret", "admin", "reconx", "changeme", "test"}


def validate_secrets(settings_obj):
    secret = settings_obj.security.jwt_secret.lower()

    if len(secret) < 32:
        raise ConfigurationError("JWT_SECRET must be at least 32 characters long.")

    for weak in WEAK_SECRETS:
        if weak in secret:
            raise ConfigurationError(f"JWT_SECRET contains weak phrase: {weak}")
