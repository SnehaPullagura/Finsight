import uuid
import json
import datetime
from datetime import timezone
from typing import Optional, Tuple, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from backend.app.auth.models import User, UserSession, SecurityEvent, AuditLog, UserRole
from backend.app.auth.schemas import UserRegister, UserLogin
from backend.app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, decode_refresh_token
from backend.app.core.exceptions import (
    AuthenticationFailedException, AccountLockedException, ValidationConflictException,
    ResourceNotFoundException, PermissionDeniedException
)
from backend.app.core.config import settings

class AuthService:
    @staticmethod
    async def register_user(db: AsyncSession, data: UserRegister, ip_address: Optional[str] = None) -> User:
        stmt = select(User).where(User.email == data.email.lower())
        result = await db.execute(stmt)
        if result.scalar_one_or_none():
            raise ValidationConflictException("An account with this email address already exists.")
        
        user = User(
            email=data.email.lower(),
            hashed_password=get_password_hash(data.password),
            full_name=data.full_name,
            preferred_currency=data.preferred_currency,
            role=UserRole.USER,
            is_active=True,
            is_verified=True
        )
        db.add(user)
        await db.flush()
        
        event = SecurityEvent(
            user_id=user.id,
            event_type="REGISTER_SUCCESS",
            ip_address=ip_address,
            details=f"User registered with email {user.email}"
        )
        db.add(event)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def authenticate_user(
        db: AsyncSession,
        login_data: UserLogin,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Tuple[User, str, str]:
        stmt = select(User).where(User.email == login_data.email.lower())
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        now = datetime.datetime.now(timezone.utc)
        
        if not user:
            get_password_hash("dummy_password_for_timing")
            raise AuthenticationFailedException()
        
        if user.locked_until and user.locked_until > now:
            minutes_left = int((user.locked_until - now).total_seconds() / 60) + 1
            raise AccountLockedException(f"Account is locked. Please try again in {minutes_left} minutes.")
        
        if not verify_password(login_data.password, user.hashed_password):
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
                user.locked_until = now + datetime.timedelta(minutes=settings.LOCKOUT_DURATION_MINUTES)
                event = SecurityEvent(
                    user_id=user.id,
                    event_type="ACCOUNT_LOCKED",
                    ip_address=ip_address,
                    user_agent=user_agent,
                    details=f"Locked out after {user.failed_login_attempts} failed login attempts"
                )
                db.add(event)
            else:
                event = SecurityEvent(
                    user_id=user.id,
                    event_type="LOGIN_FAILED",
                    ip_address=ip_address,
                    user_agent=user_agent,
                    details=f"Failed login attempt ({user.failed_login_attempts}/{settings.MAX_LOGIN_ATTEMPTS})"
                )
                db.add(event)
            await db.commit()
            raise AuthenticationFailedException()
        
        if not user.is_active:
            raise PermissionDeniedException("This account is inactive or disabled.")
        
        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_login_at = now
        user.last_login_ip = ip_address
        
        jti = str(uuid.uuid4())
        access_token = create_access_token(
            subject=user.id,
            claims={"email": user.email, "role": user.role.value}
        )
        refresh_token = create_refresh_token(
            subject=user.id,
            claims={"jti": jti, "role": user.role.value}
        )
        
        session = UserSession(
            user_id=user.id,
            refresh_token_jti=jti,
            device_info=login_data.device_info or "Unknown Device",
            ip_address=ip_address,
            user_agent=user_agent,
            is_revoked=False,
            expires_at=now + datetime.timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        db.add(session)
        
        event = SecurityEvent(
            user_id=user.id,
            event_type="LOGIN_SUCCESS",
            ip_address=ip_address,
            user_agent=user_agent,
            details=f"Successful login from {ip_address}"
        )
        db.add(event)
        
        await db.commit()
        await db.refresh(user)
        return user, access_token, refresh_token

    @staticmethod
    async def refresh_tokens(
        db: AsyncSession,
        refresh_token_str: str,
        ip_address: Optional[str] = None
    ) -> Tuple[User, str, str]:
        payload = decode_refresh_token(refresh_token_str)
        if not payload:
            raise AuthenticationFailedException("Invalid or expired refresh token")
        
        user_id = int(payload.get("sub"))
        jti = payload.get("jti")
        
        stmt = select(UserSession).where(UserSession.refresh_token_jti == jti)
        result = await db.execute(stmt)
        session = result.scalar_one_or_none()
        
        if not session or session.is_revoked:
            raise AuthenticationFailedException("Session revoked or expired")
        
        user_stmt = select(User).where(User.id == user_id)
        user_res = await db.execute(user_stmt)
        user = user_res.scalar_one_or_none()
        if not user or not user.is_active:
            raise AuthenticationFailedException("User not found or inactive")
        
        session.is_revoked = True
        
        new_jti = str(uuid.uuid4())
        new_access_token = create_access_token(
            subject=user.id,
            claims={"email": user.email, "role": user.role.value}
        )
        new_refresh_token = create_refresh_token(
            subject=user.id,
            claims={"jti": new_jti, "role": user.role.value}
        )
        
        now = datetime.datetime.now(timezone.utc)
        new_session = UserSession(
            user_id=user.id,
            refresh_token_jti=new_jti,
            device_info=session.device_info,
            ip_address=ip_address or session.ip_address,
            user_agent=session.user_agent,
            is_revoked=False,
            expires_at=now + datetime.timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        db.add(new_session)
        await db.commit()
        
        return user, new_access_token, new_refresh_token

    @staticmethod
    async def logout_session(db: AsyncSession, user_id: int) -> bool:
        await db.execute(
            update(UserSession)
            .where(UserSession.user_id == user_id)
            .values(is_revoked=True)
        )
        await db.commit()
        return True
