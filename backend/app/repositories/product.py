from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.product import Product, ProductCategory
from backend.app.repositories.base import BaseRepository

class ProductRepository(BaseRepository[Product]):
    def __init__(self, db: AsyncSession):
        super().__init__(Product, db)

    async def get_by_sku(self, sku: str, tenant_id: str) -> Optional[Product]:
        query = select(Product).where(
            Product.tenant_id == tenant_id,
            Product.sku == sku,
            Product.is_deleted == False
        )
        result = await self.db.execute(query)
        return result.scalars().first()
