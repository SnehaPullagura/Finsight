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
    tags: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Transfer tracking
    transfer_account_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("financial_accounts.id", ondelete="SET NULL"), nullable=True)
    
    # Relationships with selectin lazy loading for async safety
    account: Mapped["FinancialAccount"] = relationship(
        "FinancialAccount", foreign_keys=[account_id], back_populates="transactions", lazy="selectin"
    )
    category: Mapped[Optional["Category"]] = relationship(
        "Category", back_populates="transactions", lazy="selectin"
    )
    splits: Mapped[List["TransactionSplit"]] = relationship(
        "TransactionSplit", back_populates="transaction", cascade="all, delete-orphan", lazy="selectin"
    )

class TransactionSplit(Base, TimestampMixin):
    __tablename__ = "transaction_splits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    transaction_id: Mapped[int] = mapped_column(Integer, ForeignKey("transactions.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    transaction: Mapped["Transaction"] = relationship("Transaction", back_populates="splits", lazy="selectin")
    category: Mapped["Category"] = relationship("Category", lazy="selectin")
