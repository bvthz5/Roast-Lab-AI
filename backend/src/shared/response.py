import datetime

import structlog

from src.application.dto.base import BaseResponse, ResponseMetadata


def success_response[T](
    data: T, message: str = "Request completed successfully."
) -> BaseResponse[T]:
    """Wraps endpoint responses into a standard success response model."""
    request_id = structlog.contextvars.get_contextvars().get("request_id", "system")
    metadata = ResponseMetadata(
        timestamp=datetime.datetime.now(datetime.UTC).isoformat(),
        request_id=request_id,
    )
    return BaseResponse(success=True, message=message, data=data, metadata=metadata)
