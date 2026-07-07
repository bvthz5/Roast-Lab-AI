from fastapi import APIRouter, Depends
from httpx import AsyncClient
from qdrant_client import AsyncQdrantClient
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.base import BaseResponse
from app.infrastructure.database.session import get_db_session
from app.presentation.api.dependencies import (
    get_ollama,
    get_qdrant,
    get_redis,
)
from app.shared.response import success_response

router = APIRouter()


@router.get("/health", response_model=BaseResponse[dict[str, str]])
async def check_health(
    db: AsyncSession = Depends(get_db_session),
    redis: Redis = Depends(get_redis),
    qdrant: AsyncQdrantClient = Depends(get_qdrant),
    ollama: AsyncClient = Depends(get_ollama),
) -> BaseResponse[dict[str, str]]:
    """Verifies connection health metrics across all infrastructure backends."""
    postgres_status = "healthy"
    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        postgres_status = "unhealthy"

    redis_status = "healthy"
    try:
        await redis.ping()
    except Exception:
        redis_status = "unhealthy"

    qdrant_status = "healthy"
    try:
        await qdrant.get_collections()
    except Exception:
        qdrant_status = "unhealthy"

    ollama_status = "healthy"
    try:
        response = await ollama.get("/")
        if response.status_code != 200:
            ollama_status = "unhealthy"
    except Exception:
        ollama_status = "unhealthy"

    overall_status = "healthy"
    if "unhealthy" in (postgres_status, redis_status, qdrant_status, ollama_status):
        overall_status = "unhealthy"

    health_data = {
        "status": overall_status,
        "postgres": postgres_status,
        "redis": redis_status,
        "qdrant": qdrant_status,
        "ollama": ollama_status,
    }

    return success_response(
        data=health_data, message="Infrastructure health check completed."
    )
