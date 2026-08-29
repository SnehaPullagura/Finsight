import uuid
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class Quote(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "quotes"

    quote_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    deal_id: Optional[Mapped[str]] = mapped_column(String(36), ForeignKey("deals.id", ondelete="SET NULL"), nullable=True, index=True)
    company_id: Optional[Mapped[str]] = mapped_column(String(36), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True)
    contact_id: Optional[Mapped[str]] = mapped_column(String(36), ForeignKey("contacts.id", ondelete="SET NULL"), nullable=True)
    
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False, index=True) # draft, pending_approval, approved, sent, accepted, rejected
    
    subtotal: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    discount_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    tax_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    
    expiration_date: Optional[Mapped[date]] = mapped_column(Date, nullable=True)
    notes: Optional[Mapped[str]] = mapped_column(Text, nullable=True)

    line_items: Mapped[List["QuoteLineItem"]] = relationship("QuoteLineItem", back_populates="quote", cascade="all, delete-orphan")

class QuoteLineItem(UUIDModel, TimestampMixin):
    __tablename__ = "quote_line_items"

    quote_id: Mapped[str] = mapped_column(String(36), ForeignKey("quotes.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id: Optional[Mapped[str]] = mapped_column(String(36), nullable=True)
    item_name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    discount_pct: Mapped[float] = mapped_column(Numeric(5, 2), default=0.0, nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)

    quote: Mapped["Quote"] = relationship("Quote", back_populates="line_items")
