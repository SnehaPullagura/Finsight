from typing import Any, Dict, List, Optional

class SalesPipelineVelocityEquation:
    @staticmethod
    def compute_velocity(opportunities: int, win_rate_pct: float, avg_deal_size: float, cycle_length_days: float) -> Dict[str, Any]:
        win_rate = win_rate_pct / 100.0
        cycle = max(1.0, cycle_length_days)

        daily_rate = (opportunities * win_rate * avg_deal_size) / cycle
        monthly_rate = daily_rate * 30.0
        quarterly_rate = daily_rate * 90.0
        annual_rate = daily_rate * 365.0

        return {
            "opportunities_in_pipeline": opportunities,
            "win_rate_percentage": win_rate_pct,
            "average_deal_size": avg_deal_size,
            "sales_cycle_days": cycle_length_days,
            "daily_revenue_velocity": round(daily_rate, 2),
            "monthly_revenue_velocity": round(monthly_rate, 2),
            "quarterly_projected_velocity": round(quarterly_rate, 2),
            "annualized_velocity": round(annual_rate, 2)
        }
