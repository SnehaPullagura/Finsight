from datetime import datetime, date
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
