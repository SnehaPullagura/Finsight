import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from backend.app.budgets.models import BudgetPeriod
from backend.app.categories.schemas import CategoryResponse

class BudgetCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=128)
    category_id: Optional[int] = None
    allocated_amount: float = Field(..., gt=0)
    period: BudgetPeriod = BudgetPeriod.MONTHLY
    start_date: datetime.date
    end_date: Optional[datetime.date] = None
    notify_threshold_percent: float = Field(default=80.0, ge=1.0, le=100.0)

class BudgetUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    allocated_amount: Optional[float] = Field(default=None, gt=0)
    period: Optional[BudgetPeriod] = None
    notify_threshold_percent: Optional[float] = None
    is_active: Optional[bool] = None

class BudgetProgressResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    category_id: Optional[int] = None
    name: str
    allocated_amount: float
    spent_amount: float
    remaining_amount: float
    percentage_used: float
    is_overbudget: bool
    status: str # "good", "warning", "exceeded"
    category: Optional[CategoryResponse] = None
