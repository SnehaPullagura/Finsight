import datetime
from datetime import date, timezone
from typing import List, Dict
from collections import defaultdict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from backend.app.cashflow.schemas import CashFlowSummaryResponse, DailyCashFlowPoint
from backend.app.transactions.models import Transaction, TransactionType
from backend.app.accounts.models import FinancialAccount, AccountStatus
from backend.app.categories.models import Category

class CashFlowEngine:
    @staticmethod
    async def get_cashflow_summary(
        db: AsyncSession, user_id: int, days_past: int = 30, days_future: int = 30
    ) -> CashFlowSummaryResponse:
        today = date.today()
        start_date = today - datetime.timedelta(days=days_past)
        
        # 1. Total liquid balance across active accounts
        acc_stmt = select(func.sum(FinancialAccount.current_balance)).where(
            FinancialAccount.user_id == user_id,
            FinancialAccount.status == AccountStatus.ACTIVE
        )
        current_total_balance = (await db.execute(acc_stmt)).scalar() or 0.0
        
        # 2. Fetch past transactions
        tx_stmt = select(Transaction).where(
            Transaction.user_id == user_id,
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= today
        ).order_by(Transaction.transaction_date.asc())
        tx_res = await db.execute(tx_stmt)
        transactions = list(tx_res.scalars().all())
        
        daily_in = defaultdict(float)
        daily_out = defaultdict(float)
        cat_out = defaultdict(float)
        
        total_in = 0.0
        total_out = 0.0
        
        for t in transactions:
            if t.transaction_type in (TransactionType.INCOME, TransactionType.REFUND, TransactionType.INTEREST):
                daily_in[t.transaction_date] += t.amount
                total_in += t.amount
            elif t.transaction_type in (TransactionType.EXPENSE, TransactionType.FEE):
                daily_out[t.transaction_date] += t.amount
                total_out += t.amount
                c_name = t.category.name if t.category else "Uncategorized"
                cat_out[c_name] += t.amount
        
        net_flow = total_in - total_out
        savings_rate = (net_flow / total_in * 100.0) if total_in > 0 else 0.0
        burn_rate = (total_out / days_past) if days_past > 0 else 0.0
        runway_days = int(current_total_balance / burn_rate) if burn_rate > 0 else 365
        
        # Build timeline from start_date to today
        timeline: List[DailyCashFlowPoint] = []
        running_balance = current_total_balance - net_flow
        
        curr = start_date
        while curr <= today:
            c_in = daily_in[curr]
            c_out = daily_out[curr]
            net_d = c_in - c_out
            running_balance += net_d
            timeline.append(DailyCashFlowPoint(
                date=curr,
                cash_in=round(c_in, 2),
                cash_out=round(c_out, 2),
                net_cash_flow=round(net_d, 2),
                projected_balance=round(running_balance, 2)
            ))
            curr += datetime.timedelta(days=1)
            
        return CashFlowSummaryResponse(
            total_cash_in=round(total_in, 2),
            total_cash_out=round(total_out, 2),
            net_cash_flow=round(net_flow, 2),
            savings_rate_percent=round(savings_rate, 1),
            average_daily_burn_rate=round(burn_rate, 2),
            liquidity_runway_days=min(999, max(0, runway_days)),
            daily_timeline=timeline,
            category_cash_out_breakdown=dict(cat_out)
        )
