from typing import Any, Dict, List, Optional

class RepRampPaybackModeler:
    @staticmethod
    def calculate_rep_cost_payback(
        base_salary: float,
        on_target_earnings: float,
        ramp_months: int,
        gross_margin_pct: float,
        average_deal_size: float,
        deals_closed_per_month_post_ramp: float
    ) -> Dict[str, Any]:
        fully_loaded_cost_during_ramp = (on_target_earnings / 12.0) * ramp_months
        monthly_gross_profit = (deals_closed_per_month_post_ramp * average_deal_size) * (gross_margin_pct / 100.0)

        payback_months = round(fully_loaded_cost_during_ramp / max(1.0, monthly_gross_profit), 1)

        return {
            "fully_loaded_ramp_investment": round(fully_loaded_cost_during_ramp, 2),
            "monthly_post_ramp_gross_profit": round(monthly_gross_profit, 2),
            "ramp_investment_payback_months": payback_months,
            "rep_roi_status": "Highly Productive (< 6 Mo)" if payback_months <= 6.0 else "Healthy (6-12 Mo)" if payback_months <= 12.0 else "Prolonged Payback (> 12 Mo)"
        }
