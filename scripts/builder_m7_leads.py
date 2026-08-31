import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. models/lead.py
    write_file("backend/app/models/lead.py", """import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class Lead(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "leads"

    first_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    company_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    title: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    
    status: Mapped[str] = mapped_column(String(50), default="new", nullable=False, index=True) # new, contacted, qualified, unqualified, converted
    source: Mapped[str] = mapped_column(String(100), default="website", nullable=False, index=True)
    
    score: Mapped[int] = mapped_column(Integer, default=0, nullable=False, index=True)
    qualification_grade: Mapped[str] = mapped_column(String(2), default="C", nullable=False) # A, B, C, D, F
    qualification_details: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    
    estimated_budget: Mapped[Optional[float]] = mapped_column(Numeric(18, 2), nullable=True)
    employee_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    industry: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    intent_score: Mapped[int] = mapped_column(Integer, default=50, nullable=False) # 0 to 100
    engagement_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    owner_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    # Conversion references
    converted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    converted_contact_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("contacts.id", ondelete="SET NULL"), nullable=True)
    converted_company_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True)
    converted_deal_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    custom_fields: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    # Relationships
    owner: Mapped[Optional["backend.app.models.auth.User"]] = relationship("backend.app.models.auth.User")
    converted_contact: Mapped[Optional["backend.app.models.contact.Contact"]] = relationship("backend.app.models.contact.Contact")
    converted_company: Mapped[Optional["backend.app.models.company.Company"]] = relationship("backend.app.models.company.Company")

class LeadScoringRule(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "lead_scoring_rules"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    criteria_type: Mapped[str] = mapped_column(String(50), nullable=False) # budget, company_size, industry, engagement, intent
    operator: Mapped[str] = mapped_column(String(20), nullable=False) # gt, gte, lt, lte, eq, in, contains
    target_value: Mapped[str] = mapped_column(String(255), nullable=False)
    score_weight: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
""")

    # 2. schemas/lead.py
    write_file("backend/app/schemas/lead.py", """from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, EmailStr, Field

class LeadCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = None
    company_name: Optional[str] = None
    title: Optional[str] = None
    source: Optional[str] = "website"
    estimated_budget: Optional[float] = None
    employee_count: Optional[int] = None
    industry: Optional[str] = None
    intent_score: Optional[int] = Field(default=50, ge=0, le=100)
    engagement_count: Optional[int] = 0
    owner_id: Optional[str] = None
    notes: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None

class LeadUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company_name: Optional[str] = None
    title: Optional[str] = None
    status: Optional[str] = None
    source: Optional[str] = None
    estimated_budget: Optional[float] = None
    employee_count: Optional[int] = None
    industry: Optional[str] = None
    intent_score: Optional[int] = None
    engagement_count: Optional[int] = None
    owner_id: Optional[str] = None
    notes: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None

class LeadResponse(BaseModel):
    id: str
    tenant_id: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    company_name: Optional[str] = None
    title: Optional[str] = None
    status: str
    source: str
    score: int
    qualification_grade: str
    qualification_details: Dict[str, Any] = {}
    estimated_budget: Optional[float] = None
    employee_count: Optional[int] = None
    industry: Optional[str] = None
    intent_score: int
    engagement_count: int
    owner_id: Optional[str] = None
    converted_at: Optional[datetime] = None
    converted_contact_id: Optional[str] = None
    converted_company_id: Optional[str] = None
    converted_deal_id: Optional[str] = None
    notes: Optional[str] = None
    custom_fields: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class LeadConvertRequest(BaseModel):
    create_deal: bool = True
    deal_name: Optional[str] = None
    deal_value: Optional[float] = None
    pipeline_id: Optional[str] = None
    stage_id: Optional[str] = None

class LeadConvertResponse(BaseModel):
    lead_id: str
    contact_id: str
    company_id: Optional[str] = None
    deal_id: Optional[str] = None
    message: str

class LeadScoringRuleCreate(BaseModel):
    name: str
    criteria_type: str # budget, company_size, industry, engagement, intent
    operator: str # gt, gte, lt, lte, eq, in, contains
    target_value: str
    score_weight: int = 10

class LeadScoringRuleResponse(BaseModel):
    id: str
    name: str
    criteria_type: str
    operator: str
    target_value: str
    score_weight: int
    is_active: bool

    class Config:
        from_attributes = True
""")

    # 3. repositories/lead.py
    write_file("backend/app/repositories/lead.py", """from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.lead import Lead, LeadScoringRule
from backend.app.repositories.base import BaseRepository

class LeadRepository(BaseRepository[Lead]):
    def __init__(self, db: AsyncSession):
        super().__init__(Lead, db)

    async def get_by_email(self, email: str, tenant_id: str) -> Optional[Lead]:
        query = select(Lead).where(
            Lead.tenant_id == tenant_id,
            Lead.email == email,
            Lead.is_deleted == False
        )
        result = await self.db.execute(query)
        return result.scalars().first()

class LeadScoringRuleRepository(BaseRepository[LeadScoringRule]):
    def __init__(self, db: AsyncSession):
        super().__init__(LeadScoringRule, db)

    async def list_active_rules(self, tenant_id: str) -> List[LeadScoringRule]:
        query = select(LeadScoringRule).where(
            LeadScoringRule.tenant_id == tenant_id,
            LeadScoringRule.is_active == True
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
""")

    # 4. services/lead.py
    write_file("backend/app/services/lead.py", """from datetime import datetime
from typing import Dict, List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.exceptions import ConflictException, EntityNotFoundException, ValidationException
from backend.app.models.lead import Lead, LeadScoringRule
from backend.app.repositories.lead import LeadRepository, LeadScoringRuleRepository
from backend.app.repositories.contact import ContactRepository
from backend.app.repositories.company import CompanyRepository
from backend.app.services.base import BaseService
from backend.app.schemas.lead import (
    LeadCreate,
    LeadUpdate,
    LeadConvertRequest,
    LeadConvertResponse,
    LeadScoringRuleCreate
)

class LeadQualificationEngine:
    @staticmethod
    def evaluate_rule(lead: Lead, rule: LeadScoringRule) -> int:
        field_val = None
        if rule.criteria_type == "budget":
            field_val = float(lead.estimated_budget or 0)
        elif rule.criteria_type == "company_size":
            field_val = int(lead.employee_count or 0)
        elif rule.criteria_type == "intent":
            field_val = int(lead.intent_score or 0)
        elif rule.criteria_type == "engagement":
            field_val = int(lead.engagement_count or 0)
        elif rule.criteria_type == "industry":
            field_val = (lead.industry or "").lower()

        if field_val is None:
            return 0

        target = rule.target_value
        op = rule.operator.lower()

        try:
            if op in ["gt", "gte", "lt", "lte", "eq"] and isinstance(field_val, (int, float)):
                target_num = float(target)
                if op == "gt" and field_val > target_num:
                    return rule.score_weight
                elif op == "gte" and field_val >= target_num:
                    return rule.score_weight
                elif op == "lt" and field_val < target_num:
                    return rule.score_weight
                elif op == "lte" and field_val <= target_num:
                    return rule.score_weight
                elif op == "eq" and field_val == target_num:
                    return rule.score_weight
            elif op == "contains" and isinstance(field_val, str):
                if target.lower() in field_val:
                    return rule.score_weight
            elif op == "eq" and isinstance(field_val, str):
                if target.lower() == field_val:
                    return rule.score_weight
        except Exception:
            return 0
        return 0

    @classmethod
    def calculate_score(cls, lead: Lead, rules: List[LeadScoringRule]) -> Tuple[int, str, Dict[str, Any]]:
        total_score = 20 # Base score
        breakdown = {}

        for rule in rules:
            points = cls.evaluate_rule(lead, rule)
            if points > 0:
                total_score += points
                breakdown[rule.name] = points

        total_score = max(0, min(100, total_score))
        
        if total_score >= 80:
            grade = "A"
        elif total_score >= 65:
            grade = "B"
        elif total_score >= 50:
            grade = "C"
        elif total_score >= 35:
            grade = "D"
        else:
            grade = "F"

        return total_score, grade, breakdown

class LeadService(BaseService[Lead, LeadRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(LeadRepository(db))
        self.rule_repo = LeadScoringRuleRepository(db)
        self.contact_repo = ContactRepository(db)
        self.company_repo = CompanyRepository(db)

    async def create_lead(self, schema_in: LeadCreate, tenant_id: str, actor_id: Optional[str] = None) -> Lead:
        existing = await self.repository.get_by_email(schema_in.email, tenant_id=tenant_id)
        if existing:
            raise ConflictException(f"Lead with email '{schema_in.email}' already exists.")

        data = schema_in.model_dump(exclude_unset=True)
        if "custom_fields" not in data or data["custom_fields"] is None:
            data["custom_fields"] = {}
            
        lead = await self.repository.create(data, tenant_id=tenant_id)
        
        # Calculate initial score
        rules = await self.rule_repo.list_active_rules(tenant_id)
        score, grade, details = LeadQualificationEngine.calculate_score(lead, rules)
        lead = await self.repository.update(lead, {
            "score": score,
            "qualification_grade": grade,
            "qualification_details": details
        })
        return lead

    async def qualify_lead(self, lead_id: str, tenant_id: str) -> Lead:
        lead = await self.get(lead_id, tenant_id=tenant_id)
        rules = await self.rule_repo.list_active_rules(tenant_id)
        score, grade, details = LeadQualificationEngine.calculate_score(lead, rules)
        
        new_status = "qualified" if score >= 50 else "unqualified"
        return await self.repository.update(lead, {
            "score": score,
            "qualification_grade": grade,
            "qualification_details": details,
            "status": new_status
        })

    async def convert_lead(self, lead_id: str, req: LeadConvertRequest, tenant_id: str, actor_id: Optional[str] = None) -> LeadConvertResponse:
        lead = await self.get(lead_id, tenant_id=tenant_id)
        if lead.status == "converted":
            raise ConflictException("Lead has already been converted.")

        company_id = None
        if lead.company_name:
            company = await self.company_repo.create({
                "name": lead.company_name,
                "industry": lead.industry,
                "employee_count": lead.employee_count,
                "annual_revenue": lead.estimated_budget,
                "owner_id": lead.owner_id
            }, tenant_id=tenant_id)
            company_id = company.id

        contact = await self.contact_repo.create({
            "first_name": lead.first_name,
            "last_name": lead.last_name,
            "email": lead.email,
            "phone": lead.phone,
            "title": lead.title,
            "company_id": company_id,
            "owner_id": lead.owner_id,
            "lifecycle_stage": "opportunity" if req.create_deal else "lead",
            "lead_source": lead.source
        }, tenant_id=tenant_id)

        deal_id = None
        if req.create_deal:
            from backend.app.models.deal import Deal
            deal_name = req.deal_name or f"Deal with {lead.company_name or lead.first_name + ' ' + lead.last_name}"
            deal_val = req.deal_value if req.deal_value is not None else (lead.estimated_budget or 10000.0)
            
            # Simple direct insertion for deal
            deal = Deal(
                tenant_id=tenant_id,
                name=deal_name,
                company_id=company_id,
                contact_id=contact.id,
                owner_id=lead.owner_id,
                value=deal_val,
                probability=40,
                stage_id=req.stage_id or "default_stage",
                pipeline_id=req.pipeline_id or "default_pipeline"
            )
            self.db.add(deal)
            await self.db.flush()
            await self.db.refresh(deal)
            deal_id = deal.id

        # Update lead
        await self.repository.update(lead, {
            "status": "converted",
            "converted_at": datetime.utcnow(),
            "converted_contact_id": contact.id,
            "converted_company_id": company_id,
            "converted_deal_id": deal_id
        })

        return LeadConvertResponse(
            lead_id=lead.id,
            contact_id=contact.id,
            company_id=company_id,
            deal_id=deal_id,
            message="Lead successfully converted."
        )
""")

    # 5. endpoints/leads.py
    write_file("backend/app/api/v1/endpoints/leads.py", """from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.lead import (
    LeadCreate,
    LeadUpdate,
    LeadResponse,
    LeadConvertRequest,
    LeadConvertResponse,
    LeadScoringRuleCreate,
    LeadScoringRuleResponse
)
from backend.app.services.lead import LeadService

router = APIRouter()

@router.post("", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
async def create_lead(
    req: LeadCreate,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = LeadService(db)
    return await service.create_lead(req, tenant_id=tenant_id, actor_id=current_user.id)

@router.get("", response_model=List[LeadResponse])
async def list_leads(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    status: Optional[str] = None,
    source: Optional[str] = None,
    grade: Optional[str] = None,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = LeadService(db)
    filters = {}
    if status:
        filters["status"] = status
    if source:
        filters["source"] = source
    if grade:
        filters["qualification_grade"] = grade
    return await service.list(tenant_id=tenant_id, skip=skip, limit=limit, filters=filters)

@router.get("/{id}", response_model=LeadResponse)
async def get_lead(
    id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = LeadService(db)
    return await service.get(id, tenant_id=tenant_id)

@router.put("/{id}", response_model=LeadResponse)
async def update_lead(
    id: str,
    req: LeadUpdate,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = LeadService(db)
    return await service.update(id, req, tenant_id=tenant_id, actor_id=current_user.id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lead(
    id: str,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = LeadService(db)
    await service.delete(id, tenant_id=tenant_id, actor_id=current_user.id)

@router.post("/{id}/qualify", response_model=LeadResponse)
async def qualify_lead(
    id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = LeadService(db)
    return await service.qualify_lead(id, tenant_id=tenant_id)

@router.post("/{id}/convert", response_model=LeadConvertResponse)
async def convert_lead(
    id: str,
    req: LeadConvertRequest,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = LeadService(db)
    return await service.convert_lead(id, req, tenant_id=tenant_id, actor_id=current_user.id)

@router.post("/rules/scoring", response_model=LeadScoringRuleResponse, status_code=status.HTTP_201_CREATED)
async def create_scoring_rule(
    req: LeadScoringRuleCreate,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = LeadService(db)
    rule = await service.rule_repo.create(req.model_dump(), tenant_id=tenant_id)
    return rule

@router.get("/rules/scoring", response_model=List[LeadScoringRuleResponse])
async def list_scoring_rules(
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = LeadService(db)
    return await service.rule_repo.list(tenant_id=tenant_id)
""")

    # 6. Update api/v1/api.py
    write_file("backend/app/api/v1/api.py", """from fastapi import APIRouter
from backend.app.api.v1.endpoints import health, auth, organizations, contacts, companies, leads

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication & Authorization"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["Organizations & Teams"])
api_router.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])
api_router.include_router(companies.router, prefix="/companies", tags=["Companies"])
api_router.include_router(leads.router, prefix="/leads", tags=["Leads & Qualification"])
""")

    print("Milestone 7 Leads & Qualification created successfully!")

if __name__ == '__main__':
    run()
