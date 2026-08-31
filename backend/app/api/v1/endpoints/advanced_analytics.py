from fastapi import APIRouter, Depends
from backend.app.analytics.schemas import (
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
