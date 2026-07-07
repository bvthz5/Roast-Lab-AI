from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.ollama.client import ollama_manager
from app.infrastructure.qdrant.client import qdrant_manager
from app.infrastructure.redis.client import redis_client
from app.observability.logging import configure_logging
from app.presentation.api.v1.router import api_v1_router
from app.presentation.middleware.exceptions import register_exception_handlers
from app.presentation.middleware.logging import LoggingMiddleware
from app.shared.config import settings


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Gracefully orchestrates connection pools across application lifecycles."""
    # 1. Initialize global logger configuration
    configure_logging()

    # 2. Establish connections to external backend services
    redis_client.connect()
    qdrant_manager.connect()
    ollama_manager.connect()

    yield

    # 3. Clean up resource pools on shutdown
    await redis_client.disconnect()
    await qdrant_manager.disconnect()
    await ollama_manager.disconnect()


def create_app() -> FastAPI:
    """FastAPI Application Factory."""
    app = FastAPI(
        title="RoastLab AI API",
        description="Backend API for RoastLab AI Code Review Platform",
        version="0.1.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Configure Logging Middleware
    app.add_middleware(LoggingMiddleware)

    # Register central exception handlers
    register_exception_handlers(app)

    # Include versioned API routers
    app.include_router(api_v1_router, prefix="/api/v1")

    return app


app = create_app()
