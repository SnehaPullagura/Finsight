import datetime
from datetime import timezone, date
from typing import Optional
from sqlalchemy import String, Integer, Float, DateTime, Date, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.database.base import Base, TimestampMixin

class ForecastRecord(Base, TimestampMixin):
    __tablename__ = "forecast_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    horizon_days: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    predicted_expenses: Mapped[float] = mapped_column(Float, nullable=False)
    predicted_income: Mapped[float] = mapped_column(Float, nullable=False)
    predicted_ending_balance: Mapped[float] = mapped_column(Float, nullable=False)
    
    shortage_risk_percent: Mapped[float] = mapped_column(Float, default=0.0, nullable=False) # 0 to 100%
    confidence_interval_low: Mapped[float] = mapped_column(Float, nullable=False)
    confidence_interval_high: Mapped[float] = mapped_column(Float, nullable=False)
    
    breakdown_json: Mapped[str] = mapped_column(Text, nullable=False) # category-level predictions

    user: Mapped["User"] = relationship("User")
