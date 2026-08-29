from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class AuditLogCreate(BaseModel):
    action: str = Field(..., description="CREATE, UPDATE, DELETE, STAGE_CHANGE, LOGIN, EXPORT")
    entity_type: str
    entity_id: str
    before_snapshot: Optional[Dict[str, Any]] = None
    after_snapshot: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class AuditLogResponse(BaseModel):
    id: str
    tenant_id: str
    actor_id: Optional[str] = None
    actor_email: Optional[str] = None
    action: str
    entity_type: str
    entity_id: str
    before_snapshot: dict = {}
    after_snapshot: dict = {}
    ip_address: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True
