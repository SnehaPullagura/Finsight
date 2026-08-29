from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.lead import (
    LeadCreate,
    LeadUpdate,
    LeadResponse,
    LeadConvertRequest,
    LeadConvertResponse,
    LeadScoringRuleCreate,
    LeadScoringRuleResponse
)
from backend.app.services.lead import LeadService

router = APIRouter()

@router.post("", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
async def create_lead(
    req: LeadCreate,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = LeadService(db)
    return await service.create_lead(req, tenant_id=tenant_id, actor_id=current_user.id)

@router.get("", response_model=List[LeadResponse])
async def list_leads(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    status: Optional[str] = None,
    source: Optional[str] = None,
    grade: Optional[str] = None,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = LeadService(db)
    filters = {}
    if status:
        filters["status"] = status
    if source:
        filters["source"] = source
    if grade:
        filters["qualification_grade"] = grade
    return await service.list(tenant_id=tenant_id, skip=skip, limit=limit, filters=filters)

@router.get("/{id}", response_model=LeadResponse)
async def get_lead(
    id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = LeadService(db)
    return await service.get(id, tenant_id=tenant_id)

@router.put("/{id}", response_model=LeadResponse)
async def update_lead(
    id: str,
    req: LeadUpdate,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = LeadService(db)
    return await service.update(id, req, tenant_id=tenant_id, actor_id=current_user.id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lead(
    id: str,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = LeadService(db)
    await service.delete(id, tenant_id=tenant_id, actor_id=current_user.id)

@router.post("/{id}/qualify", response_model=LeadResponse)
async def qualify_lead(
    id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = LeadService(db)
    return await service.qualify_lead(id, tenant_id=tenant_id)

@router.post("/{id}/convert", response_model=LeadConvertResponse)
async def convert_lead(
    id: str,
    req: LeadConvertRequest,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = LeadService(db)
    return await service.convert_lead(id, req, tenant_id=tenant_id, actor_id=current_user.id)

@router.post("/rules/scoring", response_model=LeadScoringRuleResponse, status_code=status.HTTP_201_CREATED)
async def create_scoring_rule(
    req: LeadScoringRuleCreate,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = LeadService(db)
    rule = await service.rule_repo.create(req.model_dump(), tenant_id=tenant_id)
    return rule

@router.get("/rules/scoring", response_model=List[LeadScoringRuleResponse])
async def list_scoring_rules(
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = LeadService(db)
    return await service.rule_repo.list(tenant_id=tenant_id)
