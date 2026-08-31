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

    user: Mapped["User"] = relationship("User", back_populates="goals", lazy="selectin")
    contributions: Mapped[List["GoalContribution"]] = relationship("GoalContribution", back_populates="goal", cascade="all, delete-orphan", lazy="selectin")

class GoalContribution(Base, TimestampMixin):
    __tablename__ = "goal_contributions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    goal_id: Mapped[int] = mapped_column(Integer, ForeignKey("financial_goals.id", ondelete="CASCADE"), nullable=False, index=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    contribution_date: Mapped[date] = mapped_column(Date, default=lambda: date.today(), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    goal: Mapped["FinancialGoal"] = relationship("FinancialGoal", back_populates="contributions")
