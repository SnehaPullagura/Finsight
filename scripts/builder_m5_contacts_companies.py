import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. models/company.py
    write_file("backend/app/models/company.py", """import uuid
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class Company(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "companies"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    legal_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    domain: Mapped[Optional[str]] = mapped_column(String(255), index=True, nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    industry: Mapped[Optional[str]] = mapped_column(String(100), index=True, nullable=True)
    
    annual_revenue: Mapped[Optional[float]] = mapped_column(Numeric(18, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    employee_count: Mapped[Optional[int]] = mapped_column(nullable=True)
    
    parent_company_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True)
    owner_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    address_line1: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    address_line2: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), index=True, nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), index=True, nullable=True)
    
    linkedin_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    custom_fields: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    # Relationships
    contacts: Mapped[List["backend.app.models.contact.Contact"]] = relationship("backend.app.models.contact.Contact", back_populates="company")
    owner: Mapped[Optional["backend.app.models.auth.User"]] = relationship("backend.app.models.auth.User")
    subsidiaries: Mapped[List["Company"]] = relationship("Company", backref="parent_company", remote_side="Company.id")
""")

    # 2. models/contact.py
    write_file("backend/app/models/contact.py", """import uuid
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class Contact(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "contacts"

    first_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    secondary_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    mobile_phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    title: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    department: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    company_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True, index=True)
    owner_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    lifecycle_stage: Mapped[str] = mapped_column(String(50), default="lead", nullable=False, index=True) # lead, mql, sql, opportunity, customer, other
    lead_source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    address_line1: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    address_line2: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    linkedin_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    twitter_handle: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    is_do_not_call: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_do_not_email: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    custom_fields: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    # Relationships
    company: Mapped[Optional["backend.app.models.company.Company"]] = relationship("backend.app.models.company.Company", back_populates="contacts")
    owner: Mapped[Optional["backend.app.models.auth.User"]] = relationship("backend.app.models.auth.User")
""")

    # 3. schemas/company.py
    write_file("backend/app/schemas/company.py", """from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class CompanyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    legal_name: Optional[str] = None
    domain: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    annual_revenue: Optional[float] = None
    currency: Optional[str] = "USD"
    employee_count: Optional[int] = None
    parent_company_id: Optional[str] = None
    owner_id: Optional[str] = None
    phone: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    linkedin_url: Optional[str] = None
    description: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    legal_name: Optional[str] = None
    domain: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    annual_revenue: Optional[float] = None
    currency: Optional[str] = None
    employee_count: Optional[int] = None
    parent_company_id: Optional[str] = None
    owner_id: Optional[str] = None
    phone: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    linkedin_url: Optional[str] = None
    description: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None

class CompanyResponse(BaseModel):
    id: str
    tenant_id: str
    name: str
    legal_name: Optional[str] = None
    domain: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    annual_revenue: Optional[float] = None
    currency: str
    employee_count: Optional[int] = None
    parent_company_id: Optional[str] = None
    owner_id: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    linkedin_url: Optional[str] = None
    description: Optional[str] = None
    custom_fields: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
""")

    # 4. schemas/contact.py
    write_file("backend/app/schemas/contact.py", """from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, EmailStr, Field

class ContactCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    secondary_email: Optional[EmailStr] = None
    phone: Optional[str] = None
    mobile_phone: Optional[str] = None
    title: Optional[str] = None
    department: Optional[str] = None
    company_id: Optional[str] = None
    owner_id: Optional[str] = None
    lifecycle_stage: Optional[str] = "lead"
    lead_source: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    linkedin_url: Optional[str] = None
    twitter_handle: Optional[str] = None
    is_do_not_call: Optional[bool] = False
    is_do_not_email: Optional[bool] = False
    custom_fields: Optional[Dict[str, Any]] = None

class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    secondary_email: Optional[EmailStr] = None
    phone: Optional[str] = None
    mobile_phone: Optional[str] = None
    title: Optional[str] = None
    department: Optional[str] = None
    company_id: Optional[str] = None
    owner_id: Optional[str] = None
    lifecycle_stage: Optional[str] = None
    lead_source: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    linkedin_url: Optional[str] = None
    twitter_handle: Optional[str] = None
    is_do_not_call: Optional[bool] = None
    is_do_not_email: Optional[bool] = None
    custom_fields: Optional[Dict[str, Any]] = None

class ContactResponse(BaseModel):
    id: str
    tenant_id: str
    first_name: str
    last_name: str
    email: str
    secondary_email: Optional[str] = None
    phone: Optional[str] = None
    mobile_phone: Optional[str] = None
    title: Optional[str] = None
    department: Optional[str] = None
    company_id: Optional[str] = None
    owner_id: Optional[str] = None
    lifecycle_stage: str
    lead_source: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    linkedin_url: Optional[str] = None
    is_do_not_call: bool
    is_do_not_email: bool
    custom_fields: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ContactDeduplicationResult(BaseModel):
    potential_duplicates: List[ContactResponse]
    match_reasons: List[str]
""")

    # 5. repositories/company.py & repositories/contact.py
    write_file("backend/app/repositories/company.py", """from typing import List, Optional
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
""")

    write_file("backend/app/repositories/contact.py", """from typing import List, Optional
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
""")

    # 6. services/company.py & services/contact.py
    write_file("backend/app/services/company.py", """from typing import List, Optional
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
""")

    write_file("backend/app/services/contact.py", """from typing import List, Optional, Tuple
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
""")

    # 7. endpoints/contacts.py & endpoints/companies.py
    write_file("backend/app/api/v1/endpoints/contacts.py", """from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.contact import (
    ContactCreate,
    ContactUpdate,
    ContactResponse,
    ContactDeduplicationResult
)
from backend.app.services.contact import ContactService

router = APIRouter()

@router.post("", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
    req: ContactCreate,
    allow_duplicate: bool = Query(False),
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = ContactService(db)
    return await service.create_contact(req, tenant_id=tenant_id, actor_id=current_user.id, allow_duplicate=allow_duplicate)

@router.get("", response_model=List[ContactResponse])
async def list_contacts(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    company_id: Optional[str] = None,
    lifecycle_stage: Optional[str] = None,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = ContactService(db)
    filters = {}
    if company_id:
        filters["company_id"] = company_id
    if lifecycle_stage:
        filters["lifecycle_stage"] = lifecycle_stage
    return await service.list(tenant_id=tenant_id, skip=skip, limit=limit, filters=filters)

@router.get("/search", response_model=List[ContactResponse])
async def search_contacts(
    q: str = Query(..., min_length=1),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = ContactService(db)
    return await service.search(q, tenant_id=tenant_id)

@router.get("/deduplicate", response_model=ContactDeduplicationResult)
async def deduplicate_contact(
    email: str = Query(...),
    first_name: str = Query(...),
    last_name: str = Query(...),
    phone: Optional[str] = Query(None),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = ContactService(db)
    return await service.check_duplicates(email=email, phone=phone, first_name=first_name, last_name=last_name, tenant_id=tenant_id)

@router.get("/{id}", response_model=ContactResponse)
async def get_contact(
    id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = ContactService(db)
    return await service.get(id, tenant_id=tenant_id)

@router.put("/{id}", response_model=ContactResponse)
async def update_contact(
    id: str,
    req: ContactUpdate,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = ContactService(db)
    return await service.update(id, req, tenant_id=tenant_id, actor_id=current_user.id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
    id: str,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = ContactService(db)
    await service.delete(id, tenant_id=tenant_id, actor_id=current_user.id)
""")

    write_file("backend/app/api/v1/endpoints/companies.py", """from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.company import (
    CompanyCreate,
    CompanyUpdate,
    CompanyResponse
)
from backend.app.services.company import CompanyService

router = APIRouter()

@router.post("", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(
    req: CompanyCreate,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CompanyService(db)
    return await service.create_company(req, tenant_id=tenant_id, actor_id=current_user.id)

@router.get("", response_model=List[CompanyResponse])
async def list_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    industry: Optional[str] = None,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CompanyService(db)
    filters = {}
    if industry:
        filters["industry"] = industry
    return await service.list(tenant_id=tenant_id, skip=skip, limit=limit, filters=filters)

@router.get("/search", response_model=List[CompanyResponse])
async def search_companies(
    q: str = Query(..., min_length=1),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CompanyService(db)
    return await service.search(q, tenant_id=tenant_id)

@router.get("/{id}", response_model=CompanyResponse)
async def get_company(
    id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CompanyService(db)
    return await service.get(id, tenant_id=tenant_id)

@router.put("/{id}", response_model=CompanyResponse)
async def update_company(
    id: str,
    req: CompanyUpdate,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CompanyService(db)
    return await service.update(id, req, tenant_id=tenant_id, actor_id=current_user.id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    id: str,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CompanyService(db)
    await service.delete(id, tenant_id=tenant_id, actor_id=current_user.id)
""")

    # 8. Update api/v1/api.py
    write_file("backend/app/api/v1/api.py", """from fastapi import APIRouter
from backend.app.api.v1.endpoints import health, auth, organizations, contacts, companies

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication & Authorization"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["Organizations & Teams"])
api_router.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])
api_router.include_router(companies.router, prefix="/companies", tags=["Companies"])
""")

    print("Milestones 5 & 6 Contacts & Companies created successfully!")

if __name__ == '__main__':
    run()
