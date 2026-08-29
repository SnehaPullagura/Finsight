from fastapi import APIRouter, Depends, Query, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.quote_invoice import QuoteCreate, QuoteResponse
from backend.app.services.quote_invoice import QuoteService

router = APIRouter()

@router.post("", response_model=QuoteResponse, status_code=status.HTTP_201_CREATED)
async def create_quote(
    req: QuoteCreate,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = QuoteService(db)
    return await service.create_quote(req, tenant_id=tenant_id)

@router.get("", response_model=List[QuoteResponse])
async def list_quotes(
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = QuoteService(db)
    return await service.repo.list(tenant_id=tenant_id)

@router.get("/{id}", response_model=QuoteResponse)
async def get_quote(
    id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = QuoteService(db)
    return await service.repo.get_by_id(id, tenant_id=tenant_id)
