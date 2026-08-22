from pydantic import BaseModel
from typing import Any, Optional

class ErrorResponse(BaseModel):
    status_code: int
    error_type: str
    message: str
    details: Optional[Any] = None


class AppException(Exception):
    def __init__(self, status_code: int, error_type: str, message: str, details: Optional[Any] = None):
        self.status_code = status_code
        self.error_type = error_type
        self.message = message
        self.details = details
        self.error_response = ErrorResponse(
            status_code=status_code,
            error_type=error_type,
            message=message,
            details=details
        )
        super().__init__(message)


class ValidationException(AppException):
    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(status_code=422, error_type="Validation Error", message=message, details=details)


class AuthenticationException(AppException):
    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(status_code=401, error_type="Authentication Error", message=message, details=details)


class AuthorizationException(AppException):
    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(status_code=403, error_type="Authorization Error", message=message, details=details)



class NotFoundException(AppException):
    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(status_code=404, error_type="Not Found Error", message=message, details=details)


class ConflictException(AppException):
    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(status_code=409, error_type="Conflict Error", message=message, details=details)




