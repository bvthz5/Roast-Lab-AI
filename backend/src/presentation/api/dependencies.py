from httpx import AsyncClient
from qdrant_client import AsyncQdrantClient
from redis.asyncio import Redis

from src.infrastructure.ollama.client import ollama_manager
from src.infrastructure.qdrant.client import qdrant_manager
from src.infrastructure.redis.client import redis_client


async def get_redis() -> Redis:
    """Dependency injector yielding the active Redis client connection."""
    if not redis_client.client:
        redis_client.connect()
    assert redis_client.client is not None
    return redis_client.client


async def get_qdrant() -> AsyncQdrantClient:
    """Dependency injector yielding the active Qdrant vector store client."""
    if not qdrant_manager.client:
        qdrant_manager.connect()
    assert qdrant_manager.client is not None
    return qdrant_manager.client


async def get_ollama() -> AsyncClient:
    """Dependency injector yielding the active Ollama HTTPX async client."""
    if not ollama_manager.client:
        ollama_manager.connect()
    assert ollama_manager.client is not None
    return ollama_manager.client
