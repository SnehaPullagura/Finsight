from typing import Any, Dict, List, Optional

class RepHiringPaybackSchedule:
    @staticmethod
    def generate_monthly_payback_curve(monthly_cost: float, monthly_margin_ramp: List[float]) -> List[Dict[str, Any]]:
        curve = []
        cumulative_cost = 0.0
        cumulative_margin = 0.0

        for m, margin in enumerate(monthly_margin_ramp, start=1):
            cumulative_cost += monthly_cost
            cumulative_margin += margin
            net = cumulative_margin - cumulative_cost

            curve.append({
                "month": m,
                "cumulative_cost": round(cumulative_cost, 2),
                "cumulative_margin": round(cumulative_margin, 2),
                "net_profit_loss": round(net, 2),
                "is_profitable": net >= 0
            })

        return curve
