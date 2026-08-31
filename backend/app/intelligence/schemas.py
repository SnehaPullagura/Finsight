from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from backend.app.categories.schemas import CategoryResponse

class CategorizationRequest(BaseModel):
    description: str
    amount: Optional[float] = None

class CategorizationResponse(BaseModel):
    category_id: int
    category_name: str
    category_group: str
    merchant_name: str
    confidence_score: float
    is_recurring_predicted: bool
    category: Optional[CategoryResponse] = None

class DuplicateCheckRequest(BaseModel):
    account_id: int
    amount: float
    description: str
    transaction_date: str

class DuplicateCheckResponse(BaseModel):
    is_duplicate: bool
    match_confidence: float
    matched_transaction_id: Optional[int] = None
    reason: Optional[str] = None
