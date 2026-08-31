from fastapi import APIRouter, Depends, Query, status
from datetime import datetime, timedelta
from typing import List, Optional
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
