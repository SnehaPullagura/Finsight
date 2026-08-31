import enum
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Boolean, Integer, Float, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.database.base import Base, TimestampMixin

class AccountType(str, enum.Enum):
    BANK = "bank"
    SAVINGS = "savings"
    CREDIT_CARD = "credit_card"
    CASH = "cash"
    LOAN = "loan"
    INVESTMENT = "investment"

class AccountStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"

class FinancialAccount(Base, TimestampMixin):
    __tablename__ = "financial_accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    account_type: Mapped[AccountType] = mapped_column(SQLEnum(AccountType), nullable=False)
    account_number_masked: Mapped[str] = mapped_column(String(64), default="XXXX", nullable=False)
    institution_name: Mapped[str] = mapped_column(String(128), default="Self/Manual", nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="INR", nullable=False)
    
    current_balance: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    available_balance: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    credit_limit: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    interest_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    status: Mapped[AccountStatus] = mapped_column(SQLEnum(AccountStatus), default=AccountStatus.ACTIVE, nullable=False)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    last_reconciled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    user: Mapped["User"] = relationship("User", back_populates="accounts")
    transactions: Mapped[List["Transaction"]] = relationship(
        "Transaction",
        primaryjoin="FinancialAccount.id == Transaction.account_id",
        back_populates="account",
        cascade="all, delete-orphan"
    )
    balance_history: Mapped[List["AccountBalanceHistory"]] = relationship("AccountBalanceHistory", back_populates="account", cascade="all, delete-orphan")

class AccountBalanceHistory(Base, TimestampMixin):
    __tablename__ = "account_balance_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("financial_accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    balance: Mapped[float] = mapped_column(Float, nullable=False)
    snapshot_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    change_reason: Mapped[str] = mapped_column(String(128), default="transaction_sync")

    account: Mapped["FinancialAccount"] = relationship("FinancialAccount", back_populates="balance_history")
