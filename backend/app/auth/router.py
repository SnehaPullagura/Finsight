from typing import List
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.auth.schemas import (
    UserRegister, UserLogin, TokenResponse, RefreshTokenRequest,
    UserPublicResponse, SessionResponse
)
from backend.app.auth.service import AuthService
from backend.app.auth.dependencies import get_current_user
from backend.app.auth.models import User, UserSession
from backend.app.core.config import settings
from sqlalchemy import select

router = APIRouter(prefix="/auth", tags=["Identity & Security"])

@router.post("/register", response_model=UserPublicResponse, status_code=status.HTTP_201_CREATED)
async def register(
    data: UserRegister,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    ip_address = request.client.host if request.client else "127.0.0.1"
    user = await AuthService.register_user(db, data, ip_address=ip_address)
    return user

@router.post("/login", response_model=TokenResponse)
async def login(
    data: UserLogin,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    ip_address = request.client.host if request.client else "127.0.0.1"
    user_agent = request.headers.get("user-agent", "Unknown")
    user, access_token, refresh_token = await AuthService.authenticate_user(
        db, data, ip_address=ip_address, user_agent=user_agent
    )
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserPublicResponse.model_validate(user)
    )

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    data: RefreshTokenRequest,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    ip_address = request.client.host if request.client else "127.0.0.1"
    user, access_token, refresh_token = await AuthService.refresh_tokens(
        db, data.refresh_token, ip_address=ip_address
    )
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserPublicResponse.model_validate(user)
    )

@router.post("/logout")
async def logout(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await AuthService.logout_session(db, current_user.id)
    return {"message": "Successfully logged out from all active sessions."}

@router.get("/me", response_model=UserPublicResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/sessions", response_model=List[SessionResponse])
async def list_user_sessions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(UserSession).where(
        UserSession.user_id == current_user.id
    ).order_by(UserSession.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()
