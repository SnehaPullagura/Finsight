from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.auth.dependencies import get_current_user
from backend.app.auth.models import User
from backend.app.health.schemas import FinancialHealthResponse
from backend.app.health.service import FinancialHealthEngine

router = APIRouter(prefix="/health", tags=["Financial Health Engine"])

@router.get("/score", response_model=FinancialHealthResponse)
async def get_financial_health_score(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await FinancialHealthEngine.compute_health_score(db, current_user.id)
