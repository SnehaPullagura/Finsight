import secrets
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
