from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.exceptions import ConflictException, EntityNotFoundException, ValidationException
from backend.app.models.custom_field import CustomFieldDefinition
from backend.app.repositories.custom_field import CustomFieldRepository
from backend.app.schemas.custom_field import CustomFieldDefinitionCreate
from backend.app.services.base import BaseService

VALID_ENTITY_TYPES = {"contact", "company", "lead", "deal", "ticket"}
VALID_FIELD_TYPES = {"text", "number", "boolean", "date", "datetime", "select", "multiselect", "currency", "url"}

class CustomFieldService(BaseService[CustomFieldDefinition, CustomFieldRepository]):
    def __init__(self, session: AsyncSession):
        super().__init__(CustomFieldRepository(session), session)

    async def create_field_definition(self, data: CustomFieldDefinitionCreate, tenant_id: str) -> CustomFieldDefinition:
        if data.entity_type not in VALID_ENTITY_TYPES:
            raise ValidationException(f"Invalid entity_type {data.entity_type}. Must be one of {VALID_ENTITY_TYPES}")
        if data.field_type not in VALID_FIELD_TYPES:
            raise ValidationException(f"Invalid field_type {data.field_type}. Must be one of {VALID_FIELD_TYPES}")
        
        existing = await self.repository.get_by_entity_and_key(tenant_id, data.entity_type, data.field_key)
        if existing:
            raise ConflictException(f"Custom field with key '{data.field_key}' already exists for {data.entity_type}")

        payload = data.model_dump()
        payload["tenant_id"] = tenant_id
        if payload.get("options_list") is None:
            payload["options_list"] = []

        return await self.repository.create(payload)

    async def get_fields_for_entity(self, entity_type: str, tenant_id: str) -> List[CustomFieldDefinition]:
        return await self.repository.list_by_entity_type(tenant_id, entity_type)
