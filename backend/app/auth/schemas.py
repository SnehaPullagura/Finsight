import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from backend.app.auth.models import UserRole

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    full_name: str = Field(..., min_length=2, max_length=100)
    preferred_currency: str = Field(default="INR", max_length=10)

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    device_info: Optional[str] = None

class UserPublicResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    full_name: str
    role: UserRole
    is_active: bool
    is_verified: bool
    preferred_currency: str
    created_at: datetime.datetime
    last_login_at: Optional[datetime.datetime] = None

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserPublicResponse

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class SessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    device_info: Optional[str]
    ip_address: Optional[str]
    created_at: datetime.datetime
    expires_at: datetime.datetime
    is_revoked: bool

class AuditLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    action: str
    entity_type: str
    entity_id: Optional[str]
    changes_json: Optional[str]
    created_at: datetime.datetime
