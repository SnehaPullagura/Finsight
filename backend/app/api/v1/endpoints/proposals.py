from fastapi import APIRouter, Depends, Query, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.quote_invoice import ProposalCreate, ProposalResponse
from backend.app.services.quote_invoice import ProposalService

router = APIRouter()

@router.post("", response_model=ProposalResponse, status_code=status.HTTP_201_CREATED)
async def create_proposal(
    req: ProposalCreate,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = ProposalService(db)
    return await service.create_proposal(req, tenant_id=tenant_id)

@router.get("", response_model=List[ProposalResponse])
async def list_proposals(
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = ProposalService(db)
    return await service.repo.list(tenant_id=tenant_id)

@router.get("/{id}", response_model=ProposalResponse)
async def get_proposal(
    id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = ProposalService(db)
    return await service.repo.get_by_id(id, tenant_id=tenant_id)

@router.post("/{id}/accept", response_model=ProposalResponse)
async def accept_proposal(
    id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = ProposalService(db)
    return await service.accept_proposal(id, tenant_id=tenant_id)
