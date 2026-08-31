from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.auth.dependencies import get_current_user
from backend.app.auth.models import User
from backend.app.admin.schemas import PlatformMetricsResponse, ModelRegistryResponse
from backend.app.admin.service import AdminService
from backend.app.admin.models import MLModelRegistry
from sqlalchemy import select

router = APIRouter(prefix="/admin", tags=["Admin & Model Monitoring"])

@router.get("/metrics", response_model=PlatformMetricsResponse)
async def get_metrics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await AdminService.get_platform_metrics(db)

@router.get("/models", response_model=List[ModelRegistryResponse])
async def list_models(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await AdminService.seed_model_registry(db)
    res = await db.execute(select(MLModelRegistry))
    return list(res.scalars().all())
