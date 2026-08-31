import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    write_file("backend/app/models/product.py", """import uuid
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class ProductCategory(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "product_categories"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Optional[Mapped[str]] = mapped_column(String(255), nullable=True)

    products: Mapped[List["Product"]] = relationship("Product", back_populates="category")

class Product(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    sku: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    category_id: Optional[Mapped[str]] = mapped_column(String(36), ForeignKey("product_categories.id", ondelete="SET NULL"), nullable=True)
    description: Optional[Mapped[str]] = mapped_column(Text, nullable=True)
    
    unit_price: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    cost_price: Optional[Mapped[float]] = mapped_column(Numeric(18, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    tax_rate_pct: Mapped[float] = mapped_column(Numeric(5, 2), default=0.0, nullable=False)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_service: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    inventory_stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    category: Mapped[Optional["ProductCategory"]] = relationship("ProductCategory", back_populates="products")
""")

    write_file("backend/app/models/proposal.py", """import uuid
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class Proposal(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "proposals"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    proposal_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    
    deal_id: Optional[Mapped[str]] = mapped_column(String(36), ForeignKey("deals.id", ondelete="SET NULL"), nullable=True, index=True)
    company_id: Optional[Mapped[str]] = mapped_column(String(36), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True)
    contact_id: Optional[Mapped[str]] = mapped_column(String(36), ForeignKey("contacts.id", ondelete="SET NULL"), nullable=True)
    
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False, index=True) # draft, sent, viewed, accepted, rejected, expired
    
    subtotal: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    discount_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    tax_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    
    valid_until: Optional[Mapped[date]] = mapped_column(Date, nullable=True)
    accepted_at: Optional[Mapped[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    terms_and_conditions: Optional[Mapped[str]] = mapped_column(Text, nullable=True)
    custom_sections: Mapped[list] = mapped_column(JSON, default=list, nullable=False)

    line_items: Mapped[List["ProposalLineItem"]] = relationship("ProposalLineItem", back_populates="proposal", cascade="all, delete-orphan")

class ProposalLineItem(UUIDModel, TimestampMixin):
    __tablename__ = "proposal_line_items"

    proposal_id: Mapped[str] = mapped_column(String(36), ForeignKey("proposals.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id: Optional[Mapped[str]] = mapped_column(String(36), nullable=True)
    item_name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    discount_pct: Mapped[float] = mapped_column(Numeric(5, 2), default=0.0, nullable=False)
    tax_rate_pct: Mapped[float] = mapped_column(Numeric(5, 2), default=0.0, nullable=False)
    line_total: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)

    proposal: Mapped["Proposal"] = relationship("Proposal", back_populates="line_items")
""")

    write_file("backend/app/models/quote.py", """import uuid
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
""")

    write_file("backend/app/models/invoice.py", """import uuid
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class Invoice(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "invoices"

    invoice_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    deal_id: Optional[Mapped[str]] = mapped_column(String(36), ForeignKey("deals.id", ondelete="SET NULL"), nullable=True, index=True)
    quote_id: Optional[Mapped[str]] = mapped_column(String(36), ForeignKey("quotes.id", ondelete="SET NULL"), nullable=True)
    company_id: Optional[Mapped[str]] = mapped_column(String(36), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True)
    contact_id: Optional[Mapped[str]] = mapped_column(String(36), ForeignKey("contacts.id", ondelete="SET NULL"), nullable=True)
    
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False, index=True) # draft, issued, paid, partially_paid, overdue, void
    payment_status: Mapped[str] = mapped_column(String(50), default="unpaid", nullable=False) # unpaid, partial, paid
    
    issue_date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    
    subtotal: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    tax_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    amount_paid: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    
    notes: Optional[Mapped[str]] = mapped_column(Text, nullable=True)

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
    transaction_reference: Optional[Mapped[str]] = mapped_column(String(100), nullable=True)
    paid_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    invoice: Mapped["Invoice"] = relationship("Invoice", back_populates="payments")
""")

    print("Models for Products, Proposals, Quotes, Invoices generated.")

if __name__ == '__main__':
    run()
