from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, Field

class CustomFieldDefinitionCreate(BaseModel):
    entity_type: str = Field(..., description="contact, company, lead, deal, ticket")
    field_name: str = Field(min_length=1, max_length=100)
    field_key: str = Field(min_length=1, max_length=100)
    field_type: str = Field(..., description="text, number, boolean, date, datetime, select, multiselect, currency, url")
    options_list: Optional[List[str]] = None
    is_required: Optional[bool] = False
    default_value: Optional[str] = None

class CustomFieldDefinitionResponse(BaseModel):
    id: str
    tenant_id: str
    entity_type: str
    field_name: str
    field_key: str
    field_type: str
    options_list: List[str] = []
    is_required: bool
    default_value: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
