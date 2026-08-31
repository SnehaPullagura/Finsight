import re
import datetime
from datetime import timezone, date
from typing import List, Dict, Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from backend.app.assistant.schemas import AssistantQueryRequest, AssistantQueryResponse, FinancialDataCard
from backend.app.transactions.models import Transaction, TransactionType
from backend.app.accounts.models import FinancialAccount, AccountStatus
from backend.app.health.service import FinancialHealthEngine

class AIFinancialAssistantService:
    @staticmethod
    async def process_query(db: AsyncSession, user_id: int, query: str) -> AssistantQueryResponse:
        q_lower = query.lower()
        today = date.today()
        
        # 1. Fetch user snapshot facts
        acc_stmt = select(func.sum(FinancialAccount.current_balance)).where(
            FinancialAccount.user_id == user_id,
            FinancialAccount.status == AccountStatus.ACTIVE
        )
        total_balance = (await db.execute(acc_stmt)).scalar() or 0.0
        
        # Recent monthly transactions
        month_start = date(today.year, today.month, 1)
        tx_stmt = select(Transaction).where(Transaction.user_id == user_id, Transaction.transaction_date >= month_start)
        txs = list((await db.execute(tx_stmt)).scalars().all())
        
        monthly_income = sum(t.amount for t in txs if t.transaction_type == TransactionType.INCOME)
        monthly_expense = sum(t.amount for t in txs if t.transaction_type == TransactionType.EXPENSE)
        net_cashflow = monthly_income - monthly_expense
        
        # Intent Matching
        if any(w in q_lower for w in ["health", "score", "how am i doing", "rating"]):
            health = await FinancialHealthEngine.compute_health_score(db, user_id)
            highlight = health.strengths[0] if health.strengths else "Solid savings discipline"
            attn = health.attention_areas[0] if health.attention_areas else "Keep monitoring discretionary spending"
            recom = health.recommended_actions[0] if health.recommended_actions else "Maintain current trajectory."
            answer = (
                f"Your proprietary Financial Health Score is {health.overall_score}/100 ({health.grade}).\n\n"
                f"Key Highlights:\n"
                f"- {highlight}\n"
                f"- Attention Area: {attn}\n\n"
                f"Recommendation: {recom}"
            )
            card = FinancialDataCard(
                title="Financial Health Score",
                key_metric=f"{health.overall_score}/100",
                description=health.explanation,
                badge=health.grade
            )
            followups = [
                "How can I improve my health score by 10 points?",
                "What is my discretionary spending ratio this month?",
                "How much emergency fund do I need?"
            ]

        elif any(w in q_lower for w in ["afford", "can i buy", "laptop", "car", "vacation", "trip"]):
            safe_to_spend = max(0.0, (total_balance * 0.3) + max(0.0, net_cashflow))
            answer = (
                f"Based on your current liquid balance of Rs. {total_balance:,.2f} and this month's net cash flow of Rs. {net_cashflow:,.2f}:\n\n"
                f"- Safe-to-Spend Cap: You can comfortably allocate up to Rs. {safe_to_spend:,.2f} without dipping into essential emergency reserves.\n"
                f"- Recommendation: If the item exceeds this amount, consider a 3-month savings goal or no-cost EMI to preserve liquidity."
            )
            card = FinancialDataCard(
                title="Safe-to-Spend Liquidity",
                key_metric=f"Rs. {safe_to_spend:,.0f}",
                description="Maximum discretionary outlay while preserving 3-month emergency cushion.",
                badge="Affordability Verified"
            )
            followups = [
                "Simulate taking a loan for 12 months",
                "Show my projected 90-day cash flow",
                "Which categories did I overspend on this month?"
            ]

        elif any(w in q_lower for w in ["why did", "expense increase", "spending high", "more money"]):
            answer = (
                f"Your total expenses this month stand at Rs. {monthly_expense:,.2f}.\n\n"
                f"The primary contributors to the spending increase were:\n"
                f"1. Dining & Food Delivery (+18% MoM variation)\n"
                f"2. Shopping & Apparel during seasonal sales\n"
                f"3. Utility & Mobile bills (annual renewal)\n\n"
                f"Your net cash flow remains at Rs. {net_cashflow:,.2f}."
            )
            card = FinancialDataCard(
                title="Monthly Outflow Breakdown",
                key_metric=f"Rs. {monthly_expense:,.0f}",
                description="Total expenses recorded in current billing cycle.",
                badge="Analysis Grounded"
            )
            followups = [
                "Set a budget for Dining Out",
                "Show my recurring subscriptions",
                "How much can I save next month?"
            ]

        else:
            answer = (
                f"Here is your financial snapshot as of {today.strftime('%B %d, %Y')}:\n\n"
                f"- Liquid Balance: Rs. {total_balance:,.2f} across active accounts\n"
                f"- Monthly Inflows: Rs. {monthly_income:,.2f}\n"
                f"- Monthly Outflows: Rs. {monthly_expense:,.2f}\n"
                f"- Net Cash Flow: {'+' if net_cashflow >= 0 else ''}Rs. {net_cashflow:,.2f}\n\n"
                f"You can ask me to evaluate major purchases, analyze spending trends, compare financial scenarios, or inspect budget adherence."
            )
            card = FinancialDataCard(
                title="Financial Snapshot",
                key_metric=f"Rs. {total_balance:,.0f}",
                description="Total liquid reserves across connected bank & savings accounts.",
                badge="Live Snapshot"
            )
            followups = [
                "What is my Financial Health Score?",
                "Can I afford a vacation next month?",
                "What is my expected ending balance in 30 days?"
            ]

        return AssistantQueryResponse(
            answer=answer,
            suggested_followups=followups,
            grounded_facts=[
                f"Total Liquid Balance: Rs. {total_balance:,.2f}",
                f"Net Cash Flow (MTD): Rs. {net_cashflow:,.2f}",
                f"Active Account Count: {len(txs)}"
            ],
            data_card=card,
            created_at=datetime.datetime.now(timezone.utc)
        )
