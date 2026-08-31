from typing import List, Optional
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
