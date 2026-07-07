from typing import Any

from pydantic import BaseModel, Field


class ResponseMetadata(BaseModel):
    """Metadata detailing request timestamp and request ID."""

    timestamp: str = Field(description="ISO 8601 timestamp of the response")
    request_id: str = Field(description="Unique identifier for tracing the request")


class BaseResponse[T](BaseModel):
    """Base API response schema wrapping data payloads in a success envelope."""

    success: bool = True
    message: str = "Request completed successfully."
    data: T | dict[str, Any] = Field(default_factory=dict)
    errors: list[Any] | None = None
    metadata: ResponseMetadata


class BaseErrorResponse(BaseModel):
    """Base API error schema wrapping validation and domain errors."""

    success: bool = False
    message: str = "Validation failed."
    errors: list[Any] = Field(default_factory=list)
    metadata: ResponseMetadata
