import datetime
from datetime import date, timezone
from typing import List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from backend.app.budgets.models import Budget, BudgetPeriod
from backend.app.budgets.schemas import BudgetCreate, BudgetUpdate, BudgetProgressResponse
from backend.app.transactions.models import Transaction, TransactionType
from backend.app.categories.models import Category
from backend.app.core.exceptions import ResourceNotFoundException

class BudgetService:
    @staticmethod
    async def create_budget(db: AsyncSession, user_id: int, data: BudgetCreate) -> Budget:
        budget = Budget(
            user_id=user_id,
            category_id=data.category_id,
            name=data.name,
            allocated_amount=data.allocated_amount,
            period=data.period,
            start_date=data.start_date,
            end_date=data.end_date,
            notify_threshold_percent=data.notify_threshold_percent,
            is_active=True
        )
        db.add(budget)
        await db.commit()
        await db.refresh(budget)
        return budget

    @staticmethod
    async def get_budget_progress(db: AsyncSession, user_id: int) -> List[BudgetProgressResponse]:
        stmt = select(Budget).where(Budget.user_id == user_id, Budget.is_active == True)
        res = await db.execute(stmt)
        budgets = list(res.scalars().all())
        
        now = date.today()
        month_start = date(now.year, now.month, 1)
        
        progress_list = []
        for b in budgets:
            # Query actual spent
            tx_query = select(func.sum(Transaction.amount)).where(
                Transaction.user_id == user_id,
                Transaction.transaction_type == TransactionType.EXPENSE,
                Transaction.transaction_date >= month_start,
                Transaction.transaction_date <= now
            )
            if b.category_id:
                tx_query = tx_query.where(Transaction.category_id == b.category_id)
            
            spent = (await db.execute(tx_query)).scalar() or 0.0
            remaining = max(0.0, b.allocated_amount - spent)
            percent = (spent / b.allocated_amount * 100.0) if b.allocated_amount > 0 else 0.0
            
            status_str = "good"
            if percent >= 100.0:
                status_str = "exceeded"
            elif percent >= b.notify_threshold_percent:
                status_str = "warning"
            
            cat_obj = None
            if b.category_id:
                cat_res = await db.execute(select(Category).where(Category.id == b.category_id))
                cat_obj = cat_res.scalar_one_or_none()
            
            progress_list.append(BudgetProgressResponse(
                id=b.id,
                user_id=b.user_id,
                category_id=b.category_id,
                name=b.name,
                allocated_amount=b.allocated_amount,
                spent_amount=round(spent, 2),
                remaining_amount=round(remaining, 2),
                percentage_used=round(percent, 1),
                is_overbudget=spent > b.allocated_amount,
                status=status_str,
                category=cat_obj
            ))
        return progress_list
