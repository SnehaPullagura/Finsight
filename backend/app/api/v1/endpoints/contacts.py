from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.contact import (
    ContactCreate,
    ContactUpdate,
    ContactResponse,
    ContactDeduplicationResult
)
from backend.app.services.contact import ContactService

router = APIRouter()

@router.post("", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
    req: ContactCreate,
    allow_duplicate: bool = Query(False),
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = ContactService(db)
    return await service.create_contact(req, tenant_id=tenant_id, actor_id=current_user.id, allow_duplicate=allow_duplicate)

@router.get("", response_model=List[ContactResponse])
async def list_contacts(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    company_id: Optional[str] = None,
    lifecycle_stage: Optional[str] = None,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = ContactService(db)
    filters = {}
    if company_id:
        filters["company_id"] = company_id
    if lifecycle_stage:
        filters["lifecycle_stage"] = lifecycle_stage
    return await service.list(tenant_id=tenant_id, skip=skip, limit=limit, filters=filters)

@router.get("/search", response_model=List[ContactResponse])
async def search_contacts(
    q: str = Query(..., min_length=1),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = ContactService(db)
    return await service.search(q, tenant_id=tenant_id)

@router.get("/deduplicate", response_model=ContactDeduplicationResult)
async def deduplicate_contact(
    email: str = Query(...),
    first_name: str = Query(...),
    last_name: str = Query(...),
    phone: Optional[str] = Query(None),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = ContactService(db)
    return await service.check_duplicates(email=email, phone=phone, first_name=first_name, last_name=last_name, tenant_id=tenant_id)

@router.get("/{id}", response_model=ContactResponse)
async def get_contact(
    id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = ContactService(db)
    return await service.get(id, tenant_id=tenant_id)

@router.put("/{id}", response_model=ContactResponse)
async def update_contact(
    id: str,
    req: ContactUpdate,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = ContactService(db)
    return await service.update(id, req, tenant_id=tenant_id, actor_id=current_user.id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
    id: str,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = ContactService(db)
    await service.delete(id, tenant_id=tenant_id, actor_id=current_user.id)
