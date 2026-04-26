from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Agent Workspace 24/7"
    app_env: str = "development"
    log_level: str = "info"
    api_prefix: str = "/api/v1"
    jwt_secret: str = "change-me"
    cors_origin: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
