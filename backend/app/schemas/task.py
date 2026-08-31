from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    due_date: Optional[datetime] = None
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    assigned_to_id: Optional[str] = None
    is_recurring: Optional[bool] = False
    recurrence_rule: Optional[str] = None
    reminder_minutes_before: Optional[int] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None
    assigned_to_id: Optional[str] = None

class TaskResponse(BaseModel):
    id: str
    tenant_id: str
    title: str
    description: Optional[str] = None
    priority: str
    status: str
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    assigned_to_id: Optional[str] = None
    created_by_id: Optional[str] = None
    is_recurring: bool
    recurrence_rule: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
