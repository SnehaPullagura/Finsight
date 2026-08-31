import uuid
from typing import List, Optional
from sqlalchemy import Boolean, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class Pipeline(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "pipelines"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    stages: Mapped[List["PipelineStage"]] = relationship("PipelineStage", back_populates="pipeline", cascade="all, delete-orphan", order_by="PipelineStage.stage_order")
    deals: Mapped[List["backend.app.models.deal.Deal"]] = relationship("backend.app.models.deal.Deal", back_populates="pipeline")

class PipelineStage(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "pipeline_stages"

    pipeline_id: Mapped[str] = mapped_column(String(36), ForeignKey("pipelines.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    stage_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    probability: Mapped[int] = mapped_column(Integer, default=50, nullable=False) # 0 to 100
    stage_type: Mapped[str] = mapped_column(String(20), default="open", nullable=False) # open, won, lost
    sla_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    required_fields: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    pipeline: Mapped["Pipeline"] = relationship("Pipeline", back_populates="stages")
    deals: Mapped[List["backend.app.models.deal.Deal"]] = relationship("backend.app.models.deal.Deal", back_populates="stage")
