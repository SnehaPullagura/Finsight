import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from backend.app.recurring.models import RecurringCadence
from backend.app.categories.schemas import CategoryResponse

class RecurringPaymentCreate(BaseModel):
    account_id: int
    category_id: Optional[int] = None
    merchant_name: str = Field(..., min_length=2, max_length=128)
    amount: float = Field(..., gt=0)
    cadence: RecurringCadence = RecurringCadence.MONTHLY
    next_expected_date: datetime.date
    last_payment_date: Optional[datetime.date] = None

class RecurringPaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    account_id: int
    category_id: Optional[int] = None
    merchant_name: str
    amount: float
    cadence: RecurringCadence
    next_expected_date: datetime.date
    last_payment_date: Optional[datetime.date] = None
    is_active: bool
    is_auto_detected: bool
    category: Optional[CategoryResponse] = None

class RecurringCalendarEvent(BaseModel):
    merchant_name: str
    amount: float
    expected_date: datetime.date
    cadence: str
    category_name: str
