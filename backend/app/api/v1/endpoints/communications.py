from fastapi import APIRouter, Depends, Query, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.communication import (
    SendMessageRequest,
    CommunicationMessageResponse,
    CommunicationTemplateCreate,
    CommunicationTemplateResponse
)
from backend.app.services.communication import CommunicationService

router = APIRouter()

@router.post("/send", response_model=CommunicationMessageResponse, status_code=status.HTTP_201_CREATED)
async def send_message(
    req: SendMessageRequest,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CommunicationService(db)
    return await service.send_message(req, tenant_id=tenant_id, sender_email=current_user.email, user_id=current_user.id)

@router.get("/history/{entity_type}/{entity_id}", response_model=List[CommunicationMessageResponse])
async def get_history(
    entity_type: str,
    entity_id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CommunicationService(db)
    return await service.repository.list_for_entity(entity_type, entity_id, tenant_id)

@router.post("/templates", response_model=CommunicationTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(
    req: CommunicationTemplateCreate,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CommunicationService(db)
    data = req.model_dump(exclude_unset=True)
    if "available_variables" not in data or data["available_variables"] is None:
        data["available_variables"] = []
    return await service.template_repo.create(data, tenant_id=tenant_id)

@router.get("/templates", response_model=List[CommunicationTemplateResponse])
async def list_templates(
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CommunicationService(db)
    return await service.template_repo.list(tenant_id=tenant_id)
