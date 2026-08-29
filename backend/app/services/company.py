from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.company import Company
from backend.app.repositories.company import CompanyRepository
from backend.app.services.base import BaseService
from backend.app.schemas.company import CompanyCreate, CompanyUpdate

class CompanyService(BaseService[Company, CompanyRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(CompanyRepository(db))

    async def create_company(self, schema_in: CompanyCreate, tenant_id: str, actor_id: Optional[str] = None) -> Company:
        data = schema_in.model_dump(exclude_unset=True)
        if "custom_fields" not in data or data["custom_fields"] is None:
            data["custom_fields"] = {}
        return await self.repository.create(data, tenant_id=tenant_id)

    async def search(self, query_str: str, tenant_id: str) -> List[Company]:
        return await self.repository.search_companies(query_str, tenant_id=tenant_id)
