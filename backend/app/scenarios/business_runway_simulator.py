import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel

class BusinessRunwayInputs(BaseModel):
    current_cash_balance: float
    monthly_recurring_revenue: float
    monthly_mrr_growth_rate_pct: float = 5.0
    monthly_fixed_costs: float # Payroll, office, servers
    variable_cost_ratio_pct: float = 20.0 # COGS % of revenue
    planned_hiring_monthly_cost: float = 0.0
    one_time_capital_expenditure: float = 0.0

class RunwayMonthPoint(BaseModel):
    month_number: int
    date: str
    revenue: float
    expenses: float
    net_burn: float
    ending_cash: float
    is_cash_positive: bool

class BusinessRunwayResult(BaseModel):
    runway_months: int
    zero_cash_date: Optional[str]
    default_alive: bool
    current_monthly_burn_rate: float
    projected_profitable_month: Optional[int]
    total_cash_cushion: float
    timeline: List[RunwayMonthPoint]

class SmallBusinessRunwaySimulator:
    """
    SME & Startup Cash Runway and Default Alive/Dead Simulator.
    Models compound revenue growth, variable cost scaling, and payroll expansions.
    """
    @classmethod
    def simulate(cls, inp: BusinessRunwayInputs) -> BusinessRunwayResult:
        cash = inp.current_cash_balance - inp.one_time_capital_expenditure
        rev = inp.monthly_recurring_revenue
        today = datetime.date.today()
        
        timeline: List[RunwayMonthPoint] = []
        zero_date = None
        profit_mo = None
        months_alive = 0

        for m in range(1, 37): # 36-month simulation horizon
            mo_date = today + datetime.timedelta(days=m * 30)
            cogs = rev * (inp.variable_cost_ratio_pct / 100.0)
            exp = inp.monthly_fixed_costs + inp.planned_hiring_monthly_cost + cogs
            net = rev - exp
            cash += net

            if net >= 0 and profit_mo is None:
                profit_mo = m

            if cash <= 0 and zero_date is None:
                zero_date = mo_date.strftime("%B %Y")
                cash = 0.0
            elif cash > 0:
                months_alive = m

            timeline.append(RunwayMonthPoint(
                month_number=m,
                date=mo_date.strftime("%Y-%m"),
                revenue=round(rev, 2),
                expenses=round(exp, 2),
                net_burn=round(abs(net) if net < 0 else 0.0, 2),
                ending_cash=round(max(0.0, cash), 2),
                is_cash_positive=net >= 0
            ))

            rev *= (1.0 + (inp.monthly_mrr_growth_rate_pct / 100.0))

        is_default_alive = profit_mo is not None and (zero_date is None or profit_mo <= months_alive)
        current_burn = max(0.0, (inp.monthly_fixed_costs + (inp.monthly_recurring_revenue * inp.variable_cost_ratio_pct / 100.0)) - inp.monthly_recurring_revenue)

        return BusinessRunwayResult(
            runway_months=months_alive if zero_date is not None else 36,
            zero_cash_date=zero_date,
            default_alive=is_default_alive,
            current_monthly_burn_rate=round(current_burn, 2),
            projected_profitable_month=profit_mo,
            total_cash_cushion=round(inp.current_cash_balance, 2),
            timeline=timeline
        )
