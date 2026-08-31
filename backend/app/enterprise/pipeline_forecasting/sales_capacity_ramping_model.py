from typing import Any, Dict, List, Optional

class SalesCapacityRampingModel:
    """
    Simulates annual sales team capacity ramping (Month 1: 0%, Month 2: 25%, Month 3: 50%, Month 4: 75%, Month 5+: 100%).
    """
    @staticmethod
    def forecast_team_capacity(
        reps_tenure_months: List[int],
        annual_quota_per_fully_ramped_rep: float = 1000000.0
    ) -> Dict[str, Any]:
        monthly_quota = annual_quota_per_fully_ramped_rep / 12.0
        total_effective_reps = 0.0

        for t in reps_tenure_months:
            if t <= 1:
                eff = 0.0
            elif t == 2:
                eff = 0.25
            elif t == 3:
                eff = 0.50
            elif t == 4:
                eff = 0.75
            else:
                eff = 1.0
            total_effective_reps += eff

        projected_monthly_capacity = round(total_effective_reps * monthly_quota, 2)
        annualized_runway = round(projected_monthly_capacity * 12.0, 2)

        return {
            "total_headcount": len(reps_tenure_months),
            "effective_ramped_headcount": round(total_effective_reps, 2),
            "fully_ramped_ratio_pct": round((total_effective_reps / max(1, len(reps_tenure_months))) * 100.0, 1),
            "projected_monthly_quota_capacity": projected_monthly_capacity,
            "annualized_quota_capacity": annualized_runway
        }
