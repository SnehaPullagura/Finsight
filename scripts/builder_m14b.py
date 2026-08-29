import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    write_file("backend/app/schemas/product.py", """from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    sku: str = Field(min_length=1, max_length=100)
    category_id: Optional[str] = None
    description: Optional[str] = None
    unit_price: float = Field(ge=0.0)
    cost_price: Optional[float] = None
    currency: Optional[str] = "USD"
    tax_rate_pct: Optional[float] = 0.0
    is_active: Optional[bool] = True
    is_service: Optional[bool] = False
    inventory_stock: Optional[int] = 0

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    category_id: Optional[str] = None
    description: Optional[str] = None
    unit_price: Optional[float] = None
    tax_rate_pct: Optional[float] = None
    is_active: Optional[bool] = None
    inventory_stock: Optional[int] = None

class ProductResponse(BaseModel):
    id: str
    tenant_id: str
    name: str
    sku: str
    category_id: Optional[str] = None
    description: Optional[str] = None
    unit_price: float
    currency: str
    tax_rate_pct: float
    is_active: bool
    is_service: bool
    inventory_stock: int
    created_at: datetime

    class Config:
        from_attributes = True
""")

    write_file("backend/app/schemas/quote_invoice.py", """from datetime import date, datetime
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
""")

    print("Schemas for Products, Quotes, Invoices generated.")

if __name__ == '__main__':
    run()
