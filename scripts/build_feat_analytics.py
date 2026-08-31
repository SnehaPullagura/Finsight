import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/analytics/models.py
    write_file("backend/app/analytics/models.py", """import uuid
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, TenantMixin

class AnalyticsSnapshot(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "analytics_snapshots"

    snapshot_date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False, index=True)
    snapshot_type: Mapped[str] = mapped_column(String(50), default="daily_pipeline", nullable=False) # daily_pipeline, mrr_summary, lead_velocity
    total_pipeline_value: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    weighted_pipeline_value: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    open_deal_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    won_deal_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    lost_deal_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    active_mrr: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    metrics_breakdown: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

class SalesQuota(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "analytics_sales_quotas"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    fiscal_year: Mapped[int] = mapped_column(Integer, nullable=False)
    fiscal_quarter: Mapped[int] = mapped_column(Integer, nullable=False) # 1, 2, 3, 4
    quota_amount: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    attained_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    commission_rate_base: Mapped[float] = mapped_column(Numeric(5, 2), default=10.0, nullable=False)

class AttributionTouchpoint(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "analytics_attribution_touchpoints"

    deal_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("deals.id", ondelete="CASCADE"), nullable=True, index=True)
    contact_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("contacts.id", ondelete="CASCADE"), nullable=True, index=True)
    channel: Mapped[str] = mapped_column(String(100), nullable=False) # organic_search, google_ads, linkedin_ads, email_outreach, webinar
    campaign_name: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    touchpoint_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    position: Mapped[str] = mapped_column(String(50), default="middle", nullable=False) # first, middle, last, create
""")

    # 2. backend/app/analytics/engine.py
    write_file("backend/app/analytics/engine.py", """import math
import random
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple

class RevenueForecastingModel:
    @staticmethod
    def calculate_weighted_forecast(deals: List[dict]) -> Dict[str, float]:
        commit_total = 0.0
        best_case_total = 0.0
        pipeline_total = 0.0
        weighted_total = 0.0

        for d in deals:
            val = float(d.get("value", 0.0))
            prob = float(d.get("probability", 0.0))
            weighted_total += val * (prob / 100.0)
            pipeline_total += val

            if prob >= 80:
                commit_total += val
                best_case_total += val
            elif prob >= 40:
                best_case_total += val

        return {
            "unweighted_pipeline": round(pipeline_total, 2),
            "weighted_forecast": round(weighted_total, 2),
            "commit_category": round(commit_total, 2),
            "best_case_category": round(best_case_total, 2),
            "coverage_ratio": round(pipeline_total / max(1.0, commit_total), 2)
        }

    @staticmethod
    def monte_carlo_simulation(deals: List[dict], num_simulations: int = 1000) -> Dict[str, float]:
        if not deals:
            return {"p10_worst_case": 0.0, "p50_expected": 0.0, "p90_optimistic": 0.0, "mean": 0.0}

        results = []
        random.seed(42) # Deterministic seed

        for _ in range(num_simulations):
            sim_revenue = 0.0
            for d in deals:
                val = float(d.get("value", 0.0))
                prob = float(d.get("probability", 0.0)) / 100.0
                if random.random() <= prob:
                    sim_revenue += val
            results.append(sim_revenue)

        results.sort()
        n = len(results)
        p10 = results[int(n * 0.10)]
        p50 = results[int(n * 0.50)]
        p90 = results[int(n * 0.90)]
        mean_val = sum(results) / n

        return {
            "p10_worst_case": round(p10, 2),
            "p50_expected": round(p50, 2),
            "p90_optimistic": round(p90, 2),
            "mean": round(mean_val, 2)
        }

class CohortRetentionAnalysis:
    @staticmethod
    def generate_cohort_matrix(cohort_data: List[dict]) -> List[dict]:
        cohort_table = []
        for c in cohort_data:
            cohort_name = c["cohort_month"]
            initial_count = max(1, c["initial_customers"])
            monthly_active = c.get("active_per_month", [])

            retention_percentages = [
                round((active / initial_count) * 100.0, 1) for active in monthly_active
            ]

            cohort_table.append({
                "cohort": cohort_name,
                "initial_size": initial_count,
                "retention_rates": retention_percentages,
                "nrr_percentage": round(c.get("ending_mrr", 0.0) / max(1.0, c.get("starting_mrr", 1.0)) * 100.0, 1)
            })
        return cohort_table

class MultiTouchAttributionModel:
    @staticmethod
    def calculate_attribution(touchpoints: List[dict], deal_value: float) -> Dict[str, Dict[str, float]]:
        if not touchpoints:
            return {}

        n = len(touchpoints)
        models = {"first_touch": {}, "last_touch": {}, "linear": {}, "position_based": {}}

        # 1. First Touch
        first_channel = touchpoints[0]["channel"]
        models["first_touch"][first_channel] = round(deal_value, 2)

        # 2. Last Touch
        last_channel = touchpoints[-1]["channel"]
        models["last_touch"][last_channel] = round(deal_value, 2)

        # 3. Linear
        linear_val = round(deal_value / n, 2)
        for tp in touchpoints:
            ch = tp["channel"]
            models["linear"][ch] = models["linear"].get(ch, 0.0) + linear_val

        # 4. Position-Based (40% first, 40% last, 20% middle split)
        if n == 1:
            models["position_based"][first_channel] = round(deal_value, 2)
        elif n == 2:
            models["position_based"][first_channel] = round(deal_value * 0.50, 2)
            models["position_based"][last_channel] = models["position_based"].get(last_channel, 0.0) + round(deal_value * 0.50, 2)
        else:
            first_val = round(deal_value * 0.40, 2)
            last_val = round(deal_value * 0.40, 2)
            mid_val = round((deal_value * 0.20) / (n - 2), 2)

            models["position_based"][first_channel] = models["position_based"].get(first_channel, 0.0) + first_val
            models["position_based"][last_channel] = models["position_based"].get(last_channel, 0.0) + last_val
            for tp in touchpoints[1:-1]:
                ch = tp["channel"]
                models["position_based"][ch] = models["position_based"].get(ch, 0.0) + mid_val

        return models

class SalesCompensationEngine:
    @staticmethod
    def calculate_commission(
        quota: float,
        actual_closed: float,
        base_rate_pct: float = 10.0,
        accelerators: Optional[List[dict]] = None
    ) -> Dict[str, float]:
        attainment_pct = round((actual_closed / max(1.0, quota)) * 100.0, 2)
        default_accelerators = accelerators or [
            {"min_pct": 0, "max_pct": 100, "multiplier": 1.0},
            {"min_pct": 100, "max_pct": 120, "multiplier": 1.5},
            {"min_pct": 120, "max_pct": None, "multiplier": 2.0},
        ]

        total_commission = 0.0
        for tier in default_accelerators:
            min_p = tier["min_pct"]
            max_p = tier["max_pct"] or float("inf")
            mult = tier["multiplier"]

            if attainment_pct > min_p:
                portion_pct = min(attainment_pct - min_p, max_p - min_p)
                portion_revenue = quota * (portion_pct / 100.0)
                tier_commission = portion_revenue * (base_rate_pct / 100.0) * mult
                total_commission += tier_commission

        return {
            "quota": quota,
            "actual_closed": actual_closed,
            "attainment_percentage": attainment_pct,
            "total_commission_earned": round(total_commission, 2),
            "effective_commission_rate": round((total_commission / max(1.0, actual_closed)) * 100.0, 2)
        }
""")

    # 3. backend/app/analytics/schemas.py & Endpoints
    write_file("backend/app/analytics/schemas.py", """from datetime import date
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
""")

    write_file("backend/app/api/v1/endpoints/advanced_analytics.py", """from fastapi import APIRouter, Depends
from backend.app.schemas.analytics import (
    ForecastRequest,
    ForecastResponse,
    AttributionRequest,
    CommissionRequest
)
from backend.app.analytics.engine import (
    RevenueForecastingModel,
    CohortRetentionAnalysis,
    MultiTouchAttributionModel,
    SalesCompensationEngine
)

router = APIRouter()

@router.post("/forecast", response_model=ForecastResponse)
async def generate_revenue_forecast(req: ForecastRequest):
    deals_data = [d.model_dump() for d in req.deals]
    weighted = RevenueForecastingModel.calculate_weighted_forecast(deals_data)
    mc = RevenueForecastingModel.monte_carlo_simulation(deals_data, req.num_simulations or 1000)

    return ForecastResponse(
        unweighted_pipeline=weighted["unweighted_pipeline"],
        weighted_forecast=weighted["weighted_forecast"],
        commit_category=weighted["commit_category"],
        best_case_category=weighted["best_case_category"],
        coverage_ratio=weighted["coverage_ratio"],
        monte_carlo=mc
    )

@router.post("/attribution")
async def calculate_multi_touch_attribution(req: AttributionRequest):
    tps = [t.model_dump() for t in req.touchpoints]
    res = MultiTouchAttributionModel.calculate_attribution(tps, req.deal_value)
    return {"deal_value": req.deal_value, "touchpoint_count": len(tps), "models": res}

@router.post("/commissions")
async def calculate_sales_commission(req: CommissionRequest):
    return SalesCompensationEngine.calculate_commission(
        quota=req.quota,
        actual_closed=req.actual_closed,
        base_rate_pct=req.base_rate_pct or 10.0
    )

@router.get("/cohorts")
async def get_retention_cohorts():
    sample_cohorts = [
        {"cohort_month": "2026-01", "initial_customers": 50, "active_per_month": [50, 48, 46, 45, 45, 44], "starting_mrr": 50000, "ending_mrr": 58000},
        {"cohort_month": "2026-02", "initial_customers": 65, "active_per_month": [65, 62, 60, 59, 58], "starting_mrr": 65000, "ending_mrr": 74000},
        {"cohort_month": "2026-03", "initial_customers": 80, "active_per_month": [80, 77, 75, 74], "starting_mrr": 80000, "ending_mrr": 92000}
    ]
    return CohortRetentionAnalysis.generate_cohort_matrix(sample_cohorts)
""")

    print("Advanced Analytics & Forecasting Engine, Schemas, and Endpoints created.")

if __name__ == '__main__':
    run()
