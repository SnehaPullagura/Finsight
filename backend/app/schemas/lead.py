from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, EmailStr, Field

class LeadCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = None
    company_name: Optional[str] = None
    title: Optional[str] = None
    source: Optional[str] = "website"
    estimated_budget: Optional[float] = None
    employee_count: Optional[int] = None
    industry: Optional[str] = None
    intent_score: Optional[int] = Field(default=50, ge=0, le=100)
    engagement_count: Optional[int] = 0
    owner_id: Optional[str] = None
    notes: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None

class LeadUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company_name: Optional[str] = None
    title: Optional[str] = None
    status: Optional[str] = None
    source: Optional[str] = None
    estimated_budget: Optional[float] = None
    employee_count: Optional[int] = None
    industry: Optional[str] = None
    intent_score: Optional[int] = None
    engagement_count: Optional[int] = None
    owner_id: Optional[str] = None
    notes: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None

class LeadResponse(BaseModel):
    id: str
    tenant_id: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    company_name: Optional[str] = None
    title: Optional[str] = None
    status: str
    source: str
    score: int
    qualification_grade: str
    qualification_details: Dict[str, Any] = {}
    estimated_budget: Optional[float] = None
    employee_count: Optional[int] = None
    industry: Optional[str] = None
    intent_score: int
    engagement_count: int
    owner_id: Optional[str] = None
    converted_at: Optional[datetime] = None
    converted_contact_id: Optional[str] = None
    converted_company_id: Optional[str] = None
    converted_deal_id: Optional[str] = None
    notes: Optional[str] = None
    custom_fields: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class LeadConvertRequest(BaseModel):
    create_deal: bool = True
    deal_name: Optional[str] = None
    deal_value: Optional[float] = None
    pipeline_id: Optional[str] = None
    stage_id: Optional[str] = None

class LeadConvertResponse(BaseModel):
    lead_id: str
    contact_id: str
    company_id: Optional[str] = None
    deal_id: Optional[str] = None
    message: str

class LeadScoringRuleCreate(BaseModel):
    name: str
    criteria_type: str # budget, company_size, industry, engagement, intent
    operator: str # gt, gte, lt, lte, eq, in, contains
    target_value: str
    score_weight: int = 10

class LeadScoringRuleResponse(BaseModel):
    id: str
    name: str
    criteria_type: str
    operator: str
    target_value: str
    score_weight: int
    is_active: bool

    class Config:
        from_attributes = True
