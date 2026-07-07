from typing import Any, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")

class ResponseMetadata(BaseModel):
    timestamp: str = Field(description="ISO 8601 timestamp of the response")
    request_id: str = Field(description="Unique identifier for tracing the request")

class BaseResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "Request completed successfully."
    data: T | dict[str, Any] = Field(default_factory=dict)
    errors: list[Any] | None = None
    metadata: ResponseMetadata

class BaseErrorResponse(BaseModel):
    success: bool = False
    message: str = "Validation failed."
    errors: list[Any] = Field(default_factory=list)
    metadata: ResponseMetadata
