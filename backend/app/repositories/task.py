from typing import List, Optional
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.task import Task
from backend.app.repositories.base import BaseRepository

class TaskRepository(BaseRepository[Task]):
    def __init__(self, db: AsyncSession):
        super().__init__(Task, db)

    async def list_user_tasks(self, user_id: str, tenant_id: str) -> List[Task]:
        query = select(Task).where(
            Task.tenant_id == tenant_id,
            Task.assigned_to_id == user_id,
            Task.is_deleted == False
        ).order_by(Task.due_date.asc().nullslast())
        result = await self.db.execute(query)
        return list(result.scalars().all())
