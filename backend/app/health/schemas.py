import datetime
from typing import List, Dict
from pydantic import BaseModel, ConfigDict

class HealthPillarScore(BaseModel):
    pillar_name: str
    score: float # 0 - 100
    weight: float
    status: str # "strong", "moderate", "weak"
    metric_value: str
    description: str

class FinancialHealthResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    overall_score: int # 0 - 100
    grade: str
    score_change_mom: int
    explanation: str
    pillars: List[HealthPillarScore]
    strengths: List[str]
    attention_areas: List[str]
    recommended_actions: List[str]
    calculated_at: datetime.datetime
