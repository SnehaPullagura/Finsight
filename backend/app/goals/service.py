import datetime
from datetime import date, timezone
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from backend.app.goals.models import FinancialGoal, GoalContribution, GoalStatus
from backend.app.goals.schemas import GoalCreate, GoalUpdate, GoalContributionCreate, GoalResponse
from backend.app.core.exceptions import ResourceNotFoundException

class GoalService:
    @staticmethod
    async def create_goal(db: AsyncSession, user_id: int, data: GoalCreate) -> FinancialGoal:
        goal = FinancialGoal(
            user_id=user_id,
            name=data.name,
            goal_type=data.goal_type,
            target_amount=data.target_amount,
            current_amount=data.current_amount,
            target_date=data.target_date,
            monthly_contribution=data.monthly_contribution,
            account_id=data.account_id,
            status=GoalStatus.IN_PROGRESS,
            notes=data.notes
        )
        db.add(goal)
        await db.commit()
        await db.refresh(goal)
        return goal

    @staticmethod
    async def list_goals(db: AsyncSession, user_id: int) -> List[GoalResponse]:
        stmt = select(FinancialGoal).where(FinancialGoal.user_id == user_id).order_by(FinancialGoal.target_date.asc())
        res = await db.execute(stmt)
        goals = list(res.scalars().all())
        
        today = date.today()
        responses = []
        for g in goals:
            pct = (g.current_amount / g.target_amount * 100.0) if g.target_amount > 0 else 0.0
            
            # Forecast sufficiency
            months_left = max(1, (g.target_date.year - today.year) * 12 + (g.target_date.month - today.month))
            needed_per_month = (g.target_amount - g.current_amount) / months_left if months_left > 0 else 0
            
            sufficiency = "on_track"
            if g.monthly_contribution < needed_per_month * 0.9:
                sufficiency = "behind"
            elif g.monthly_contribution > needed_per_month * 1.1:
                sufficiency = "ahead"
            
            projected_months = ((g.target_amount - g.current_amount) / g.monthly_contribution) if g.monthly_contribution > 0 else 999
            proj_date = today + datetime.timedelta(days=int(projected_months * 30.5)) if projected_months < 300 else None
            
            responses.append(GoalResponse(
                id=g.id,
                user_id=g.user_id,
                name=g.name,
                goal_type=g.goal_type,
                target_amount=g.target_amount,
                current_amount=g.current_amount,
                target_date=g.target_date,
                monthly_contribution=g.monthly_contribution,
                status=g.status,
                percentage_completed=round(min(100.0, pct), 1),
                projected_completion_date=proj_date,
                sufficiency_status=sufficiency,
                notes=g.notes,
                created_at=g.created_at
            ))
        return responses

    @staticmethod
    async def add_contribution(
        db: AsyncSession, user_id: int, goal_id: int, data: GoalContributionCreate
    ) -> FinancialGoal:
        stmt = select(FinancialGoal).where(FinancialGoal.id == goal_id, FinancialGoal.user_id == user_id)
        res = await db.execute(stmt)
        goal = res.scalar_one_or_none()
        if not goal:
            raise ResourceNotFoundException("Financial Goal", goal_id)
        
        contrib = GoalContribution(
            goal_id=goal.id,
            amount=data.amount,
            contribution_date=data.contribution_date or date.today(),
            notes=data.notes
        )
        db.add(contrib)
        goal.current_amount += data.amount
        if goal.current_amount >= goal.target_amount:
            goal.status = GoalStatus.ACHIEVED
        
        await db.commit()
        await db.refresh(goal)
        return goal
