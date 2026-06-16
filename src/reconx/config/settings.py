from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    reconx_api_key: Optional[str] = None
    shodan_api_key: Optional[str] = None
    github_token: Optional[str] = None
    
    database_url: str = "sqlite+aiosqlite:///reconx.db"
    
    jwt_secret: str = "change_me"
    jwt_algorithm: str = "HS256"
    
    log_level: str = "INFO"
    worker_threads: int = 10

    class Config:
        env_file = ".env"

settings = Settings()
