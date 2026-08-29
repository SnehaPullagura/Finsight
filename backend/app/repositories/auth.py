from typing import List, Optional
from datetime import datetime
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from backend.app.models.auth import User, Role, Permission, UserRole, RolePermission, UserSession, PasswordResetToken, EmailVerificationToken
from backend.app.repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def get_by_email(self, email: str) -> Optional[User]:
        query = select(User).where(User.email == email, User.is_deleted == False).options(
            selectinload(User.roles).selectinload(UserRole.role)
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_with_roles(self, user_id: str) -> Optional[User]:
        query = select(User).where(User.id == user_id, User.is_deleted == False).options(
            selectinload(User.roles).selectinload(UserRole.role)
        )
        result = await self.db.execute(query)
        return result.scalars().first()

class RoleRepository(BaseRepository[Role]):
    def __init__(self, db: AsyncSession):
        super().__init__(Role, db)

    async def get_by_name(self, name: str, tenant_id: Optional[str] = None) -> Optional[Role]:
        query = select(Role).where(Role.name == name)
        if tenant_id:
            query = query.where(Role.tenant_id == tenant_id)
        else:
            query = query.where(Role.tenant_id == None)
        query = query.options(selectinload(Role.permissions).selectinload(RolePermission.permission))
        result = await self.db.execute(query)
        return result.scalars().first()

    async def list_roles_for_tenant(self, tenant_id: Optional[str] = None) -> List[Role]:
        query = select(Role).where(
            (Role.tenant_id == tenant_id) | (Role.tenant_id == None)
        ).options(selectinload(Role.permissions).selectinload(RolePermission.permission))
        result = await self.db.execute(query)
        return list(result.scalars().all())

class PermissionRepository(BaseRepository[Permission]):
    def __init__(self, db: AsyncSession):
        super().__init__(Permission, db)

    async def get_by_code(self, code: str) -> Optional[Permission]:
        query = select(Permission).where(Permission.code == code)
        result = await self.db.execute(query)
        return result.scalars().first()

class UserSessionRepository(BaseRepository[UserSession]):
    def __init__(self, db: AsyncSession):
        super().__init__(UserSession, db)

    async def get_valid_session(self, user_id: str, refresh_token_hash: str) -> Optional[UserSession]:
        query = select(UserSession).where(
            UserSession.user_id == user_id,
            UserSession.refresh_token_hash == refresh_token_hash,
            UserSession.is_revoked == False,
            UserSession.expires_at > datetime.utcnow()
        )
        result = await self.db.execute(query)
        return result.scalars().first()
