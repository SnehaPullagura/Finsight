from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.audit import AuditLog
from backend.app.repositories.audit import AuditLogRepository
from backend.app.schemas.audit import AuditLogCreate
from backend.app.services.base import BaseService

class AuditLogService(BaseService[AuditLog, AuditLogRepository]):
    def __init__(self, session: AsyncSession):
        super().__init__(AuditLogRepository(session), session)

    async def log_event(
        self,
        tenant_id: str,
        action: str,
        entity_type: str,
        entity_id: str,
        actor_id: Optional[str] = None,
        actor_email: Optional[str] = None,
        before_snapshot: Optional[Dict[str, Any]] = None,
        after_snapshot: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> AuditLog:
        payload = {
            "tenant_id": tenant_id,
            "actor_id": actor_id,
            "actor_email": actor_email,
            "action": action.upper(),
            "entity_type": entity_type.lower(),
            "entity_id": entity_id,
            "before_snapshot": before_snapshot or {},
            "after_snapshot": after_snapshot or {},
            "ip_address": ip_address,
            "user_agent": user_agent
        }
        return await self.repository.create(payload)

    async def get_entity_history(self, tenant_id: str, entity_type: str, entity_id: str) -> List[AuditLog]:
        return await self.repository.list_logs(
            tenant_id=tenant_id,
            entity_type=entity_type,
            entity_id=entity_id,
            limit=100
        )
