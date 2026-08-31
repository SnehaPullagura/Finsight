from datetime import date
from typing import Dict, List, Optional
from pydantic import BaseModel

class SubscriptionCreateRequest(BaseModel):
    company_id: str
    contact_id: Optional[str] = None
    plan_name: str
    billing_frequency: str = "monthly" # monthly, quarterly, annual
    monthly_base_price: float
    currency: str = "USD"
    start_date: Optional[date] = None

class SubscriptionResponse(BaseModel):
    id: str
    company_id: str
    plan_name: str
    status: str
    billing_frequency: str
    currency: str
    mrr_amount: float
    arr_amount: float
    start_date: date
    current_period_start: date
    current_period_end: date
    auto_renew: bool

class UpgradePlanRequest(BaseModel):
    new_plan_name: str
    new_monthly_price: float
    effective_date: Optional[date] = None

class ProrationPreviewResponse(BaseModel):
    credit_for_unused_old_plan: float
    charge_for_new_plan: float
    net_payable_now: float
    new_recurring_mrr: float
