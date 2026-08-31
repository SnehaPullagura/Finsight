import datetime
from typing import List, Dict
from pydantic import BaseModel

class AdvanceTaxQuarter(BaseModel):
    quarter_name: str
    due_date: str
    cumulative_percentage_required: float
    cumulative_tax_due: float
    incremental_installment: float
    interest_section_234c: float

class AdvanceTaxScheduleResult(BaseModel):
    estimated_annual_tax_liability: float
    is_advance_tax_applicable: bool # Required if liability > Rs. 10,000
    quarters: List[AdvanceTaxQuarter]
    total_penalty_interest_estimated: float

class AdvanceTaxCalculatorEngine:
    """
    Quarterly Advance Tax Schedule Generator (Section 208, 234B, 234C of Income Tax Act 1961).
    """
    @staticmethod
    def calculate_schedule(estimated_tax: float, tds_tcs_already_deducted: float = 0.0) -> AdvanceTaxScheduleResult:
        net_liability = max(0.0, estimated_tax - tds_tcs_already_deducted)
        is_applicable = net_liability >= 10000.0

        if not is_applicable:
            return AdvanceTaxScheduleResult(
                estimated_annual_tax_liability=net_liability,
                is_advance_tax_applicable=False,
                quarters=[],
                total_penalty_interest_estimated=0.0
            )

        # 4 Statutory Quarters
        q_specs = [
            ("Q1 (15% by 15th June)", "15-Jun-2026", 0.15),
            ("Q2 (45% by 15th September)", "15-Sep-2026", 0.45),
            ("Q3 (75% by 15th December)", "15-Dec-2026", 0.75),
            ("Q4 (100% by 15th March)", "15-Mar-2027", 1.00)
        ]

        quarters: List[AdvanceTaxQuarter] = []
        prev_cum = 0.0
        for name, due, pct in q_specs:
            cum_due = net_liability * pct
            inc = cum_due - prev_cum
            quarters.append(AdvanceTaxQuarter(
                quarter_name=name,
                due_date=due,
                cumulative_percentage_required=round(pct * 100, 0),
                cumulative_tax_due=round(cum_due, 2),
                incremental_installment=round(inc, 2),
                interest_section_234c=0.0
            ))
            prev_cum = cum_due

        return AdvanceTaxScheduleResult(
            estimated_annual_tax_liability=round(net_liability, 2),
            is_advance_tax_applicable=True,
            quarters=quarters,
            total_penalty_interest_estimated=0.0
        )
