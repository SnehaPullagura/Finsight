from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class CurrencyConvertRequest(BaseModel):
    amount: float
    from_currency: str = "USD"
    to_currency: str = "EUR"

class CurrencyConvertResponse(BaseModel):
    original_amount: float
    from_currency: str
    converted_amount: float
    to_currency: str
    rate: float

class PriceCalculationItem(BaseModel):
    product_id: str
    unit_price: float
    quantity: int
    discount_percentage: Optional[float] = 0.0
    flat_discount: Optional[float] = 0.0
    tax_rate_pct: Optional[float] = 0.0

class CPQCalculationResponse(BaseModel):
    subtotal: float
    total_discount: float
    net_amount: float
    tax_amount: float
    total_amount: float
    currency: str
    line_breakdowns: List[Dict[str, float]]
