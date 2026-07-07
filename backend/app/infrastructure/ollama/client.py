import httpx
import structlog

from app.shared.config import settings

logger = structlog.get_logger("infrastructure.ollama")


class OllamaClientManager:
    """Async Client wrapper for local Ollama LLM requests."""

    def __init__(self) -> None:
        self.client: httpx.AsyncClient | None = None

    def connect(self) -> None:
        """Establish Async Client connection pool for Ollama requests."""
        if not self.client:
            self.client = httpx.AsyncClient(
                base_url=settings.OLLAMA_BASE_URL, timeout=60.0
            )
            logger.info("Ollama httpx client initialized")

    async def disconnect(self) -> None:
        """Close Async Client connection pool gracefully."""
        if self.client:
            await self.client.aclose()
            self.client = None
            logger.info("Ollama httpx client closed")

    async def ping(self) -> bool:
        """Verify Ollama availability."""
        if not self.client:
            return False
        try:
            response = await self.client.get("/")
            return response.status_code == 200
        except Exception as e:
            logger.error("Ollama ping failed", error=str(e))
            return False


ollama_manager = OllamaClientManager()
