from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.auth.dependencies import get_current_user
from backend.app.auth.models import User
from backend.app.cashflow.schemas import CashFlowSummaryResponse
from backend.app.cashflow.service import CashFlowEngine

router = APIRouter(prefix="/cashflow", tags=["Cash Flow Engine"])

@router.get("/summary", response_model=CashFlowSummaryResponse)
async def get_cashflow_summary(
    days_past: int = Query(default=30, ge=7, le=180),
    days_future: int = Query(default=30, ge=7, le=90),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await CashFlowEngine.get_cashflow_summary(db, current_user.id, days_past, days_future)
