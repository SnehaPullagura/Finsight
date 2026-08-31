from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.company import (
    CompanyCreate,
    CompanyUpdate,
    CompanyResponse
)
from backend.app.services.company import CompanyService

router = APIRouter()

@router.post("", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(
    req: CompanyCreate,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CompanyService(db)
    return await service.create_company(req, tenant_id=tenant_id, actor_id=current_user.id)

@router.get("", response_model=List[CompanyResponse])
async def list_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    industry: Optional[str] = None,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CompanyService(db)
    filters = {}
    if industry:
        filters["industry"] = industry
    return await service.list(tenant_id=tenant_id, skip=skip, limit=limit, filters=filters)

@router.get("/search", response_model=List[CompanyResponse])
async def search_companies(
    q: str = Query(..., min_length=1),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CompanyService(db)
    return await service.search(q, tenant_id=tenant_id)

@router.get("/{id}", response_model=CompanyResponse)
async def get_company(
    id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CompanyService(db)
    return await service.get(id, tenant_id=tenant_id)

@router.put("/{id}", response_model=CompanyResponse)
async def update_company(
    id: str,
    req: CompanyUpdate,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CompanyService(db)
    return await service.update(id, req, tenant_id=tenant_id, actor_id=current_user.id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    id: str,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CompanyService(db)
    await service.delete(id, tenant_id=tenant_id, actor_id=current_user.id)
