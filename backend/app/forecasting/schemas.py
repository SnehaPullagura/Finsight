import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, ConfigDict

class ForecastPoint(BaseModel):
    date: datetime.date
    predicted_balance: float
    lower_bound: float
    upper_bound: float
    expected_cash_in: float
    expected_cash_out: float

class CategoryForecast(BaseModel):
    category_name: str
    predicted_amount: float
    historical_average: float
    trend_percent: float

class FinancialForecastResponse(BaseModel):
    horizon_days: int
    predicted_total_income: float
    predicted_total_expenses: float
    predicted_net_savings: float
    current_balance: float
    projected_ending_balance: float
    shortage_risk_probability: float # 0.0 - 1.0
    risk_level: str # "low", "medium", "high"
    savings_trajectory: Dict[str, float] # 30d, 60d, 90d, 180d, 365d
    daily_projections: List[ForecastPoint]
    category_forecasts: List[CategoryForecast]
    forecast_generated_at: datetime.datetime
