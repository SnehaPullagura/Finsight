from datetime import datetime
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.task import Task
from backend.app.repositories.task import TaskRepository
from backend.app.services.base import BaseService
from backend.app.schemas.task import TaskCreate, TaskUpdate

class TaskService(BaseService[Task, TaskRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(TaskRepository(db))

    async def create_task(self, schema_in: TaskCreate, tenant_id: str, user_id: Optional[str] = None) -> Task:
        data = schema_in.model_dump(exclude_unset=True)
        data["created_by_id"] = user_id
        if not data.get("assigned_to_id"):
            data["assigned_to_id"] = user_id
        return await self.repository.create(data, tenant_id=tenant_id)

    async def complete_task(self, task_id: str, tenant_id: str) -> Task:
        task = await self.get(task_id, tenant_id=tenant_id)
        return await self.repository.update(task, {
            "status": "completed",
            "completed_at": datetime.utcnow()
        })
