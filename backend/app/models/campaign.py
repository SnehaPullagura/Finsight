import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class CampaignSegment(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "campaign_segments"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    target_entity: Mapped[str] = mapped_column(String(50), default="contact", nullable=False)
    filter_criteria: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    campaigns: Mapped[List["Campaign"]] = relationship("Campaign", back_populates="segment")

class Campaign(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "campaigns"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(50), default="email", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False, index=True)
    segment_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("campaign_segments.id", ondelete="SET NULL"), nullable=True)
    template_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    total_recipients: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    sent_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    open_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    click_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    conversion_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    budget: Mapped[Optional[float]] = mapped_column(Numeric(18, 2), nullable=True)
    revenue_attributed: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)

    segment: Mapped[Optional["CampaignSegment"]] = relationship("CampaignSegment", back_populates="campaigns")
    recipients: Mapped[List["CampaignRecipient"]] = relationship("CampaignRecipient", back_populates="campaign", cascade="all, delete-orphan")

class CampaignRecipient(UUIDModel, TimestampMixin):
    __tablename__ = "campaign_recipients"

    campaign_id: Mapped[str] = mapped_column(String(36), ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)

    campaign: Mapped["Campaign"] = relationship("Campaign", back_populates="recipients")
