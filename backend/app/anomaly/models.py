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

    user: Mapped["User"] = relationship("User", lazy="selectin")
    transaction: Mapped["Transaction"] = relationship("Transaction", lazy="selectin")
