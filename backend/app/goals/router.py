from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.auth.dependencies import get_current_user
from backend.app.auth.models import User
from backend.app.goals.schemas import GoalCreate, GoalUpdate, GoalContributionCreate, GoalResponse
from backend.app.goals.service import GoalService

router = APIRouter(prefix="/goals", tags=["Financial Goals"])

@router.post("", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
async def create_goal(
    data: GoalCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    g = await GoalService.create_goal(db, current_user.id, data)
    goals = await GoalService.list_goals(db, current_user.id)
    return next(item for item in goals if item.id == g.id)

@router.get("", response_model=List[GoalResponse])
async def list_goals(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await GoalService.list_goals(db, current_user.id)

@router.post("/{goal_id}/contribute", response_model=GoalResponse)
async def contribute_to_goal(
    goal_id: int,
    data: GoalContributionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await GoalService.add_contribution(db, current_user.id, goal_id, data)
    goals = await GoalService.list_goals(db, current_user.id)
    return next(item for item in goals if item.id == goal_id)
