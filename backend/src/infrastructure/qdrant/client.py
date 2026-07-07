import structlog
from qdrant_client import AsyncQdrantClient

from src.shared.config import settings

logger = structlog.get_logger("infrastructure.qdrant")


class QdrantClientManager:
    """Manager to orchestrate async connections to Qdrant vector database."""

    def __init__(self) -> None:
        self.client: AsyncQdrantClient | None = None

    def connect(self) -> None:
        """Establish Async Connection to Qdrant."""
        if not self.client:
            self.client = AsyncQdrantClient(url=settings.QDRANT_URL)
            logger.info("Qdrant async client connected")

    async def disconnect(self) -> None:
        """Gracefully disconnect Qdrant client."""
        if self.client:
            await self.client.close()
            self.client = None
            logger.info("Qdrant client disconnected")


qdrant_manager = QdrantClientManager()
