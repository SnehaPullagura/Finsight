from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, EmailStr, Field

class EventAttendeeCreate(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    status: Optional[str] = "accepted"

class EventAttendeeResponse(BaseModel):
    id: str
    email: str
    name: Optional[str] = None
    status: str
    is_organizer: bool

    class Config:
        from_attributes = True

class CalendarEventCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    location: Optional[str] = None
    meeting_url: Optional[str] = None
    start_time: datetime
    end_time: datetime
    is_all_day: Optional[bool] = False
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    attendees: Optional[List[EventAttendeeCreate]] = None

class CalendarEventResponse(BaseModel):
    id: str
    tenant_id: str
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    meeting_url: Optional[str] = None
    start_time: datetime
    end_time: datetime
    is_all_day: bool
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    organizer_id: str
    attendees: List[EventAttendeeResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True
