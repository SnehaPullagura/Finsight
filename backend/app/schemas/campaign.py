from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class SegmentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = None
    target_entity: Optional[str] = "contact"
    filter_criteria: Optional[Dict[str, Any]] = None

class SegmentResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    target_entity: str
    filter_criteria: Dict[str, Any] = {}
    created_at: datetime

    class Config:
        from_attributes = True

class CampaignCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    type: Optional[str] = "email"
    segment_id: Optional[str] = None
    template_id: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    budget: Optional[float] = None

class CampaignResponse(BaseModel):
    id: str
    tenant_id: str
    name: str
    type: str
    status: str
    segment_id: Optional[str] = None
    template_id: Optional[str] = None
    total_recipients: int
    sent_count: int
    open_count: int
    click_count: int
    conversion_count: int
    revenue_attributed: float
    created_at: datetime

    class Config:
        from_attributes = True
