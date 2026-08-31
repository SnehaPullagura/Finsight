import uuid
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class Subscription(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "billing_subscriptions"

    company_id: Mapped[str] = mapped_column(String(36), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    contact_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("contacts.id", ondelete="SET NULL"), nullable=True)
    plan_name: Mapped[str] = mapped_column(String(150), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False, index=True) # active, trialing, past_due, canceled, paused, expired
    billing_frequency: Mapped[str] = mapped_column(String(50), default="monthly", nullable=False) # monthly, quarterly, annual, custom
    
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    mrr_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False, index=True)
    arr_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    current_period_start: Mapped[date] = mapped_column(Date, nullable=False)
    current_period_end: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    trial_end: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    canceled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    cancel_at_period_end: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    auto_renew: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    payment_method_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    company: Mapped["backend.app.models.company.Company"] = relationship("backend.app.models.company.Company")
    items: Mapped[List["SubscriptionItem"]] = relationship("SubscriptionItem", back_populates="subscription", cascade="all, delete-orphan")

class SubscriptionItem(UUIDModel, TimestampMixin):
    __tablename__ = "billing_subscription_items"

    subscription_id: Mapped[str] = mapped_column(String(36), ForeignKey("billing_subscriptions.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id: Mapped[str] = mapped_column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    item_name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    discount_pct: Mapped[float] = mapped_column(Numeric(5, 2), default=0.0, nullable=False)
    item_mrr: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)

    subscription: Mapped["Subscription"] = relationship("Subscription", back_populates="items")
    product: Mapped["backend.app.models.product.Product"] = relationship("backend.app.models.product.Product")

class UsageMeter(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "billing_usage_meters"

    meter_code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    meter_name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    unit_of_measure: Mapped[str] = mapped_column(String(50), default="count", nullable=False) # api_calls, storage_gb, compute_hours, active_users
    aggregation_type: Mapped[str] = mapped_column(String(50), default="sum", nullable=False) # sum, max, last, average
    unit_price: Mapped[float] = mapped_column(Numeric(18, 4), default=0.0, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)

class UsageRecord(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "billing_usage_records"

    meter_id: Mapped[str] = mapped_column(String(36), ForeignKey("billing_usage_meters.id", ondelete="CASCADE"), nullable=False, index=True)
    company_id: Mapped[str] = mapped_column(String(36), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    subscription_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("billing_subscriptions.id", ondelete="SET NULL"), nullable=True)
    quantity: Mapped[float] = mapped_column(Numeric(18, 4), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    is_invoiced: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    idempotency_key: Mapped[Optional[str]] = mapped_column(String(100), unique=True, index=True, nullable=True)

class TaxRate(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "billing_tax_rates"

    jurisdiction_country: Mapped[str] = mapped_column(String(2), nullable=False, index=True) # ISO-2
    jurisdiction_state: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    tax_name: Mapped[str] = mapped_column(String(100), nullable=False)
    rate_percentage: Mapped[float] = mapped_column(Numeric(5, 3), nullable=False)
    is_compound: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

class CreditNote(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "billing_credit_notes"

    credit_note_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    invoice_id: Mapped[str] = mapped_column(String(36), ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False, index=True)
    company_id: Mapped[str] = mapped_column(String(36), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    reason: Mapped[str] = mapped_column(String(100), nullable=False) # billing_error, customer_goodwill, service_downgrade, SLA_breach_refund
    amount: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="applied", nullable=False) # draft, applied, refunded, void
    issued_date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
