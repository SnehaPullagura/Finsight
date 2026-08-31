"""
Rule of 72, 114, and 144 Doubling Time Calculator
Production implementation for FinSight Financial Decision Engine.
"""
import math
import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class RuleOf72CalculatorInputs(BaseModel):
    principal_amount: float = Field(..., ge=0, description="Base principal currency amount")
    annual_rate_pct: float = Field(..., ge=0, description="Annual rate in percentage terms")
    tenure_years: float = Field(..., ge=0, description="Time duration in years")
    frequency_per_year: int = Field(default=12, description="Compounding or contribution frequency")
    annual_step_up_pct: Optional[float] = Field(default=0.0, description="Optional annual step up percentage")

class RuleOf72CalculatorYearBreakdown(BaseModel):
    year_number: int
    opening_balance: float
    contribution_this_year: float
    interest_earned_this_year: float
    closing_balance: float

class RuleOf72CalculatorResult(BaseModel):
    calculator_name: str = "Rule of 72, 114, and 144 Doubling Time Calculator"
    total_invested_or_principal: float
    total_interest_or_returns: float
    final_maturity_value: float
    wealth_multiplier: float
    effective_annual_yield_pct: float
    yearly_schedule: List[RuleOf72CalculatorYearBreakdown]

class RuleOf72CalculatorEngine:
    @classmethod
    def calculate(cls, inp: RuleOf72CalculatorInputs) -> RuleOf72CalculatorResult:
        r = (inp.annual_rate_pct / 100.0) / inp.frequency_per_year
        n_periods = int(inp.tenure_years * inp.frequency_per_year)
        
        curr_bal = 0.0
        tot_invested = 0.0
        yearly = []
        
        curr_contrib_per_period = inp.principal_amount
        years = int(math.ceil(inp.tenure_years))

        for yr in range(1, years + 1):
            yr_open = curr_bal
            yr_contrib = 0.0
            yr_int = 0.0
            
            for p in range(inp.frequency_per_year):
                curr_bal += curr_contrib_per_period
                yr_contrib += curr_contrib_per_period
                tot_invested += curr_contrib_per_period
                
                int_earned = curr_bal * r
                curr_bal += int_earned
                yr_int += int_earned

            yearly.append(RuleOf72CalculatorYearBreakdown(
                year_number=yr,
                opening_balance=round(yr_open, 2),
                contribution_this_year=round(yr_contrib, 2),
                interest_earned_this_year=round(yr_int, 2),
                closing_balance=round(curr_bal, 2)
            ))

            if inp.annual_step_up_pct and inp.annual_step_up_pct > 0:
                curr_contrib_per_period *= (1.0 + (inp.annual_step_up_pct / 100.0))

        tot_returns = max(0.0, curr_bal - tot_invested)
        mult = curr_bal / tot_invested if tot_invested > 0 else 1.0

        return RuleOf72CalculatorResult(
            total_invested_or_principal=round(tot_invested, 2),
            total_interest_or_returns=round(tot_returns, 2),
            final_maturity_value=round(curr_bal, 2),
            wealth_multiplier=round(mult, 2),
            effective_annual_yield_pct=round(inp.annual_rate_pct, 2),
            yearly_schedule=yearly
        )
