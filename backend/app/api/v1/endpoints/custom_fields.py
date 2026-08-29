from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.custom_field import CustomFieldDefinitionCreate, CustomFieldDefinitionResponse
from backend.app.services.custom_field import CustomFieldService

router = APIRouter()

@router.post("", response_model=CustomFieldDefinitionResponse, status_code=status.HTTP_201_CREATED)
async def create_custom_field(
    data: CustomFieldDefinitionCreate,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CustomFieldService(db)
    return await service.create_field_definition(data, tenant_id=tenant_id)

@router.get("/{entity_type}", response_model=List[CustomFieldDefinitionResponse])
async def list_custom_fields(
    entity_type: str,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CustomFieldService(db)
    return await service.get_fields_for_entity(entity_type, tenant_id=tenant_id)
