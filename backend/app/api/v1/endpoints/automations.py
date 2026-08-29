from fastapi import APIRouter, Depends, Query, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.automation import WorkflowCreate, WorkflowResponse, WorkflowTriggerRequest, ExecutionLogResponse
from backend.app.services.automation import WorkflowService

router = APIRouter()

@router.post("", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
async def create_workflow(
    req: WorkflowCreate,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = WorkflowService(db)
    return await service.create_workflow(req, tenant_id=tenant_id)

@router.get("", response_model=List[WorkflowResponse])
async def list_workflows(
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = WorkflowService(db)
    workflows = await service.list(tenant_id=tenant_id)
    # Load rules for each
    res = []
    for wf in workflows:
        loaded = await service.repository.get_with_rules(wf.id, tenant_id)
        res.append(loaded or wf)
    return res

@router.post("/trigger", response_model=List[ExecutionLogResponse])
async def trigger_workflows(
    req: WorkflowTriggerRequest,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = WorkflowService(db)
    return await service.execute_trigger(req, tenant_id=tenant_id)

@router.get("/logs", response_model=List[ExecutionLogResponse])
async def list_execution_logs(
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = WorkflowService(db)
    return await service.log_repo.list(tenant_id=tenant_id)
