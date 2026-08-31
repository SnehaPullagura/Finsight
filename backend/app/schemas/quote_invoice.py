from datetime import date, datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class LineItemInput(BaseModel):
    product_id: Optional[str] = None
    item_name: str
    quantity: int = 1
    unit_price: float
    discount_pct: Optional[float] = 0.0
    tax_rate_pct: Optional[float] = 0.0

class LineItemOutput(BaseModel):
    id: str
    item_name: str
    quantity: int
    unit_price: float
    total_amount: float

    class Config:
        from_attributes = True

class ProposalCreate(BaseModel):
    title: str
    deal_id: Optional[str] = None
    company_id: Optional[str] = None
    contact_id: Optional[str] = None
    valid_until: Optional[date] = None
    terms_and_conditions: Optional[str] = None
    line_items: List[LineItemInput] = []

class ProposalResponse(BaseModel):
    id: str
    tenant_id: str
    proposal_number: str
    title: str
    status: str
    deal_id: Optional[str] = None
    company_id: Optional[str] = None
    contact_id: Optional[str] = None
    subtotal: float
    discount_amount: float
    tax_amount: float
    total_amount: float
    currency: str
    valid_until: Optional[date] = None
    created_at: datetime

    class Config:
        from_attributes = True

class QuoteCreate(BaseModel):
    deal_id: Optional[str] = None
    company_id: Optional[str] = None
    contact_id: Optional[str] = None
    expiration_date: Optional[date] = None
    notes: Optional[str] = None
    line_items: List[LineItemInput] = []

class QuoteResponse(BaseModel):
    id: str
    tenant_id: str
    quote_number: str
    status: str
    deal_id: Optional[str] = None
    total_amount: float
    currency: str
    expiration_date: Optional[date] = None
    created_at: datetime

    class Config:
        from_attributes = True

class InvoiceCreate(BaseModel):
    deal_id: Optional[str] = None
    quote_id: Optional[str] = None
    company_id: Optional[str] = None
    contact_id: Optional[str] = None
    issue_date: Optional[date] = None
    due_date: date
    notes: Optional[str] = None
    line_items: List[LineItemInput] = []

class PaymentRecordCreate(BaseModel):
    amount: float
    payment_method: Optional[str] = "bank_transfer"
    transaction_reference: Optional[str] = None

class InvoiceResponse(BaseModel):
    id: str
    tenant_id: str
    invoice_number: str
    status: str
    payment_status: str
    issue_date: date
    due_date: date
    subtotal: float
    tax_amount: float
    total_amount: float
    amount_paid: float
    currency: str
    created_at: datetime

    class Config:
        from_attributes = True
