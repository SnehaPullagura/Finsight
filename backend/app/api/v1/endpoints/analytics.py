from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.analytics import DashboardSummaryResponse
from backend.app.services.analytics import AnalyticsService

router = APIRouter()

@router.get("/dashboard", response_model=DashboardSummaryResponse)
async def get_dashboard(
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = AnalyticsService(db)
    return await service.get_dashboard_summary(tenant_id=tenant_id)
