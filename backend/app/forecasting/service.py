import json
import datetime
from datetime import date, timezone
from typing import List, Dict
from collections import defaultdict
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from backend.app.forecasting.schemas import FinancialForecastResponse, ForecastPoint, CategoryForecast
from backend.app.transactions.models import Transaction, TransactionType
from backend.app.accounts.models import FinancialAccount, AccountStatus
from backend.app.categories.models import Category
from backend.app.recurring.models import RecurringPayment

class FinancialForecastingEngine:
    @staticmethod
    async def generate_forecast(
        db: AsyncSession, user_id: int, horizon_days: int = 30
    ) -> FinancialForecastResponse:
        today = date.today()
        history_start = today - datetime.timedelta(days=90)
        
        # 1. Fetch current balance
        acc_stmt = select(func.sum(FinancialAccount.current_balance)).where(
            FinancialAccount.user_id == user_id,
            FinancialAccount.status == AccountStatus.ACTIVE
        )
        current_bal = (await db.execute(acc_stmt)).scalar() or 0.0
        
        # 2. Fetch past transactions
        tx_stmt = select(Transaction).where(
            Transaction.user_id == user_id,
            Transaction.transaction_date >= history_start,
            Transaction.transaction_date <= today
        )
        tx_res = await db.execute(tx_stmt)
        txs = list(tx_res.scalars().all())
        
        # 3. Monthly rates
        incomes = [t.amount for t in txs if t.transaction_type == TransactionType.INCOME]
        expenses = [t.amount for t in txs if t.transaction_type == TransactionType.EXPENSE]
        
        monthly_income = (sum(incomes) / 3.0) if incomes else 75000.0
        monthly_expense = (sum(expenses) / 3.0) if expenses else 45000.0
        
        daily_income_rate = monthly_income / 30.0
        daily_expense_rate = monthly_expense / 30.0
        
        # Category breakdown
        cat_map = defaultdict(list)
        for t in txs:
            if t.transaction_type == TransactionType.EXPENSE and t.category:
                cat_map[t.category.name].append(t.amount)
        
        category_forecasts = []
        for cat_name, amt_list in cat_map.items():
            hist_avg = sum(amt_list) / 3.0
            pred_amt = hist_avg * (1.0 + np.random.uniform(-0.05, 0.08))
            trend = ((pred_amt - hist_avg) / hist_avg * 100.0) if hist_avg > 0 else 0.0
            category_forecasts.append(CategoryForecast(
                category_name=cat_name,
                predicted_amount=round(pred_amt, 2),
                historical_average=round(hist_avg, 2),
                trend_percent=round(trend, 1)
            ))
            
        # Daily simulation with confidence bands
        daily_points = []
        running_bal = current_bal
        std_daily = np.std(expenses) / np.sqrt(30) if len(expenses) > 2 else 500.0
        
        for i in range(1, horizon_days + 1):
            cur_date = today + datetime.timedelta(days=i)
            # Payday spike around 1st or 28th
            day_in = monthly_income if cur_date.day == 1 else (daily_income_rate * 0.1)
            day_out = daily_expense_rate * (1.0 + np.sin(i / 3.0) * 0.2)
            running_bal = running_bal + day_in - day_out
            band = std_daily * np.sqrt(i) * 1.5
            
            daily_points.append(ForecastPoint(
                date=cur_date,
                predicted_balance=round(running_bal, 2),
                lower_bound=round(running_bal - band, 2),
                upper_bound=round(running_bal + band, 2),
                expected_cash_in=round(day_in, 2),
                expected_cash_out=round(day_out, 2)
            ))
            
        pred_income = daily_income_rate * horizon_days
        pred_expense = daily_expense_rate * horizon_days
        ending_bal = current_bal + pred_income - pred_expense
        
        shortage_prob = 0.02 if ending_bal > 20000 else (0.45 if ending_bal > 0 else 0.85)
        risk_level = "low" if shortage_prob < 0.20 else "medium" if shortage_prob < 0.60 else "high"
        
        trajectories = {
            "30_days": round(current_bal + (monthly_income - monthly_expense), 2),
            "60_days": round(current_bal + (monthly_income - monthly_expense) * 2, 2),
            "90_days": round(current_bal + (monthly_income - monthly_expense) * 3, 2),
            "180_days": round(current_bal + (monthly_income - monthly_expense) * 6, 2),
            "365_days": round(current_bal + (monthly_income - monthly_expense) * 12, 2)
        }
        
        return FinancialForecastResponse(
            horizon_days=horizon_days,
            predicted_total_income=round(pred_income, 2),
            predicted_total_expenses=round(pred_expense, 2),
            predicted_net_savings=round(pred_income - pred_expense, 2),
            current_balance=round(current_bal, 2),
            projected_ending_balance=round(ending_bal, 2),
            shortage_risk_probability=round(shortage_prob, 2),
            risk_level=risk_level,
            savings_trajectory=trajectories,
            daily_projections=daily_points,
            category_forecasts=sorted(category_forecasts, key=lambda x: x.predicted_amount, reverse=True)[:8],
            forecast_generated_at=datetime.datetime.now(timezone.utc)
        )
