import uuid
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, TenantMixin

class AnalyticsSnapshot(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "analytics_snapshots"

    snapshot_date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False, index=True)
    snapshot_type: Mapped[str] = mapped_column(String(50), default="daily_pipeline", nullable=False) # daily_pipeline, mrr_summary, lead_velocity
    total_pipeline_value: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    weighted_pipeline_value: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    open_deal_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    won_deal_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    lost_deal_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    active_mrr: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    metrics_breakdown: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

class SalesQuota(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "analytics_sales_quotas"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    fiscal_year: Mapped[int] = mapped_column(Integer, nullable=False)
    fiscal_quarter: Mapped[int] = mapped_column(Integer, nullable=False) # 1, 2, 3, 4
    quota_amount: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    attained_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    commission_rate_base: Mapped[float] = mapped_column(Numeric(5, 2), default=10.0, nullable=False)

class AttributionTouchpoint(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "analytics_attribution_touchpoints"

    deal_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("deals.id", ondelete="CASCADE"), nullable=True, index=True)
    contact_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("contacts.id", ondelete="CASCADE"), nullable=True, index=True)
    channel: Mapped[str] = mapped_column(String(100), nullable=False) # organic_search, google_ads, linkedin_ads, email_outreach, webinar
    campaign_name: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    touchpoint_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    position: Mapped[str] = mapped_column(String(50), default="middle", nullable=False) # first, middle, last, create
