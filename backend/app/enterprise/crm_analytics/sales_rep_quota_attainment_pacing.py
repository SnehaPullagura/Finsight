from datetime import date
from typing import Any, Dict, List, Optional

class QuotaAttainmentPacingModeler:
    @staticmethod
    def calculate_pacing_trajectory(
        quarter_quota: float,
        actual_closed_revenue: float,
        days_elapsed_in_quarter: int,
        total_days_in_quarter: int = 90
    ) -> Dict[str, Any]:
        expected_attainment_pct = round((days_elapsed_in_quarter / float(total_days_in_quarter)) * 100.0, 1)
        actual_attainment_pct = round((actual_closed_revenue / max(1.0, quarter_quota)) * 100.0, 1)
        pacing_index = round((actual_attainment_pct / max(0.1, expected_attainment_pct)) * 100.0, 1)

        projected_quarter_finish = round(actual_closed_revenue * (total_days_in_quarter / max(1, days_elapsed_in_quarter)), 2)

        return {
            "quarter_quota": quarter_quota,
            "actual_closed_revenue": actual_closed_revenue,
            "days_elapsed": days_elapsed_in_quarter,
            "expected_attainment_pct": expected_attainment_pct,
            "actual_attainment_pct": actual_attainment_pct,
            "pacing_index_pct": pacing_index,
            "projected_quarter_finish": projected_quarter_finish,
            "pacing_status": "Ahead of Plan" if pacing_index >= 110 else "On Pace" if pacing_index >= 90 else "Behind Pacing"
        }
