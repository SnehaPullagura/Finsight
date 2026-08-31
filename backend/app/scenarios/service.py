import numpy as np
from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from backend.app.scenarios.models import Scenario
from backend.app.scenarios.schemas import ScenarioCreate, ScenarioResponse, ScenarioComparisonMatrix
from backend.app.transactions.models import Transaction, TransactionType
from backend.app.accounts.models import FinancialAccount, AccountStatus
from backend.app.health.service import FinancialHealthEngine

class ScenarioSimulationEngine:
    @staticmethod
    def calculate_emi(principal: float, annual_rate: float, tenure_months: int) -> float:
        if principal <= 0 or tenure_months <= 0:
            return 0.0
        r = (annual_rate / 12.0) / 100.0
        if r == 0:
            return principal / tenure_months
        emi = (principal * r * (1 + r)**tenure_months) / ((1 + r)**tenure_months - 1)
        return emi

    @staticmethod
    async def simulate_scenario(db: AsyncSession, user_id: int, data: ScenarioCreate) -> Scenario:
        # 1. Fetch current baseline
        acc_stmt = select(func.sum(FinancialAccount.current_balance)).where(
            FinancialAccount.user_id == user_id,
            FinancialAccount.status == AccountStatus.ACTIVE
        )
        current_bal = (await db.execute(acc_stmt)).scalar() or 0.0
        
        # Recent 30 days income and expense
        tx_stmt = select(Transaction).where(Transaction.user_id == user_id)
        txs = list((await db.execute(tx_stmt)).scalars().all())
        
        base_income = sum(t.amount for t in txs if t.transaction_type == TransactionType.INCOME) / max(1.0, len(txs)/30.0) or 80000.0
        base_expense = sum(t.amount for t in txs if t.transaction_type == TransactionType.EXPENSE) / max(1.0, len(txs)/30.0) or 45000.0
        
        # 2. Compute EMI
        emi = ScenarioSimulationEngine.calculate_emi(data.loan_amount, data.loan_interest_rate, data.loan_tenure_months)
        
        # 3. New net cash flow
        new_income = base_income + data.monthly_income_delta
        new_expense = base_expense + data.monthly_expense_delta + emi
        net_flow = new_income - new_expense
        
        # 4. Projected balances
        start_bal = current_bal - data.one_time_lump_sum
        bal_6m = start_bal + (net_flow * 6)
        bal_12m = start_bal + (net_flow * 12)
        
        # 5. Feasibility & Health Score Impact
        is_feasible = bal_12m > 0 and net_flow > 0
        score_delta = +5 if net_flow > (base_income - base_expense) else -8 if net_flow < 0 else -3
        
        notes = (
            f"Feasible: generates +₹{net_flow:,.0f}/mo net cash flow with ₹{bal_12m:,.0f} projected balance after 12 months."
            if is_feasible else
            f"Risk warning: scenario creates cash flow strain (Net flow: ₹{net_flow:,.0f}/mo, 12M balance: ₹{bal_12m:,.0f})."
        )
        
        scenario = Scenario(
            user_id=user_id,
            name=data.name,
            description=data.description,
            monthly_income_delta=data.monthly_income_delta,
            monthly_expense_delta=data.monthly_expense_delta,
            one_time_lump_sum=data.one_time_lump_sum,
            loan_amount=data.loan_amount,
            loan_tenure_months=data.loan_tenure_months,
            loan_interest_rate=data.loan_interest_rate,
            calculated_monthly_emi=round(emi, 2),
            projected_6m_balance=round(bal_6m, 2),
            projected_12m_balance=round(bal_12m, 2),
            health_score_delta=score_delta,
            is_feasible=is_feasible,
            feasibility_notes=notes
        )
        db.add(scenario)
        await db.commit()
        await db.refresh(scenario)
        return scenario

    @staticmethod
    async def get_comparison_matrix(db: AsyncSession, user_id: int) -> ScenarioComparisonMatrix:
        stmt = select(Scenario).where(Scenario.user_id == user_id).order_by(Scenario.created_at.desc())
        res = await db.execute(stmt)
        scenarios = list(res.scalars().all())
        
        # Base Case
        acc_stmt = select(func.sum(FinancialAccount.current_balance)).where(
            FinancialAccount.user_id == user_id,
            FinancialAccount.status == AccountStatus.ACTIVE
        )
        current_bal = (await db.execute(acc_stmt)).scalar() or 0.0
        
        base_case = {
            "current_balance": round(current_bal, 2),
            "projected_6m_balance": round(current_bal + 150000.0, 2),
            "projected_12m_balance": round(current_bal + 300000.0, 2),
            "baseline_health_score": 78.0
        }
        
        verdict = "Scenarios evaluated against baseline liquidity and debt-service capacity."
        if scenarios:
            best = max(scenarios, key=lambda s: s.projected_12m_balance)
            verdict = f"Scenario '{best.name}' yields the highest wealth outcome with ₹{best.projected_12m_balance:,.0f} 12-month balance."
            
        return ScenarioComparisonMatrix(
            base_case=base_case,
            scenarios=scenarios,
            comparison_verdict=verdict
        )
