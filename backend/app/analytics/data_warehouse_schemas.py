from datetime import date, datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class DimTime(BaseModel):
    date_key: int # YYYYMMDD
    full_date: date
    day_of_week: int
    day_name: str
    month: int
    month_name: str
    quarter: int
    year: int
    is_weekend: bool
    is_holiday: bool = False

class DimCompany(BaseModel):
    company_key: str
    name: str
    industry: str
    tier: str
    country: str
    city: str
    employee_range: str
    annual_revenue_band: str

class DimContact(BaseModel):
    contact_key: str
    company_key: str
    first_name: str
    last_name: str
    email: str
    title: str
    lifecycle_stage: str
    lead_source: str

class DimSalesRep(BaseModel):
    rep_key: str
    first_name: str
    last_name: str
    email: str
    team_name: str
    region: str
    quota_tier: str

class FactDealSnapshot(BaseModel):
    deal_key: str
    date_key: int
    company_key: str
    contact_key: str
    rep_key: str
    pipeline_key: str
    stage_key: str
    deal_amount: float
    probability_percentage: float
    weighted_amount: float
    is_won: bool = False
    is_lost: bool = False
    days_in_current_stage: int = 0
    total_sales_cycle_days: int = 0

class FactSubscriptionMRR(BaseModel):
    subscription_key: str
    date_key: int
    company_key: str
    plan_key: str
    mrr_amount: float
    arr_amount: float
    expansion_mrr: float = 0.0
    contraction_mrr: float = 0.0
    churn_mrr: float = 0.0
    net_new_mrr: float = 0.0

class FactSupportTicket(BaseModel):
    ticket_key: str
    date_key: int
    company_key: str
    contact_key: str
    assigned_rep_key: str
    priority: str
    category: str
    resolution_time_hours: float
    first_response_time_hours: float
    sla_response_breached: bool = False
    sla_resolution_breached: bool = False
    csat_score: Optional[int] = None
