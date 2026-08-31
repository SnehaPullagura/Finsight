from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.auth.dependencies import get_current_user
from backend.app.auth.models import User
from backend.app.forecasting.schemas import FinancialForecastResponse
from backend.app.forecasting.service import FinancialForecastingEngine

router = APIRouter(prefix="/forecasts", tags=["Financial Forecasting Engine"])

@router.get("/expenses", response_model=FinancialForecastResponse)
async def get_forecast(
    horizon_days: int = Query(default=30, ge=14, le=90),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await FinancialForecastingEngine.generate_forecast(db, current_user.id, horizon_days)
