import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. models/organization.py
    write_file("backend/app/models/organization.py", """import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, UniqueConstraint, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class Organization(UUIDModel, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    domain: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    plan_tier: Mapped[str] = mapped_column(String(50), default="enterprise", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    logo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    settings: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    members: Mapped[List["OrganizationMember"]] = relationship("OrganizationMember", back_populates="organization", cascade="all, delete-orphan")
    teams: Mapped[List["Team"]] = relationship("Team", back_populates="organization", cascade="all, delete-orphan")
    departments: Mapped[List["Department"]] = relationship("Department", back_populates="organization", cascade="all, delete-orphan")
    invitations: Mapped[List["OrganizationInvitation"]] = relationship("OrganizationInvitation", back_populates="organization", cascade="all, delete-orphan")

class OrganizationMember(UUIDModel, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "organization_members"

    organization_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("roles.id", ondelete="SET NULL"), nullable=True)
    is_owner: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False) # active, suspended, invited

    organization: Mapped["Organization"] = relationship("Organization", back_populates="members")
    user: Mapped["backend.app.models.auth.User"] = relationship("backend.app.models.auth.User")
    role: Mapped[Optional["backend.app.models.auth.Role"]] = relationship("backend.app.models.auth.Role")

    __table_args__ = (UniqueConstraint("organization_id", "user_id", name="uq_org_member"),)

class Team(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "teams"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    leader_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    organization: Mapped["Organization"] = relationship("Organization", back_populates="teams", foreign_keys=["Team.tenant_id"])
    members: Mapped[List["TeamMember"]] = relationship("TeamMember", back_populates="team", cascade="all, delete-orphan")

class TeamMember(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "team_members"

    team_id: Mapped[str] = mapped_column(String(36), ForeignKey("teams.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    team: Mapped["Team"] = relationship("Team", back_populates="members")
    user: Mapped["backend.app.models.auth.User"] = relationship("backend.app.models.auth.User")

    __table_args__ = (UniqueConstraint("team_id", "user_id", name="uq_team_member"),)

class Department(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "departments"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    head_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    organization: Mapped["Organization"] = relationship("Organization", back_populates="departments", foreign_keys=["Department.tenant_id"])

class OrganizationInvitation(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "organization_invitations"

    email: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    role_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("roles.id", ondelete="SET NULL"), nullable=True)
    token: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False) # pending, accepted, revoked

    organization: Mapped["Organization"] = relationship("Organization", back_populates="invitations", foreign_keys=["OrganizationInvitation.tenant_id"])
""")

    # 2. schemas/organization.py
    write_file("backend/app/schemas/organization.py", """from datetime import datetime
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
""")

    # 3. repositories/organization.py
    write_file("backend/app/repositories/organization.py", """from typing import List, Optional
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from backend.app.models.organization import Organization, OrganizationMember, Team, TeamMember, OrganizationInvitation, Department
from backend.app.repositories.base import BaseRepository

class OrganizationRepository(BaseRepository[Organization]):
    def __init__(self, db: AsyncSession):
        super().__init__(Organization, db)

    async def get_by_slug(self, slug: str) -> Optional[Organization]:
        query = select(Organization).where(Organization.slug == slug, Organization.is_deleted == False)
        result = await self.db.execute(query)
        return result.scalars().first()

class OrganizationMemberRepository(BaseRepository[OrganizationMember]):
    def __init__(self, db: AsyncSession):
        super().__init__(OrganizationMember, db)

    async def get_by_org_and_user(self, org_id: str, user_id: str) -> Optional[OrganizationMember]:
        query = select(OrganizationMember).where(
            OrganizationMember.organization_id == org_id,
            OrganizationMember.user_id == user_id,
            OrganizationMember.is_deleted == False
        ).options(selectinload(OrganizationMember.user), selectinload(OrganizationMember.role))
        result = await self.db.execute(query)
        return result.scalars().first()

    async def list_members(self, org_id: str) -> List[OrganizationMember]:
        query = select(OrganizationMember).where(
            OrganizationMember.organization_id == org_id,
            OrganizationMember.is_deleted == False
        ).options(selectinload(OrganizationMember.user), selectinload(OrganizationMember.role))
        result = await self.db.execute(query)
        return list(result.scalars().all())

class TeamRepository(BaseRepository[Team]):
    def __init__(self, db: AsyncSession):
        super().__init__(Team, db)

class InvitationRepository(BaseRepository[OrganizationInvitation]):
    def __init__(self, db: AsyncSession):
        super().__init__(OrganizationInvitation, db)

    async def get_by_token(self, token: str) -> Optional[OrganizationInvitation]:
        query = select(OrganizationInvitation).where(
            OrganizationInvitation.token == token,
            OrganizationInvitation.status == "pending",
            OrganizationInvitation.expires_at > datetime.utcnow()
        )
        result = await self.db.execute(query)
        return result.scalars().first()
""")

    # 4. services/organization.py
    write_file("backend/app/services/organization.py", """import secrets
import re
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.exceptions import ConflictException, EntityNotFoundException, ValidationException
from backend.app.models.organization import Organization, OrganizationMember, Team, OrganizationInvitation
from backend.app.repositories.organization import OrganizationRepository, OrganizationMemberRepository, TeamRepository, InvitationRepository
from backend.app.repositories.auth import UserRepository, RoleRepository
from backend.app.schemas.organization import OrganizationCreate, OrganizationUpdate, TeamCreate, InvitationCreate

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

class OrganizationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.org_repo = OrganizationRepository(db)
        self.member_repo = OrganizationMemberRepository(db)
        self.team_repo = TeamRepository(db)
        self.inv_repo = InvitationRepository(db)
        self.user_repo = UserRepository(db)
        self.role_repo = RoleRepository(db)

    async def create_organization(self, schema_in: OrganizationCreate, owner_user_id: str) -> Organization:
        base_slug = schema_in.slug or slugify(schema_in.name)
        slug = base_slug
        counter = 1
        while await self.org_repo.get_by_slug(slug):
            slug = f"{base_slug}-{counter}"
            counter += 1

        org = await self.org_repo.create({
            "name": schema_in.name,
            "slug": slug,
            "domain": schema_in.domain,
            "plan_tier": schema_in.plan_tier or "enterprise",
            "is_active": True,
            "settings": {}
        })

        # Add creator as owner member
        await self.member_repo.create({
            "organization_id": org.id,
            "user_id": owner_user_id,
            "is_owner": True,
            "status": "active"
        })

        return org

    async def get_organization(self, org_id: str) -> Organization:
        org = await self.org_repo.get_by_id(org_id)
        if not org:
            raise EntityNotFoundException("Organization", org_id)
        return org

    async def update_organization(self, org_id: str, schema_in: OrganizationUpdate) -> Organization:
        org = await self.get_organization(org_id)
        return await self.org_repo.update(org, schema_in.model_dump(exclude_unset=True))

    async def list_members(self, org_id: str) -> List[OrganizationMember]:
        return await self.member_repo.list_members(org_id)

    async def invite_member(self, org_id: str, schema_in: InvitationCreate) -> OrganizationInvitation:
        token = secrets.token_urlsafe(32)
        invitation = await self.inv_repo.create({
            "tenant_id": org_id,
            "email": schema_in.email,
            "role_id": schema_in.role_id,
            "token": token,
            "expires_at": datetime.utcnow() + timedelta(days=7),
            "status": "pending"
        })
        return invitation

    async def accept_invitation(self, token: str, user_id: str) -> OrganizationMember:
        invitation = await self.inv_repo.get_by_token(token)
        if not invitation:
            raise ValidationException("Invalid or expired invitation token.")

        member = await self.member_repo.get_by_org_and_user(invitation.tenant_id, user_id)
        if member:
            raise ConflictException("User is already a member of this organization.")

        new_member = await self.member_repo.create({
            "organization_id": invitation.tenant_id,
            "user_id": user_id,
            "role_id": invitation.role_id,
            "is_owner": False,
            "status": "active"
        })

        await self.inv_repo.update(invitation, {"status": "accepted"})
        return new_member

    async def create_team(self, org_id: str, schema_in: TeamCreate) -> Team:
        return await self.team_repo.create(schema_in.model_dump(), tenant_id=org_id)

    async def list_teams(self, org_id: str) -> List[Team]:
        return await self.team_repo.list(tenant_id=org_id)
""")

    # 5. api/v1/endpoints/organizations.py
    write_file("backend/app/api/v1/endpoints/organizations.py", """from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.organization import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationResponse,
    TeamCreate,
    TeamResponse,
    MemberResponse,
    InvitationCreate,
    InvitationResponse,
    AcceptInvitationRequest
)
from backend.app.services.organization import OrganizationService

router = APIRouter()

@router.post("", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    req: OrganizationCreate,
    current_user: CurrentUserContext = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    org_service = OrganizationService(db)
    org = await org_service.create_organization(req, owner_user_id=current_user.id)
    return org

@router.get("/current", response_model=OrganizationResponse)
async def get_current_organization(
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    org_service = OrganizationService(db)
    return await org_service.get_organization(tenant_id)

@router.put("/current", response_model=OrganizationResponse)
async def update_current_organization(
    req: OrganizationUpdate,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    org_service = OrganizationService(db)
    return await org_service.update_organization(tenant_id, req)

@router.get("/members", response_model=List[MemberResponse])
async def list_organization_members(
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    org_service = OrganizationService(db)
    members = await org_service.list_members(tenant_id)
    return [
        MemberResponse(
            id=m.id,
            user_id=m.user_id,
            email=m.user.email if m.user else "",
            first_name=m.user.first_name if m.user else "",
            last_name=m.user.last_name if m.user else "",
            is_owner=m.is_owner,
            status=m.status,
            role_name=m.role.name if m.role else None
        )
        for m in members
    ]

@router.post("/invitations", response_model=InvitationResponse, status_code=status.HTTP_201_CREATED)
async def invite_member(
    req: InvitationCreate,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    org_service = OrganizationService(db)
    return await org_service.invite_member(tenant_id, req)

@router.post("/invitations/accept", status_code=status.HTTP_200_OK)
async def accept_invitation(
    req: AcceptInvitationRequest,
    current_user: CurrentUserContext = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    org_service = OrganizationService(db)
    await org_service.accept_invitation(req.token, current_user.id)
    return {"message": "Invitation accepted successfully."}

@router.get("/teams", response_model=List[TeamResponse])
async def list_teams(
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    org_service = OrganizationService(db)
    return await org_service.list_teams(tenant_id)

@router.post("/teams", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
async def create_team(
    req: TeamCreate,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    org_service = OrganizationService(db)
    return await org_service.create_team(tenant_id, req)
""")

    # 6. Update api/v1/api.py
    write_file("backend/app/api/v1/api.py", """from fastapi import APIRouter
from backend.app.api.v1.endpoints import health, auth, organizations

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication & Authorization"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["Organizations & Teams"])
""")

    print("Milestone 4 Organizations created successfully!")

if __name__ == '__main__':
    run()
