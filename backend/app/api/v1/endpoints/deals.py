from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.deal import (
    DealCreate,
    DealUpdate,
    DealStageTransitionRequest,
    DealResponse,
    KanbanBoardResponse
)
from backend.app.services.deal import DealService

router = APIRouter()

@router.post("", response_model=DealResponse, status_code=status.HTTP_201_CREATED)
async def create_deal(
    req: DealCreate,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = DealService(db)
    return await service.create_deal(req, tenant_id=tenant_id, actor_id=current_user.id)

@router.get("", response_model=List[DealResponse])
async def list_deals(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    pipeline_id: Optional[str] = None,
    stage_id: Optional[str] = None,
    status: Optional[str] = None,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = DealService(db)
    filters = {}
    if pipeline_id:
        filters["pipeline_id"] = pipeline_id
    if stage_id:
        filters["stage_id"] = stage_id
    if status:
        filters["status"] = status
    return await service.list(tenant_id=tenant_id, skip=skip, limit=limit, filters=filters)

@router.get("/kanban", response_model=KanbanBoardResponse)
async def get_kanban_board(
    pipeline_id: Optional[str] = Query(None),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = DealService(db)
    return await service.get_kanban_board(pipeline_id, tenant_id=tenant_id)

@router.get("/{id}", response_model=DealResponse)
async def get_deal(
    id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = DealService(db)
    return await service.get(id, tenant_id=tenant_id)

@router.put("/{id}", response_model=DealResponse)
async def update_deal(
    id: str,
    req: DealUpdate,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = DealService(db)
    return await service.update(id, req, tenant_id=tenant_id, actor_id=current_user.id)

@router.post("/{id}/stage", response_model=DealResponse)
async def transition_deal_stage(
    id: str,
    req: DealStageTransitionRequest,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = DealService(db)
    return await service.transition_stage(id, req, tenant_id=tenant_id, actor_id=current_user.id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_deal(
    id: str,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = DealService(db)
    await service.delete(id, tenant_id=tenant_id, actor_id=current_user.id)
