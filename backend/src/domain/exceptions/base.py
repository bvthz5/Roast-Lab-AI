from typing import Any


class DomainError(Exception):
    """Base exception class for all domain business logic errors."""

    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int = 400,
        errors: list[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.errors = errors or []


class ResourceNotFoundError(DomainError):
    """Exception raised when a requested resource is missing."""

    def __init__(
        self,
        message: str,
        error_code: str = "NOT_FOUND",
        errors: list[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(message, error_code, status_code=404, errors=errors)


class UnauthorizedError(DomainError):
    """Exception raised for authentication or permission failures."""

    def __init__(
        self,
        message: str,
        error_code: str = "UNAUTHORIZED",
        errors: list[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(message, error_code, status_code=401, errors=errors)


class AIFailureError(DomainError):
    """Exception raised when LLM inference or RAG pipelines fail."""

    def __init__(
        self,
        message: str,
        error_code: str = "AI_FAILURE",
        errors: list[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(message, error_code, status_code=502, errors=errors)
