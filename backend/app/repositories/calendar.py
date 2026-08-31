from typing import List, Optional
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
