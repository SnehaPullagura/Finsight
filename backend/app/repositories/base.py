from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from datetime import datetime
from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get_by_id(self, id: str, tenant_id: Optional[str] = None) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == id)
        if tenant_id and hasattr(self.model, "tenant_id"):
            query = query.where(self.model.tenant_id == tenant_id)
        if hasattr(self.model, "is_deleted"):
            query = query.where(self.model.is_deleted == False)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def list(
        self,
        tenant_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[Any] = None
    ) -> List[ModelType]:
        query = select(self.model)
        if tenant_id and hasattr(self.model, "tenant_id"):
            query = query.where(self.model.tenant_id == tenant_id)
        if hasattr(self.model, "is_deleted"):
            query = query.where(self.model.is_deleted == False)
            
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field) and value is not None:
                    query = query.where(getattr(self.model, field) == value)

        if order_by is not None:
            query = query.order_by(order_by)
        elif hasattr(self.model, "created_at"):
            query = query.order_by(self.model.created_at.desc())

        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count(self, tenant_id: Optional[str] = None, filters: Optional[Dict[str, Any]] = None) -> int:
        query = select(func.count(self.model.id))
        if tenant_id and hasattr(self.model, "tenant_id"):
            query = query.where(self.model.tenant_id == tenant_id)
        if hasattr(self.model, "is_deleted"):
            query = query.where(self.model.is_deleted == False)
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field) and value is not None:
                    query = query.where(getattr(self.model, field) == value)
        result = await self.db.execute(query)
        return result.scalar() or 0

    async def create(self, obj_in: Dict[str, Any], tenant_id: Optional[str] = None) -> ModelType:
        data = obj_in.copy()
        if tenant_id and hasattr(self.model, "tenant_id") and "tenant_id" not in data:
            data["tenant_id"] = tenant_id
        db_obj = self.model(**data)
        self.db.add(db_obj)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: ModelType, obj_in: Dict[str, Any]) -> ModelType:
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        if hasattr(db_obj, "updated_at"):
            setattr(db_obj, "updated_at", datetime.utcnow())
        self.db.add(db_obj)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj

    async def soft_delete(self, id: str, tenant_id: Optional[str] = None) -> bool:
        db_obj = await self.get_by_id(id, tenant_id=tenant_id)
        if not db_obj:
            return False
        if hasattr(db_obj, "is_deleted"):
            setattr(db_obj, "is_deleted", True)
            if hasattr(db_obj, "deleted_at"):
                setattr(db_obj, "deleted_at", datetime.utcnow())
            self.db.add(db_obj)
            await self.db.flush()
            return True
        else:
            await self.db.delete(db_obj)
            await self.db.flush()
            return True
