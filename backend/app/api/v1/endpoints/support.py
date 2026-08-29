from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.support import (
    TicketCreate,
    TicketUpdate,
    TicketResponse,
    TicketCommentCreate,
    TicketCommentResponse,
    TicketResolveRequest
)
from backend.app.services.support import SupportService

router = APIRouter()

@router.post("/tickets", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    req: TicketCreate,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = SupportService(db)
    return await service.create_ticket(req, tenant_id=tenant_id, author_id=current_user.id)

@router.get("/tickets", response_model=List[TicketResponse])
async def list_tickets(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = SupportService(db)
    filters = {}
    if status:
        filters["status"] = status
    if priority:
        filters["priority"] = priority
    return await service.list(tenant_id=tenant_id, filters=filters)

@router.get("/tickets/{id}", response_model=TicketResponse)
async def get_ticket(
    id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = SupportService(db)
    return await service.get(id, tenant_id=tenant_id)

@router.post("/tickets/{id}/comments", response_model=TicketCommentResponse, status_code=status.HTTP_201_CREATED)
async def add_comment(
    id: str,
    req: TicketCommentCreate,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = SupportService(db)
    return await service.add_comment(id, req, author_id=current_user.id, tenant_id=tenant_id)

@router.post("/tickets/{id}/resolve", response_model=TicketResponse)
async def resolve_ticket(
    id: str,
    req: TicketResolveRequest,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = SupportService(db)
    return await service.resolve_ticket(id, req.resolution_notes, tenant_id=tenant_id)
