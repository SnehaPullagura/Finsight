from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.lead import Lead, LeadScoringRule
from backend.app.repositories.base import BaseRepository

class LeadRepository(BaseRepository[Lead]):
    def __init__(self, db: AsyncSession):
        super().__init__(Lead, db)

    async def get_by_email(self, email: str, tenant_id: str) -> Optional[Lead]:
        query = select(Lead).where(
            Lead.tenant_id == tenant_id,
            Lead.email == email,
            Lead.is_deleted == False
        )
        result = await self.db.execute(query)
        return result.scalars().first()

class LeadScoringRuleRepository(BaseRepository[LeadScoringRule]):
    def __init__(self, db: AsyncSession):
        super().__init__(LeadScoringRule, db)

    async def list_active_rules(self, tenant_id: str) -> List[LeadScoringRule]:
        query = select(LeadScoringRule).where(
            LeadScoringRule.tenant_id == tenant_id,
            LeadScoringRule.is_active == True
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
