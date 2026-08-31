from datetime import date
from typing import Dict, List, Optional
from pydantic import BaseModel

class DealForecastInput(BaseModel):
    name: str
    value: float
    probability: float
    stage: str

class ForecastRequest(BaseModel):
    deals: List[DealForecastInput]
    num_simulations: Optional[int] = 1000

class ForecastResponse(BaseModel):
    unweighted_pipeline: float
    weighted_forecast: float
    commit_category: float
    best_case_category: float
    coverage_ratio: float
    monte_carlo: Dict[str, float]

class AttributionTouchpointInput(BaseModel):
    channel: str
    campaign_name: Optional[str] = None

class AttributionRequest(BaseModel):
    deal_value: float
    touchpoints: List[AttributionTouchpointInput]

class CommissionRequest(BaseModel):
    quota: float
    actual_closed: float
    base_rate_pct: Optional[float] = 10.0
