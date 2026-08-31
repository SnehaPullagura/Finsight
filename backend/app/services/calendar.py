from datetime import datetime
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
