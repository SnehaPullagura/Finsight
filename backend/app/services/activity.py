from datetime import datetime
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.activity import Activity
from backend.app.repositories.activity import ActivityRepository
from backend.app.services.base import BaseService
from backend.app.schemas.activity import ActivityCreate

class ActivityService(BaseService[Activity, ActivityRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(ActivityRepository(db))

    async def create_activity(self, schema_in: ActivityCreate, tenant_id: str, user_id: Optional[str] = None) -> Activity:
        data = schema_in.model_dump(exclude_unset=True)
        if not data.get("performed_at"):
            data["performed_at"] = datetime.utcnow()
        if "metadata_json" not in data or data["metadata_json"] is None:
            data["metadata_json"] = {}
        data["user_id"] = user_id
        return await self.repository.create(data, tenant_id=tenant_id)

    async def get_timeline(self, entity_type: str, entity_id: str, tenant_id: str) -> List[Activity]:
        return await self.repository.get_timeline_for_entity(entity_type, entity_id, tenant_id)
