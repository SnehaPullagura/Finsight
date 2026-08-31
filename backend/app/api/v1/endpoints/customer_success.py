from fastapi import APIRouter, Depends, Query, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.customer_success import (
    SuccessPlanCreate,
    SuccessPlanResponse,
    MilestoneCreate,
    MilestoneResponse
)
from backend.app.services.customer_success import CustomerSuccessService

router = APIRouter()

@router.post("/plans", response_model=SuccessPlanResponse, status_code=status.HTTP_201_CREATED)
async def create_plan(
    req: SuccessPlanCreate,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CustomerSuccessService(db)
    return await service.create_plan(req, tenant_id=tenant_id)

@router.get("/plans", response_model=List[SuccessPlanResponse])
async def list_plans(
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CustomerSuccessService(db)
    return await service.list(tenant_id=tenant_id)

@router.get("/plans/{id}", response_model=SuccessPlanResponse)
async def get_plan(
    id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CustomerSuccessService(db)
    return await service.repository.get_with_milestones(id, tenant_id)

@router.post("/plans/{id}/recalculate-health", response_model=SuccessPlanResponse)
async def recalculate_health(
    id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CustomerSuccessService(db)
    return await service.recalculate_health_score(id, tenant_id=tenant_id)
