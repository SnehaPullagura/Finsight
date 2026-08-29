from typing import AsyncGenerator, Optional
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
import jwt

from backend.app.core.config import settings
from backend.app.core.database import get_db
from backend.app.core.security import decode_token
from backend.app.core.exceptions import AuthenticationException, TenantAccessViolationException

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/login",
    auto_error=False
)

class CurrentUserContext:
    def __init__(self, id: str, email: str, tenant_id: str, roles: list):
        self.id = id
        self.email = email
        self.tenant_id = tenant_id
        self.roles = roles

async def get_current_user_optional(
    token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> Optional[CurrentUserContext]:
    if not token:
        return None
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        tenant_id = payload.get("tenant_id")
        roles = payload.get("roles", [])
        if not user_id:
            return None
        return CurrentUserContext(id=user_id, email=payload.get("email", ""), tenant_id=tenant_id, roles=roles)
    except Exception:
        return None

async def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> CurrentUserContext:
    if not token:
        raise AuthenticationException("Not authenticated")
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        tenant_id = payload.get("tenant_id")
        roles = payload.get("roles", [])
        if not user_id:
            raise AuthenticationException("Invalid token payload")
        return CurrentUserContext(id=user_id, email=payload.get("email", ""), tenant_id=tenant_id, roles=roles)
    except jwt.PyJWTError:
        raise AuthenticationException("Invalid or expired authentication token")

async def get_current_tenant_id(
    current_user: CurrentUserContext = Depends(get_current_user),
    x_tenant_id: Optional[str] = Header(None)
) -> str:
    # If user has a tenant_id bound in token, enforce it
    if current_user.tenant_id:
        if x_tenant_id and x_tenant_id != current_user.tenant_id:
            raise TenantAccessViolationException("Tenant ID mismatch between header and credentials")
        return current_user.tenant_id
    if x_tenant_id:
        return x_tenant_id
    raise TenantAccessViolationException("No active organization context found")
