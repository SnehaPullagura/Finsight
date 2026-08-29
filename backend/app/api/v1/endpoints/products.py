from fastapi import APIRouter, Depends, Query, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from backend.app.services.product import ProductService

router = APIRouter()

@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    req: ProductCreate,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = ProductService(db)
    return await service.create_product(req, tenant_id=tenant_id)

@router.get("", response_model=List[ProductResponse])
async def list_products(
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = ProductService(db)
    return await service.list(tenant_id=tenant_id)

@router.get("/{id}", response_model=ProductResponse)
async def get_product(
    id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = ProductService(db)
    return await service.get(id, tenant_id=tenant_id)

@router.put("/{id}", response_model=ProductResponse)
async def update_product(
    id: str,
    req: ProductUpdate,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = ProductService(db)
    return await service.update(id, req, tenant_id=tenant_id)
