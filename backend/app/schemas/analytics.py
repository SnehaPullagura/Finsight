from datetime import date
from typing import Dict, List, Optional, Any
from pydantic import BaseModel

class MetricCard(BaseModel):
    label: str
    value: float
    formatted_value: str
    change_pct: Optional[float] = None
    trend: Optional[str] = "up" # up, down, neutral

class FunnelStage(BaseModel):
    stage_name: str
    count: int
    value: float
    conversion_rate_pct: float

class TimeSeriesPoint(BaseModel):
    period: str
    revenue: float
    deals_count: int

class RepPerformance(BaseModel):
    user_id: str
    user_name: str
    deals_won_count: int
    revenue_won: float
    target: float
    quota_attainment_pct: float

class DashboardSummaryResponse(BaseModel):
    total_pipeline_value: MetricCard
    weighted_forecast: MetricCard
    win_rate: MetricCard
    active_deals_count: MetricCard
    lead_conversion_rate: MetricCard
    customer_avg_health: MetricCard
    sla_compliance_rate: MetricCard
    
    revenue_trend: List[TimeSeriesPoint]
    conversion_funnel: List[FunnelStage]
    rep_leaderboard: List[RepPerformance]
