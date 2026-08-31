from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from backend.app.models.customer_success import CustomerSuccessPlan, OnboardingMilestone
from backend.app.repositories.base import BaseRepository

class SuccessPlanRepository(BaseRepository[CustomerSuccessPlan]):
    def __init__(self, db: AsyncSession):
        super().__init__(CustomerSuccessPlan, db)

    async def get_with_milestones(self, id: str, tenant_id: str) -> Optional[CustomerSuccessPlan]:
        query = select(CustomerSuccessPlan).where(
            CustomerSuccessPlan.id == id,
            CustomerSuccessPlan.tenant_id == tenant_id,
            CustomerSuccessPlan.is_deleted == False
        ).options(selectinload(CustomerSuccessPlan.milestones))
        result = await self.db.execute(query)
        return result.scalars().first()
