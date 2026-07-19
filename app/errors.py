from __future__ import annotations


class AppError(Exception):
    def __init__(self, code: str, message: str, *, status: int = 400) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status


class ValidationError(AppError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(code, message, status=400)


class UnauthorizedError(AppError):
    def __init__(self, message: str = "The session is not authorized for this operation.") -> None:
        super().__init__("unauthorized", message, status=403)


class NotFoundError(AppError):
    def __init__(self, message: str = "The requested resource was not found.") -> None:
        super().__init__("not_found", message, status=404)


class ProviderError(AppError):
    def __init__(self, message: str = "The AI service could not complete the request.") -> None:
        super().__init__("provider_error", message, status=502)

