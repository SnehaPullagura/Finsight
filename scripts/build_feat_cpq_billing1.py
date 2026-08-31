import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/cpq/models.py
    write_file("backend/app/cpq/models.py", """import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class PriceBook(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "cpq_price_books"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_standard: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    valid_from: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    valid_to: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    entries: Mapped[List["PriceBookEntry"]] = relationship("PriceBookEntry", back_populates="price_book", cascade="all, delete-orphan")

class PriceBookEntry(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "cpq_price_book_entries"

    price_book_id: Mapped[str] = mapped_column(String(36), ForeignKey("cpq_price_books.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id: Mapped[str] = mapped_column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    list_price: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    min_price: Mapped[Optional[float]] = mapped_column(Numeric(18, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    price_book: Mapped["PriceBook"] = relationship("PriceBook", back_populates="entries")
    product: Mapped["backend.app.models.product.Product"] = relationship("backend.app.models.product.Product")

class DiscountSchedule(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "cpq_discount_schedules"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    discount_type: Mapped[str] = mapped_column(String(50), default="volume", nullable=False) # volume, slab, term
    aggregation_scope: Mapped[str] = mapped_column(String(50), default="line", nullable=False) # line, group, quote
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    tiers: Mapped[List["DiscountTier"]] = relationship("DiscountTier", back_populates="schedule", cascade="all, delete-orphan", order_by="DiscountTier.tier_order.asc()")

class DiscountTier(UUIDModel, TimestampMixin):
    __tablename__ = "cpq_discount_tiers"

    schedule_id: Mapped[str] = mapped_column(String(36), ForeignKey("cpq_discount_schedules.id", ondelete="CASCADE"), nullable=False, index=True)
    tier_order: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    tier_name: Mapped[str] = mapped_column(String(100), nullable=False)
    lower_bound: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    upper_bound: Mapped[Optional[int]] = mapped_column(Integer, nullable=True) # None = unbounded
    discount_percentage: Mapped[float] = mapped_column(Numeric(5, 2), default=0.0, nullable=False)
    flat_discount_amount: Mapped[Optional[float]] = mapped_column(Numeric(18, 2), nullable=True)

    schedule: Mapped["DiscountSchedule"] = relationship("DiscountSchedule", back_populates="tiers")

class ProductBundle(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "cpq_product_bundles"

    parent_product_id: Mapped[str] = mapped_column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    bundle_name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    options: Mapped[List["ProductOption"]] = relationship("ProductOption", back_populates="bundle", cascade="all, delete-orphan")
    parent_product: Mapped["backend.app.models.product.Product"] = relationship("backend.app.models.product.Product")

class ProductOption(UUIDModel, TimestampMixin):
    __tablename__ = "cpq_product_options"

    bundle_id: Mapped[str] = mapped_column(String(36), ForeignKey("cpq_product_bundles.id", ondelete="CASCADE"), nullable=False, index=True)
    component_product_id: Mapped[str] = mapped_column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    option_type: Mapped[str] = mapped_column(String(50), default="component", nullable=False) # component, accessory, related
    default_quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    min_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    max_quantity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_required: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    unit_price_override: Mapped[Optional[float]] = mapped_column(Numeric(18, 2), nullable=True)

    bundle: Mapped["ProductBundle"] = relationship("ProductBundle", back_populates="options")
    component_product: Mapped["backend.app.models.product.Product"] = relationship("backend.app.models.product.Product")
""")

    # 2. backend/app/billing/models.py
    write_file("backend/app/billing/models.py", """import uuid
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
""")

    print("CPQ and Billing models created.")

if __name__ == '__main__':
    run()
