import json
from typing import Annotated

from pydantic import BeforeValidator
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors_origins(v: str | list[str]) -> list[str]:
    """Parse CORS origins from env string or list representation."""
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, (list, str)):
        try:
            return json.loads(v) if isinstance(v, str) else v
        except Exception:
            return []
    return v


class Settings(BaseSettings):
    """Pydantic settings configuration class loaded from environment."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # Application Settings
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str = "generate-a-secure-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    BACKEND_CORS_ORIGINS: Annotated[list[str], BeforeValidator(parse_cors_origins)] = [
        "http://localhost:3000"
    ]

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@db:5432/roastlab"

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"

    # Vector store & LLM
    QDRANT_URL: str = "http://qdrant:6333"
    OLLAMA_BASE_URL: str = "http://ollama:11434"


settings = Settings()
