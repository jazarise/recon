import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "sqlite:///reconx.db"
    API_KEY_SHODAN: str = ""
    API_KEY_VIRUSTOTAL: str = ""
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
