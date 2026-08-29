from fastapi import APIRouter, Depends, Query, status
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
