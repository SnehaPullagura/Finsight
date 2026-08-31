from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.activity import Activity
from backend.app.repositories.base import BaseRepository

class ActivityRepository(BaseRepository[Activity]):
    def __init__(self, db: AsyncSession):
        super().__init__(Activity, db)

    async def get_timeline_for_entity(self, entity_type: str, entity_id: str, tenant_id: str, limit: int = 100) -> List[Activity]:
        query = select(Activity).where(
            Activity.tenant_id == tenant_id,
            Activity.entity_type == entity_type,
            Activity.entity_id == entity_id,
            Activity.is_deleted == False
        ).order_by(Activity.performed_at.desc()).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())
