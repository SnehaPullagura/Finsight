import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. models/activity.py, models/task.py, models/calendar.py
    write_file("backend/app/models/activity.py", """import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class Activity(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "activities"

    # Polymorphic entity association
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # contact, company, lead, deal, ticket, proposal
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    
    activity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # CALL, MEETING, EMAIL, TASK, NOTE, STATUS_CHANGE, FOLLOW_UP
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Execution metadata
    performed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Outcomes & sentiment
    outcome: Mapped[Optional[str]] = mapped_column(String(100), nullable=True) # connected, left_voicemail, no_answer, scheduled_meeting, resolved
    sentiment: Mapped[Optional[str]] = mapped_column(String(20), nullable=True) # positive, neutral, negative
    
    user_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    user: Mapped[Optional["backend.app.models.auth.User"]] = relationship("backend.app.models.auth.User")
    participants: Mapped[List["ActivityParticipant"]] = relationship("ActivityParticipant", back_populates="activity", cascade="all, delete-orphan")

class ActivityParticipant(UUIDModel):
    __tablename__ = "activity_participants"

    activity_id: Mapped[str] = mapped_column(String(36), ForeignKey("activities.id", ondelete="CASCADE"), nullable=False, index=True)
    participant_type: Mapped[str] = mapped_column(String(50), nullable=False) # contact, user, lead
    participant_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(50), default="attendee", nullable=False) # host, attendee, organizer

    activity: Mapped["Activity"] = relationship("Activity", back_populates="participants")
""")

    write_file("backend/app/models/task.py", """import uuid
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class Task(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "tasks"

    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    priority: Mapped[str] = mapped_column(String(20), default="medium", nullable=False, index=True) # urgent, high, medium, low
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False, index=True) # pending, in_progress, completed, cancelled
    
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Associated CRM entity
    entity_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True) # contact, company, lead, deal, ticket
    entity_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True, index=True)
    
    assigned_to_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    created_by_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # Recurrence & reminders
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    recurrence_rule: Mapped[Optional[str]] = mapped_column(String(100), nullable=True) # daily, weekly, monthly, cron
    reminder_minutes_before: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    assigned_to: Mapped[Optional["backend.app.models.auth.User"]] = relationship("backend.app.models.auth.User", foreign_keys=[assigned_to_id])
    created_by: Mapped[Optional["backend.app.models.auth.User"]] = relationship("backend.app.models.auth.User", foreign_keys=[created_by_id])
""")

    write_file("backend/app/models/calendar.py", """import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class CalendarEvent(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "calendar_events"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    meeting_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    is_all_day: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Associated CRM entity
    entity_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    entity_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True, index=True)
    
    organizer_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    recurrence_rule: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    organizer: Mapped["backend.app.models.auth.User"] = relationship("backend.app.models.auth.User")
    attendees: Mapped[List["EventAttendee"]] = relationship("EventAttendee", back_populates="event", cascade="all, delete-orphan")

class EventAttendee(UUIDModel, TimestampMixin):
    __tablename__ = "event_attendees"

    event_id: Mapped[str] = mapped_column(String(36), ForeignKey("calendar_events.id", ondelete="CASCADE"), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="accepted", nullable=False) # accepted, declined, tentative, needs_action
    is_organizer: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    event: Mapped["CalendarEvent"] = relationship("CalendarEvent", back_populates="attendees")
""")

    # 2. Schemas
    write_file("backend/app/schemas/activity.py", """from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class ActivityCreate(BaseModel):
    entity_type: str = Field(..., description="contact, company, lead, deal, ticket, proposal")
    entity_id: str
    activity_type: str = Field(..., description="CALL, MEETING, EMAIL, TASK, NOTE, STATUS_CHANGE, FOLLOW_UP")
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    performed_at: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    outcome: Optional[str] = None
    sentiment: Optional[str] = None
    metadata_json: Optional[Dict[str, Any]] = None

class ActivityResponse(BaseModel):
    id: str
    tenant_id: str
    entity_type: str
    entity_id: str
    activity_type: str
    title: str
    description: Optional[str] = None
    performed_at: datetime
    duration_minutes: Optional[int] = None
    outcome: Optional[str] = None
    sentiment: Optional[str] = None
    user_id: Optional[str] = None
    metadata_json: Dict[str, Any] = {}
    created_at: datetime

    class Config:
        from_attributes = True
""")

    write_file("backend/app/schemas/task.py", """from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    due_date: Optional[datetime] = None
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    assigned_to_id: Optional[str] = None
    is_recurring: Optional[bool] = False
    recurrence_rule: Optional[str] = None
    reminder_minutes_before: Optional[int] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None
    assigned_to_id: Optional[str] = None

class TaskResponse(BaseModel):
    id: str
    tenant_id: str
    title: str
    description: Optional[str] = None
    priority: str
    status: str
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    assigned_to_id: Optional[str] = None
    created_by_id: Optional[str] = None
    is_recurring: bool
    recurrence_rule: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
""")

    write_file("backend/app/schemas/calendar.py", """from datetime import datetime
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
""")

    # 3. Repositories
    write_file("backend/app/repositories/activity.py", """from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.activity import Activity
from backend.app.repositories.base import BaseRepository

class ActivityRepository(BaseRepository[Activity]):
    def __init__(self, db: AsyncSession):
        super().__init__(Activity, db)

    async def get_timeline_for_entity(self, entity_type: str, entity_id: str, tenant_id: str, limit: int = 100) -> List[Activity]:
        query = select(Activity).where(
            Activity.tenant_id == tenant_id,
            Activity.entity_type == entity_type,
            Activity.entity_id == entity_id,
            Activity.is_deleted == False
        ).order_by(Activity.performed_at.desc()).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())
""")

    write_file("backend/app/repositories/task.py", """from typing import List, Optional
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.task import Task
from backend.app.repositories.base import BaseRepository

class TaskRepository(BaseRepository[Task]):
    def __init__(self, db: AsyncSession):
        super().__init__(Task, db)

    async def list_user_tasks(self, user_id: str, tenant_id: str) -> List[Task]:
        query = select(Task).where(
            Task.tenant_id == tenant_id,
            Task.assigned_to_id == user_id,
            Task.is_deleted == False
        ).order_by(Task.due_date.asc().nullslast())
        result = await self.db.execute(query)
        return list(result.scalars().all())
""")

    write_file("backend/app/repositories/calendar.py", """from typing import List, Optional
from datetime import datetime
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from backend.app.models.calendar import CalendarEvent, EventAttendee
from backend.app.repositories.base import BaseRepository

class CalendarRepository(BaseRepository[CalendarEvent]):
    def __init__(self, db: AsyncSession):
        super().__init__(CalendarEvent, db)

    async def get_events_between(self, start: datetime, end: datetime, tenant_id: str) -> List[CalendarEvent]:
        query = select(CalendarEvent).where(
            CalendarEvent.tenant_id == tenant_id,
            CalendarEvent.is_deleted == False,
            CalendarEvent.start_time <= end,
            CalendarEvent.end_time >= start
        ).options(selectinload(CalendarEvent.attendees)).order_by(CalendarEvent.start_time.asc())
        result = await self.db.execute(query)
        return list(result.scalars().all())
""")

    # 4. Services
    write_file("backend/app/services/activity.py", """from datetime import datetime
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.activity import Activity
from backend.app.repositories.activity import ActivityRepository
from backend.app.services.base import BaseService
from backend.app.schemas.activity import ActivityCreate

class ActivityService(BaseService[Activity, ActivityRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(ActivityRepository(db))

    async def create_activity(self, schema_in: ActivityCreate, tenant_id: str, user_id: Optional[str] = None) -> Activity:
        data = schema_in.model_dump(exclude_unset=True)
        if not data.get("performed_at"):
            data["performed_at"] = datetime.utcnow()
        if "metadata_json" not in data or data["metadata_json"] is None:
            data["metadata_json"] = {}
        data["user_id"] = user_id
        return await self.repository.create(data, tenant_id=tenant_id)

    async def get_timeline(self, entity_type: str, entity_id: str, tenant_id: str) -> List[Activity]:
        return await self.repository.get_timeline_for_entity(entity_type, entity_id, tenant_id)
""")

    write_file("backend/app/services/task.py", """from datetime import datetime
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.task import Task
from backend.app.repositories.task import TaskRepository
from backend.app.services.base import BaseService
from backend.app.schemas.task import TaskCreate, TaskUpdate

class TaskService(BaseService[Task, TaskRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(TaskRepository(db))

    async def create_task(self, schema_in: TaskCreate, tenant_id: str, user_id: Optional[str] = None) -> Task:
        data = schema_in.model_dump(exclude_unset=True)
        data["created_by_id"] = user_id
        if not data.get("assigned_to_id"):
            data["assigned_to_id"] = user_id
        return await self.repository.create(data, tenant_id=tenant_id)

    async def complete_task(self, task_id: str, tenant_id: str) -> Task:
        task = await self.get(task_id, tenant_id=tenant_id)
        return await self.repository.update(task, {
            "status": "completed",
            "completed_at": datetime.utcnow()
        })
""")

    write_file("backend/app/services/calendar.py", """from datetime import datetime
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.calendar import CalendarEvent, EventAttendee
from backend.app.repositories.calendar import CalendarRepository
from backend.app.services.base import BaseService
from backend.app.schemas.calendar import CalendarEventCreate

class CalendarService(BaseService[CalendarEvent, CalendarRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(CalendarRepository(db))

    async def create_event(self, schema_in: CalendarEventCreate, tenant_id: str, organizer_id: str) -> CalendarEvent:
        data = schema_in.model_dump(exclude_unset=True, exclude={"attendees"})
        data["organizer_id"] = organizer_id
        event = await self.repository.create(data, tenant_id=tenant_id)

        if schema_in.attendees:
            for att in schema_in.attendees:
                att_obj = EventAttendee(
                    event_id=event.id,
                    email=att.email,
                    name=att.name,
                    status=att.status or "accepted"
                )
                self.repository.db.add(att_obj)
            await self.repository.db.flush()
        
        return event

    async def get_events(self, start: datetime, end: datetime, tenant_id: str) -> List[CalendarEvent]:
        return await self.repository.get_events_between(start, end, tenant_id)
""")

    # 5. Endpoints
    write_file("backend/app/api/v1/endpoints/activities.py", """from fastapi import APIRouter, Depends, Query, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.activity import ActivityCreate, ActivityResponse
from backend.app.services.activity import ActivityService

router = APIRouter()

@router.post("", response_model=ActivityResponse, status_code=status.HTTP_201_CREATED)
async def create_activity(
    req: ActivityCreate,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = ActivityService(db)
    return await service.create_activity(req, tenant_id=tenant_id, user_id=current_user.id)

@router.get("/timeline/{entity_type}/{entity_id}", response_model=List[ActivityResponse])
async def get_entity_timeline(
    entity_type: str,
    entity_id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = ActivityService(db)
    return await service.get_timeline(entity_type, entity_id, tenant_id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_activity(
    id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = ActivityService(db)
    await service.delete(id, tenant_id=tenant_id)
""")

    write_file("backend/app/api/v1/endpoints/tasks.py", """from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from backend.app.services.task import TaskService

router = APIRouter()

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    req: TaskCreate,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = TaskService(db)
    return await service.create_task(req, tenant_id=tenant_id, user_id=current_user.id)

@router.get("", response_model=List[TaskResponse])
async def list_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    assigned_to_id: Optional[str] = None,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = TaskService(db)
    filters = {}
    if status:
        filters["status"] = status
    if priority:
        filters["priority"] = priority
    if assigned_to_id:
        filters["assigned_to_id"] = assigned_to_id
    return await service.list(tenant_id=tenant_id, filters=filters)

@router.get("/{id}", response_model=TaskResponse)
async def get_task(
    id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = TaskService(db)
    return await service.get(id, tenant_id=tenant_id)

@router.put("/{id}", response_model=TaskResponse)
async def update_task(
    id: str,
    req: TaskUpdate,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = TaskService(db)
    return await service.update(id, req, tenant_id=tenant_id)

@router.post("/{id}/complete", response_model=TaskResponse)
async def complete_task(
    id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = TaskService(db)
    return await service.complete_task(id, tenant_id=tenant_id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = TaskService(db)
    await service.delete(id, tenant_id=tenant_id)
""")

    write_file("backend/app/api/v1/endpoints/calendar.py", """from fastapi import APIRouter, Depends, Query, status
from datetime import datetime, timedelta
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.calendar import CalendarEventCreate, CalendarEventResponse
from backend.app.services.calendar import CalendarService

router = APIRouter()

@router.post("/events", response_model=CalendarEventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    req: CalendarEventCreate,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CalendarService(db)
    return await service.create_event(req, tenant_id=tenant_id, organizer_id=current_user.id)

@router.get("/events", response_model=List[CalendarEventResponse])
async def list_events(
    start: Optional[datetime] = Query(None),
    end: Optional[datetime] = Query(None),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CalendarService(db)
    start_dt = start or (datetime.utcnow() - timedelta(days=30))
    end_dt = end or (datetime.utcnow() + timedelta(days=60))
    return await service.get_events(start_dt, end_dt, tenant_id=tenant_id)
""")

    # 6. Update api/v1/api.py
    write_file("backend/app/api/v1/api.py", """from fastapi import APIRouter
from backend.app.api.v1.endpoints import (
    health, auth, organizations, contacts, companies, leads, pipelines, deals,
    activities, tasks, calendar
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication & Authorization"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["Organizations & Teams"])
api_router.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])
api_router.include_router(companies.router, prefix="/companies", tags=["Companies"])
api_router.include_router(leads.router, prefix="/leads", tags=["Leads & Qualification"])
api_router.include_router(pipelines.router, prefix="/pipelines", tags=["Sales Pipelines"])
api_router.include_router(deals.router, prefix="/deals", tags=["Deals"])
api_router.include_router(activities.router, prefix="/activities", tags=["Activity Timeline"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(calendar.router, prefix="/calendar", tags=["Calendar"])
""")

    print("Milestones 9, 10, 11 (Activities, Tasks, Calendar) created successfully!")

if __name__ == '__main__':
    run()
