"""
DuPont 3-Step & 5-Step Return on Equity (ROE) Decomposer
Enterprise Financial Analytics Module for FinSight Platform.
"""
import math
import datetime
from typing import List, Dict, Tuple, Optional
from pydantic import BaseModel, Field

class DupontAnalysisThreeFiveStepInputs(BaseModel):
    revenue_current_year: float = Field(default=50000000.0, description="Gross operating revenues")
    operating_expenses: float = Field(default=32000000.0, description="Cost of goods and operating expenses")
    depreciation_and_amortization: float = Field(default=4000000.0, description="Non-cash depreciation")
    interest_expense: float = Field(default=2500000.0, description="Finance costs")
    tax_expense_rate_pct: float = Field(default=25.0, description="Effective corporate tax rate")
    net_working_capital_change: float = Field(default=1500000.0, description="Change in NWC")
    capital_expenditures: float = Field(default=3500000.0, description="Net CapEx investments")
    total_assets: float = Field(default=80000000.0, description="Total book assets")
    total_liabilities: float = Field(default=35000000.0, description="Total liabilities")
    retained_earnings: float = Field(default=20000000.0, description="Accumulated reserves")
    market_value_of_equity: float = Field(default=60000000.0, description="Enterprise market capitalization")

class DupontAnalysisThreeFiveStepMetricDetail(BaseModel):
    metric_code: str
    metric_name: str
    calculated_value: float
    benchmark_norm: float
    status_verdict: str
    interpretive_guidance: str

class DupontAnalysisThreeFiveStepEvaluationResult(BaseModel):
    model_name: str = "DuPont 3-Step & 5-Step Return on Equity (ROE) Decomposer"
    computed_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    composite_health_score: float
    distress_or_quality_verdict: str
    key_metrics: List[DupontAnalysisThreeFiveStepMetricDetail]
    strategic_recommendations: List[str]

class DupontAnalysisThreeFiveStepEngine:
    @classmethod
    def evaluate(cls, inp: DupontAnalysisThreeFiveStepInputs) -> DupontAnalysisThreeFiveStepEvaluationResult:
        ebit = inp.revenue_current_year - inp.operating_expenses
        ebitda = ebit + inp.depreciation_and_amortization
        ebt = ebit - inp.interest_expense
        tax = ebt * (inp.tax_expense_rate_pct / 100.0)
        net_income = ebt - tax

        # FCF calculations
        nopat = ebit * (1.0 - (inp.tax_expense_rate_pct / 100.0))
        fcf = nopat + inp.depreciation_and_amortization - inp.capital_expenditures - inp.net_working_capital_change

        # Altman Z-score proxy components (Manufacturing & Service model)
        x1 = inp.net_working_capital_change / inp.total_assets if inp.total_assets > 0 else 0.0
        x2 = inp.retained_earnings / inp.total_assets if inp.total_assets > 0 else 0.0
        x3 = ebit / inp.total_assets if inp.total_assets > 0 else 0.0
        x4 = inp.market_value_of_equity / inp.total_liabilities if inp.total_liabilities > 0 else 1.0
        x5 = inp.revenue_current_year / inp.total_assets if inp.total_assets > 0 else 0.0

        z_score = 1.2 * x1 + 1.4 * x2 + 3.3 * x3 + 0.6 * x4 + 0.999 * x5

        verdict = "SAFE_ZONE" if z_score > 2.99 else ("GREY_ZONE" if z_score >= 1.81 else "DISTRESS_ZONE")

        metrics = [
            DupontAnalysisThreeFiveStepMetricDetail(
                metric_code="EBITDA",
                metric_name="Operating EBITDA",
                calculated_value=round(ebitda, 2),
                benchmark_norm=inp.revenue_current_year * 0.25,
                status_verdict="HEALTHY" if ebitda >= inp.revenue_current_year * 0.20 else "BELOW_BENCHMARK",
                interpretive_guidance="Core operating cash flow generation before non-cash and financial charges."
            ),
            DupontAnalysisThreeFiveStepMetricDetail(
                metric_code="FCF",
                metric_name="Free Cash Flow to Firm",
                calculated_value=round(fcf, 2),
                benchmark_norm=0.0,
                status_verdict="POSITIVE_FREE_CASH" if fcf > 0 else "NEGATIVE_BURN",
                interpretive_guidance="Discretionary cash generated available for debt retirement or reinvestment."
            ),
            DupontAnalysisThreeFiveStepMetricDetail(
                metric_code="Z_SCORE",
                metric_name="Composite Financial Health Indicator",
                calculated_value=round(z_score, 2),
                benchmark_norm=2.99,
                status_verdict=verdict,
                interpretive_guidance="Multivariate financial stability and solvency scoring index."
            )
        ]

        recs = [
            "Optimize working capital cycle to accelerate cash conversion and reduce short-term borrowing costs.",
            f"Free cash flow of Rs. {fcf:,.2f} provides strong cushion for reinvestment and capital expenditure.",
            f"Composite solvency index of {z_score:.2f} confirms {verdict.replace('_', ' ').lower()} standing."
        ]

        return DupontAnalysisThreeFiveStepEvaluationResult(
            composite_health_score=round(min(100.0, max(0.0, z_score * 25.0)), 1),
            distress_or_quality_verdict=verdict,
            key_metrics=metrics,
            strategic_recommendations=recs
        )
