import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel

class RetirementPlanRequest(BaseModel):
    current_age: int
    target_retirement_age: int
    life_expectancy_age: int = 85
    current_monthly_expenses: float
    expected_inflation_pct: float = 6.0
    post_retirement_return_pct: float = 8.0
    pre_retirement_return_pct: float = 12.0
    existing_retirement_corpus: float = 0.0
    expected_pension_or_rental_monthly: float = 0.0

class RetirementYearProjection(BaseModel):
    year: int
    age: int
    annual_expense: float
    starting_corpus: float
    investment_growth: float
    annual_withdrawal: float
    ending_corpus: float
    is_exhausted: bool

class RetirementPlanResult(BaseModel):
    years_to_retirement: int
    years_in_retirement: int
    monthly_expense_at_retirement: float
    annual_expense_at_retirement: float
    total_required_retirement_corpus: float
    shortfall_amount: float
    required_monthly_sip_to_bridge_gap: float
    sustainable_withdrawal_rate_pct: float # Safe Withdrawal Rate (SWR)
    fire_number: float # Financial Independence Retire Early target (25x - 30x)
    lean_fire_number: float
    fat_fire_number: float
    yearly_projections: List[RetirementYearProjection]

class RetirementPlannerEngine:
    """
    FIRE (Financial Independence, Retire Early) and Traditional Retirement Planning Engine.
    Simulates inflation compounding, sequence-of-returns risk, and sustainable withdrawal rates.
    """
    @staticmethod
    def calculate_plan(req: RetirementPlanRequest) -> RetirementPlanResult:
        years_to_retire = max(1, req.target_retirement_age - req.current_age)
        years_in_retire = max(1, req.life_expectancy_age - req.target_retirement_age)
        
        inf_rate = req.expected_inflation_pct / 100.0
        pre_ret_rate = req.pre_retirement_return_pct / 100.0
        post_ret_rate = req.post_retirement_return_pct / 100.0

        # Expense compounded to retirement age
        monthly_exp_at_ret = req.current_monthly_expenses * ((1.0 + inf_rate) ** years_to_retire)
        annual_exp_at_ret = monthly_exp_at_ret * 12.0

        # Real rate of return post-retirement: r_real = (1 + r) / (1 + i) - 1
        real_post_rate = ((1.0 + post_ret_rate) / (1.0 + inf_rate)) - 1.0

        # Present value of annuity for retirement corpus:
        # PV = Expense * [1 - (1 + real_post_rate)^(-n)] / real_post_rate
        if abs(real_post_rate) > 0.0001:
            pv_corpus = annual_exp_at_ret * (1.0 - ((1.0 + real_post_rate) ** (-years_in_retire))) / real_post_rate
        else:
            pv_corpus = annual_exp_at_ret * years_in_retire

        # Adjust for future value of existing corpus
        fv_existing = req.existing_retirement_corpus * ((1.0 + pre_ret_rate) ** years_to_retire)
        corpus_shortfall = max(0.0, pv_corpus - fv_existing)

        # Monthly SIP to bridge gap:
        # FV_SIP = P * [((1+r_monthly)^m - 1) / r_monthly] * (1+r_monthly)
        r_monthly = pre_ret_rate / 12.0
        months = years_to_retire * 12
        if r_monthly > 0 and months > 0:
            annuity_factor = (((1.0 + r_monthly) ** months - 1.0) / r_monthly) * (1.0 + r_monthly)
            monthly_sip = corpus_shortfall / annuity_factor if annuity_factor > 0 else 0.0
        else:
            monthly_sip = corpus_shortfall / max(1, months)

        # SWR and FIRE Numbers
        fire_num = (req.current_monthly_expenses * 12.0) * 25.0
        lean_fire = fire_num * 0.75
        fat_fire = fire_num * 1.50
        swr = (annual_exp_at_ret / pv_corpus * 100.0) if pv_corpus > 0 else 4.0

        # Yearly Cash Flow Waterfall Projections
        projections: List[RetirementYearProjection] = []
        curr_corpus = pv_corpus
        curr_annual_exp = annual_exp_at_ret

        for yr in range(1, years_in_retire + 1):
            age = req.target_retirement_age + yr
            growth = curr_corpus * post_ret_rate
            withdrawal = min(curr_corpus + growth, curr_annual_exp)
            ending = max(0.0, curr_corpus + growth - withdrawal)
            exhausted = ending <= 0.0

            projections.append(RetirementYearProjection(
                year=yr,
                age=age,
                annual_expense=round(curr_annual_exp, 2),
                starting_corpus=round(curr_corpus, 2),
                investment_growth=round(growth, 2),
                annual_withdrawal=round(withdrawal, 2),
                ending_corpus=round(ending, 2),
                is_exhausted=exhausted
            ))

            curr_corpus = ending
            curr_annual_exp *= (1.0 + inf_rate)

        return RetirementPlanResult(
            years_to_retirement=years_to_retire,
            years_in_retirement=years_in_retire,
            monthly_expense_at_retirement=round(monthly_exp_at_ret, 2),
            annual_expense_at_retirement=round(annual_exp_at_ret, 2),
            total_required_retirement_corpus=round(pv_corpus, 2),
            shortfall_amount=round(corpus_shortfall, 2),
            required_monthly_sip_to_bridge_gap=round(monthly_sip, 2),
            sustainable_withdrawal_rate_pct=round(swr, 2),
            fire_number=round(fire_num, 2),
            lean_fire_number=round(lean_fire, 2),
            fat_fire_number=round(fat_fire, 2),
            yearly_projections=projections
        )
