import uuid
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class Deal(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "deals"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    value: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False, index=True)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    probability: Mapped[int] = mapped_column(Integer, default=50, nullable=False) # 0-100
    
    expected_close_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, index=True)
    actual_close_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    pipeline_id: Mapped[str] = mapped_column(String(36), ForeignKey("pipelines.id", ondelete="RESTRICT"), nullable=False, index=True)
    stage_id: Mapped[str] = mapped_column(String(36), ForeignKey("pipeline_stages.id", ondelete="RESTRICT"), nullable=False, index=True)
    
    company_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True, index=True)
    contact_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("contacts.id", ondelete="SET NULL"), nullable=True, index=True)
    owner_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    status: Mapped[str] = mapped_column(String(20), default="open", nullable=False, index=True) # open, won, lost
    loss_reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    custom_fields: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    # Relationships
    pipeline: Mapped["backend.app.models.pipeline.Pipeline"] = relationship("backend.app.models.pipeline.Pipeline", back_populates="deals")
    stage: Mapped["backend.app.models.pipeline.PipelineStage"] = relationship("backend.app.models.pipeline.PipelineStage", back_populates="deals")
    company: Mapped[Optional["backend.app.models.company.Company"]] = relationship("backend.app.models.company.Company")
    contact: Mapped[Optional["backend.app.models.contact.Contact"]] = relationship("backend.app.models.contact.Contact")
    owner: Mapped[Optional["backend.app.models.auth.User"]] = relationship("backend.app.models.auth.User")
    stage_history: Mapped[List["DealStageHistory"]] = relationship("DealStageHistory", back_populates="deal", cascade="all, delete-orphan", order_by="DealStageHistory.created_at.desc()")
    products: Mapped[List["DealProduct"]] = relationship("DealProduct", back_populates="deal", cascade="all, delete-orphan")

class DealStageHistory(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "deal_stage_histories"

    deal_id: Mapped[str] = mapped_column(String(36), ForeignKey("deals.id", ondelete="CASCADE"), nullable=False, index=True)
    from_stage_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    to_stage_id: Mapped[str] = mapped_column(String(36), nullable=False)
    changed_by_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    duration_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    deal: Mapped["Deal"] = relationship("Deal", back_populates="stage_history")

class DealProduct(UUIDModel, TimestampMixin):
    __tablename__ = "deal_products"

    deal_id: Mapped[str] = mapped_column(String(36), ForeignKey("deals.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    discount_pct: Mapped[float] = mapped_column(Numeric(5, 2), default=0.0, nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)

    deal: Mapped["Deal"] = relationship("Deal", back_populates="products")
