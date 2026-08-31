import uuid
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
