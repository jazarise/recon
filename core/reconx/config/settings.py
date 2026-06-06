from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # App config
    APP_NAME: str = Field("ReconX", description="Name of the application")
    VERSION: str = Field("1.0.0", description="Application version")
    DEBUG: bool = Field(False, description="Enable debug mode")
    
    # DB config
    DATABASE_URL: str = Field(
        "sqlite+aiosqlite:///reconx.db", 
        description="Database connection URL"
    )

    # API config
    API_HOST: str = Field("127.0.0.1", description="API server host")
    API_PORT: int = Field(8000, description="API server port")

    # Plugin config
    PLUGIN_DIR: str = Field("plugins", description="Directory to load external plugins from")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
