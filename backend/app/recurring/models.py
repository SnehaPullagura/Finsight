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

    user: Mapped["User"] = relationship("User", back_populates="recurring_payments", lazy="selectin")
    category: Mapped[Optional["Category"]] = relationship("Category", lazy="selectin")
    account: Mapped["FinancialAccount"] = relationship("FinancialAccount", lazy="selectin")
