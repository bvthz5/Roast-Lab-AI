import time
import uuid
from collections.abc import Callable
from typing import Any, cast

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger("presentation.middleware.logging")


class LoggingMiddleware(BaseHTTPMiddleware):
    """HTTP middleware to trace requests, track latency, and log structured records."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())

        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
        )

        start_time = time.perf_counter()

        try:
            response = cast(Response, await call_next(request))
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

            response.headers["X-Request-ID"] = request_id

            logger.info(
                "Request processed",
                status_code=response.status_code,
                duration_ms=duration_ms,
            )
            return response
        except Exception as e:
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            logger.exception(
                "Request failed with unhandled exception",
                duration_ms=duration_ms,
                error=str(e),
            )
            raise e
