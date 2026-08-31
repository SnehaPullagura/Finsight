from typing import Any, Dict, List, Optional

class RepHiringIRRCalculator:
    @staticmethod
    def calculate_sales_capacity_irr(
        initial_onboarding_investment: float,
        annual_cash_margin_stream: List[float]
    ) -> Dict[str, Any]:
        total_inflow = sum(annual_cash_margin_stream)
        net_gain = total_inflow - initial_onboarding_investment
        roi_multiple = round(total_inflow / max(1.0, initial_onboarding_investment), 2)
        annualized_yield_pct = round((net_gain / max(1.0, initial_onboarding_investment) / max(1, len(annual_cash_margin_stream))) * 100.0, 1)

        return {
            "initial_investment_cost": initial_onboarding_investment,
            "cash_inflow_stream": annual_cash_margin_stream,
            "total_gross_margin_inflow": round(total_inflow, 2),
            "net_capacity_profit": round(net_gain, 2),
            "capacity_roi_multiple": roi_multiple,
            "annualized_hiring_irr_pct": annualized_yield_pct,
            "hiring_verdict": "High Return Investment (> 100% IRR)" if annualized_yield_pct >= 100.0 else "Solid Return (50% - 100%)"
        }
