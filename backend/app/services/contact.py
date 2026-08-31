from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.exceptions import ConflictException
from backend.app.models.contact import Contact
from backend.app.repositories.contact import ContactRepository
from backend.app.services.base import BaseService
from backend.app.schemas.contact import ContactCreate, ContactUpdate, ContactDeduplicationResult, ContactResponse

class ContactService(BaseService[Contact, ContactRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(ContactRepository(db))

    async def create_contact(self, schema_in: ContactCreate, tenant_id: str, actor_id: Optional[str] = None, allow_duplicate: bool = False) -> Contact:
        if not allow_duplicate:
            existing = await self.repository.get_by_email(schema_in.email, tenant_id=tenant_id)
            if existing:
                raise ConflictException(f"Contact with email '{schema_in.email}' already exists in this organization.")

        data = schema_in.model_dump(exclude_unset=True)
        if "custom_fields" not in data or data["custom_fields"] is None:
            data["custom_fields"] = {}
        return await self.repository.create(data, tenant_id=tenant_id)

    async def check_duplicates(self, email: str, phone: Optional[str], first_name: str, last_name: str, tenant_id: str) -> ContactDeduplicationResult:
        dupes = await self.repository.find_duplicates(email, phone, first_name, last_name, tenant_id=tenant_id)
        reasons = []
        for d in dupes:
            if d.email.lower() == email.lower():
                reasons.append(f"Matching email: {d.email}")
            elif phone and (d.phone == phone or d.mobile_phone == phone):
                reasons.append(f"Matching phone: {phone}")
            elif d.first_name.lower() == first_name.lower() and d.last_name.lower() == last_name.lower():
                reasons.append(f"Matching full name: {d.first_name} {d.last_name}")

        return ContactDeduplicationResult(
            potential_duplicates=[ContactResponse.model_validate(d) for d in dupes],
            match_reasons=list(set(reasons))
        )

    async def search(self, query_str: str, tenant_id: str) -> List[Contact]:
        return await self.repository.search_contacts(query_str, tenant_id=tenant_id)
