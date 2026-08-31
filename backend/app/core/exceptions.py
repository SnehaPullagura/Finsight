from typing import Any, Dict, Optional
from fastapi import HTTPException, status

class FinSightException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: str = "An error occurred",
        error_code: str = "GENERIC_ERROR",
        headers: Optional[Dict[str, str]] = None,
        extra: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code
        self.extra = extra or {}

class AuthenticationFailedException(FinSightException):
    def __init__(self, detail: str = "Invalid email or password"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="AUTH_INVALID_CREDENTIALS",
            headers={"WWW-Authenticate": "Bearer"}
        )

class TokenExpiredException(FinSightException):
    def __init__(self, detail: str = "Authentication token has expired"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="AUTH_TOKEN_EXPIRED",
            headers={"WWW-Authenticate": "Bearer"}
        )

class PermissionDeniedException(FinSightException):
    def __init__(self, detail: str = "You do not have permission to perform this action"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code="AUTH_PERMISSION_DENIED"
        )

class AccountLockedException(FinSightException):
    def __init__(self, detail: str = "Account temporarily locked due to excessive failed attempts"):
        super().__init__(
            status_code=status.HTTP_423_LOCKED,
            detail=detail,
            error_code="AUTH_ACCOUNT_LOCKED"
        )

class ResourceNotFoundException(FinSightException):
    def __init__(self, resource_name: str = "Resource", resource_id: Any = None):
        detail = f"{resource_name} not found"
        if resource_id:
            detail = f"{resource_name} with ID '{resource_id}' was not found"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code="RESOURCE_NOT_FOUND"
        )

class ValidationConflictException(FinSightException):
    def __init__(self, detail: str = "Resource already exists or violates constraint"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            error_code="RESOURCE_CONFLICT"
        )

class RateLimitExceededException(FinSightException):
    def __init__(self, detail: str = "Rate limit exceeded. Please try again later."):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
            error_code="RATE_LIMIT_EXCEEDED"
        )
