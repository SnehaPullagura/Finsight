import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    write_file("backend/app/api/v1/endpoints/products.py", """from fastapi import APIRouter, Depends, Query, status
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
""")

    write_file("backend/app/api/v1/endpoints/proposals.py", """from fastapi import APIRouter, Depends, Query, status
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
""")

    write_file("backend/app/api/v1/endpoints/quotes.py", """from fastapi import APIRouter, Depends, Query, status
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
""")

    write_file("backend/app/api/v1/endpoints/invoices.py", """from fastapi import APIRouter, Depends, Query, status
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
""")

    write_file("backend/app/api/v1/api.py", """from fastapi import APIRouter
from backend.app.api.v1.endpoints import (
    health, auth, organizations, contacts, companies, leads, pipelines, deals,
    activities, tasks, calendar, communications, documents,
    products, proposals, quotes, invoices
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication & Authorization"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["Organizations & Teams"])
api_router.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])
api_router.include_router(companies.router, prefix="/companies", tags=["Companies"])
api_router.include_router(leads.router, prefix="/leads", tags=["Leads & Qualification"])
api_router.include_router(pipelines.router, prefix="/pipelines", tags=["Sales Pipelines"])
api_router.include_router(deals.router, prefix="/deals", tags=["Deals"])
api_router.include_router(activities.router, prefix="/activities", tags=["Activity Timeline"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(calendar.router, prefix="/calendar", tags=["Calendar"])
api_router.include_router(communications.router, prefix="/communications", tags=["Communication System"])
api_router.include_router(documents.router, prefix="/documents", tags=["Document Management"])
api_router.include_router(products.router, prefix="/products", tags=["Product Catalog"])
api_router.include_router(proposals.router, prefix="/proposals", tags=["Proposals"])
api_router.include_router(quotes.router, prefix="/quotes", tags=["Quotes"])
api_router.include_router(invoices.router, prefix="/invoices", tags=["Invoices"])
""")

    print("Endpoints for Products, Quotes, Invoices generated.")

if __name__ == '__main__':
    run()
