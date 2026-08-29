from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class PipelineStageCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    stage_order: int = 0
    probability: int = Field(default=50, ge=0, le=100)
    stage_type: Optional[str] = "open"
    sla_days: Optional[int] = None
    required_fields: Optional[Dict[str, Any]] = None

class PipelineStageResponse(BaseModel):
    id: str
    pipeline_id: str
    name: str
    stage_order: int
    probability: int
    stage_type: str
    sla_days: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class PipelineCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = None
    is_default: Optional[bool] = False
    stages: Optional[List[PipelineStageCreate]] = None

class PipelineUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_default: Optional[bool] = None
    is_active: Optional[bool] = None

class PipelineResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    is_default: bool
    is_active: bool
    stages: List[PipelineStageResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True
