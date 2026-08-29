from typing import List, Optional
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.company import Company
from backend.app.repositories.base import BaseRepository

class CompanyRepository(BaseRepository[Company]):
    def __init__(self, db: AsyncSession):
        super().__init__(Company, db)

    async def get_by_domain(self, domain: str, tenant_id: str) -> Optional[Company]:
        query = select(Company).where(
            Company.tenant_id == tenant_id,
            Company.domain == domain,
            Company.is_deleted == False
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def search_companies(self, query_str: str, tenant_id: str, limit: int = 20) -> List[Company]:
        pattern = f"%{query_str}%"
        query = select(Company).where(
            Company.tenant_id == tenant_id,
            Company.is_deleted == False,
            or_(
                Company.name.ilike(pattern),
                Company.domain.ilike(pattern),
                Company.industry.ilike(pattern),
                Company.city.ilike(pattern)
            )
        ).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())
