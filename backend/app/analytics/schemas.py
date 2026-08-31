from typing import List, Dict
from pydantic import BaseModel

class MoMComparison(BaseModel):
    current_month: str
    previous_month: str
    income_current: float
    income_previous: float
    income_growth_percent: float
    expense_current: float
    expense_previous: float
    expense_growth_percent: float
    savings_rate_current: float
    savings_rate_previous: float

class SpendingVelocity(BaseModel):
    daily_burn_rate: float
    projected_month_end_expense: float
    days_elapsed: int
    days_remaining: int
    pace_status: str # "ahead_of_budget", "on_pace", "burning_fast"

class AnalyticsOverviewResponse(BaseModel):
    mom: MoMComparison
    velocity: SpendingVelocity
    financial_stability_index: float # 0 - 100
    recurring_expense_ratio: float # % of expenses that are fixed subscriptions/EMIs
    discretionary_ratio: float # % of expenses that are wants
    top_merchants: List[Dict[str, float]]
    category_distribution: Dict[str, float]
