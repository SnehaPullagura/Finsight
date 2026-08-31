import datetime
from typing import List, Dict
from pydantic import BaseModel

class DailyCashFlowPoint(BaseModel):
    date: datetime.date
    cash_in: float
    cash_out: float
    net_cash_flow: float
    projected_balance: float

class CashFlowSummaryResponse(BaseModel):
    total_cash_in: float
    total_cash_out: float
    net_cash_flow: float
    savings_rate_percent: float
    average_daily_burn_rate: float
    liquidity_runway_days: int
    daily_timeline: List[DailyCashFlowPoint]
    category_cash_out_breakdown: Dict[str, float]
