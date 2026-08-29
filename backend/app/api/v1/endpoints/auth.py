from fastapi import APIRouter, Depends, Request, status
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
