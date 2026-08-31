import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from backend.app.anomaly.models import AnomalyType
from backend.app.transactions.schemas import TransactionResponse

class AnomalyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    transaction_id: int
    anomaly_type: AnomalyType
    anomaly_score: float
    severity: str
    explanation: str
    is_acknowledged: bool
    is_false_positive: bool
    transaction: Optional[TransactionResponse] = None
    created_at: datetime.datetime

class AnomalyAcknowledgeRequest(BaseModel):
    is_false_positive: bool = False
    feedback_notes: Optional[str] = None
