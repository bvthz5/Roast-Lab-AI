import structlog
from redis.asyncio import Redis, from_url

from src.shared.config import settings

logger = structlog.get_logger("infrastructure.redis")


class RedisClient:
    """Async Redis Client singleton wrapper."""

    def __init__(self) -> None:
        self.client: Redis | None = None

    def connect(self) -> None:
        """Establish Redis Connection Pool."""
        if not self.client:
            self.client = from_url(settings.REDIS_URL, decode_responses=True)
            logger.info("Redis client connected")

    async def disconnect(self) -> None:
        """Close connection pool gracefully."""
        if self.client:
            await self.client.close()
            self.client = None
            logger.info("Redis client disconnected")

    async def ping(self) -> bool:
        """Ping Redis to check alive status."""
        if not self.client:
            return False
        try:
            return await self.client.ping()
        except Exception as e:
            logger.error("Redis ping failed", error=str(e))
            return False


redis_client = RedisClient()
