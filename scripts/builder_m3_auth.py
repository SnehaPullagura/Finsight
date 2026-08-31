import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. models/auth.py
    write_file("backend/app/models/auth.py", """import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin

class User(UUIDModel, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # MFA Settings
    mfa_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    mfa_secret: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    sessions: Mapped[List["UserSession"]] = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    roles: Mapped[List["UserRole"]] = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")

class Role(UUIDModel, TimestampMixin):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_system: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    tenant_id: Mapped[Optional[str]] = mapped_column(String(36), index=True, nullable=True)

    permissions: Mapped[List["RolePermission"]] = relationship("RolePermission", back_populates="role", cascade="all, delete-orphan")
    users: Mapped[List["UserRole"]] = relationship("UserRole", back_populates="role", cascade="all, delete-orphan")

class Permission(UUIDModel):
    __tablename__ = "permissions"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    module: Mapped[str] = mapped_column(String(50), index=True, nullable=False)

    roles: Mapped[List["RolePermission"]] = relationship("RolePermission", back_populates="permission", cascade="all, delete-orphan")

class UserRole(UUIDModel, TimestampMixin):
    __tablename__ = "user_roles"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role_id: Mapped[str] = mapped_column(String(36), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False, index=True)
    tenant_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)

    user: Mapped["User"] = relationship("User", back_populates="roles")
    role: Mapped["Role"] = relationship("Role", back_populates="users")

    __table_args__ = (UniqueConstraint("user_id", "role_id", "tenant_id", name="uq_user_role_tenant"),)

class RolePermission(UUIDModel):
    __tablename__ = "role_permissions"

    role_id: Mapped[str] = mapped_column(String(36), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False, index=True)
    permission_id: Mapped[str] = mapped_column(String(36), ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False, index=True)

    role: Mapped["Role"] = relationship("Role", back_populates="permissions")
    permission: Mapped["Permission"] = relationship("Permission", back_populates="roles")

    __table_args__ = (UniqueConstraint("role_id", "permission_id", name="uq_role_permission"),)

class UserSession(UUIDModel, TimestampMixin):
    __tablename__ = "user_sessions"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    refresh_token_hash: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="sessions")

class PasswordResetToken(UUIDModel, TimestampMixin):
    __tablename__ = "password_reset_tokens"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

class EmailVerificationToken(UUIDModel, TimestampMixin):
    __tablename__ = "email_verification_tokens"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
""")

    # 2. schemas/auth.py
    write_file("backend/app/schemas/auth.py", """from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    phone: Optional[str] = None
    organization_name: Optional[str] = None

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str
    mfa_code: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: str
    tenant_id: Optional[str] = None
    email: str
    first_name: str
    last_name: str
    roles: List[str] = []

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(min_length=8)

class VerifyEmailRequest(BaseModel):
    token: str

class MFASetupResponse(BaseModel):
    secret: str
    qr_code_uri: str

class MFAVerifyRequest(BaseModel):
    code: str

class UserResponse(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: bool
    is_verified: bool
    is_superuser: bool
    mfa_enabled: bool
    created_at: datetime
    roles: List[str] = []

    class Config:
        from_attributes = True

class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    permission_codes: List[str] = []

class RoleResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    is_system: bool
    tenant_id: Optional[str] = None
    permissions: List[str] = []

    class Config:
        from_attributes = True

class PermissionResponse(BaseModel):
    id: str
    name: str
    code: str
    description: Optional[str] = None
    module: str

    class Config:
        from_attributes = True
""")

    # 3. repositories/auth.py
    write_file("backend/app/repositories/auth.py", """from typing import List, Optional
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
""")

    # 4. services/auth.py
    write_file("backend/app/services/auth.py", """import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import settings
from backend.app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
    generate_totp_secret,
    get_totp_uri,
    verify_totp_code
)
from backend.app.core.exceptions import AuthenticationException, ConflictException, EntityNotFoundException, ValidationException
from backend.app.models.auth import User, Role, UserRole, UserSession, PasswordResetToken, EmailVerificationToken
from backend.app.repositories.auth import UserRepository, RoleRepository, PermissionRepository, UserSessionRepository
from backend.app.schemas.auth import UserRegisterRequest, UserLoginRequest, TokenResponse, UserResponse

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.role_repo = RoleRepository(db)
        self.perm_repo = PermissionRepository(db)
        self.session_repo = UserSessionRepository(db)

    async def register(self, req: UserRegisterRequest) -> User:
        existing = await self.user_repo.get_by_email(req.email)
        if existing:
            raise ConflictException(f"User with email '{req.email}' already exists.")

        user = await self.user_repo.create({
            "email": req.email,
            "hashed_password": get_password_hash(req.password),
            "first_name": req.first_name,
            "last_name": req.last_name,
            "phone": req.phone,
            "is_active": True,
            "is_verified": False,
            "is_superuser": False,
        })
        return user

    async def authenticate(self, req: UserLoginRequest, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> Tuple[TokenResponse, User]:
        user = await self.user_repo.get_by_email(req.email)
        if not user or not verify_password(req.password, user.hashed_password):
            raise AuthenticationException("Invalid email or password.")

        if not user.is_active:
            raise AuthenticationException("Account is disabled. Please contact administrator.")

        if user.mfa_enabled:
            if not req.mfa_code:
                raise AuthenticationException("MFA code is required for this account.")
            if not user.mfa_secret or not verify_totp_code(user.mfa_secret, req.mfa_code):
                raise AuthenticationException("Invalid MFA authentication code.")

        # Update last login
        await self.user_repo.update(user, {"last_login_at": datetime.utcnow()})

        # Extract roles and tenant_id
        roles = [ur.role.name for ur in user.roles if ur.role]
        tenant_id = user.roles[0].tenant_id if user.roles else None

        access_token = create_access_token(
            subject=user.id,
            tenant_id=tenant_id,
            roles=roles
        )
        refresh_token = create_refresh_token(
            subject=user.id,
            tenant_id=tenant_id
        )

        # Store session
        await self.session_repo.create({
            "user_id": user.id,
            "refresh_token_hash": hash_token(refresh_token),
            "ip_address": ip_address,
            "user_agent": user_agent,
            "expires_at": datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            "is_revoked": False
        })

        token_resp = TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user_id=user.id,
            tenant_id=tenant_id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            roles=roles
        )
        return token_resp, user

    async def refresh_access_token(self, refresh_token: str) -> TokenResponse:
        try:
            payload = decode_token(refresh_token)
            if payload.get("type") != "refresh":
                raise AuthenticationException("Invalid token type")
            user_id = payload.get("sub")
            tenant_id = payload.get("tenant_id")
        except Exception:
            raise AuthenticationException("Invalid or expired refresh token")

        session = await self.session_repo.get_valid_session(user_id, hash_token(refresh_token))
        if not session:
            raise AuthenticationException("Session revoked or expired")

        user = await self.user_repo.get_with_roles(user_id)
        if not user or not user.is_active:
            raise AuthenticationException("User account inactive")

        roles = [ur.role.name for ur in user.roles if ur.role]
        new_access_token = create_access_token(
            subject=user.id,
            tenant_id=tenant_id,
            roles=roles
        )

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user_id=user.id,
            tenant_id=tenant_id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            roles=roles
        )

    async def logout(self, user_id: str, refresh_token: Optional[str] = None):
        if refresh_token:
            session = await self.session_repo.get_valid_session(user_id, hash_token(refresh_token))
            if session:
                await self.session_repo.update(session, {"is_revoked": True})

    async def setup_mfa(self, user_id: str) -> Tuple[str, str]:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise EntityNotFoundException("User", user_id)
        secret = generate_totp_secret()
        uri = get_totp_uri(secret, user.email)
        await self.user_repo.update(user, {"mfa_secret": secret})
        return secret, uri

    async def verify_mfa_setup(self, user_id: str, code: str) -> bool:
        user = await self.user_repo.get_by_id(user_id)
        if not user or not user.mfa_secret:
            raise ValidationException("MFA setup has not been initiated")
        if not verify_totp_code(user.mfa_secret, code):
            raise ValidationException("Invalid TOTP verification code")
        await self.user_repo.update(user, {"mfa_enabled": True})
        return True
""")

    # 5. api/v1/endpoints/auth.py
    write_file("backend/app/api/v1/endpoints/auth.py", """from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, CurrentUserContext
from backend.app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    UserResponse,
    MFASetupResponse,
    MFAVerifyRequest,
    PasswordResetRequest,
    PasswordResetConfirm,
    VerifyEmailRequest
)
from backend.app.services.auth import AuthService

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(req: UserRegisterRequest, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    user = await auth_service.register(req)
    return UserResponse(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        avatar_url=user.avatar_url,
        is_active=user.is_active,
        is_verified=user.is_verified,
        is_superuser=user.is_superuser,
        mfa_enabled=user.mfa_enabled,
        created_at=user.created_at,
        roles=[]
    )

@router.post("/login", response_model=TokenResponse)
async def login(req: UserLoginRequest, request: Request, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    ip = request.client.host if request.client else None
    user_agent = request.headers.get("User-Agent")
    token_resp, _ = await auth_service.authenticate(req, ip_address=ip, user_agent=user_agent)
    return token_resp

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(req: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    return await auth_service.refresh_access_token(req.refresh_token)

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    req: RefreshTokenRequest,
    current_user: CurrentUserContext = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    await auth_service.logout(current_user.id, req.refresh_token)
    return {"message": "Successfully logged out."}

@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: CurrentUserContext = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    user = await auth_service.user_repo.get_with_roles(current_user.id)
    roles = [ur.role.name for ur in user.roles if ur.role]
    return UserResponse(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        avatar_url=user.avatar_url,
        is_active=user.is_active,
        is_verified=user.is_verified,
        is_superuser=user.is_superuser,
        mfa_enabled=user.mfa_enabled,
        created_at=user.created_at,
        roles=roles
    )

@router.post("/mfa/setup", response_model=MFASetupResponse)
async def setup_mfa(
    current_user: CurrentUserContext = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    secret, uri = await auth_service.setup_mfa(current_user.id)
    return MFASetupResponse(secret=secret, qr_code_uri=uri)

@router.post("/mfa/verify", status_code=status.HTTP_200_OK)
async def verify_mfa(
    req: MFAVerifyRequest,
    current_user: CurrentUserContext = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    await auth_service.verify_mfa_setup(current_user.id, req.code)
    return {"message": "MFA has been successfully verified and enabled."}
""")

    # 6. Update api/v1/api.py
    write_file("backend/app/api/v1/api.py", """from fastapi import APIRouter
from backend.app.api.v1.endpoints import health, auth

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication & Authorization"])
""")

    print("Milestone 3 & 4 Auth files created successfully!")

if __name__ == '__main__':
    run()
