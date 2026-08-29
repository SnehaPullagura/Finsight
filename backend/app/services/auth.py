import hashlib
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
