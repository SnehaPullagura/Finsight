from typing import List, Optional
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
