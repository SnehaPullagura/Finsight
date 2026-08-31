from fastapi import APIRouter, Depends, Query, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.pipeline import (
    PipelineCreate,
    PipelineUpdate,
    PipelineResponse,
    PipelineStageCreate,
    PipelineStageResponse
)
from backend.app.services.pipeline import PipelineService

router = APIRouter()

@router.post("", response_model=PipelineResponse, status_code=status.HTTP_201_CREATED)
async def create_pipeline(
    req: PipelineCreate,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = PipelineService(db)
    return await service.create_pipeline(req, tenant_id=tenant_id)

@router.get("", response_model=List[PipelineResponse])
async def list_pipelines(
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = PipelineService(db)
    return await service.list_pipelines(tenant_id=tenant_id)

@router.get("/{id}", response_model=PipelineResponse)
async def get_pipeline(
    id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = PipelineService(db)
    pipeline = await service.repository.get_with_stages(id, tenant_id)
    return pipeline

@router.post("/{id}/stages", response_model=PipelineStageResponse, status_code=status.HTTP_201_CREATED)
async def create_stage(
    id: str,
    req: PipelineStageCreate,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = PipelineService(db)
    data = req.model_dump()
    data["pipeline_id"] = id
    return await service.stage_repo.create(data, tenant_id=tenant_id)
