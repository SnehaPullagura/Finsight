from typing import List, Optional
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
