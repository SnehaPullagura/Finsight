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
