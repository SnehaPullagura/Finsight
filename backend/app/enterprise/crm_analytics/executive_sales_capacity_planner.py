from typing import Any, Dict, List, Optional

class SalesCapacityPlanner:
    @staticmethod
    def plan_hiring_capacity(
        annual_revenue_target: float,
        ramped_rep_annual_quota: float,
        average_ramp_months: int,
        expected_annual_attrition_pct: float = 15.0
    ) -> Dict[str, Any]:
        base_reps_needed = annual_revenue_target / max(1.0, ramped_rep_annual_quota)
        attrition_buffer = base_reps_needed * (expected_annual_attrition_pct / 100.0)
        ramp_lag_multiplier = 1.0 + (average_ramp_months / 12.0)

        total_headcount_target = round((base_reps_needed + attrition_buffer) * ramp_lag_multiplier, 1)

        return {
            "annual_revenue_target": annual_revenue_target,
            "annual_quota_per_rep": ramped_rep_annual_quota,
            "base_ramped_reps_required": round(base_reps_needed, 1),
            "attrition_headcount_buffer": round(attrition_buffer, 1),
            "total_headcount_to_hire": total_headcount_target,
            "quarterly_hiring_cadence": [
                {"quarter": "Q1", "target_hires": int(total_headcount_target * 0.4)},
                {"quarter": "Q2", "target_hires": int(total_headcount_target * 0.3)},
                {"quarter": "Q3", "target_hires": int(total_headcount_target * 0.2)},
                {"quarter": "Q4", "target_hires": int(total_headcount_target * 0.1)}
            ]
        }
