from typing import List, Optional
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.contact import Contact
from backend.app.repositories.base import BaseRepository

class ContactRepository(BaseRepository[Contact]):
    def __init__(self, db: AsyncSession):
        super().__init__(Contact, db)

    async def get_by_email(self, email: str, tenant_id: str) -> Optional[Contact]:
        query = select(Contact).where(
            Contact.tenant_id == tenant_id,
            or_(Contact.email == email, Contact.secondary_email == email),
            Contact.is_deleted == False
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def find_duplicates(self, email: str, phone: Optional[str], first_name: str, last_name: str, tenant_id: str) -> List[Contact]:
        conditions = [Contact.email == email]
        if phone:
            conditions.append(Contact.phone == phone)
            conditions.append(Contact.mobile_phone == phone)
        conditions.append((Contact.first_name == first_name) & (Contact.last_name == last_name))
        
        query = select(Contact).where(
            Contact.tenant_id == tenant_id,
            Contact.is_deleted == False,
            or_(*conditions)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def search_contacts(self, query_str: str, tenant_id: str, limit: int = 20) -> List[Contact]:
        pattern = f"%{query_str}%"
        query = select(Contact).where(
            Contact.tenant_id == tenant_id,
            Contact.is_deleted == False,
            or_(
                Contact.first_name.ilike(pattern),
                Contact.last_name.ilike(pattern),
                Contact.email.ilike(pattern),
                Contact.phone.ilike(pattern),
                Contact.title.ilike(pattern)
            )
        ).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())
