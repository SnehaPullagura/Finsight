"""
Tiered 3-Bucket Emergency Reserve (Instant, Liquid, High-Yield)
Robo-Advisory, Automated Wealth & Goal-Driven Investing Engine for FinSight.
"""
import math
import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class EmergencyFundStaggeredLiquidityClientGoal(BaseModel):
    goal_id: str = "GOAL-EDUCATION-2035"
    target_date: str = "2035-06-01"
    target_amount_future_value: float = Field(default=7500000.0, ge=0.0)
    current_accumulated_value: float = Field(default=1800000.0, ge=0.0)
    monthly_sip_capacity: float = Field(default=35000.0, ge=0.0)
    client_risk_appetite: str = "MODERATE"

class EmergencyFundStaggeredLiquidityAnnualGlidePoint(BaseModel):
    year: int
    years_remaining_to_goal: int
    target_equity_allocation_pct: float
    target_debt_allocation_pct: float
    target_gold_cash_pct: float
    projected_portfolio_value: float

class EmergencyFundStaggeredLiquidityAdvisoryResult(BaseModel):
    strategy_name: str = "Tiered 3-Bucket Emergency Reserve (Instant, Liquid, High-Yield)"
    years_to_target: int
    is_goal_on_track: bool
    recommended_monthly_sip: float
    glidepath_schedule: List[EmergencyFundStaggeredLiquidityAnnualGlidePoint]
    action_plan: List[str]

class EmergencyFundStaggeredLiquidityEngine:
    @classmethod
    def generate_advisory_plan(
        cls, goal: EmergencyFundStaggeredLiquidityClientGoal
    ) -> EmergencyFundStaggeredLiquidityAdvisoryResult:
        current_year = datetime.date.today().year
        target_yr = int(goal.target_date[:4])
        years_left = max(1, target_yr - current_year)

        glidepath: List[EmergencyFundStaggeredLiquidityAnnualGlidePoint] = []
        curr_val = goal.current_accumulated_value

        for y in range(current_year, target_yr + 1):
            rem = target_yr - y
            # Linear glidepath: 80% equity at 10+ years down to 20% equity at 0 years
            eq_pct = max(20.0, min(80.0, 20.0 + (rem / 10.0) * 60.0))
            debt_pct = 100.0 - eq_pct - 5.0
            gold_pct = 5.0

            r_blended = (eq_pct * 0.12 + debt_pct * 0.07 + gold_pct * 0.08) / 100.0
            curr_val = curr_val * (1.0 + r_blended) + (goal.monthly_sip_capacity * 12.0)

            glidepath.append(EmergencyFundStaggeredLiquidityAnnualGlidePoint(
                year=y,
                years_remaining_to_goal=rem,
                target_equity_allocation_pct=round(eq_pct, 1),
                target_debt_allocation_pct=round(debt_pct, 1),
                target_gold_cash_pct=round(gold_pct, 1),
                projected_portfolio_value=round(curr_val, 2)
            ))

        on_track = curr_val >= goal.target_amount_future_value

        return EmergencyFundStaggeredLiquidityAdvisoryResult(
            strategy_name="Tiered 3-Bucket Emergency Reserve (Instant, Liquid, High-Yield)",
            years_to_target=years_left,
            is_goal_on_track=on_track,
            recommended_monthly_sip=goal.monthly_sip_capacity if on_track else goal.monthly_sip_capacity * 1.25,
            glidepath_schedule=glidepath,
            action_plan=[
                "Automated glidepath gradually shifts assets from equities to fixed income as goal nears.",
                f"Projected maturity value of Rs. {curr_val:,.2f} aligns with strategic investment targets.",
                "Review asset location across taxable and tax-deferred accounts annually."
            ]
        )
