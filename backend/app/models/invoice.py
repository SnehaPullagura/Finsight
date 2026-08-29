import uuid
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class Invoice(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "invoices"

    invoice_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    deal_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("deals.id", ondelete="SET NULL"), nullable=True, index=True)
    quote_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("quotes.id", ondelete="SET NULL"), nullable=True)
    company_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True)
    contact_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("contacts.id", ondelete="SET NULL"), nullable=True)
    
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False, index=True) # draft, issued, paid, partially_paid, overdue, void
    payment_status: Mapped[str] = mapped_column(String(50), default="unpaid", nullable=False) # unpaid, partial, paid
    
    issue_date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    
    subtotal: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    tax_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    amount_paid: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    line_items: Mapped[List["InvoiceLineItem"]] = relationship("InvoiceLineItem", back_populates="invoice", cascade="all, delete-orphan")
    payments: Mapped[List["InvoicePayment"]] = relationship("InvoicePayment", back_populates="invoice", cascade="all, delete-orphan")

class InvoiceLineItem(UUIDModel, TimestampMixin):
    __tablename__ = "invoice_line_items"

    invoice_id: Mapped[str] = mapped_column(String(36), ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False, index=True)
    item_name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    tax_rate_pct: Mapped[float] = mapped_column(Numeric(5, 2), default=0.0, nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)

    invoice: Mapped["Invoice"] = relationship("Invoice", back_populates="line_items")

class InvoicePayment(UUIDModel, TimestampMixin):
    __tablename__ = "invoice_payments"

    invoice_id: Mapped[str] = mapped_column(String(36), ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False, index=True)
    amount: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    payment_method: Mapped[str] = mapped_column(String(50), default="bank_transfer", nullable=False)
    transaction_reference: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    paid_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    invoice: Mapped["Invoice"] = relationship("Invoice", back_populates="payments")
