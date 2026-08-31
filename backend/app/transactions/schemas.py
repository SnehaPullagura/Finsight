import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from backend.app.transactions.models import TransactionType, TransactionStatus
from backend.app.categories.schemas import CategoryResponse

class TransactionSplitCreate(BaseModel):
    category_id: int
    amount: float
    notes: Optional[str] = None

class TransactionSplitResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    category_id: int
    amount: float
    notes: Optional[str] = None

class TransactionCreate(BaseModel):
    account_id: int
    category_id: Optional[int] = None
    amount: float = Field(..., gt=0)
    transaction_type: TransactionType
    transaction_date: datetime.date
    description: str = Field(..., min_length=1, max_length=255)
    raw_description: Optional[str] = None
    merchant_name: Optional[str] = None
    status: TransactionStatus = TransactionStatus.CLEARED
    is_recurring: bool = False
    is_discretionary: bool = False
    tags: Optional[str] = None
    notes: Optional[str] = None
    transfer_account_id: Optional[int] = None
    splits: Optional[List[TransactionSplitCreate]] = None

class TransactionUpdate(BaseModel):
    account_id: Optional[int] = None
    category_id: Optional[int] = None
    amount: Optional[float] = Field(default=None, gt=0)
    transaction_type: Optional[TransactionType] = None
    transaction_date: Optional[datetime.date] = None
    description: Optional[str] = None
    merchant_name: Optional[str] = None
    status: Optional[TransactionStatus] = None
    is_recurring: Optional[bool] = None
    is_discretionary: Optional[bool] = None
    tags: Optional[str] = None
    notes: Optional[str] = None

class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    account_id: int
    category_id: Optional[int] = None
    amount: float
    transaction_type: TransactionType
    transaction_date: datetime.date
    description: str
    raw_description: Optional[str] = None
    merchant_name: Optional[str] = None
    status: TransactionStatus
    is_recurring: bool
    is_discretionary: bool
    confidence_score: float
    is_user_confirmed: bool
    tags: Optional[str] = None
    notes: Optional[str] = None
    transfer_account_id: Optional[int] = None
    category: Optional[CategoryResponse] = None
    splits: Optional[List[TransactionSplitResponse]] = None
    created_at: datetime.datetime

class TransactionSearchFilter(BaseModel):
    account_id: Optional[int] = None
    category_id: Optional[int] = None
    transaction_type: Optional[TransactionType] = None
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None
    search: Optional[str] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    is_recurring: Optional[bool] = None
    limit: int = 50
    offset: int = 0
