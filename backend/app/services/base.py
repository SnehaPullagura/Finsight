from typing import Any, Dict, Generic, List, Optional, TypeVar
from backend.app.models.base import Base
from backend.app.repositories.base import BaseRepository
from backend.app.core.exceptions import EntityNotFoundException, TenantAccessViolationException

ModelType = TypeVar("ModelType", bound=Base)
RepoType = TypeVar("RepoType", bound=BaseRepository)

class BaseService(Generic[ModelType, RepoType]):
    def __init__(self, repository: RepoType):
        self.repository = repository

    async def get(self, id: str, tenant_id: Optional[str] = None) -> ModelType:
        entity = await self.repository.get_by_id(id, tenant_id=tenant_id)
        if not entity:
            raise EntityNotFoundException(self.repository.model.__name__, id)
        return entity

    async def list(
        self,
        tenant_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ModelType]:
        return await self.repository.list(tenant_id=tenant_id, skip=skip, limit=limit, filters=filters)

    async def count(self, tenant_id: Optional[str] = None, filters: Optional[Dict[str, Any]] = None) -> int:
        return await self.repository.count(tenant_id=tenant_id, filters=filters)

    async def create(self, schema_in: Any, tenant_id: Optional[str] = None, actor_id: Optional[str] = None) -> ModelType:
        data = schema_in.model_dump() if hasattr(schema_in, "model_dump") else dict(schema_in)
        return await self.repository.create(data, tenant_id=tenant_id)

    async def update(self, id: str, schema_in: Any, tenant_id: Optional[str] = None, actor_id: Optional[str] = None) -> ModelType:
        entity = await self.get(id, tenant_id=tenant_id)
        data = schema_in.model_dump(exclude_unset=True) if hasattr(schema_in, "model_dump") else dict(schema_in)
        return await self.repository.update(entity, data)

    async def delete(self, id: str, tenant_id: Optional[str] = None, actor_id: Optional[str] = None) -> bool:
        entity = await self.get(id, tenant_id=tenant_id)
        return await self.repository.soft_delete(id, tenant_id=tenant_id)
