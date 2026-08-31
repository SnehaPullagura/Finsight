import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel

class AssistantQueryRequest(BaseModel):
    query: str
    conversation_history: Optional[List[Dict[str, str]]] = None

class FinancialDataCard(BaseModel):
    title: str
    key_metric: str
    description: str
    badge: Optional[str] = None

class AssistantQueryResponse(BaseModel):
    answer: str
    suggested_followups: List[str]
    grounded_facts: List[str]
    data_card: Optional[FinancialDataCard] = None
    created_at: datetime.datetime
