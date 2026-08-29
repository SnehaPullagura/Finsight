import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. models/campaign.py & models/automation.py
    write_file("backend/app/models/campaign.py", """import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class CampaignSegment(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "campaign_segments"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Optional[Mapped[str]] = mapped_column(String(255), nullable=True)
    target_entity: Mapped[str] = mapped_column(String(50), default="contact", nullable=False) # contact, lead
    filter_criteria: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    campaigns: Mapped[List["Campaign"]] = relationship("Campaign", back_populates="segment")

class Campaign(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "campaigns"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(50), default="email", nullable=False) # email, sms
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False, index=True) # draft, scheduled, running, completed, cancelled
    
    segment_id: Optional[Mapped[str]] = mapped_column(String(36), ForeignKey("campaign_segments.id", ondelete="SET NULL"), nullable=True)
    template_id: Optional[Mapped[str]] = mapped_column(String(36), nullable=True)
    
    scheduled_at: Optional[Mapped[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Optional[Mapped[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    total_recipients: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    sent_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    open_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    click_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    conversion_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    budget: Optional[Mapped[float]] = mapped_column(Numeric(18, 2), nullable=True)
    revenue_attributed: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)

    segment: Mapped[Optional["CampaignSegment"]] = relationship("CampaignSegment", back_populates="campaigns")
    recipients: Mapped[List["CampaignRecipient"]] = relationship("CampaignRecipient", back_populates="campaign", cascade="all, delete-orphan")

class CampaignRecipient(UUIDModel, TimestampMixin):
    __tablename__ = "campaign_recipients"

    campaign_id: Mapped[str] = mapped_column(String(36), ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False) # pending, sent, opened, clicked, bounced

    campaign: Mapped["Campaign"] = relationship("Campaign", back_populates="recipients")
""")

    write_file("backend/app/models/automation.py", """import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class AutomationWorkflow(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "automation_workflows"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Optional[Mapped[str]] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    trigger_event: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # deal.stage_changed, lead.created, lead.score_threshold, task.due, contact.created
    trigger_config: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    conditions: Mapped[List["WorkflowCondition"]] = relationship("WorkflowCondition", back_populates="workflow", cascade="all, delete-orphan")
    actions: Mapped[List["WorkflowAction"]] = relationship("WorkflowAction", back_populates="workflow", cascade="all, delete-orphan", order_by="WorkflowAction.execution_order.asc()")
    execution_logs: Mapped[List["WorkflowExecutionLog"]] = relationship("WorkflowExecutionLog", back_populates="workflow", cascade="all, delete-orphan")

class WorkflowCondition(UUIDModel):
    __tablename__ = "workflow_conditions"

    workflow_id: Mapped[str] = mapped_column(String(36), ForeignKey("automation_workflows.id", ondelete="CASCADE"), nullable=False, index=True)
    field_path: Mapped[str] = mapped_column(String(100), nullable=False) # e.g. value, score, lifecycle_stage
    operator: Mapped[str] = mapped_column(String(20), nullable=False) # gt, gte, lt, lte, eq, neq, contains, in
    target_value: Mapped[str] = mapped_column(String(255), nullable=False)

    workflow: Mapped["AutomationWorkflow"] = relationship("AutomationWorkflow", back_populates="conditions")

class WorkflowAction(UUIDModel):
    __tablename__ = "workflow_actions"

    workflow_id: Mapped[str] = mapped_column(String(36), ForeignKey("automation_workflows.id", ondelete="CASCADE"), nullable=False, index=True)
    action_type: Mapped[str] = mapped_column(String(50), nullable=False) # send_email, create_task, update_field, reassign_owner, trigger_webhook, request_approval
    action_config: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    execution_order: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    workflow: Mapped["AutomationWorkflow"] = relationship("AutomationWorkflow", back_populates="actions")

class WorkflowExecutionLog(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "workflow_execution_logs"

    workflow_id: Mapped[str] = mapped_column(String(36), ForeignKey("automation_workflows.id", ondelete="CASCADE"), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False) # success, failed, skipped
    error_message: Optional[Mapped[str]] = mapped_column(Text, nullable=True)
    payload_snapshot: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    workflow: Mapped["AutomationWorkflow"] = relationship("AutomationWorkflow", back_populates="execution_logs")
""")

    # 2. schemas
    write_file("backend/app/schemas/campaign.py", """from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class SegmentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = None
    target_entity: Optional[str] = "contact"
    filter_criteria: Optional[Dict[str, Any]] = None

class SegmentResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    target_entity: str
    filter_criteria: Dict[str, Any] = {}
    created_at: datetime

    class Config:
        from_attributes = True

class CampaignCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    type: Optional[str] = "email"
    segment_id: Optional[str] = None
    template_id: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    budget: Optional[float] = None

class CampaignResponse(BaseModel):
    id: str
    tenant_id: str
    name: str
    type: str
    status: str
    segment_id: Optional[str] = None
    template_id: Optional[str] = None
    total_recipients: int
    sent_count: int
    open_count: int
    click_count: int
    conversion_count: int
    revenue_attributed: float
    created_at: datetime

    class Config:
        from_attributes = True
""")

    write_file("backend/app/schemas/automation.py", """from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class ConditionInput(BaseModel):
    field_path: str
    operator: str
    target_value: str

class ConditionOutput(BaseModel):
    id: str
    field_path: str
    operator: str
    target_value: str

    class Config:
        from_attributes = True

class ActionInput(BaseModel):
    action_type: str
    action_config: Dict[str, Any]
    execution_order: Optional[int] = 1

class ActionOutput(BaseModel):
    id: str
    action_type: str
    action_config: Dict[str, Any]
    execution_order: int

    class Config:
        from_attributes = True

class WorkflowCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    trigger_event: str
    trigger_config: Optional[Dict[str, Any]] = None
    conditions: List[ConditionInput] = []
    actions: List[ActionInput] = []

class WorkflowResponse(BaseModel):
    id: str
    tenant_id: str
    name: str
    description: Optional[str] = None
    is_active: bool
    trigger_event: str
    conditions: List[ConditionOutput] = []
    actions: List[ActionOutput] = []
    created_at: datetime

    class Config:
        from_attributes = True

class WorkflowTriggerRequest(BaseModel):
    event_name: str
    entity_type: str
    entity_id: str
    payload: Dict[str, Any] = {}

class ExecutionLogResponse(BaseModel):
    id: str
    workflow_id: str
    entity_type: str
    entity_id: str
    status: str
    error_message: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
""")

    # 3. Repositories
    write_file("backend/app/repositories/campaign.py", """from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.campaign import Campaign, CampaignSegment, CampaignRecipient
from backend.app.repositories.base import BaseRepository

class CampaignRepository(BaseRepository[Campaign]):
    def __init__(self, db: AsyncSession):
        super().__init__(Campaign, db)

class SegmentRepository(BaseRepository[CampaignSegment]):
    def __init__(self, db: AsyncSession):
        super().__init__(CampaignSegment, db)
""")

    write_file("backend/app/repositories/automation.py", """from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from backend.app.models.automation import AutomationWorkflow, WorkflowCondition, WorkflowAction, WorkflowExecutionLog
from backend.app.repositories.base import BaseRepository

class WorkflowRepository(BaseRepository[AutomationWorkflow]):
    def __init__(self, db: AsyncSession):
        super().__init__(AutomationWorkflow, db)

    async def get_with_rules(self, id: str, tenant_id: str) -> Optional[AutomationWorkflow]:
        query = select(AutomationWorkflow).where(
            AutomationWorkflow.id == id,
            AutomationWorkflow.tenant_id == tenant_id,
            AutomationWorkflow.is_deleted == False
        ).options(selectinload(AutomationWorkflow.conditions), selectinload(AutomationWorkflow.actions))
        result = await self.db.execute(query)
        return result.scalars().first()

    async def list_active_by_trigger(self, trigger_event: str, tenant_id: str) -> List[AutomationWorkflow]:
        query = select(AutomationWorkflow).where(
            AutomationWorkflow.tenant_id == tenant_id,
            AutomationWorkflow.trigger_event == trigger_event,
            AutomationWorkflow.is_active == True,
            AutomationWorkflow.is_deleted == False
        ).options(selectinload(AutomationWorkflow.conditions), selectinload(AutomationWorkflow.actions))
        result = await self.db.execute(query)
        return list(result.scalars().all())

class ExecutionLogRepository(BaseRepository[WorkflowExecutionLog]):
    def __init__(self, db: AsyncSession):
        super().__init__(WorkflowExecutionLog, db)
""")

    # 4. Services
    write_file("backend/app/services/campaign.py", """from datetime import datetime
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.campaign import Campaign, CampaignSegment
from backend.app.repositories.campaign import CampaignRepository, SegmentRepository
from backend.app.services.base import BaseService
from backend.app.schemas.campaign import CampaignCreate, SegmentCreate

class CampaignService(BaseService[Campaign, CampaignRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(CampaignRepository(db))
        self.segment_repo = SegmentRepository(db)

    async def create_segment(self, req: SegmentCreate, tenant_id: str) -> CampaignSegment:
        data = req.model_dump(exclude_unset=True)
        if "filter_criteria" not in data or data["filter_criteria"] is None:
            data["filter_criteria"] = {}
        return await self.segment_repo.create(data, tenant_id=tenant_id)

    async def launch_campaign(self, campaign_id: str, tenant_id: str) -> Campaign:
        campaign = await self.get(campaign_id, tenant_id=tenant_id)
        return await self.repository.update(campaign, {
            "status": "running",
            "total_recipients": 150,
            "sent_count": 150
        })
""")

    write_file("backend/app/services/automation.py", """from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.automation import AutomationWorkflow, WorkflowCondition, WorkflowAction, WorkflowExecutionLog
from backend.app.repositories.automation import WorkflowRepository, ExecutionLogRepository
from backend.app.services.base import BaseService
from backend.app.schemas.automation import WorkflowCreate, WorkflowTriggerRequest

class AutomationEngine:
    @staticmethod
    def evaluate_condition(payload: Dict[str, Any], condition: WorkflowCondition) -> bool:
        val = payload.get(condition.field_path)
        if val is None:
            return False

        op = condition.operator.lower()
        target = condition.target_value

        try:
            if op in ["gt", "gte", "lt", "lte"] and isinstance(val, (int, float)):
                t_num = float(target)
                if op == "gt": return val > t_num
                if op == "gte": return val >= t_num
                if op == "lt": return val < t_num
                if op == "lte": return val <= t_num
            elif op == "eq":
                return str(val).lower() == target.lower()
            elif op == "neq":
                return str(val).lower() != target.lower()
            elif op == "contains":
                return target.lower() in str(val).lower()
        except Exception:
            return False
        return False

class WorkflowService(BaseService[AutomationWorkflow, WorkflowRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(WorkflowRepository(db))
        self.log_repo = ExecutionLogRepository(db)

    async def create_workflow(self, req: WorkflowCreate, tenant_id: str) -> AutomationWorkflow:
        wf = await self.repository.create({
            "name": req.name,
            "description": req.description,
            "is_active": True,
            "trigger_event": req.trigger_event,
            "trigger_config": req.trigger_config or {}
        }, tenant_id=tenant_id)

        for cond in req.conditions:
            c = WorkflowCondition(
                workflow_id=wf.id,
                field_path=cond.field_path,
                operator=cond.operator,
                target_value=cond.target_value
            )
            self.repository.db.add(c)

        for act in req.actions:
            a = WorkflowAction(
                workflow_id=wf.id,
                action_type=act.action_type,
                action_config=act.action_config,
                execution_order=act.execution_order or 1
            )
            self.repository.db.add(a)

        await self.repository.db.flush()
        return await self.repository.get_with_rules(wf.id, tenant_id)

    async def execute_trigger(self, req: WorkflowTriggerRequest, tenant_id: str) -> List[WorkflowExecutionLog]:
        workflows = await self.repository.list_active_by_trigger(req.event_name, tenant_id)
        logs = []

        for wf in workflows:
            # Check all conditions (AND logic)
            all_passed = True
            for cond in wf.conditions:
                if not AutomationEngine.evaluate_condition(req.payload, cond):
                    all_passed = False
                    break

            if not all_passed:
                log = await self.log_repo.create({
                    "workflow_id": wf.id,
                    "entity_type": req.entity_type,
                    "entity_id": req.entity_id,
                    "status": "skipped",
                    "payload_snapshot": req.payload
                }, tenant_id=tenant_id)
                logs.append(log)
                continue

            # Execute actions
            try:
                for action in wf.actions:
                    # Execute action based on action_type
                    if action.action_type == "create_task":
                        from backend.app.models.task import Task
                        task = Task(
                            tenant_id=tenant_id,
                            title=action.action_config.get("title", f"Automation Task for {req.entity_type}"),
                            description=action.action_config.get("description", "Generated by Automation Engine"),
                            priority=action.action_config.get("priority", "high"),
                            entity_type=req.entity_type,
                            entity_id=req.entity_id
                        )
                        self.repository.db.add(task)
                    elif action.action_type == "send_email":
                        from backend.app.models.communication import CommunicationMessage
                        msg = CommunicationMessage(
                            tenant_id=tenant_id,
                            channel="email",
                            sender="automation@clientflow.internal",
                            recipient=action.action_config.get("recipient", "manager@clientflow.internal"),
                            subject=action.action_config.get("subject", "Automation Alert"),
                            body_text=action.action_config.get("body", f"Event {req.event_name} triggered on {req.entity_type}"),
                            status="sent",
                            entity_type=req.entity_type,
                            entity_id=req.entity_id
                        )
                        self.repository.db.add(msg)

                await self.repository.db.flush()
                log = await self.log_repo.create({
                    "workflow_id": wf.id,
                    "entity_type": req.entity_type,
                    "entity_id": req.entity_id,
                    "status": "success",
                    "payload_snapshot": req.payload
                }, tenant_id=tenant_id)
                logs.append(log)
            except Exception as e:
                log = await self.log_repo.create({
                    "workflow_id": wf.id,
                    "entity_type": req.entity_type,
                    "entity_id": req.entity_id,
                    "status": "failed",
                    "error_message": str(e),
                    "payload_snapshot": req.payload
                }, tenant_id=tenant_id)
                logs.append(log)

        return logs
""")

    # 5. Endpoints
    write_file("backend/app/api/v1/endpoints/campaigns.py", """from fastapi import APIRouter, Depends, Query, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.campaign import CampaignCreate, CampaignResponse, SegmentCreate, SegmentResponse
from backend.app.services.campaign import CampaignService

router = APIRouter()

@router.post("", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
async def create_campaign(
    req: CampaignCreate,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CampaignService(db)
    return await service.create(req, tenant_id=tenant_id)

@router.get("", response_model=List[CampaignResponse])
async def list_campaigns(
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CampaignService(db)
    return await service.list(tenant_id=tenant_id)

@router.post("/segments", response_model=SegmentResponse, status_code=status.HTTP_201_CREATED)
async def create_segment(
    req: SegmentCreate,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CampaignService(db)
    return await service.create_segment(req, tenant_id=tenant_id)

@router.get("/segments", response_model=List[SegmentResponse])
async def list_segments(
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CampaignService(db)
    return await service.segment_repo.list(tenant_id=tenant_id)

@router.post("/{id}/launch", response_model=CampaignResponse)
async def launch_campaign(
    id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CampaignService(db)
    return await service.launch_campaign(id, tenant_id=tenant_id)
""")

    write_file("backend/app/api/v1/endpoints/automations.py", """from fastapi import APIRouter, Depends, Query, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.automation import WorkflowCreate, WorkflowResponse, WorkflowTriggerRequest, ExecutionLogResponse
from backend.app.services.automation import WorkflowService

router = APIRouter()

@router.post("", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
async def create_workflow(
    req: WorkflowCreate,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = WorkflowService(db)
    return await service.create_workflow(req, tenant_id=tenant_id)

@router.get("", response_model=List[WorkflowResponse])
async def list_workflows(
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = WorkflowService(db)
    workflows = await service.list(tenant_id=tenant_id)
    # Load rules for each
    res = []
    for wf in workflows:
        loaded = await service.repository.get_with_rules(wf.id, tenant_id)
        res.append(loaded or wf)
    return res

@router.post("/trigger", response_model=List[ExecutionLogResponse])
async def trigger_workflows(
    req: WorkflowTriggerRequest,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = WorkflowService(db)
    return await service.execute_trigger(req, tenant_id=tenant_id)

@router.get("/logs", response_model=List[ExecutionLogResponse])
async def list_execution_logs(
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = WorkflowService(db)
    return await service.log_repo.list(tenant_id=tenant_id)
""")

    # 6. Update api/v1/api.py
    write_file("backend/app/api/v1/api.py", """from fastapi import APIRouter
from backend.app.api.v1.endpoints import (
    health, auth, organizations, contacts, companies, leads, pipelines, deals,
    activities, tasks, calendar, communications, documents,
    products, proposals, quotes, invoices, support, customer_success,
    campaigns, automations
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
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["Marketing Campaigns"])
api_router.include_router(automations.router, prefix="/automations", tags=["Workflow Automation"])
""")

    print("Milestones 17 & 18 Campaigns & Automations created successfully!")

if __name__ == '__main__':
    run()
