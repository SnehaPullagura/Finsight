import os
import sys
from scripts.common import write_file

def build_phase2():
    print("Building Phase 2: Financial Core (Transactions, Budgets, Goals, Recurring Payments)...")

    # 1. Transactions Module (Module 03)
    write_file("backend/app/transactions/__init__.py", "")

    write_file("backend/app/transactions/models.py", """
import enum
from datetime import datetime, timezone, date
from typing import Optional, List
from sqlalchemy import String, Boolean, Integer, Float, DateTime, Date, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.database.base import Base, TimestampMixin

class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"
    REFUND = "refund"
    FEE = "fee"
    INTEREST = "interest"

class TransactionStatus(str, enum.Enum):
    CLEARED = "cleared"
    PENDING = "pending"
    RECONCILED = "reconciled"

class Transaction(Base, TimestampMixin):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("financial_accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True)
    
    amount: Mapped[float] = mapped_column(Float, nullable=False, index=True)
    transaction_type: Mapped[TransactionType] = mapped_column(SQLEnum(TransactionType), nullable=False, index=True)
    transaction_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    raw_description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    merchant_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True, index=True)
    
    status: Mapped[TransactionStatus] = mapped_column(SQLEnum(TransactionStatus), default=TransactionStatus.CLEARED, nullable=False)
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_discretionary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Intelligence attributes
    confidence_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    is_user_confirmed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    tags: Mapped[Optional[str]] = mapped_column(String(255), nullable=True) # comma-separated tags
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Transfer tracking
    transfer_account_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("financial_accounts.id", ondelete="SET NULL"), nullable=True)
    
    # Relationships
    account: Mapped["FinancialAccount"] = relationship("FinancialAccount", foreign_keys=[account_id], back_populates="transactions")
    category: Mapped[Optional["Category"]] = relationship("Category", back_populates="transactions")
    splits: Mapped[List["TransactionSplit"]] = relationship("TransactionSplit", back_populates="transaction", cascade="all, delete-orphan")

class TransactionSplit(Base, TimestampMixin):
    __tablename__ = "transaction_splits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    transaction_id: Mapped[int] = mapped_column(Integer, ForeignKey("transactions.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    transaction: Mapped["Transaction"] = relationship("Transaction", back_populates="splits")
    category: Mapped["Category"] = relationship("Category")
""")

    write_file("backend/app/transactions/schemas.py", """
import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from backend.app.transactions.models import TransactionType, TransactionStatus
from backend.app.categories.schemas import CategoryResponse

class TransactionSplitCreate(BaseModel):
    category_id: int
    amount: float
    notes: Optional[str] = None

class TransactionSplitResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    category_id: int
    amount: float
    notes: Optional[str] = None

class TransactionCreate(BaseModel):
    account_id: int
    category_id: Optional[int] = None
    amount: float = Field(..., gt=0)
    transaction_type: TransactionType
    transaction_date: datetime.date
    description: str = Field(..., min_length=1, max_length=255)
    raw_description: Optional[str] = None
    merchant_name: Optional[str] = None
    status: TransactionStatus = TransactionStatus.CLEARED
    is_recurring: bool = False
    is_discretionary: bool = False
    tags: Optional[str] = None
    notes: Optional[str] = None
    transfer_account_id: Optional[int] = None
    splits: Optional[List[TransactionSplitCreate]] = None

class TransactionUpdate(BaseModel):
    account_id: Optional[int] = None
    category_id: Optional[int] = None
    amount: Optional[float] = Field(default=None, gt=0)
    transaction_type: Optional[TransactionType] = None
    transaction_date: Optional[datetime.date] = None
    description: Optional[str] = None
    merchant_name: Optional[str] = None
    status: Optional[TransactionStatus] = None
    is_recurring: Optional[bool] = None
    is_discretionary: Optional[bool] = None
    tags: Optional[str] = None
    notes: Optional[str] = None

class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    account_id: int
    category_id: Optional[int] = None
    amount: float
    transaction_type: TransactionType
    transaction_date: datetime.date
    description: str
    raw_description: Optional[str] = None
    merchant_name: Optional[str] = None
    status: TransactionStatus
    is_recurring: bool
    is_discretionary: bool
    confidence_score: float
    is_user_confirmed: bool
    tags: Optional[str] = None
    notes: Optional[str] = None
    transfer_account_id: Optional[int] = None
    category: Optional[CategoryResponse] = None
    splits: Optional[List[TransactionSplitResponse]] = None
    created_at: datetime.datetime

class TransactionSearchFilter(BaseModel):
    account_id: Optional[int] = None
    category_id: Optional[int] = None
    transaction_type: Optional[TransactionType] = None
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None
    search: Optional[str] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    is_recurring: Optional[bool] = None
    limit: int = 50
    offset: int = 0
""")

    write_file("backend/app/transactions/service.py", """
import datetime
from datetime import timezone, date
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, or_, func
from backend.app.transactions.models import Transaction, TransactionSplit, TransactionType, TransactionStatus
from backend.app.transactions.schemas import TransactionCreate, TransactionUpdate, TransactionSearchFilter
from backend.app.accounts.models import FinancialAccount, AccountBalanceHistory
from backend.app.accounts.service import AccountService
from backend.app.core.exceptions import ResourceNotFoundException, FinSightException

class TransactionService:
    @staticmethod
    async def create_transaction(db: AsyncSession, user_id: int, data: TransactionCreate) -> Transaction:
        # Validate account ownership
        account = await AccountService.get_account(db, user_id, data.account_id)
        
        # Calculate impact on account balance
        balance_delta = 0.0
        if data.transaction_type in (TransactionType.INCOME, TransactionType.REFUND, TransactionType.INTEREST):
            balance_delta = data.amount
        elif data.transaction_type in (TransactionType.EXPENSE, TransactionType.FEE):
            balance_delta = -data.amount
        elif data.transaction_type == TransactionType.TRANSFER:
            balance_delta = -data.amount
        
        account.current_balance += balance_delta
        account.available_balance += balance_delta
        
        tx = Transaction(
            user_id=user_id,
            account_id=data.account_id,
            category_id=data.category_id,
            amount=data.amount,
            transaction_type=data.transaction_type,
            transaction_date=data.transaction_date,
            description=data.description,
            raw_description=data.raw_description or data.description,
            merchant_name=data.merchant_name or data.description.split()[0] if data.description else "Unknown",
            status=data.status,
            is_recurring=data.is_recurring,
            is_discretionary=data.is_discretionary,
            confidence_score=1.0,
            is_user_confirmed=True,
            tags=data.tags,
            notes=data.notes,
            transfer_account_id=data.transfer_account_id
        )
        db.add(tx)
        await db.flush()
        
        # Handle splits if provided
        if data.splits:
            split_total = sum(s.amount for s in data.splits)
            if abs(split_total - data.amount) > 0.01:
                raise FinSightException(detail="Sum of transaction splits must equal total transaction amount.")
            for s in data.splits:
                split = TransactionSplit(
                    transaction_id=tx.id,
                    category_id=s.category_id,
                    amount=s.amount,
                    notes=s.notes
                )
                db.add(split)
        
        # Record balance history
        history = AccountBalanceHistory(
            account_id=account.id,
            balance=account.current_balance,
            snapshot_date=datetime.datetime.now(timezone.utc),
            change_reason=f"tx_{tx.id}_{data.transaction_type.value}"
        )
        db.add(history)
        
        # Handle transfer counterpart
        if data.transaction_type == TransactionType.TRANSFER and data.transfer_account_id:
            transfer_acc = await AccountService.get_account(db, user_id, data.transfer_account_id)
            transfer_acc.current_balance += data.amount
            transfer_acc.available_balance += data.amount
            
            counter_history = AccountBalanceHistory(
                account_id=transfer_acc.id,
                balance=transfer_acc.current_balance,
                snapshot_date=datetime.datetime.now(timezone.utc),
                change_reason=f"transfer_in_from_tx_{tx.id}"
            )
            db.add(counter_history)
        
        await db.commit()
        await db.refresh(tx)
        return tx

    @staticmethod
    async def list_transactions(
        db: AsyncSession, user_id: int, filters: TransactionSearchFilter
    ) -> Tuple[List[Transaction], int]:
        query = select(Transaction).where(Transaction.user_id == user_id)
        
        if filters.account_id:
            query = query.where(Transaction.account_id == filters.account_id)
        if filters.category_id:
            query = query.where(Transaction.category_id == filters.category_id)
        if filters.transaction_type:
            query = query.where(Transaction.transaction_type == filters.transaction_type)
        if filters.start_date:
            query = query.where(Transaction.transaction_date >= filters.start_date)
        if filters.end_date:
            query = query.where(Transaction.transaction_date <= filters.end_date)
        if filters.min_amount is not None:
            query = query.where(Transaction.amount >= filters.min_amount)
        if filters.max_amount is not None:
            query = query.where(Transaction.amount <= filters.max_amount)
        if filters.is_recurring is not None:
            query = query.where(Transaction.is_recurring == filters.is_recurring)
        if filters.search:
            s = f"%{filters.search.lower()}%"
            query = query.where(
                or_(
                    func.lower(Transaction.description).like(s),
                    func.lower(Transaction.merchant_name).like(s),
                    func.lower(Transaction.tags).like(s)
                )
            )
        
        count_stmt = select(func.count()).select_from(query.subquery())
        total_count = (await db.execute(count_stmt)).scalar() or 0
        
        query = query.order_by(Transaction.transaction_date.desc(), Transaction.id.desc())
        query = query.offset(filters.offset).limit(filters.limit)
        
        result = await db.execute(query)
        return list(result.scalars().all()), total_count

    @staticmethod
    async def get_transaction(db: AsyncSession, user_id: int, tx_id: int) -> Transaction:
        stmt = select(Transaction).where(
            Transaction.id == tx_id,
            Transaction.user_id == user_id
        )
        result = await db.execute(stmt)
        tx = result.scalar_one_or_none()
        if not tx:
            raise ResourceNotFoundException("Transaction", tx_id)
        return tx

    @staticmethod
    async def update_transaction(
        db: AsyncSession, user_id: int, tx_id: int, data: TransactionUpdate
    ) -> Transaction:
        tx = await TransactionService.get_transaction(db, user_id, tx_id)
        update_data = data.model_dump(exclude_unset=True)
        for k, v in update_data.items():
            setattr(tx, k, v)
        tx.is_user_confirmed = True
        await db.commit()
        await db.refresh(tx)
        return tx

    @staticmethod
    async def delete_transaction(db: AsyncSession, user_id: int, tx_id: int) -> bool:
        tx = await TransactionService.get_transaction(db, user_id, tx_id)
        # Reverse balance impact
        account = await AccountService.get_account(db, user_id, tx.account_id)
        if tx.transaction_type in (TransactionType.INCOME, TransactionType.REFUND, TransactionType.INTEREST):
            account.current_balance -= tx.amount
        elif tx.transaction_type in (TransactionType.EXPENSE, TransactionType.FEE, TransactionType.TRANSFER):
            account.current_balance += tx.amount
        
        await db.delete(tx)
        await db.commit()
        return True
""")

    write_file("backend/app/transactions/router.py", """
from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.auth.dependencies import get_current_user
from backend.app.auth.models import User
from backend.app.transactions.schemas import (
    TransactionCreate, TransactionUpdate, TransactionResponse, TransactionSearchFilter
)
from backend.app.transactions.service import TransactionService
from backend.app.transactions.models import TransactionType

router = APIRouter(prefix="/transactions", tags=["Transaction Management"])

@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    data: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await TransactionService.create_transaction(db, current_user.id, data)

@router.get("", response_model=List[TransactionResponse])
async def list_transactions(
    account_id: Optional[int] = None,
    category_id: Optional[int] = None,
    transaction_type: Optional[TransactionType] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    search: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    is_recurring: Optional[bool] = None,
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    filters = TransactionSearchFilter(
        account_id=account_id,
        category_id=category_id,
        transaction_type=transaction_type,
        start_date=start_date,
        end_date=end_date,
        search=search,
        min_amount=min_amount,
        max_amount=max_amount,
        is_recurring=is_recurring,
        limit=limit,
        offset=offset
    )
    items, total = await TransactionService.list_transactions(db, current_user.id, filters)
    return items

@router.get("/{tx_id}", response_model=TransactionResponse)
async def get_transaction(
    tx_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await TransactionService.get_transaction(db, current_user.id, tx_id)

@router.put("/{tx_id}", response_model=TransactionResponse)
async def update_transaction(
    tx_id: int,
    data: TransactionUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await TransactionService.update_transaction(db, current_user.id, tx_id, data)

@router.delete("/{tx_id}")
async def delete_transaction(
    tx_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await TransactionService.delete_transaction(db, current_user.id, tx_id)
    return {"message": "Transaction deleted successfully"}
""")

    # 2. Budget Management Module (Module 05)
    write_file("backend/app/budgets/__init__.py", "")

    write_file("backend/app/budgets/models.py", """
import enum
from datetime import datetime, timezone, date
from typing import Optional, List
from sqlalchemy import String, Boolean, Integer, Float, DateTime, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.database.base import Base, TimestampMixin

class BudgetPeriod(str, enum.Enum):
    MONTHLY = "monthly"
    WEEKLY = "weekly"
    CUSTOM = "custom"

class Budget(Base, TimestampMixin):
    __tablename__ = "budgets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=True, index=True)
    
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    allocated_amount: Mapped[float] = mapped_column(Float, nullable=False)
    period: Mapped[BudgetPeriod] = mapped_column(SQLEnum(BudgetPeriod), default=BudgetPeriod.MONTHLY, nullable=False)
    
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    notify_threshold_percent: Mapped[float] = mapped_column(Float, default=80.0, nullable=False) # 80% warning
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="budgets")
    category: Mapped[Optional["Category"]] = relationship("Category", back_populates="budgets")
""")

    write_file("backend/app/budgets/schemas.py", """
import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from backend.app.budgets.models import BudgetPeriod
from backend.app.categories.schemas import CategoryResponse

class BudgetCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=128)
    category_id: Optional[int] = None
    allocated_amount: float = Field(..., gt=0)
    period: BudgetPeriod = BudgetPeriod.MONTHLY
    start_date: datetime.date
    end_date: Optional[datetime.date] = None
    notify_threshold_percent: float = Field(default=80.0, ge=1.0, le=100.0)

class BudgetUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    allocated_amount: Optional[float] = Field(default=None, gt=0)
    period: Optional[BudgetPeriod] = None
    notify_threshold_percent: Optional[float] = None
    is_active: Optional[bool] = None

class BudgetProgressResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    category_id: Optional[int] = None
    name: str
    allocated_amount: float
    spent_amount: float
    remaining_amount: float
    percentage_used: float
    is_overbudget: bool
    status: str # "good", "warning", "exceeded"
    category: Optional[CategoryResponse] = None
""")

    write_file("backend/app/budgets/service.py", """
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
""")

    write_file("backend/app/budgets/router.py", """
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
""")

    # 3. Financial Goals Module (Module 06)
    write_file("backend/app/goals/__init__.py", "")

    write_file("backend/app/goals/models.py", """
import enum
from datetime import datetime, timezone, date
from typing import Optional, List
from sqlalchemy import String, Boolean, Integer, Float, DateTime, Date, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.database.base import Base, TimestampMixin

class GoalType(str, enum.Enum):
    EMERGENCY_FUND = "emergency_fund"
    HOUSE = "house"
    EDUCATION = "education"
    VEHICLE = "vehicle"
    TRAVEL = "travel"
    CUSTOM = "custom"

class GoalStatus(str, enum.Enum):
    IN_PROGRESS = "in_progress"
    ACHIEVED = "achieved"
    PAUSED = "paused"
    ABANDONED = "abandoned"

class FinancialGoal(Base, TimestampMixin):
    __tablename__ = "financial_goals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    account_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("financial_accounts.id", ondelete="SET NULL"), nullable=True)
    
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    goal_type: Mapped[GoalType] = mapped_column(SQLEnum(GoalType), default=GoalType.CUSTOM, nullable=False)
    target_amount: Mapped[float] = mapped_column(Float, nullable=False)
    current_amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    target_date: Mapped[date] = mapped_column(Date, nullable=False)
    monthly_contribution: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    
    status: Mapped[GoalStatus] = mapped_column(SQLEnum(GoalStatus), default=GoalStatus.IN_PROGRESS, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="goals")
    contributions: Mapped[List["GoalContribution"]] = relationship("GoalContribution", back_populates="goal", cascade="all, delete-orphan")

class GoalContribution(Base, TimestampMixin):
    __tablename__ = "goal_contributions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    goal_id: Mapped[int] = mapped_column(Integer, ForeignKey("financial_goals.id", ondelete="CASCADE"), nullable=False, index=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    contribution_date: Mapped[date] = mapped_column(Date, default=lambda: date.today(), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    goal: Mapped["FinancialGoal"] = relationship("FinancialGoal", back_populates="contributions")
""")

    write_file("backend/app/goals/schemas.py", """
import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from backend.app.goals.models import GoalType, GoalStatus

class GoalCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=128)
    goal_type: GoalType = GoalType.CUSTOM
    target_amount: float = Field(..., gt=0)
    current_amount: float = Field(default=0.0, ge=0)
    target_date: datetime.date
    monthly_contribution: float = Field(default=0.0, ge=0)
    account_id: Optional[int] = None
    notes: Optional[str] = None

class GoalUpdate(BaseModel):
    name: Optional[str] = None
    target_amount: Optional[float] = None
    current_amount: Optional[float] = None
    target_date: Optional[datetime.date] = None
    monthly_contribution: Optional[float] = None
    status: Optional[GoalStatus] = None
    notes: Optional[str] = None

class GoalContributionCreate(BaseModel):
    amount: float = Field(..., gt=0)
    contribution_date: Optional[datetime.date] = None
    notes: Optional[str] = None

class GoalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    name: str
    goal_type: GoalType
    target_amount: float
    current_amount: float
    target_date: datetime.date
    monthly_contribution: float
    status: GoalStatus
    percentage_completed: float
    projected_completion_date: Optional[datetime.date] = None
    sufficiency_status: str # "on_track", "behind", "ahead"
    notes: Optional[str] = None
    created_at: datetime.datetime
""")

    write_file("backend/app/goals/service.py", """
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
""")

    write_file("backend/app/goals/router.py", """
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
""")

    # 4. Recurring Payments Module (Module 07)
    write_file("backend/app/recurring/__init__.py", "")

    write_file("backend/app/recurring/models.py", """
import enum
from datetime import datetime, timezone, date
from typing import Optional, List
from sqlalchemy import String, Boolean, Integer, Float, DateTime, Date, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.database.base import Base, TimestampMixin

class RecurringCadence(str, enum.Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"

class RecurringPayment(Base, TimestampMixin):
    __tablename__ = "recurring_payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("financial_accounts.id", ondelete="CASCADE"), nullable=False)
    category_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    
    merchant_name: Mapped[str] = mapped_column(String(128), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    cadence: Mapped[RecurringCadence] = mapped_column(SQLEnum(RecurringCadence), default=RecurringCadence.MONTHLY, nullable=False)
    
    next_expected_date: Mapped[date] = mapped_column(Date, nullable=False)
    last_payment_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_auto_detected: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="recurring_payments")
    category: Mapped[Optional["Category"]] = relationship("Category")
    account: Mapped["FinancialAccount"] = relationship("FinancialAccount")
""")

    write_file("backend/app/recurring/schemas.py", """
import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from backend.app.recurring.models import RecurringCadence
from backend.app.categories.schemas import CategoryResponse

class RecurringPaymentCreate(BaseModel):
    account_id: int
    category_id: Optional[int] = None
    merchant_name: str = Field(..., min_length=2, max_length=128)
    amount: float = Field(..., gt=0)
    cadence: RecurringCadence = RecurringCadence.MONTHLY
    next_expected_date: datetime.date
    last_payment_date: Optional[datetime.date] = None

class RecurringPaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    account_id: int
    category_id: Optional[int] = None
    merchant_name: str
    amount: float
    cadence: RecurringCadence
    next_expected_date: datetime.date
    last_payment_date: Optional[datetime.date] = None
    is_active: bool
    is_auto_detected: bool
    category: Optional[CategoryResponse] = None

class RecurringCalendarEvent(BaseModel):
    merchant_name: str
    amount: float
    expected_date: datetime.date
    cadence: str
    category_name: str
""")

    write_file("backend/app/recurring/service.py", """
import datetime
from datetime import date, timezone
from typing import List
from collections import defaultdict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.app.recurring.models import RecurringPayment, RecurringCadence
from backend.app.recurring.schemas import RecurringPaymentCreate, RecurringCalendarEvent
from backend.app.transactions.models import Transaction, TransactionType
from backend.app.categories.models import Category

class RecurringService:
    @staticmethod
    async def create_recurring(db: AsyncSession, user_id: int, data: RecurringPaymentCreate) -> RecurringPayment:
        rec = RecurringPayment(
            user_id=user_id,
            account_id=data.account_id,
            category_id=data.category_id,
            merchant_name=data.merchant_name,
            amount=data.amount,
            cadence=data.cadence,
            next_expected_date=data.next_expected_date,
            last_payment_date=data.last_payment_date,
            is_active=True,
            is_auto_detected=False
        )
        db.add(rec)
        await db.commit()
        await db.refresh(rec)
        return rec

    @staticmethod
    async def list_recurring(db: AsyncSession, user_id: int) -> List[RecurringPayment]:
        stmt = select(RecurringPayment).where(
            RecurringPayment.user_id == user_id,
            RecurringPayment.is_active == True
        ).order_by(RecurringPayment.next_expected_date.asc())
        res = await db.execute(stmt)
        return list(res.scalars().all())

    @staticmethod
    async def detect_recurring(db: AsyncSession, user_id: int) -> List[RecurringPayment]:
        # Group expense transactions by merchant and similar amounts
        stmt = select(Transaction).where(
            Transaction.user_id == user_id,
            Transaction.transaction_type == TransactionType.EXPENSE
        ).order_by(Transaction.transaction_date.desc()).limit(300)
        res = await db.execute(stmt)
        txs = list(res.scalars().all())
        
        merchant_groups = defaultdict(list)
        for t in txs:
            if t.merchant_name:
                merchant_groups[t.merchant_name.lower()].append(t)
        
        detected = []
        for m_name, group in merchant_groups.items():
            if len(group) >= 2:
                # Check intervals
                dates = sorted([t.transaction_date for t in group])
                diffs = [(dates[i] - dates[i-1]).days for i in range(1, len(dates))]
                avg_diff = sum(diffs) / len(diffs) if diffs else 0
                
                # Check monthly pattern (25 - 35 days)
                if 25 <= avg_diff <= 35:
                    latest = dates[-1]
                    next_date = latest + datetime.timedelta(days=30)
                    # Check if already saved
                    chk = await db.execute(
                        select(RecurringPayment).where(
                            RecurringPayment.user_id == user_id,
                            RecurringPayment.merchant_name == group[0].merchant_name
                        )
                    )
                    existing = chk.scalar_one_or_none()
                    if not existing:
                        rec = RecurringPayment(
                            user_id=user_id,
                            account_id=group[0].account_id,
                            category_id=group[0].category_id,
                            merchant_name=group[0].merchant_name,
                            amount=group[0].amount,
                            cadence=RecurringCadence.MONTHLY,
                            next_expected_date=next_date,
                            last_payment_date=latest,
                            is_active=True,
                            is_auto_detected=True
                        )
                        db.add(rec)
                        detected.append(rec)
        if detected:
            await db.commit()
        return await RecurringService.list_recurring(db, user_id)

    @staticmethod
    async def get_payment_calendar(db: AsyncSession, user_id: int, days_ahead: int = 60) -> List[RecurringCalendarEvent]:
        recurring = await RecurringService.list_recurring(db, user_id)
        events = []
        today = date.today()
        horizon = today + datetime.timedelta(days=days_ahead)
        
        for r in recurring:
            cat_name = "Subscription / Bill"
            if r.category_id:
                c_res = await db.execute(select(Category).where(Category.id == r.category_id))
                c = c_res.scalar_one_or_none()
                if c:
                    cat_name = c.name
            
            curr_date = r.next_expected_date
            while curr_date <= horizon:
                events.append(RecurringCalendarEvent(
                    merchant_name=r.merchant_name,
                    amount=r.amount,
                    expected_date=curr_date,
                    cadence=r.cadence.value,
                    category_name=cat_name
                ))
                if r.cadence == RecurringCadence.MONTHLY:
                    curr_date = curr_date + datetime.timedelta(days=30)
                elif r.cadence == RecurringCadence.WEEKLY:
                    curr_date = curr_date + datetime.timedelta(days=7)
                elif r.cadence == RecurringCadence.YEARLY:
                    curr_date = curr_date + datetime.timedelta(days=365)
                else:
                    break
        return sorted(events, key=lambda x: x.expected_date)
""")

    write_file("backend/app/recurring/router.py", """
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.auth.dependencies import get_current_user
from backend.app.auth.models import User
from backend.app.recurring.schemas import (
    RecurringPaymentCreate, RecurringPaymentResponse, RecurringCalendarEvent
)
from backend.app.recurring.service import RecurringService

router = APIRouter(prefix="/recurring", tags=["Recurring Payments"])

@router.post("", response_model=RecurringPaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_recurring(
    data: RecurringPaymentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await RecurringService.create_recurring(db, current_user.id, data)

@router.get("", response_model=List[RecurringPaymentResponse])
async def list_recurring(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await RecurringService.list_recurring(db, current_user.id)

@router.post("/detect", response_model=List[RecurringPaymentResponse])
async def detect_recurring_payments(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await RecurringService.detect_recurring(db, current_user.id)

@router.get("/calendar", response_model=List[RecurringCalendarEvent])
async def get_recurring_calendar(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await RecurringService.get_payment_calendar(db, current_user.id)
""")

    print("Phase 2 builder completed successfully!")

if __name__ == "__main__":
    build_phase2()
