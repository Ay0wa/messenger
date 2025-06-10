from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Messenger API"
    app_version: str = "0.1.0"
    debug: bool = Field(default=False, description="Debug mode")
    
    database_url: str = Field(
        default="postgresql+asyncpg://messenger_user:messenger_pass@localhost:5432/messenger",
        description="Database URL"
    )
    
    redis_url: str = Field(
        default="redis://localhost:6379",
        description="Redis URL"
    )
    
    secret_key: str = Field(
        default="your-secret-key-here-change-in-production",
        description="Secret key for JWT"
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    websocket_ping_interval: int = 30
    websocket_ping_timeout: int = 10
    
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
        description="CORS allowed origins"
    )
    
    log_level: str = "INFO"
    
    enable_metrics: bool = True
    metrics_port: int = 9090

    model_config = SettingsConfigDict(env_prefix="APP_")

@lru_cache()
def get_settings() -> Settings:
    return Settings()