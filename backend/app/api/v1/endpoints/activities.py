from fastapi import APIRouter, Depends, Query, status
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
