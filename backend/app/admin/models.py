import datetime
from datetime import timezone
from typing import Optional
from sqlalchemy import String, Boolean, Integer, Float, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.database.base import Base, TimestampMixin

class MLModelRegistry(Base, TimestampMixin):
    __tablename__ = "ml_model_registry"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    model_name: Mapped[str] = mapped_column(String(64), index=True, nullable=False) # categorizer, forecaster, anomaly_detector
    version: Mapped[str] = mapped_column(String(32), nullable=False)
    algorithm: Mapped[str] = mapped_column(String(64), nullable=False)
    accuracy_or_metric: Mapped[float] = mapped_column(Float, nullable=False)
    training_sample_count: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    artifact_path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    metadata_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
