import uuid
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class Proposal(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "proposals"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    proposal_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    
    deal_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("deals.id", ondelete="SET NULL"), nullable=True, index=True)
    company_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True)
    contact_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("contacts.id", ondelete="SET NULL"), nullable=True)
    
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False, index=True) # draft, sent, viewed, accepted, rejected, expired
    
    subtotal: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    discount_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    tax_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    
    valid_until: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    accepted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    terms_and_conditions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    custom_sections: Mapped[list] = mapped_column(JSON, default=list, nullable=False)

    line_items: Mapped[List["ProposalLineItem"]] = relationship("ProposalLineItem", back_populates="proposal", cascade="all, delete-orphan")

class ProposalLineItem(UUIDModel, TimestampMixin):
    __tablename__ = "proposal_line_items"

    proposal_id: Mapped[str] = mapped_column(String(36), ForeignKey("proposals.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    item_name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    discount_pct: Mapped[float] = mapped_column(Numeric(5, 2), default=0.0, nullable=False)
    tax_rate_pct: Mapped[float] = mapped_column(Numeric(5, 2), default=0.0, nullable=False)
    line_total: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)

    proposal: Mapped["Proposal"] = relationship("Proposal", back_populates="line_items")
