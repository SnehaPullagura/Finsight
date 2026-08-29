from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, EmailStr, Field

class ContactCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    secondary_email: Optional[EmailStr] = None
    phone: Optional[str] = None
    mobile_phone: Optional[str] = None
    title: Optional[str] = None
    department: Optional[str] = None
    company_id: Optional[str] = None
    owner_id: Optional[str] = None
    lifecycle_stage: Optional[str] = "lead"
    lead_source: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    linkedin_url: Optional[str] = None
    twitter_handle: Optional[str] = None
    is_do_not_call: Optional[bool] = False
    is_do_not_email: Optional[bool] = False
    custom_fields: Optional[Dict[str, Any]] = None

class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    secondary_email: Optional[EmailStr] = None
    phone: Optional[str] = None
    mobile_phone: Optional[str] = None
    title: Optional[str] = None
    department: Optional[str] = None
    company_id: Optional[str] = None
    owner_id: Optional[str] = None
    lifecycle_stage: Optional[str] = None
    lead_source: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    linkedin_url: Optional[str] = None
    twitter_handle: Optional[str] = None
    is_do_not_call: Optional[bool] = None
    is_do_not_email: Optional[bool] = None
    custom_fields: Optional[Dict[str, Any]] = None

class ContactResponse(BaseModel):
    id: str
    tenant_id: str
    first_name: str
    last_name: str
    email: str
    secondary_email: Optional[str] = None
    phone: Optional[str] = None
    mobile_phone: Optional[str] = None
    title: Optional[str] = None
    department: Optional[str] = None
    company_id: Optional[str] = None
    owner_id: Optional[str] = None
    lifecycle_stage: str
    lead_source: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    linkedin_url: Optional[str] = None
    is_do_not_call: bool
    is_do_not_email: bool
    custom_fields: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ContactDeduplicationResult(BaseModel):
    potential_duplicates: List[ContactResponse]
    match_reasons: List[str]
