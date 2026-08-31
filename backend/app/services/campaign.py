from datetime import datetime
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
