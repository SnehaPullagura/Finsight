import datetime
from datetime import timezone
from typing import Optional, List
from sqlalchemy import String, Boolean, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.database.base import Base, TimestampMixin

class Scenario(Base, TimestampMixin):
    __tablename__ = "scenarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    name: Mapped[str] = mapped_column(String(128), nullable=False) # e.g. "Take Home Loan + ₹15K Promotion"
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Variable Adjustments
    monthly_income_delta: Mapped[float] = mapped_column(Float, default=0.0, nullable=False) # e.g. +10000
    monthly_expense_delta: Mapped[float] = mapped_column(Float, default=0.0, nullable=False) # e.g. +5000 rent
    one_time_lump_sum: Mapped[float] = mapped_column(Float, default=0.0, nullable=False) # e.g. -300000 down payment
    loan_amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False) # e.g. 500000
    loan_tenure_months: Mapped[int] = mapped_column(Integer, default=0, nullable=False) # 36
    loan_interest_rate: Mapped[float] = mapped_column(Float, default=10.5, nullable=False)
    
    # Computed Impact
    calculated_monthly_emi: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    projected_6m_balance: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    projected_12m_balance: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    health_score_delta: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_feasible: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    feasibility_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="scenarios")
