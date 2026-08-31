from typing import Any, Dict, Optional
from fastapi import HTTPException, status

class ClientFlowException(HTTPException):
    def __init__(
        self,
        status_code: int,
        message: str,
        error_code: str = "CLIENTFLOW_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "error_code": error_code,
                "message": message,
                "details": details or {}
            }
        )

class EntityNotFoundException(ClientFlowException):
    def __init__(self, entity_name: str, entity_id: Any):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=f"{entity_name} with id '{entity_id}' was not found.",
            error_code="ENTITY_NOT_FOUND",
            details={"entity": entity_name, "id": str(entity_id)}
        )

class TenantAccessViolationException(ClientFlowException):
    def __init__(self, message: str = "Tenant access violation. Operation not permitted."):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=message,
            error_code="TENANT_ACCESS_VIOLATION"
        )

class PermissionDeniedException(ClientFlowException):
    def __init__(self, permission_name: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=f"Missing required permission: '{permission_name}'",
            error_code="PERMISSION_DENIED",
            details={"required_permission": permission_name}
        )

class AuthenticationException(ClientFlowException):
    def __init__(self, message: str = "Invalid credentials or expired token"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            error_code="AUTHENTICATION_FAILED"
        )

class ConflictException(ClientFlowException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message=message,
            error_code="RESOURCE_CONFLICT"
        )

class ValidationException(ClientFlowException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=message,
            error_code="VALIDATION_FAILED",
            details=details
        )
