import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. models/pipeline.py & models/deal.py
    write_file("backend/app/models/pipeline.py", """import uuid
from typing import List, Optional
from sqlalchemy import Boolean, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class Pipeline(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "pipelines"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    stages: Mapped[List["PipelineStage"]] = relationship("PipelineStage", back_populates="pipeline", cascade="all, delete-orphan", order_by="PipelineStage.stage_order")
    deals: Mapped[List["backend.app.models.deal.Deal"]] = relationship("backend.app.models.deal.Deal", back_populates="pipeline")

class PipelineStage(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "pipeline_stages"

    pipeline_id: Mapped[str] = mapped_column(String(36), ForeignKey("pipelines.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    stage_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    probability: Mapped[int] = mapped_column(Integer, default=50, nullable=False) # 0 to 100
    stage_type: Mapped[str] = mapped_column(String(20), default="open", nullable=False) # open, won, lost
    sla_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    required_fields: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    pipeline: Mapped["Pipeline"] = relationship("Pipeline", back_populates="stages")
    deals: Mapped[List["backend.app.models.deal.Deal"]] = relationship("backend.app.models.deal.Deal", back_populates="stage")
""")

    write_file("backend/app/models/deal.py", """import uuid
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class Deal(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "deals"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    value: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False, index=True)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    probability: Mapped[int] = mapped_column(Integer, default=50, nullable=False) # 0-100
    
    expected_close_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, index=True)
    actual_close_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    pipeline_id: Mapped[str] = mapped_column(String(36), ForeignKey("pipelines.id", ondelete="RESTRICT"), nullable=False, index=True)
    stage_id: Mapped[str] = mapped_column(String(36), ForeignKey("pipeline_stages.id", ondelete="RESTRICT"), nullable=False, index=True)
    
    company_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True, index=True)
    contact_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("contacts.id", ondelete="SET NULL"), nullable=True, index=True)
    owner_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    status: Mapped[str] = mapped_column(String(20), default="open", nullable=False, index=True) # open, won, lost
    loss_reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    custom_fields: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    # Relationships
    pipeline: Mapped["backend.app.models.pipeline.Pipeline"] = relationship("backend.app.models.pipeline.Pipeline", back_populates="deals")
    stage: Mapped["backend.app.models.pipeline.PipelineStage"] = relationship("backend.app.models.pipeline.PipelineStage", back_populates="deals")
    company: Mapped[Optional["backend.app.models.company.Company"]] = relationship("backend.app.models.company.Company")
    contact: Mapped[Optional["backend.app.models.contact.Contact"]] = relationship("backend.app.models.contact.Contact")
    owner: Mapped[Optional["backend.app.models.auth.User"]] = relationship("backend.app.models.auth.User")
    stage_history: Mapped[List["DealStageHistory"]] = relationship("DealStageHistory", back_populates="deal", cascade="all, delete-orphan", order_by="DealStageHistory.created_at.desc()")
    products: Mapped[List["DealProduct"]] = relationship("DealProduct", back_populates="deal", cascade="all, delete-orphan")

class DealStageHistory(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "deal_stage_histories"

    deal_id: Mapped[str] = mapped_column(String(36), ForeignKey("deals.id", ondelete="CASCADE"), nullable=False, index=True)
    from_stage_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    to_stage_id: Mapped[str] = mapped_column(String(36), nullable=False)
    changed_by_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    duration_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    deal: Mapped["Deal"] = relationship("Deal", back_populates="stage_history")

class DealProduct(UUIDModel, TimestampMixin):
    __tablename__ = "deal_products"

    deal_id: Mapped[str] = mapped_column(String(36), ForeignKey("deals.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    discount_pct: Mapped[float] = mapped_column(Numeric(5, 2), default=0.0, nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)

    deal: Mapped["Deal"] = relationship("Deal", back_populates="products")
""")

    # 2. schemas/pipeline.py & schemas/deal.py
    write_file("backend/app/schemas/pipeline.py", """from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class PipelineStageCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    stage_order: int = 0
    probability: int = Field(default=50, ge=0, le=100)
    stage_type: Optional[str] = "open"
    sla_days: Optional[int] = None
    required_fields: Optional[Dict[str, Any]] = None

class PipelineStageResponse(BaseModel):
    id: str
    pipeline_id: str
    name: str
    stage_order: int
    probability: int
    stage_type: str
    sla_days: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class PipelineCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = None
    is_default: Optional[bool] = False
    stages: Optional[List[PipelineStageCreate]] = None

class PipelineUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_default: Optional[bool] = None
    is_active: Optional[bool] = None

class PipelineResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    is_default: bool
    is_active: bool
    stages: List[PipelineStageResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True
""")

    write_file("backend/app/schemas/deal.py", """from datetime import date, datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class DealProductCreate(BaseModel):
    product_id: Optional[str] = None
    product_name: str
    quantity: int = 1
    unit_price: float
    discount_pct: Optional[float] = 0.0

class DealProductResponse(BaseModel):
    id: str
    product_name: str
    quantity: int
    unit_price: float
    discount_pct: float
    total_amount: float

    class Config:
        from_attributes = True

class DealCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    value: float = Field(default=0.0, ge=0.0)
    currency: Optional[str] = "USD"
    probability: Optional[int] = Field(default=50, ge=0, le=100)
    expected_close_date: Optional[date] = None
    pipeline_id: str
    stage_id: str
    company_id: Optional[str] = None
    contact_id: Optional[str] = None
    owner_id: Optional[str] = None
    products: Optional[List[DealProductCreate]] = None
    custom_fields: Optional[Dict[str, Any]] = None

class DealUpdate(BaseModel):
    name: Optional[str] = None
    value: Optional[float] = None
    currency: Optional[str] = None
    probability: Optional[int] = None
    expected_close_date: Optional[date] = None
    actual_close_date: Optional[date] = None
    pipeline_id: Optional[str] = None
    stage_id: Optional[str] = None
    company_id: Optional[str] = None
    contact_id: Optional[str] = None
    owner_id: Optional[str] = None
    status: Optional[str] = None
    loss_reason: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None

class DealStageTransitionRequest(BaseModel):
    stage_id: str
    loss_reason: Optional[str] = None

class DealResponse(BaseModel):
    id: str
    tenant_id: str
    name: str
    value: float
    currency: str
    probability: int
    expected_close_date: Optional[date] = None
    actual_close_date: Optional[date] = None
    pipeline_id: str
    stage_id: str
    company_id: Optional[str] = None
    contact_id: Optional[str] = None
    owner_id: Optional[str] = None
    status: str
    loss_reason: Optional[str] = None
    custom_fields: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class KanbanColumn(BaseModel):
    stage_id: str
    stage_name: str
    probability: int
    stage_type: str
    deals: List[DealResponse] = []
    total_value: float = 0.0
    deal_count: int = 0

class KanbanBoardResponse(BaseModel):
    pipeline_id: str
    pipeline_name: str
    columns: List[KanbanColumn]
""")

    # 3. repositories/pipeline.py & repositories/deal.py
    write_file("backend/app/repositories/pipeline.py", """from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from backend.app.models.pipeline import Pipeline, PipelineStage
from backend.app.repositories.base import BaseRepository

class PipelineRepository(BaseRepository[Pipeline]):
    def __init__(self, db: AsyncSession):
        super().__init__(Pipeline, db)

    async def get_with_stages(self, id: str, tenant_id: str) -> Optional[Pipeline]:
        query = select(Pipeline).where(
            Pipeline.id == id,
            Pipeline.tenant_id == tenant_id,
            Pipeline.is_deleted == False
        ).options(selectinload(Pipeline.stages))
        result = await self.db.execute(query)
        return result.scalars().first()

    async def list_pipelines_with_stages(self, tenant_id: str) -> List[Pipeline]:
        query = select(Pipeline).where(
            Pipeline.tenant_id == tenant_id,
            Pipeline.is_deleted == False
        ).options(selectinload(Pipeline.stages)).order_by(Pipeline.created_at)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_default_pipeline(self, tenant_id: str) -> Optional[Pipeline]:
        query = select(Pipeline).where(
            Pipeline.tenant_id == tenant_id,
            Pipeline.is_default == True,
            Pipeline.is_deleted == False
        ).options(selectinload(Pipeline.stages))
        result = await self.db.execute(query)
        return result.scalars().first()

class PipelineStageRepository(BaseRepository[PipelineStage]):
    def __init__(self, db: AsyncSession):
        super().__init__(PipelineStage, db)

    async def list_by_pipeline(self, pipeline_id: str, tenant_id: str) -> List[PipelineStage]:
        query = select(PipelineStage).where(
            PipelineStage.pipeline_id == pipeline_id,
            PipelineStage.tenant_id == tenant_id
        ).order_by(PipelineStage.stage_order)
        result = await self.db.execute(query)
        return list(result.scalars().all())
""")

    write_file("backend/app/repositories/deal.py", """from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from backend.app.models.deal import Deal, DealStageHistory, DealProduct
from backend.app.repositories.base import BaseRepository

class DealRepository(BaseRepository[Deal]):
    def __init__(self, db: AsyncSession):
        super().__init__(Deal, db)

    async def get_with_relations(self, id: str, tenant_id: str) -> Optional[Deal]:
        query = select(Deal).where(
            Deal.id == id,
            Deal.tenant_id == tenant_id,
            Deal.is_deleted == False
        ).options(
            selectinload(Deal.stage),
            selectinload(Deal.pipeline),
            selectinload(Deal.products),
            selectinload(Deal.stage_history)
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def list_by_pipeline(self, pipeline_id: str, tenant_id: str) -> List[Deal]:
        query = select(Deal).where(
            Deal.pipeline_id == pipeline_id,
            Deal.tenant_id == tenant_id,
            Deal.is_deleted == False
        ).order_by(Deal.created_at.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())

class DealStageHistoryRepository(BaseRepository[DealStageHistory]):
    def __init__(self, db: AsyncSession):
        super().__init__(DealStageHistory, db)
""")

    # 4. services/pipeline.py & services/deal.py
    write_file("backend/app/services/pipeline.py", """from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.exceptions import EntityNotFoundException
from backend.app.models.pipeline import Pipeline, PipelineStage
from backend.app.repositories.pipeline import PipelineRepository, PipelineStageRepository
from backend.app.services.base import BaseService
from backend.app.schemas.pipeline import PipelineCreate, PipelineUpdate, PipelineStageCreate

DEFAULT_STAGES = [
    {"name": "Lead / Qualification", "stage_order": 1, "probability": 10, "stage_type": "open"},
    {"name": "Meeting / Discovery", "stage_order": 2, "probability": 30, "stage_type": "open"},
    {"name": "Proposal / Quote", "stage_order": 3, "probability": 60, "stage_type": "open"},
    {"name": "Negotiation", "stage_order": 4, "probability": 80, "stage_type": "open"},
    {"name": "Closed Won", "stage_order": 5, "probability": 100, "stage_type": "won"},
    {"name": "Closed Lost", "stage_order": 6, "probability": 0, "stage_type": "lost"},
]

class PipelineService(BaseService[Pipeline, PipelineRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(PipelineRepository(db))
        self.stage_repo = PipelineStageRepository(db)

    async def create_default_pipeline_if_none(self, tenant_id: str) -> Pipeline:
        existing = await self.repository.get_default_pipeline(tenant_id)
        if existing:
            return existing

        pipeline = await self.repository.create({
            "name": "Standard Sales Pipeline",
            "description": "Default sales pipeline for new deals",
            "is_default": True,
            "is_active": True
        }, tenant_id=tenant_id)

        for s in DEFAULT_STAGES:
            await self.stage_repo.create({
                "pipeline_id": pipeline.id,
                "name": s["name"],
                "stage_order": s["stage_order"],
                "probability": s["probability"],
                "stage_type": s["stage_type"]
            }, tenant_id=tenant_id)

        return await self.repository.get_with_stages(pipeline.id, tenant_id)

    async def create_pipeline(self, schema_in: PipelineCreate, tenant_id: str) -> Pipeline:
        pipeline = await self.repository.create({
            "name": schema_in.name,
            "description": schema_in.description,
            "is_default": schema_in.is_default or False,
            "is_active": True
        }, tenant_id=tenant_id)

        stages_to_create = schema_in.stages or [PipelineStageCreate(**s) for s in DEFAULT_STAGES]
        for idx, stage in enumerate(stages_to_create):
            data = stage.model_dump()
            data["pipeline_id"] = pipeline.id
            if not data.get("stage_order"):
                data["stage_order"] = idx + 1
            await self.stage_repo.create(data, tenant_id=tenant_id)

        return await self.repository.get_with_stages(pipeline.id, tenant_id)

    async def list_pipelines(self, tenant_id: str) -> List[Pipeline]:
        pipelines = await self.repository.list_pipelines_with_stages(tenant_id)
        if not pipelines:
            await self.create_default_pipeline_if_none(tenant_id)
            pipelines = await self.repository.list_pipelines_with_stages(tenant_id)
        return pipelines
""")

    write_file("backend/app/services/deal.py", """from datetime import datetime, date
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.exceptions import EntityNotFoundException, ValidationException
from backend.app.models.deal import Deal, DealStageHistory, DealProduct
from backend.app.repositories.deal import DealRepository, DealStageHistoryRepository
from backend.app.repositories.pipeline import PipelineRepository, PipelineStageRepository
from backend.app.services.base import BaseService
from backend.app.schemas.deal import (
    DealCreate,
    DealUpdate,
    DealStageTransitionRequest,
    DealResponse,
    KanbanBoardResponse,
    KanbanColumn
)

class DealService(BaseService[Deal, DealRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(DealRepository(db))
        self.stage_repo = PipelineStageRepository(db)
        self.pipeline_repo = PipelineRepository(db)
        self.history_repo = DealStageHistoryRepository(db)

    async def create_deal(self, schema_in: DealCreate, tenant_id: str, actor_id: Optional[str] = None) -> Deal:
        # Validate stage
        stage = await self.stage_repo.get_by_id(schema_in.stage_id, tenant_id=tenant_id)
        if not stage:
            raise EntityNotFoundException("PipelineStage", schema_in.stage_id)

        data = schema_in.model_dump(exclude_unset=True, exclude={"products"})
        if "custom_fields" not in data or data["custom_fields"] is None:
            data["custom_fields"] = {}
        if not data.get("probability"):
            data["probability"] = stage.probability
            
        data["status"] = stage.stage_type

        deal = await self.repository.create(data, tenant_id=tenant_id)

        # Log initial stage
        await self.history_repo.create({
            "deal_id": deal.id,
            "from_stage_id": None,
            "to_stage_id": stage.id,
            "changed_by_id": actor_id
        }, tenant_id=tenant_id)

        return deal

    async def transition_stage(self, deal_id: str, req: DealStageTransitionRequest, tenant_id: str, actor_id: Optional[str] = None) -> Deal:
        deal = await self.get(deal_id, tenant_id=tenant_id)
        stage = await self.stage_repo.get_by_id(req.stage_id, tenant_id=tenant_id)
        if not stage:
            raise EntityNotFoundException("PipelineStage", req.stage_id)

        old_stage_id = deal.stage_id
        update_data = {
            "stage_id": stage.id,
            "probability": stage.probability,
            "status": stage.stage_type
        }
        
        if stage.stage_type == "won":
            update_data["actual_close_date"] = date.today()
            update_data["loss_reason"] = None
        elif stage.stage_type == "lost":
            update_data["actual_close_date"] = date.today()
            update_data["loss_reason"] = req.loss_reason or "Unspecified"

        updated_deal = await self.repository.update(deal, update_data)

        # Record history
        await self.history_repo.create({
            "deal_id": deal.id,
            "from_stage_id": old_stage_id,
            "to_stage_id": stage.id,
            "changed_by_id": actor_id
        }, tenant_id=tenant_id)

        return updated_deal

    async def get_kanban_board(self, pipeline_id: Optional[str], tenant_id: str) -> KanbanBoardResponse:
        if not pipeline_id:
            default_p = await self.pipeline_repo.get_default_pipeline(tenant_id)
            if not default_p:
                from backend.app.services.pipeline import PipelineService
                p_service = PipelineService(self.repository.db)
                default_p = await p_service.create_default_pipeline_if_none(tenant_id)
            pipeline_id = default_p.id

        pipeline = await self.pipeline_repo.get_with_stages(pipeline_id, tenant_id)
        if not pipeline:
            raise EntityNotFoundException("Pipeline", pipeline_id)

        deals = await self.repository.list_by_pipeline(pipeline.id, tenant_id)
        
        columns = []
        for stage in sorted(pipeline.stages, key=lambda s: s.stage_order):
            stage_deals = [d for d in deals if d.stage_id == stage.id]
            total_val = sum(float(d.value or 0.0) for d in stage_deals)
            columns.append(KanbanColumn(
                stage_id=stage.id,
                stage_name=stage.name,
                probability=stage.probability,
                stage_type=stage.stage_type,
                deals=[DealResponse.model_validate(d) for d in stage_deals],
                total_value=total_val,
                deal_count=len(stage_deals)
            ))

        return KanbanBoardResponse(
            pipeline_id=pipeline.id,
            pipeline_name=pipeline.name,
            columns=columns
        )
""")

    # 5. endpoints/pipelines.py & endpoints/deals.py
    write_file("backend/app/api/v1/endpoints/pipelines.py", """from fastapi import APIRouter, Depends, Query, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.pipeline import (
    PipelineCreate,
    PipelineUpdate,
    PipelineResponse,
    PipelineStageCreate,
    PipelineStageResponse
)
from backend.app.services.pipeline import PipelineService

router = APIRouter()

@router.post("", response_model=PipelineResponse, status_code=status.HTTP_201_CREATED)
async def create_pipeline(
    req: PipelineCreate,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = PipelineService(db)
    return await service.create_pipeline(req, tenant_id=tenant_id)

@router.get("", response_model=List[PipelineResponse])
async def list_pipelines(
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = PipelineService(db)
    return await service.list_pipelines(tenant_id=tenant_id)

@router.get("/{id}", response_model=PipelineResponse)
async def get_pipeline(
    id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = PipelineService(db)
    pipeline = await service.repository.get_with_stages(id, tenant_id)
    return pipeline

@router.post("/{id}/stages", response_model=PipelineStageResponse, status_code=status.HTTP_201_CREATED)
async def create_stage(
    id: str,
    req: PipelineStageCreate,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = PipelineService(db)
    data = req.model_dump()
    data["pipeline_id"] = id
    return await service.stage_repo.create(data, tenant_id=tenant_id)
""")

    write_file("backend/app/api/v1/endpoints/deals.py", """from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.deal import (
    DealCreate,
    DealUpdate,
    DealStageTransitionRequest,
    DealResponse,
    KanbanBoardResponse
)
from backend.app.services.deal import DealService

router = APIRouter()

@router.post("", response_model=DealResponse, status_code=status.HTTP_201_CREATED)
async def create_deal(
    req: DealCreate,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = DealService(db)
    return await service.create_deal(req, tenant_id=tenant_id, actor_id=current_user.id)

@router.get("", response_model=List[DealResponse])
async def list_deals(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    pipeline_id: Optional[str] = None,
    stage_id: Optional[str] = None,
    status: Optional[str] = None,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = DealService(db)
    filters = {}
    if pipeline_id:
        filters["pipeline_id"] = pipeline_id
    if stage_id:
        filters["stage_id"] = stage_id
    if status:
        filters["status"] = status
    return await service.list(tenant_id=tenant_id, skip=skip, limit=limit, filters=filters)

@router.get("/kanban", response_model=KanbanBoardResponse)
async def get_kanban_board(
    pipeline_id: Optional[str] = Query(None),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = DealService(db)
    return await service.get_kanban_board(pipeline_id, tenant_id=tenant_id)

@router.get("/{id}", response_model=DealResponse)
async def get_deal(
    id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = DealService(db)
    return await service.get(id, tenant_id=tenant_id)

@router.put("/{id}", response_model=DealResponse)
async def update_deal(
    id: str,
    req: DealUpdate,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = DealService(db)
    return await service.update(id, req, tenant_id=tenant_id, actor_id=current_user.id)

@router.post("/{id}/stage", response_model=DealResponse)
async def transition_deal_stage(
    id: str,
    req: DealStageTransitionRequest,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = DealService(db)
    return await service.transition_stage(id, req, tenant_id=tenant_id, actor_id=current_user.id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_deal(
    id: str,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = DealService(db)
    await service.delete(id, tenant_id=tenant_id, actor_id=current_user.id)
""")

    # 6. Update api/v1/api.py
    write_file("backend/app/api/v1/api.py", """from fastapi import APIRouter
from backend.app.api.v1.endpoints import (
    health, auth, organizations, contacts, companies, leads, pipelines, deals
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
""")

    print("Milestone 8 Pipelines & Deals created successfully!")

if __name__ == '__main__':
    run()
