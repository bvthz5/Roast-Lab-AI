import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """Factory to create the FastAPI application instance."""
    app = FastAPI(
        title="RoastLab AI API",
        description="Backend API for RoastLab AI Code Review Platform",
        version="0.1.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],  # Frontend dev server
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", tags=["System"])
    async def health_check():
        return {"status": "healthy", "service": "RoastLab API"}

    return app

app = create_app()
