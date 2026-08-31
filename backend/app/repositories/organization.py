from typing import List, Optional
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
