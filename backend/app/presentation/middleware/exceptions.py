import datetime

import structlog
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.domain.exceptions.base import DomainError

logger = structlog.get_logger("presentation.middleware.exceptions")


def register_exception_handlers(app: FastAPI) -> None:
    """Register application handlers mapping exceptions to standard formats."""

    @app.exception_handler(DomainError)
    async def domain_exception_handler(
        _request: Request, exc: DomainError
    ) -> JSONResponse:
        request_id = structlog.contextvars.get_contextvars().get("request_id", "")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.message,
                "errors": exc.errors
                if exc.errors
                else [{"code": exc.error_code, "message": exc.message}],
                "metadata": {
                    "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
                    "requestId": request_id,
                },
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        _request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        request_id = structlog.contextvars.get_contextvars().get("request_id", "")
        errors = []
        for error in exc.errors():
            errors.append(
                {
                    "field": ".".join([str(x) for x in error.get("loc", [])]),
                    "type": error.get("type", ""),
                    "message": error.get("msg", ""),
                }
            )

        logger.warn("Validation error occurred", errors=errors)
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "message": "Validation failed.",
                "errors": errors,
                "metadata": {
                    "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
                    "requestId": request_id,
                },
            },
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        _request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        request_id = structlog.contextvars.get_contextvars().get("request_id", "")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.detail,
                "errors": [{"message": exc.detail}],
                "metadata": {
                    "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
                    "requestId": request_id,
                },
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(
        _request: Request, exc: Exception
    ) -> JSONResponse:
        request_id = structlog.contextvars.get_contextvars().get("request_id", "")
        logger.exception("Unexpected error occurred", error=str(exc))
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "An unexpected error occurred. Please try again later.",
                "errors": [{"message": "Internal Server Error"}],
                "metadata": {
                    "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
                    "requestId": request_id,
                },
            },
        )
