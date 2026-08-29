from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.custom_field import CustomFieldDefinition
from backend.app.repositories.base import BaseRepository

class CustomFieldRepository(BaseRepository[CustomFieldDefinition]):
    def __init__(self, session: AsyncSession):
        super().__init__(CustomFieldDefinition, session)

    async def get_by_entity_and_key(self, tenant_id: str, entity_type: str, field_key: str) -> Optional[CustomFieldDefinition]:
        stmt = select(CustomFieldDefinition).where(
            and_(
                CustomFieldDefinition.tenant_id == tenant_id,
                CustomFieldDefinition.entity_type == entity_type,
                CustomFieldDefinition.field_key == field_key
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list_by_entity_type(self, tenant_id: str, entity_type: str) -> List[CustomFieldDefinition]:
        stmt = select(CustomFieldDefinition).where(
            and_(
                CustomFieldDefinition.tenant_id == tenant_id,
                CustomFieldDefinition.entity_type == entity_type
            )
        ).order_by(CustomFieldDefinition.created_at.asc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
