from fastapi import APIRouter, Depends, Query, status
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
