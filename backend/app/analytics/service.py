import datetime
from datetime import date, timezone
from typing import Dict, List
from collections import defaultdict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.app.analytics.schemas import AnalyticsOverviewResponse, MoMComparison, SpendingVelocity
from backend.app.transactions.models import Transaction, TransactionType

class FinancialAnalyticsService:
    @staticmethod
    async def get_analytics_overview(db: AsyncSession, user_id: int) -> AnalyticsOverviewResponse:
        today = date.today()
        curr_month_start = date(today.year, today.month, 1)
        prev_month_end = curr_month_start - datetime.timedelta(days=1)
        prev_month_start = date(prev_month_end.year, prev_month_end.month, 1)
        
        stmt = select(Transaction).where(
            Transaction.user_id == user_id,
            Transaction.transaction_date >= prev_month_start,
            Transaction.transaction_date <= today
        )
        res = await db.execute(stmt)
        txs = list(res.scalars().all())
        
        curr_inc = sum(t.amount for t in txs if t.transaction_type == TransactionType.INCOME and t.transaction_date >= curr_month_start)
        curr_exp = sum(t.amount for t in txs if t.transaction_type == TransactionType.EXPENSE and t.transaction_date >= curr_month_start)
        prev_inc = sum(t.amount for t in txs if t.transaction_type == TransactionType.INCOME and t.transaction_date < curr_month_start)
        prev_exp = sum(t.amount for t in txs if t.transaction_type == TransactionType.EXPENSE and t.transaction_date < curr_month_start)
        
        inc_growth = ((curr_inc - prev_inc) / prev_inc * 100.0) if prev_inc > 0 else 0.0
        exp_growth = ((curr_exp - prev_exp) / prev_exp * 100.0) if prev_exp > 0 else 0.0
        
        curr_savings_rate = ((curr_inc - curr_exp) / curr_inc * 100.0) if curr_inc > 0 else 0.0
        prev_savings_rate = ((prev_inc - prev_exp) / prev_inc * 100.0) if prev_inc > 0 else 0.0
        
        days_elapsed = max(1, today.day)
        days_in_month = 30
        daily_burn = curr_exp / days_elapsed
        projected_exp = daily_burn * days_in_month
        
        pace = "on_pace"
        if prev_exp > 0 and projected_exp > prev_exp * 1.15:
            pace = "burning_fast"
        elif prev_exp > 0 and projected_exp < prev_exp * 0.90:
            pace = "ahead_of_budget"
            
        # Top merchants & Category breakdown
        merchant_spend = defaultdict(float)
        cat_spend = defaultdict(float)
        recurring_spend = 0.0
        discretionary_spend = 0.0
        
        for t in txs:
            if t.transaction_type == TransactionType.EXPENSE:
                if t.merchant_name:
                    merchant_spend[t.merchant_name] += t.amount
                c_name = t.category.name if t.category else "Other"
                cat_spend[c_name] += t.amount
                if t.is_recurring:
                    recurring_spend += t.amount
                if t.is_discretionary:
                    discretionary_spend += t.amount
                    
        total_exp = max(1.0, curr_exp + prev_exp)
        rec_ratio = (recurring_spend / total_exp * 100.0)
        disc_ratio = (discretionary_spend / total_exp * 100.0)
        fsi = min(100.0, max(20.0, 75.0 + (curr_savings_rate * 0.5) - (exp_growth * 0.2)))
        
        top_m = [
            {"merchant": k, "amount": round(v, 2)}
            for k, v in sorted(merchant_spend.items(), key=lambda x: x[1], reverse=True)[:6]
        ]
        
        return AnalyticsOverviewResponse(
            mom=MoMComparison(
                current_month=today.strftime("%B %Y"),
                previous_month=prev_month_start.strftime("%B %Y"),
                income_current=round(curr_inc, 2),
                income_previous=round(prev_inc, 2),
                income_growth_percent=round(inc_growth, 1),
                expense_current=round(curr_exp, 2),
                expense_previous=round(prev_exp, 2),
                expense_growth_percent=round(exp_growth, 1),
                savings_rate_current=round(curr_savings_rate, 1),
                savings_rate_previous=round(prev_savings_rate, 1)
            ),
            velocity=SpendingVelocity(
                daily_burn_rate=round(daily_burn, 2),
                projected_month_end_expense=round(projected_exp, 2),
                days_elapsed=days_elapsed,
                days_remaining=days_in_month - days_elapsed,
                pace_status=pace
            ),
            financial_stability_index=round(fsi, 1),
            recurring_expense_ratio=round(rec_ratio, 1),
            discretionary_ratio=round(disc_ratio, 1),
            top_merchants=top_m,
            category_distribution=dict(cat_spend)
        )
