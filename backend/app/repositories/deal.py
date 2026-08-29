from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from backend.app.models.deal import Deal, DealStageHistory, DealProduct
from backend.app.repositories.base import BaseRepository

class DealRepository(BaseRepository[Deal]):
    def __init__(self, db: AsyncSession):
        super().__init__(Deal, db)

    async def get_with_relations(self, id: str, tenant_id: str) -> Optional[Deal]:
        query = select(Deal).where(
            Deal.id == id,
            Deal.tenant_id == tenant_id,
            Deal.is_deleted == False
        ).options(
            selectinload(Deal.stage),
            selectinload(Deal.pipeline),
            selectinload(Deal.products),
            selectinload(Deal.stage_history)
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def list_by_pipeline(self, pipeline_id: str, tenant_id: str) -> List[Deal]:
        query = select(Deal).where(
            Deal.pipeline_id == pipeline_id,
            Deal.tenant_id == tenant_id,
            Deal.is_deleted == False
        ).order_by(Deal.created_at.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())

class DealStageHistoryRepository(BaseRepository[DealStageHistory]):
    def __init__(self, db: AsyncSession):
        super().__init__(DealStageHistory, db)
