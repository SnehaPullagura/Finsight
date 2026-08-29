from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class AILeadSummaryResponse(BaseModel):
    lead_id: str
    summary: str
    key_strengths: List[str]
    risk_factors: List[str]
    suggested_next_steps: List[str]
    estimated_fit_score: int

class AIDealRiskAnalysisResponse(BaseModel):
    deal_id: str
    deal_name: str
    win_probability_pct: int
    risk_level: str # low, medium, high, critical
    identified_risks: List[str]
    deal_momentum_score: int
    actionable_recommendations: List[str]

class AIEmailDraftRequest(BaseModel):
    recipient_name: str
    context_topic: str
    objective: str # schedule_meeting, follow_up, proposal_review, renewal_checkin
    tone: Optional[str] = "professional"

class AIEmailDraftResponse(BaseModel):
    subject: str
    body_text: str
    call_to_action: str

class AINLQueryRequest(BaseModel):
    query_text: str

class AINLQueryResponse(BaseModel):
    interpreted_intent: str
    target_entity: str
    applied_filters: Dict[str, Any]
    sql_or_search_expression: str
    insights_summary: str
