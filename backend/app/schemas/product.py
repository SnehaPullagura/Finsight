from datetime import datetime
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
