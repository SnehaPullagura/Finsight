from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.auth.dependencies import get_current_user
from backend.app.auth.models import User
from backend.app.budgets.schemas import BudgetCreate, BudgetUpdate, BudgetProgressResponse
from backend.app.budgets.service import BudgetService

router = APIRouter(prefix="/budgets", tags=["Budget Management"])

@router.post("", response_model=BudgetProgressResponse, status_code=status.HTTP_201_CREATED)
async def create_budget(
    data: BudgetCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    b = await BudgetService.create_budget(db, current_user.id, data)
    progress_items = await BudgetService.get_budget_progress(db, current_user.id)
    return next(p for p in progress_items if p.id == b.id)

@router.get("", response_model=List[BudgetProgressResponse])
async def list_budgets(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await BudgetService.get_budget_progress(db, current_user.id)
