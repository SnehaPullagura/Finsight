from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.exceptions import ConflictException
from backend.app.models.product import Product
from backend.app.repositories.product import ProductRepository
from backend.app.services.base import BaseService
from backend.app.schemas.product import ProductCreate, ProductUpdate

class ProductService(BaseService[Product, ProductRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(ProductRepository(db))

    async def create_product(self, schema_in: ProductCreate, tenant_id: str) -> Product:
        existing = await self.repository.get_by_sku(schema_in.sku, tenant_id)
        if existing:
            raise ConflictException(f"Product with SKU '{schema_in.sku}' already exists.")
        return await self.repository.create(schema_in.model_dump(), tenant_id=tenant_id)
