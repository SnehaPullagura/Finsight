from typing import Optional
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.app.database.session import get_db
from backend.app.auth.models import User, UserRole
from backend.app.core.security import decode_access_token
from backend.app.core.exceptions import AuthenticationFailedException, TokenExpiredException, PermissionDeniedException

security_scheme = HTTPBearer(auto_error=False)

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    if not credentials or not credentials.credentials:
        raise AuthenticationFailedException("Missing or invalid Authorization header")
    
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise TokenExpiredException()
    
    user_id = payload.get("sub")
    if not user_id:
        raise AuthenticationFailedException("Token missing subject identifier")
    
    stmt = select(User).where(User.id == int(user_id))
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise AuthenticationFailedException("User not found")
    if not user.is_active:
        raise PermissionDeniedException("User account is inactive")
    
    return user

async def get_current_active_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise PermissionDeniedException("Administrative privileges required")
    return current_user
