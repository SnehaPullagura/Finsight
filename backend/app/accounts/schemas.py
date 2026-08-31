import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from backend.app.accounts.models import AccountType, AccountStatus

class AccountCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=128)
    account_type: AccountType
    account_number: Optional[str] = Field(default=None, max_length=64)
    institution_name: Optional[str] = Field(default="Self/Manual", max_length=128)
    currency: str = Field(default="INR", max_length=10)
    current_balance: float = Field(default=0.0)
    credit_limit: Optional[float] = None
    interest_rate: Optional[float] = None
    is_primary: bool = False
    notes: Optional[str] = None

class AccountUpdate(BaseModel):
    name: Optional[str] = None
    institution_name: Optional[str] = None
    current_balance: Optional[float] = None
    credit_limit: Optional[float] = None
    interest_rate: Optional[float] = None
    status: Optional[AccountStatus] = None
    is_primary: bool = False
    notes: Optional[str] = None

class AccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    name: str
    account_type: AccountType
    account_number_masked: str
    institution_name: str
    currency: str
    current_balance: float
    available_balance: float
    credit_limit: Optional[float] = None
    interest_rate: Optional[float] = None
    status: AccountStatus
    is_primary: bool
    last_reconciled_at: Optional[datetime.datetime] = None
    notes: Optional[str] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime

class BalanceHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    account_id: int
    balance: float
    snapshot_date: datetime.datetime
    change_reason: str

class AccountReconcileRequest(BaseModel):
    actual_balance: float
    notes: Optional[str] = None
