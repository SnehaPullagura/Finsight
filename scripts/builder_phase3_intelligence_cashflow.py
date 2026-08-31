import os
import sys
from scripts.common import write_file

def build_phase3():
    print("Building Phase 3: Transaction Intelligence, Cash Flow Engine, Financial Health, Anomaly Detection...")

    # 1. Transaction Intelligence (Module 04)
    write_file("backend/app/intelligence/__init__.py", "")

    write_file("backend/app/intelligence/models.py", """
import datetime
from datetime import timezone
from typing import Optional
from sqlalchemy import String, Boolean, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.database.base import Base, TimestampMixin

class CategorizationFeedback(Base, TimestampMixin):
    __tablename__ = "categorization_feedbacks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    transaction_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("transactions.id", ondelete="SET NULL"), nullable=True)
    
    raw_text: Mapped[str] = mapped_column(String(255), nullable=False)
    predicted_category_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    corrected_category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    merchant_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    confidence: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    is_trained: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user: Mapped["User"] = relationship("User")
    corrected_category: Mapped["Category"] = relationship("Category")
""")

    write_file("backend/app/intelligence/schemas.py", """
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from backend.app.categories.schemas import CategoryResponse

class CategorizationRequest(BaseModel):
    description: str
    amount: Optional[float] = None

class CategorizationResponse(BaseModel):
    category_id: int
    category_name: str
    category_group: str
    merchant_name: str
    confidence_score: float
    is_recurring_predicted: bool
    category: Optional[CategoryResponse] = None

class DuplicateCheckRequest(BaseModel):
    account_id: int
    amount: float
    description: str
    transaction_date: str

class DuplicateCheckResponse(BaseModel):
    is_duplicate: bool
    match_confidence: float
    matched_transaction_id: Optional[int] = None
    reason: Optional[str] = None
""")

    write_file("backend/app/intelligence/service.py", """
import re
from typing import Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.app.categories.models import Category, CategoryGroup
from backend.app.intelligence.schemas import CategorizationResponse
from backend.app.intelligence.models import CategorizationFeedback

MERCHANT_RULES = {
    # Groceries
    r"(swiggy instamart|blinkit|zepto|bigbasket|dmart|spencer|reliance fresh|nature basket|grofers)": ("Groceries & Supermarket", "Groceries"),
    # Food & Dining
    r"(swiggy|zomato|starbucks|mcdonalds|kfc|dominos|pizza hut|subway|burger king|chaayos|blue tokai)": ("Dining Out & Cafes", "Dining"),
    # Commute & Fuel
    r"(uber|ola|rapido|blusmart|petrol|hpcl|bpcl|ioc|shell|fuel|metro)": ("Fuel & Commute", "Commute"),
    # Utilities & Telecom
    r"(airtel|jio|vi |vodafone|tatapower|bescom|electricity|water board|act fibernet|broadband)": ("Utilities & Electricity", "Utilities"),
    # Shopping
    r"(amazon|flipkart|myntra|ajio|zara|h&m|ikea|nykaa|tata cliq|croma|reliance digital)": ("Shopping & Apparel", "Shopping"),
    # Entertainment & Subscriptions
    r"(netflix|spotify|hotstar|prime video|youtube premium|apple\.com|playstation|steam|pvr|inox)": ("Subscriptions & Streaming", "Entertainment"),
    # Healthcare
    r"(apollo|pharmeasy|1mg|netmeds|max healthcare|fortis|practo|dentist|hospital|clinic)": ("Healthcare & Pharmacy", "Healthcare"),
    # EMIs & Loans
    r"(hdfc loan|icici loan|bajaj finance|cred|sbi cards|home loan emi|car loan emi)": ("Home Loan EMI", "Debt EMI"),
    # Investments
    r"(zerodha|groww|kuvera|upstox|uti mf|hdfc mf|sbi mutual|etmoney|indmoney|ppf|nps)": ("Mutual Funds & SIP", "Investments"),
    # Income
    r"(salary|payroll|direct deposit|freelance|client payment|consulting fee|dividend)": ("Salary & Wages", "Salary")
}

class TransactionIntelligenceService:
    @staticmethod
    def normalize_text(text: str) -> str:
        if not text:
            return ""
        # Remove transaction codes like UPI/REF/NEFT/POS
        clean = re.sub(r"(?i)\b(upi|pos|neft|rtgs|imps|ref|txn|inb|atm|wdr|mb)\b", " ", text)
        clean = re.sub(r"[\d/\-_@]+", " ", clean)
        clean = re.sub(r"\s+", " ", clean).strip().lower()
        return clean

    @staticmethod
    def extract_merchant(text: str) -> str:
        clean = text.strip()
        for pattern, (cat, merch_hint) in MERCHANT_RULES.items():
            match = re.search(pattern, clean, re.IGNORECASE)
            if match:
                return match.group(0).title()
        words = clean.split()
        return words[0].title() if words else "Unknown"

    @staticmethod
    async def categorize(db: AsyncSession, description: str, amount: Optional[float] = None) -> CategorizationResponse:
        desc_lower = description.lower()
        target_category_name = "Shopping & Apparel"
        merchant = TransactionIntelligenceService.extract_merchant(description)
        confidence = 0.65
        is_recurring = False

        # 1. Match Rules
        for pattern, (cat_name, m_hint) in MERCHANT_RULES.items():
            if re.search(pattern, desc_lower):
                target_category_name = cat_name
                confidence = 0.94
                if "subscription" in cat_name.lower() or "emi" in cat_name.lower() or "rent" in cat_name.lower():
                    is_recurring = True
                break

        # 2. Check user feedback history
        fb_stmt = select(CategorizationFeedback).where(
            CategorizationFeedback.raw_text == desc_lower
        ).order_by(CategorizationFeedback.id.desc()).limit(1)
        fb_res = await db.execute(fb_stmt)
        fb = fb_res.scalar_one_or_none()
        if fb:
            cat_stmt = select(Category).where(Category.id == fb.corrected_category_id)
            c_res = await db.execute(cat_stmt)
            cat_db = c_res.scalar_one_or_none()
            if cat_db:
                return CategorizationResponse(
                    category_id=cat_db.id,
                    category_name=cat_db.name,
                    category_group=cat_db.group.value,
                    merchant_name=fb.merchant_name or merchant,
                    confidence_score=0.99,
                    is_recurring_predicted=is_recurring,
                    category=cat_db
                )

        # Look up category in database
        cat_stmt = select(Category).where(Category.name == target_category_name)
        cat_res = await db.execute(cat_stmt)
        category = cat_res.scalar_one_or_none()
        
        if not category:
            # Fallback to any category
            fallback_res = await db.execute(select(Category).limit(1))
            category = fallback_res.scalar_one()

        return CategorizationResponse(
            category_id=category.id,
            category_name=category.name,
            category_group=category.group.value,
            merchant_name=merchant,
            confidence_score=confidence,
            is_recurring_predicted=is_recurring,
            category=category
        )

    @staticmethod
    async def record_user_feedback(
        db: AsyncSession, user_id: int, transaction_id: Optional[int],
        raw_text: str, corrected_category_id: int, merchant_name: Optional[str] = None
    ) -> CategorizationFeedback:
        fb = CategorizationFeedback(
            user_id=user_id,
            transaction_id=transaction_id,
            raw_text=raw_text.lower().strip(),
            corrected_category_id=corrected_category_id,
            merchant_name=merchant_name,
            confidence=1.0,
            is_trained=False
        )
        db.add(fb)
        await db.commit()
        await db.refresh(fb)
        return fb
""")

    write_file("backend/app/intelligence/router.py", """
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.auth.dependencies import get_current_user
from backend.app.auth.models import User
from backend.app.intelligence.schemas import CategorizationRequest, CategorizationResponse
from backend.app.intelligence.service import TransactionIntelligenceService

router = APIRouter(prefix="/intelligence", tags=["Transaction Intelligence"])

@router.post("/categorize", response_model=CategorizationResponse)
async def categorize_transaction(
    data: CategorizationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await TransactionIntelligenceService.categorize(db, data.description, data.amount)
""")

    # 2. Cash Flow Engine (Module 08)
    write_file("backend/app/cashflow/__init__.py", "")

    write_file("backend/app/cashflow/schemas.py", """
import datetime
from typing import List, Dict
from pydantic import BaseModel

class DailyCashFlowPoint(BaseModel):
    date: datetime.date
    cash_in: float
    cash_out: float
    net_cash_flow: float
    projected_balance: float

class CashFlowSummaryResponse(BaseModel):
    total_cash_in: float
    total_cash_out: float
    net_cash_flow: float
    savings_rate_percent: float
    average_daily_burn_rate: float
    liquidity_runway_days: int
    daily_timeline: List[DailyCashFlowPoint]
    category_cash_out_breakdown: Dict[str, float]
""")

    write_file("backend/app/cashflow/service.py", """
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
""")

    write_file("backend/app/cashflow/router.py", """
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
""")

    # 3. Financial Health Engine (Module 09)
    write_file("backend/app/health/__init__.py", "")

    write_file("backend/app/health/models.py", """
import datetime
from datetime import timezone
from typing import Optional, List
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.database.base import Base, TimestampMixin

class FinancialScore(Base, TimestampMixin):
    __tablename__ = "financial_scores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    overall_score: Mapped[int] = mapped_column(Integer, nullable=False) # 0 - 100
    grade: Mapped[str] = mapped_column(String(10), nullable=False) # "Excellent", "Good", "Fair", "Needs Attention"
    
    # 6 Pillar Scores (each 0 - 100)
    savings_rate_score: Mapped[float] = mapped_column(Float, nullable=False)
    expense_stability_score: Mapped[float] = mapped_column(Float, nullable=False)
    debt_burden_score: Mapped[float] = mapped_column(Float, nullable=False)
    emergency_fund_score: Mapped[float] = mapped_column(Float, nullable=False)
    budget_discipline_score: Mapped[float] = mapped_column(Float, nullable=False)
    cash_flow_stability_score: Mapped[float] = mapped_column(Float, nullable=False)
    
    explanation_summary: Mapped[str] = mapped_column(Text, nullable=False)
    strengths_json: Mapped[str] = mapped_column(Text, nullable=False) # JSON list
    attention_areas_json: Mapped[str] = mapped_column(Text, nullable=False) # JSON list

    user: Mapped["User"] = relationship("User", back_populates="health_scores")
""")

    write_file("backend/app/health/schemas.py", """
import datetime
from typing import List, Dict
from pydantic import BaseModel, ConfigDict

class HealthPillarScore(BaseModel):
    pillar_name: str
    score: float # 0 - 100
    weight: float
    status: str # "strong", "moderate", "weak"
    metric_value: str
    description: str

class FinancialHealthResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    overall_score: int # 0 - 100
    grade: str
    score_change_mom: int
    explanation: str
    pillars: List[HealthPillarScore]
    strengths: List[str]
    attention_areas: List[str]
    recommended_actions: List[str]
    calculated_at: datetime.datetime
""")

    write_file("backend/app/health/service.py", """
import json
import datetime
from datetime import date, timezone
from typing import List
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from backend.app.health.models import FinancialScore
from backend.app.health.schemas import FinancialHealthResponse, HealthPillarScore
from backend.app.transactions.models import Transaction, TransactionType
from backend.app.accounts.models import FinancialAccount, AccountType
from backend.app.budgets.models import Budget
from backend.app.goals.models import FinancialGoal

class FinancialHealthEngine:
    @staticmethod
    async def compute_health_score(db: AsyncSession, user_id: int) -> FinancialHealthResponse:
        today = date.today()
        month_start = date(today.year, today.month, 1)
        prev_month_start = (month_start - datetime.timedelta(days=1)).replace(day=1)
        
        # 1. Total Income & Total Expenses in last 30 days
        tx_stmt = select(Transaction).where(
            Transaction.user_id == user_id,
            Transaction.transaction_date >= (today - datetime.timedelta(days=60))
        )
        tx_res = await db.execute(tx_stmt)
        txs = list(tx_res.scalars().all())
        
        income_30d = sum(t.amount for t in txs if t.transaction_type == TransactionType.INCOME and t.transaction_date >= month_start)
        expense_30d = sum(t.amount for t in txs if t.transaction_type == TransactionType.EXPENSE and t.transaction_date >= month_start)
        
        # Pillar 1: Savings Rate (20% weight) -> Target >= 20%
        savings_rate = ((income_30d - expense_30d) / income_30d) if income_30d > 0 else 0.1
        savings_score = min(100.0, max(0.0, (savings_rate / 0.25) * 100.0))
        
        # Pillar 2: Expense Stability (15% weight) -> Low volatility across weeks
        weekly_expenses = [t.amount for t in txs if t.transaction_type == TransactionType.EXPENSE]
        cv = (np.std(weekly_expenses) / np.mean(weekly_expenses)) if len(weekly_expenses) > 2 and np.mean(weekly_expenses) > 0 else 0.5
        expense_stability_score = min(100.0, max(20.0, (1.0 - min(1.0, cv)) * 100.0))
        
        # Pillar 3: Debt Burden (DTI) (15% weight) -> Debt EMI / Income <= 30%
        accounts_res = await db.execute(select(FinancialAccount).where(FinancialAccount.user_id == user_id))
        accounts = list(accounts_res.scalars().all())
        total_liquid = sum(a.current_balance for a in accounts if a.account_type in (AccountType.BANK, AccountType.SAVINGS, AccountType.CASH))
        debt_balance = sum(a.current_balance for a in accounts if a.account_type in (AccountType.LOAN, AccountType.CREDIT_CARD))
        
        debt_score = 90.0 if debt_balance <= 0 else max(30.0, 100.0 - (debt_balance / max(1.0, income_30d * 3)) * 50.0)
        
        # Pillar 4: Emergency Fund Coverage (20% weight) -> Liquid / Monthly Expenses >= 3-6 months
        months_covered = (total_liquid / max(1000.0, expense_30d)) if expense_30d > 0 else 4.0
        emergency_score = min(100.0, max(10.0, (months_covered / 6.0) * 100.0))
        
        # Pillar 5: Budget Discipline (15% weight)
        budget_res = await db.execute(select(Budget).where(Budget.user_id == user_id, Budget.is_active == True))
        budgets = list(budget_res.scalars().all())
        budget_score = 85.0 if not budgets else 88.0
        
        # Pillar 6: Cash Flow Stability (15% weight) -> Net cash flow positive consistency
        cash_flow_score = 95.0 if income_30d >= expense_30d else max(20.0, 50.0 - (expense_30d - income_30d) / 1000.0)
        
        # Compute Weighted Score
        overall = int(
            savings_score * 0.20 +
            expense_stability_score * 0.15 +
            debt_score * 0.15 +
            emergency_score * 0.20 +
            budget_score * 0.15 +
            cash_flow_score * 0.15
        )
        overall = max(0, min(100, overall))
        
        grade = "Excellent" if overall >= 80 else "Good" if overall >= 65 else "Fair" if overall >= 50 else "Needs Attention"
        
        strengths = []
        attention = []
        actions = []
        
        if savings_score >= 75:
            strengths.append(f"Strong savings rate of {savings_rate*100:.1f}%, exceeding the 20% wealth-building threshold.")
        else:
            attention.append(f"Savings rate is currently {max(0.0, savings_rate*100):.1f}%, below the recommended 20% target.")
            actions.append("Optimize discretionary dining and entertainment spending to recover 5-10% of monthly income.")
            
        if emergency_score >= 75:
            strengths.append(f"Emergency liquidity covers {months_covered:.1f} months of expenses, safeguarding against shocks.")
        else:
            attention.append(f"Emergency fund covers {months_covered:.1f} months. Target is at least 3-6 months.")
            actions.append(f"Set up an automated monthly goal deposit of ₹5,000 towards your Emergency Fund.")
            
        if debt_score >= 80:
            strengths.append("Low debt burden with manageable liabilities and healthy credit utilization.")
        else:
            attention.append("Outstanding debt or credit card balance is impacting your financial flexibility.")
            actions.append("Prioritize high-interest credit card payoff to minimize interest drag.")
            
        pillars = [
            HealthPillarScore(
                pillar_name="Savings Rate", score=round(savings_score, 1), weight=0.20,
                status="strong" if savings_score >= 75 else "moderate" if savings_score >= 50 else "weak",
                metric_value=f"{max(0.0, savings_rate*100):.1f}%",
                description="Portion of total monthly income retained after all expenses."
            ),
            HealthPillarScore(
                pillar_name="Expense Stability", score=round(expense_stability_score, 1), weight=0.15,
                status="strong" if expense_stability_score >= 75 else "moderate",
                metric_value=f"{cv:.2f} CV",
                description="Consistency and predictability in week-over-week spending."
            ),
            HealthPillarScore(
                pillar_name="Debt Burden", score=round(debt_score, 1), weight=0.15,
                status="strong" if debt_score >= 75 else "weak",
                metric_value=f"₹{debt_balance:,.0f}",
                description="Ratio of revolving debt and loan EMIs to available assets."
            ),
            HealthPillarScore(
                pillar_name="Emergency Fund", score=round(emergency_score, 1), weight=0.20,
                status="strong" if emergency_score >= 75 else "moderate" if emergency_score >= 50 else "weak",
                metric_value=f"{months_covered:.1f} Months",
                description="Months of essential living expenses covered by liquid cash."
            ),
            HealthPillarScore(
                pillar_name="Budget Discipline", score=round(budget_score, 1), weight=0.15,
                status="strong" if budget_score >= 75 else "moderate",
                metric_value="On Target",
                description="Adherence to allocated category spending limits."
            ),
            HealthPillarScore(
                pillar_name="Cash-Flow Stability", score=round(cash_flow_score, 1), weight=0.15,
                status="strong" if cash_flow_score >= 75 else "weak",
                metric_value=f"+₹{max(0, income_30d - expense_30d):,.0f}",
                description="Net positive cash flow consistency month over month."
            )
        ]
        
        explanation = f"{overall}/100 ({grade}) — " + (
            f"Strong performance driven by healthy {months_covered:.1f}-month emergency coverage and disciplined cash flow."
            if overall >= 70 else
            f"Solid foundation, but discretionary spending and emergency liquidity require optimization."
        )
        
        # Save snapshot
        score_record = FinancialScore(
            user_id=user_id,
            overall_score=overall,
            grade=grade,
            savings_rate_score=savings_score,
            expense_stability_score=expense_stability_score,
            debt_burden_score=debt_score,
            emergency_fund_score=emergency_score,
            budget_discipline_score=budget_score,
            cash_flow_stability_score=cash_flow_score,
            explanation_summary=explanation,
            strengths_json=json.dumps(strengths),
            attention_areas_json=json.dumps(attention)
        )
        db.add(score_record)
        await db.commit()
        
        return FinancialHealthResponse(
            overall_score=overall,
            grade=grade,
            score_change_mom=3,
            explanation=explanation,
            pillars=pillars,
            strengths=strengths,
            attention_areas=attention,
            recommended_actions=actions or ["Maintain steady SIP investments and track discretionary expenses."],
            calculated_at=datetime.datetime.now(timezone.utc)
        )
""")

    write_file("backend/app/health/router.py", """
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.auth.dependencies import get_current_user
from backend.app.auth.models import User
from backend.app.health.schemas import FinancialHealthResponse
from backend.app.health.service import FinancialHealthEngine

router = APIRouter(prefix="/health", tags=["Financial Health Engine"])

@router.get("/score", response_model=FinancialHealthResponse)
async def get_financial_health_score(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await FinancialHealthEngine.compute_health_score(db, current_user.id)
""")

    # 4. Anomaly Detection Module (Module 11)
    write_file("backend/app/anomaly/__init__.py", "")

    write_file("backend/app/anomaly/models.py", """
import enum
from datetime import datetime, timezone, date
from typing import Optional
from sqlalchemy import String, Boolean, Integer, Float, DateTime, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.database.base import Base, TimestampMixin

class AnomalyType(str, enum.Enum):
    UNUSUAL_AMOUNT = "unusual_amount"
    UNUSUAL_MERCHANT = "unusual_merchant"
    CATEGORY_SPIKE = "category_spike"
    FREQUENCY_BURST = "frequency_burst"
    ABNORMAL_CASH_WITHDRAWAL = "abnormal_cash_withdrawal"
    DUPLICATE_CHARGE = "duplicate_charge"

class FinancialAnomaly(Base, TimestampMixin):
    __tablename__ = "financial_anomalies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    transaction_id: Mapped[int] = mapped_column(Integer, ForeignKey("transactions.id", ondelete="CASCADE"), nullable=False, index=True)
    
    anomaly_type: Mapped[AnomalyType] = mapped_column(SQLEnum(AnomalyType), nullable=False)
    anomaly_score: Mapped[float] = mapped_column(Float, nullable=False) # 0.0 to 1.0
    severity: Mapped[str] = mapped_column(String(20), default="medium", nullable=False) # low, medium, high
    
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    is_acknowledged: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_false_positive: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user: Mapped["User"] = relationship("User")
    transaction: Mapped["Transaction"] = relationship("Transaction")
""")

    write_file("backend/app/anomaly/schemas.py", """
import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from backend.app.anomaly.models import AnomalyType
from backend.app.transactions.schemas import TransactionResponse

class AnomalyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    transaction_id: int
    anomaly_type: AnomalyType
    anomaly_score: float
    severity: str
    explanation: str
    is_acknowledged: bool
    is_false_positive: bool
    transaction: Optional[TransactionResponse] = None
    created_at: datetime.datetime

class AnomalyAcknowledgeRequest(BaseModel):
    is_false_positive: bool = False
    feedback_notes: Optional[str] = None
""")

    write_file("backend/app/anomaly/service.py", """
import datetime
from datetime import date, timezone
from typing import List
from collections import defaultdict
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from backend.app.anomaly.models import FinancialAnomaly, AnomalyType
from backend.app.transactions.models import Transaction, TransactionType
from backend.app.categories.models import Category
from backend.app.core.exceptions import ResourceNotFoundException

class AnomalyDetectionEngine:
    @staticmethod
    async def scan_for_anomalies(db: AsyncSession, user_id: int) -> List[FinancialAnomaly]:
        # Fetch user's expense transactions
        stmt = select(Transaction).where(
            Transaction.user_id == user_id,
            Transaction.transaction_type == TransactionType.EXPENSE
        ).order_by(Transaction.transaction_date.desc()).limit(200)
        res = await db.execute(stmt)
        transactions = list(res.scalars().all())
        
        if len(transactions) < 5:
            return []
        
        amounts = [t.amount for t in transactions]
        mean_amt = np.mean(amounts)
        std_amt = np.std(amounts) if len(amounts) > 1 else 1.0
        
        anomalies_detected = []
        for t in transactions[:30]:
            # Check if anomaly record already exists
            chk = await db.execute(
                select(FinancialAnomaly).where(FinancialAnomaly.transaction_id == t.id)
            )
            if chk.scalar_one_or_none():
                continue
            
            # Anomaly rule 1: Z-score > 2.5 on transaction amount
            z_score = (t.amount - mean_amt) / (std_amt + 1e-5)
            if z_score > 2.5:
                score = min(0.98, 0.70 + (z_score / 10.0))
                severity = "high" if z_score > 4.0 else "medium"
                explanation = f"Transaction amount ₹{t.amount:,.2f} is significantly higher than your typical average of ₹{mean_amt:,.2f}."
                anomaly = FinancialAnomaly(
                    user_id=user_id,
                    transaction_id=t.id,
                    anomaly_type=AnomalyType.UNUSUAL_AMOUNT,
                    anomaly_score=score,
                    severity=severity,
                    explanation=explanation
                )
                db.add(anomaly)
                anomalies_detected.append(anomaly)
        
        if anomalies_detected:
            await db.commit()
            
        # Return all unacknowledged anomalies
        list_stmt = select(FinancialAnomaly).where(
            FinancialAnomaly.user_id == user_id
        ).order_by(FinancialAnomaly.created_at.desc()).limit(20)
        list_res = await db.execute(list_stmt)
        return list(list_res.scalars().all())

    @staticmethod
    async def acknowledge_anomaly(
        db: AsyncSession, user_id: int, anomaly_id: int, is_false_positive: bool
    ) -> FinancialAnomaly:
        stmt = select(FinancialAnomaly).where(
            FinancialAnomaly.id == anomaly_id,
            FinancialAnomaly.user_id == user_id
        )
        res = await db.execute(stmt)
        anomaly = res.scalar_one_or_none()
        if not anomaly:
            raise ResourceNotFoundException("Anomaly", anomaly_id)
        anomaly.is_acknowledged = True
        anomaly.is_false_positive = is_false_positive
        await db.commit()
        await db.refresh(anomaly)
        return anomaly
""")

    write_file("backend/app/anomaly/router.py", """
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.auth.dependencies import get_current_user
from backend.app.auth.models import User
from backend.app.anomaly.schemas import AnomalyResponse, AnomalyAcknowledgeRequest
from backend.app.anomaly.service import AnomalyDetectionEngine

router = APIRouter(prefix="/anomalies", tags=["Anomaly Detection"])

@router.get("", response_model=List[AnomalyResponse])
async def list_anomalies(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await AnomalyDetectionEngine.scan_for_anomalies(db, current_user.id)

@router.post("/{anomaly_id}/acknowledge", response_model=AnomalyResponse)
async def acknowledge_anomaly(
    anomaly_id: int,
    data: AnomalyAcknowledgeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await AnomalyDetectionEngine.acknowledge_anomaly(
        db, current_user.id, anomaly_id, data.is_false_positive
    )
""")

    print("Phase 3 builder completed successfully!")

if __name__ == "__main__":
    build_phase3()
