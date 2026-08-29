from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class TicketCommentCreate(BaseModel):
    body: str = Field(min_length=1)
    is_internal: Optional[bool] = False

class TicketCommentResponse(BaseModel):
    id: str
    author_id: Optional[str] = None
    body: str
    is_internal: bool
    created_at: datetime

    class Config:
        from_attributes = True

class TicketCreate(BaseModel):
    subject: str = Field(min_length=1, max_length=255)
    description: str
    priority: Optional[str] = "medium"
    category: Optional[str] = "technical"
    contact_id: Optional[str] = None
    company_id: Optional[str] = None
    assigned_to_id: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None

class TicketUpdate(BaseModel):
    subject: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    category: Optional[str] = None
    assigned_to_id: Optional[str] = None
    is_escalated: Optional[bool] = None
    custom_fields: Optional[Dict[str, Any]] = None

class TicketResolveRequest(BaseModel):
    resolution_notes: str

class TicketResponse(BaseModel):
    id: str
    tenant_id: str
    ticket_number: str
    subject: str
    description: str
    priority: str
    status: str
    category: str
    contact_id: Optional[str] = None
    company_id: Optional[str] = None
    assigned_to_id: Optional[str] = None
    is_escalated: bool
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
