from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class CompanyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    legal_name: Optional[str] = None
    domain: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    annual_revenue: Optional[float] = None
    currency: Optional[str] = "USD"
    employee_count: Optional[int] = None
    parent_company_id: Optional[str] = None
    owner_id: Optional[str] = None
    phone: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    linkedin_url: Optional[str] = None
    description: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    legal_name: Optional[str] = None
    domain: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    annual_revenue: Optional[float] = None
    currency: Optional[str] = None
    employee_count: Optional[int] = None
    parent_company_id: Optional[str] = None
    owner_id: Optional[str] = None
    phone: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    linkedin_url: Optional[str] = None
    description: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None

class CompanyResponse(BaseModel):
    id: str
    tenant_id: str
    name: str
    legal_name: Optional[str] = None
    domain: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    annual_revenue: Optional[float] = None
    currency: str
    employee_count: Optional[int] = None
    parent_company_id: Optional[str] = None
    owner_id: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    linkedin_url: Optional[str] = None
    description: Optional[str] = None
    custom_fields: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
