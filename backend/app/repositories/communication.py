from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.communication import CommunicationMessage, CommunicationTemplate
from backend.app.repositories.base import BaseRepository

class CommunicationRepository(BaseRepository[CommunicationMessage]):
    def __init__(self, db: AsyncSession):
        super().__init__(CommunicationMessage, db)

    async def list_for_entity(self, entity_type: str, entity_id: str, tenant_id: str) -> List[CommunicationMessage]:
        query = select(CommunicationMessage).where(
            CommunicationMessage.tenant_id == tenant_id,
            CommunicationMessage.entity_type == entity_type,
            CommunicationMessage.entity_id == entity_id,
            CommunicationMessage.is_deleted == False
        ).order_by(CommunicationMessage.created_at.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())

class TemplateRepository(BaseRepository[CommunicationTemplate]):
    def __init__(self, db: AsyncSession):
        super().__init__(CommunicationTemplate, db)
