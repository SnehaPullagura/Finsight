from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.auth.dependencies import get_current_user
from backend.app.auth.models import User
from backend.app.analytics.schemas import AnalyticsOverviewResponse
from backend.app.analytics.service import FinancialAnalyticsService

router = APIRouter(prefix="/analytics", tags=["Financial Analytics"])

@router.get("/overview", response_model=AnalyticsOverviewResponse)
async def get_analytics_overview(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await FinancialAnalyticsService.get_analytics_overview(db, current_user.id)
