from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Agent Workspace 24/7"
    app_env: str = "development"
    log_level: str = "info"
    api_prefix: str = "/api/v1"
    jwt_secret: str = "change-me"
    cors_origin: str = "http://localhost:3000"
    postgres_db: str = "student_workspace"
    postgres_user: str = "student_workspace"
    postgres_password: str = "student_workspace"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    database_url: str = "postgresql+psycopg://student_workspace:student_workspace@localhost:5432/student_workspace"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
