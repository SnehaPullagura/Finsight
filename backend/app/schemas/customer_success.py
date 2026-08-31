from datetime import date, datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class MilestoneCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    due_date: Optional[date] = None

class MilestoneResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    is_completed: bool
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SuccessPlanCreate(BaseModel):
    company_id: str
    owner_id: Optional[str] = None
    status: Optional[str] = "onboarding"
    target_renewal_date: Optional[date] = None
    renewal_value: Optional[float] = None
    goals: Optional[List[str]] = None

class SuccessPlanResponse(BaseModel):
    id: str
    tenant_id: str
    company_id: str
    owner_id: Optional[str] = None
    status: str
    health_score: int
    health_grade: str
    target_renewal_date: Optional[date] = None
    renewal_value: Optional[float] = None
    churn_risk_reason: Optional[str] = None
    goals: List[str] = []
    milestones: List[MilestoneResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True
