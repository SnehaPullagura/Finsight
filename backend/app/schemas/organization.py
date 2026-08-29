from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, EmailStr, Field

class OrganizationCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    slug: Optional[str] = None
    domain: Optional[str] = None
    plan_tier: Optional[str] = "enterprise"

class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    plan_tier: Optional[str] = None
    logo_url: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None

class OrganizationResponse(BaseModel):
    id: str
    name: str
    slug: str
    domain: Optional[str] = None
    plan_tier: str
    is_active: bool
    logo_url: Optional[str] = None
    settings: Dict[str, Any] = {}
    created_at: datetime

    class Config:
        from_attributes = True

class TeamCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: Optional[str] = None
    leader_id: Optional[str] = None

class TeamResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    leader_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class MemberResponse(BaseModel):
    id: str
    user_id: str
    email: str
    first_name: str
    last_name: str
    is_owner: bool
    status: str
    role_name: Optional[str] = None

class InvitationCreate(BaseModel):
    email: EmailStr
    role_id: Optional[str] = None

class InvitationResponse(BaseModel):
    id: str
    email: str
    status: str
    expires_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class AcceptInvitationRequest(BaseModel):
    token: str
