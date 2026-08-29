from datetime import date, datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class DealProductCreate(BaseModel):
    product_id: Optional[str] = None
    product_name: str
    quantity: int = 1
    unit_price: float
    discount_pct: Optional[float] = 0.0

class DealProductResponse(BaseModel):
    id: str
    product_name: str
    quantity: int
    unit_price: float
    discount_pct: float
    total_amount: float

    class Config:
        from_attributes = True

class DealCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    value: float = Field(default=0.0, ge=0.0)
    currency: Optional[str] = "USD"
    probability: Optional[int] = Field(default=50, ge=0, le=100)
    expected_close_date: Optional[date] = None
    pipeline_id: str
    stage_id: str
    company_id: Optional[str] = None
    contact_id: Optional[str] = None
    owner_id: Optional[str] = None
    products: Optional[List[DealProductCreate]] = None
    custom_fields: Optional[Dict[str, Any]] = None

class DealUpdate(BaseModel):
    name: Optional[str] = None
    value: Optional[float] = None
    currency: Optional[str] = None
    probability: Optional[int] = None
    expected_close_date: Optional[date] = None
    actual_close_date: Optional[date] = None
    pipeline_id: Optional[str] = None
    stage_id: Optional[str] = None
    company_id: Optional[str] = None
    contact_id: Optional[str] = None
    owner_id: Optional[str] = None
    status: Optional[str] = None
    loss_reason: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None

class DealStageTransitionRequest(BaseModel):
    stage_id: str
    loss_reason: Optional[str] = None

class DealResponse(BaseModel):
    id: str
    tenant_id: str
    name: str
    value: float
    currency: str
    probability: int
    expected_close_date: Optional[date] = None
    actual_close_date: Optional[date] = None
    pipeline_id: str
    stage_id: str
    company_id: Optional[str] = None
    contact_id: Optional[str] = None
    owner_id: Optional[str] = None
    status: str
    loss_reason: Optional[str] = None
    custom_fields: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class KanbanColumn(BaseModel):
    stage_id: str
    stage_name: str
    probability: int
    stage_type: str
    deals: List[DealResponse] = []
    total_value: float = 0.0
    deal_count: int = 0

class KanbanBoardResponse(BaseModel):
    pipeline_id: str
    pipeline_name: str
    columns: List[KanbanColumn]
