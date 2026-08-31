from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class ActivityCreate(BaseModel):
    entity_type: str = Field(..., description="contact, company, lead, deal, ticket, proposal")
    entity_id: str
    activity_type: str = Field(..., description="CALL, MEETING, EMAIL, TASK, NOTE, STATUS_CHANGE, FOLLOW_UP")
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    performed_at: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    outcome: Optional[str] = None
    sentiment: Optional[str] = None
    metadata_json: Optional[Dict[str, Any]] = None

class ActivityResponse(BaseModel):
    id: str
    tenant_id: str
    entity_type: str
    entity_id: str
    activity_type: str
    title: str
    description: Optional[str] = None
    performed_at: datetime
    duration_minutes: Optional[int] = None
    outcome: Optional[str] = None
    sentiment: Optional[str] = None
    user_id: Optional[str] = None
    metadata_json: Dict[str, Any] = {}
    created_at: datetime

    class Config:
        from_attributes = True
