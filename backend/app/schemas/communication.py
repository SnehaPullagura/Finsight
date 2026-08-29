from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, EmailStr, Field

class SendMessageRequest(BaseModel):
    channel: str = Field("email", description="email, sms, internal_message")
    recipient: str
    subject: Optional[str] = None
    body_text: str
    body_html: Optional[str] = None
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    template_id: Optional[str] = None
    template_vars: Optional[Dict[str, Any]] = None

class CommunicationMessageResponse(BaseModel):
    id: str
    tenant_id: str
    channel: str
    sender: str
    recipient: str
    subject: Optional[str] = None
    body_text: str
    body_html: Optional[str] = None
    status: str
    tracking_id: Optional[str] = None
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    sent_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class CommunicationTemplateCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    channel: Optional[str] = "email"
    category: Optional[str] = "general"
    subject_template: Optional[str] = None
    body_template: str
    available_variables: Optional[List[str]] = None

class CommunicationTemplateResponse(BaseModel):
    id: str
    name: str
    channel: str
    category: str
    subject_template: Optional[str] = None
    body_template: str
    available_variables: List[str] = []
    created_at: datetime

    class Config:
        from_attributes = True
