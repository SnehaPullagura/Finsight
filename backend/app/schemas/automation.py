from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class ConditionInput(BaseModel):
    field_path: str
    operator: str
    target_value: str

class ConditionOutput(BaseModel):
    id: str
    field_path: str
    operator: str
    target_value: str

    class Config:
        from_attributes = True

class ActionInput(BaseModel):
    action_type: str
    action_config: Dict[str, Any]
    execution_order: Optional[int] = 1

class ActionOutput(BaseModel):
    id: str
    action_type: str
    action_config: Dict[str, Any]
    execution_order: int

    class Config:
        from_attributes = True

class WorkflowCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    trigger_event: str
    trigger_config: Optional[Dict[str, Any]] = None
    conditions: List[ConditionInput] = []
    actions: List[ActionInput] = []

class WorkflowResponse(BaseModel):
    id: str
    tenant_id: str
    name: str
    description: Optional[str] = None
    is_active: bool
    trigger_event: str
    conditions: List[ConditionOutput] = []
    actions: List[ActionOutput] = []
    created_at: datetime

    class Config:
        from_attributes = True

class WorkflowTriggerRequest(BaseModel):
    event_name: str
    entity_type: str
    entity_id: str
    payload: Dict[str, Any] = {}

class ExecutionLogResponse(BaseModel):
    id: str
    workflow_id: str
    entity_type: str
    entity_id: str
    status: str
    error_message: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
