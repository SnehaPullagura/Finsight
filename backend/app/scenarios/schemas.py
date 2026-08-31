import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field, ConfigDict

class ScenarioCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=128)
    description: Optional[str] = None
    monthly_income_delta: float = 0.0
    monthly_expense_delta: float = 0.0
    one_time_lump_sum: float = 0.0
    loan_amount: float = 0.0
    loan_tenure_months: int = 0
    loan_interest_rate: float = 10.5

class ScenarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    name: str
    description: Optional[str] = None
    monthly_income_delta: float
    monthly_expense_delta: float
    one_time_lump_sum: float
    loan_amount: float
    loan_tenure_months: int
    loan_interest_rate: float
    calculated_monthly_emi: float
    projected_6m_balance: float
    projected_12m_balance: float
    health_score_delta: int
    is_feasible: bool
    feasibility_notes: Optional[str] = None
    created_at: datetime.datetime

class ScenarioComparisonMatrix(BaseModel):
    base_case: Dict[str, float]
    scenarios: List[ScenarioResponse]
    comparison_verdict: str
