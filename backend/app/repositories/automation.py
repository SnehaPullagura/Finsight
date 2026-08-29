from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from backend.app.models.automation import AutomationWorkflow, WorkflowCondition, WorkflowAction, WorkflowExecutionLog
from backend.app.repositories.base import BaseRepository

class WorkflowRepository(BaseRepository[AutomationWorkflow]):
    def __init__(self, db: AsyncSession):
        super().__init__(AutomationWorkflow, db)

    async def get_with_rules(self, id: str, tenant_id: str) -> Optional[AutomationWorkflow]:
        query = select(AutomationWorkflow).where(
            AutomationWorkflow.id == id,
            AutomationWorkflow.tenant_id == tenant_id,
            AutomationWorkflow.is_deleted == False
        ).options(selectinload(AutomationWorkflow.conditions), selectinload(AutomationWorkflow.actions))
        result = await self.db.execute(query)
        return result.scalars().first()

    async def list_active_by_trigger(self, trigger_event: str, tenant_id: str) -> List[AutomationWorkflow]:
        query = select(AutomationWorkflow).where(
            AutomationWorkflow.tenant_id == tenant_id,
            AutomationWorkflow.trigger_event == trigger_event,
            AutomationWorkflow.is_active == True,
            AutomationWorkflow.is_deleted == False
        ).options(selectinload(AutomationWorkflow.conditions), selectinload(AutomationWorkflow.actions))
        result = await self.db.execute(query)
        return list(result.scalars().all())

class ExecutionLogRepository(BaseRepository[WorkflowExecutionLog]):
    def __init__(self, db: AsyncSession):
        super().__init__(WorkflowExecutionLog, db)
