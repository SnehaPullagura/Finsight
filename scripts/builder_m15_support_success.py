import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. models/support.py & models/customer_success.py
    write_file("backend/app/models/support.py", """import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class Ticket(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "support_tickets"

    ticket_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    priority: Mapped[str] = mapped_column(String(20), default="medium", nullable=False, index=True) # urgent, high, medium, low
    status: Mapped[str] = mapped_column(String(20), default="open", nullable=False, index=True) # open, pending, in_progress, resolved, closed
    category: Mapped[str] = mapped_column(String(50), default="technical", nullable=False, index=True)
    
    contact_id: Optional[Mapped[str]] = mapped_column(String(36), ForeignKey("contacts.id", ondelete="SET NULL"), nullable=True, index=True)
    company_id: Optional[Mapped[str]] = mapped_column(String(36), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True, index=True)
    assigned_to_id: Optional[Mapped[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    created_by_id: Optional[Mapped[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    sla_due_at: Optional[Mapped[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    resolved_at: Optional[Mapped[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    resolution_notes: Optional[Mapped[str]] = mapped_column(Text, nullable=True)
    is_escalated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    custom_fields: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    contact: Mapped[Optional["backend.app.models.contact.Contact"]] = relationship("backend.app.models.contact.Contact")
    company: Mapped[Optional["backend.app.models.company.Company"]] = relationship("backend.app.models.company.Company")
    assigned_to: Mapped[Optional["backend.app.models.auth.User"]] = relationship("backend.app.models.auth.User", foreign_keys=[assigned_to_id])
    comments: Mapped[List["TicketComment"]] = relationship("TicketComment", back_populates="ticket", cascade="all, delete-orphan", order_by="TicketComment.created_at.asc()")

class TicketComment(UUIDModel, TimestampMixin):
    __tablename__ = "ticket_comments"

    ticket_id: Mapped[str] = mapped_column(String(36), ForeignKey("support_tickets.id", ondelete="CASCADE"), nullable=False, index=True)
    author_id: Optional[Mapped[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    is_internal: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    ticket: Mapped["Ticket"] = relationship("Ticket", back_populates="comments")
    author: Mapped[Optional["backend.app.models.auth.User"]] = relationship("backend.app.models.auth.User")
""")

    write_file("backend/app/models/customer_success.py", """import uuid
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class CustomerSuccessPlan(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "customer_success_plans"

    company_id: Mapped[str] = mapped_column(String(36), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    owner_id: Optional[Mapped[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    status: Mapped[str] = mapped_column(String(50), default="onboarding", nullable=False, index=True) # onboarding, active, at_risk, churned
    health_score: Mapped[int] = mapped_column(Integer, default=80, nullable=False, index=True) # 0 to 100
    health_grade: Mapped[str] = mapped_column(String(20), default="good", nullable=False) # good, warning, critical
    
    target_renewal_date: Optional[Mapped[date]] = mapped_column(Date, nullable=True, index=True)
    renewal_value: Optional[Mapped[float]] = mapped_column(Numeric(18, 2), nullable=True)
    churn_risk_reason: Optional[Mapped[str]] = mapped_column(String(255), nullable=True)
    goals: Mapped[list] = mapped_column(JSON, default=list, nullable=False)

    company: Mapped["backend.app.models.company.Company"]] = relationship("backend.app.models.company.Company")
    owner: Mapped[Optional["backend.app.models.auth.User"]] = relationship("backend.app.models.auth.User")
    milestones: Mapped[List["OnboardingMilestone"]] = relationship("OnboardingMilestone", back_populates="plan", cascade="all, delete-orphan", order_by="OnboardingMilestone.created_at.asc()")

class OnboardingMilestone(UUIDModel, TimestampMixin):
    __tablename__ = "onboarding_milestones"

    plan_id: Mapped[str] = mapped_column(String(36), ForeignKey("customer_success_plans.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Optional[Mapped[str]] = mapped_column(Text, nullable=True)
    due_date: Optional[Mapped[date]] = mapped_column(Date, nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    completed_at: Optional[Mapped[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    plan: Mapped["CustomerSuccessPlan"] = relationship("CustomerSuccessPlan", back_populates="milestones")
""")

    # 2. schemas
    write_file("backend/app/schemas/support.py", """from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class TicketCommentCreate(BaseModel):
    body: str = Field(min_length=1)
    is_internal: Optional[bool] = False

class TicketCommentResponse(BaseModel):
    id: str
    author_id: Optional[str] = None
    body: str
    is_internal: bool
    created_at: datetime

    class Config:
        from_attributes = True

class TicketCreate(BaseModel):
    subject: str = Field(min_length=1, max_length=255)
    description: str
    priority: Optional[str] = "medium"
    category: Optional[str] = "technical"
    contact_id: Optional[str] = None
    company_id: Optional[str] = None
    assigned_to_id: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None

class TicketUpdate(BaseModel):
    subject: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    category: Optional[str] = None
    assigned_to_id: Optional[str] = None
    is_escalated: Optional[bool] = None
    custom_fields: Optional[Dict[str, Any]] = None

class TicketResolveRequest(BaseModel):
    resolution_notes: str

class TicketResponse(BaseModel):
    id: str
    tenant_id: str
    ticket_number: str
    subject: str
    description: str
    priority: str
    status: str
    category: str
    contact_id: Optional[str] = None
    company_id: Optional[str] = None
    assigned_to_id: Optional[str] = None
    is_escalated: bool
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
""")

    write_file("backend/app/schemas/customer_success.py", """from datetime import date, datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class MilestoneCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    due_date: Optional[date] = None

class MilestoneResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    is_completed: bool
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SuccessPlanCreate(BaseModel):
    company_id: str
    owner_id: Optional[str] = None
    status: Optional[str] = "onboarding"
    target_renewal_date: Optional[date] = None
    renewal_value: Optional[float] = None
    goals: Optional[List[str]] = None

class SuccessPlanResponse(BaseModel):
    id: str
    tenant_id: str
    company_id: str
    owner_id: Optional[str] = None
    status: str
    health_score: int
    health_grade: str
    target_renewal_date: Optional[date] = None
    renewal_value: Optional[float] = None
    churn_risk_reason: Optional[str] = None
    goals: List[str] = []
    milestones: List[MilestoneResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True
""")

    # 3. Repositories
    write_file("backend/app/repositories/support.py", """from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from backend.app.models.support import Ticket, TicketComment
from backend.app.repositories.base import BaseRepository

class TicketRepository(BaseRepository[Ticket]):
    def __init__(self, db: AsyncSession):
        super().__init__(Ticket, db)

    async def get_with_comments(self, id: str, tenant_id: str) -> Optional[Ticket]:
        query = select(Ticket).where(
            Ticket.id == id,
            Ticket.tenant_id == tenant_id,
            Ticket.is_deleted == False
        ).options(selectinload(Ticket.comments).selectinload(TicketComment.author))
        result = await self.db.execute(query)
        return result.scalars().first()
""")

    write_file("backend/app/repositories/customer_success.py", """from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from backend.app.models.customer_success import CustomerSuccessPlan, OnboardingMilestone
from backend.app.repositories.base import BaseRepository

class SuccessPlanRepository(BaseRepository[CustomerSuccessPlan]):
    def __init__(self, db: AsyncSession):
        super().__init__(CustomerSuccessPlan, db)

    async def get_with_milestones(self, id: str, tenant_id: str) -> Optional[CustomerSuccessPlan]:
        query = select(CustomerSuccessPlan).where(
            CustomerSuccessPlan.id == id,
            CustomerSuccessPlan.tenant_id == tenant_id,
            CustomerSuccessPlan.is_deleted == False
        ).options(selectinload(CustomerSuccessPlan.milestones))
        result = await self.db.execute(query)
        return result.scalars().first()
""")

    # 4. Services
    write_file("backend/app/services/support.py", """import secrets
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.support import Ticket, TicketComment
from backend.app.repositories.support import TicketRepository
from backend.app.services.base import BaseService
from backend.app.schemas.support import TicketCreate, TicketUpdate, TicketCommentCreate

class SupportService(BaseService[Ticket, TicketRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(TicketRepository(db))

    async def create_ticket(self, req: TicketCreate, tenant_id: str, author_id: Optional[str] = None) -> Ticket:
        t_num = f"TCK-{secrets.token_hex(4).upper()}"
        sla_hours = 4 if req.priority == "urgent" else (8 if req.priority == "high" else 24)
        sla_due = datetime.utcnow() + timedelta(hours=sla_hours)

        data = req.model_dump(exclude_unset=True)
        data["ticket_number"] = t_num
        data["created_by_id"] = author_id
        data["sla_due_at"] = sla_due
        if "custom_fields" not in data or data["custom_fields"] is None:
            data["custom_fields"] = {}

        ticket = await self.repository.create(data, tenant_id=tenant_id)

        # Log timeline activity if linked to company/contact
        if ticket.company_id:
            from backend.app.models.activity import Activity
            self.repository.db.add(Activity(
                tenant_id=tenant_id,
                entity_type="company",
                entity_id=ticket.company_id,
                activity_type="TASK",
                title=f"Support Ticket Created: {ticket.ticket_number}",
                description=ticket.subject
            ))
            await self.repository.db.flush()

        return ticket

    async def add_comment(self, ticket_id: str, req: TicketCommentCreate, author_id: Optional[str] = None, tenant_id: str = None) -> TicketComment:
        ticket = await self.get(ticket_id, tenant_id=tenant_id)
        comment = TicketComment(
            ticket_id=ticket.id,
            author_id=author_id,
            body=req.body,
            is_internal=req.is_internal or False
        )
        self.repository.db.add(comment)
        await self.repository.db.flush()
        return comment

    async def resolve_ticket(self, ticket_id: str, notes: str, tenant_id: str) -> Ticket:
        ticket = await self.get(ticket_id, tenant_id=tenant_id)
        return await self.repository.update(ticket, {
            "status": "resolved",
            "resolved_at": datetime.utcnow(),
            "resolution_notes": notes
        })
""")

    write_file("backend/app/services/customer_success.py", """from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.customer_success import CustomerSuccessPlan, OnboardingMilestone
from backend.app.models.support import Ticket
from backend.app.repositories.customer_success import SuccessPlanRepository
from backend.app.services.base import BaseService
from backend.app.schemas.customer_success import SuccessPlanCreate, MilestoneCreate

class CustomerSuccessService(BaseService[CustomerSuccessPlan, SuccessPlanRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(SuccessPlanRepository(db))

    async def create_plan(self, req: SuccessPlanCreate, tenant_id: str) -> CustomerSuccessPlan:
        data = req.model_dump(exclude_unset=True)
        if "goals" not in data or data["goals"] is None:
            data["goals"] = ["Complete onboarding setup", "Configure team access", "Import existing CRM records"]
            
        data["health_score"] = 85
        data["health_grade"] = "good"
        plan = await self.repository.create(data, tenant_id=tenant_id)

        # Standard onboarding milestones
        milestones = [
            "Technical Kickoff & Architecture Review",
            "Data Migration (Contacts & Companies)",
            "Sales Pipeline Configuration",
            "Team Training & User Onboarding"
        ]
        for m in milestones:
            self.repository.db.add(OnboardingMilestone(
                plan_id=plan.id,
                title=m,
                is_completed=False
            ))
        await self.repository.db.flush()

        return await self.repository.get_with_milestones(plan.id, tenant_id)

    async def recalculate_health_score(self, plan_id: str, tenant_id: str) -> CustomerSuccessPlan:
        plan = await self.repository.get_with_milestones(plan_id, tenant_id)
        if not plan:
            return None

        # 1. Milestone progress
        completed_m = len([m for m in plan.milestones if m.is_completed])
        total_m = len(plan.milestones) or 1
        milestone_ratio = completed_m / total_m

        # 2. Open urgent/high support tickets count
        query = select(func.count(Ticket.id)).where(
            Ticket.company_id == plan.company_id,
            Ticket.status.in_(["open", "pending", "in_progress"]),
            Ticket.priority.in_(["urgent", "high"]),
            Ticket.tenant_id == tenant_id,
            Ticket.is_deleted == False
        )
        res = await self.repository.db.execute(query)
        urgent_tickets = res.scalar() or 0

        # Health score formula
        base_score = 70 + int(milestone_ratio * 30) - (urgent_tickets * 15)
        score = max(0, min(100, base_score))

        if score >= 75:
            grade = "good"
            status = "active"
            churn_reason = None
        elif score >= 50:
            grade = "warning"
            status = "active"
            churn_reason = "Elevated support tickets or incomplete onboarding milestones"
        else:
            grade = "critical"
            status = "at_risk"
            churn_reason = "High volume of critical support issues"

        return await self.repository.update(plan, {
            "health_score": score,
            "health_grade": grade,
            "status": status,
            "churn_risk_reason": churn_reason
        })
""")

    # 5. Endpoints
    write_file("backend/app/api/v1/endpoints/support.py", """from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.support import (
    TicketCreate,
    TicketUpdate,
    TicketResponse,
    TicketCommentCreate,
    TicketCommentResponse,
    TicketResolveRequest
)
from backend.app.services.support import SupportService

router = APIRouter()

@router.post("/tickets", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    req: TicketCreate,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = SupportService(db)
    return await service.create_ticket(req, tenant_id=tenant_id, author_id=current_user.id)

@router.get("/tickets", response_model=List[TicketResponse])
async def list_tickets(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = SupportService(db)
    filters = {}
    if status:
        filters["status"] = status
    if priority:
        filters["priority"] = priority
    return await service.list(tenant_id=tenant_id, filters=filters)

@router.get("/tickets/{id}", response_model=TicketResponse)
async def get_ticket(
    id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = SupportService(db)
    return await service.get(id, tenant_id=tenant_id)

@router.post("/tickets/{id}/comments", response_model=TicketCommentResponse, status_code=status.HTTP_201_CREATED)
async def add_comment(
    id: str,
    req: TicketCommentCreate,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = SupportService(db)
    return await service.add_comment(id, req, author_id=current_user.id, tenant_id=tenant_id)

@router.post("/tickets/{id}/resolve", response_model=TicketResponse)
async def resolve_ticket(
    id: str,
    req: TicketResolveRequest,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = SupportService(db)
    return await service.resolve_ticket(id, req.resolution_notes, tenant_id=tenant_id)
""")

    write_file("backend/app/api/v1/endpoints/customer_success.py", """from fastapi import APIRouter, Depends, Query, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.customer_success import (
    SuccessPlanCreate,
    SuccessPlanResponse,
    MilestoneCreate,
    MilestoneResponse
)
from backend.app.services.customer_success import CustomerSuccessService

router = APIRouter()

@router.post("/plans", response_model=SuccessPlanResponse, status_code=status.HTTP_201_CREATED)
async def create_plan(
    req: SuccessPlanCreate,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CustomerSuccessService(db)
    return await service.create_plan(req, tenant_id=tenant_id)

@router.get("/plans", response_model=List[SuccessPlanResponse])
async def list_plans(
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CustomerSuccessService(db)
    return await service.list(tenant_id=tenant_id)

@router.get("/plans/{id}", response_model=SuccessPlanResponse)
async def get_plan(
    id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CustomerSuccessService(db)
    return await service.repository.get_with_milestones(id, tenant_id)

@router.post("/plans/{id}/recalculate-health", response_model=SuccessPlanResponse)
async def recalculate_health(
    id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CustomerSuccessService(db)
    return await service.recalculate_health_score(id, tenant_id=tenant_id)
""")

    # 6. Update api/v1/api.py
    write_file("backend/app/api/v1/api.py", """from fastapi import APIRouter
from backend.app.api.v1.endpoints import (
    health, auth, organizations, contacts, companies, leads, pipelines, deals,
    activities, tasks, calendar, communications, documents,
    products, proposals, quotes, invoices, support, customer_success
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication & Authorization"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["Organizations & Teams"])
api_router.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])
api_router.include_router(companies.router, prefix="/companies", tags=["Companies"])
api_router.include_router(leads.router, prefix="/leads", tags=["Leads & Qualification"])
api_router.include_router(pipelines.router, prefix="/pipelines", tags=["Sales Pipelines"])
api_router.include_router(deals.router, prefix="/deals", tags=["Deals"])
api_router.include_router(activities.router, prefix="/activities", tags=["Activity Timeline"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(calendar.router, prefix="/calendar", tags=["Calendar"])
api_router.include_router(communications.router, prefix="/communications", tags=["Communication System"])
api_router.include_router(documents.router, prefix="/documents", tags=["Document Management"])
api_router.include_router(products.router, prefix="/products", tags=["Product Catalog"])
api_router.include_router(proposals.router, prefix="/proposals", tags=["Proposals"])
api_router.include_router(quotes.router, prefix="/quotes", tags=["Quotes"])
api_router.include_router(invoices.router, prefix="/invoices", tags=["Invoices"])
api_router.include_router(support.router, prefix="/support", tags=["Customer Support"])
api_router.include_router(customer_success.router, prefix="/customer-success", tags=["Customer Success"])
""")

    print("Milestones 15 & 16 Customer Support & Success created successfully!")

if __name__ == '__main__':
    run()
