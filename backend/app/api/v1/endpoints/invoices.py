from fastapi import APIRouter, Depends, Query, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.quote_invoice import InvoiceCreate, InvoiceResponse, PaymentRecordCreate
from backend.app.services.quote_invoice import InvoiceService

router = APIRouter()

@router.post("", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
async def create_invoice(
    req: InvoiceCreate,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = InvoiceService(db)
    return await service.create_invoice(req, tenant_id=tenant_id)

@router.get("", response_model=List[InvoiceResponse])
async def list_invoices(
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = InvoiceService(db)
    return await service.repo.list(tenant_id=tenant_id)

@router.get("/{id}", response_model=InvoiceResponse)
async def get_invoice(
    id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = InvoiceService(db)
    return await service.repo.get_by_id(id, tenant_id=tenant_id)

@router.post("/{id}/payments", response_model=InvoiceResponse)
async def record_payment(
    id: str,
    req: PaymentRecordCreate,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = InvoiceService(db)
    return await service.record_payment(id, req, tenant_id=tenant_id)
