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

    user: Mapped["User"] = relationship("User", back_populates="budgets", lazy="selectin")
    category: Mapped[Optional["Category"]] = relationship("Category", back_populates="budgets", lazy="selectin")
