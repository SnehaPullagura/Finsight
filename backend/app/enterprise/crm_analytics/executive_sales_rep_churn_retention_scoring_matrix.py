from typing import Any, Dict, List, Optional
from collections import defaultdict

class RepRetentionScoringMatrix:
    @staticmethod
    def calculate_cohort_retention(reps_cohorts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for r in reps_cohorts:
            name = r.get("rep_name")
            starting_arr = float(r.get("closed_arr_baseline", 100000.0))
            retained_arr = float(r.get("retained_arr_12m", 90000.0))

            nrr_pct = round((retained_arr / max(1.0, starting_arr)) * 100.0, 1)
            tier = "World Class NRR (> 110%)" if nrr_pct >= 110.0 else "Solid Retention (95% - 110%)" if nrr_pct >= 95.0 else "Elevated Churn (< 95%)"

            results.append({
                "rep_name": name,
                "closed_arr_baseline": starting_arr,
                "retained_arr_12m": retained_arr,
                "cohort_nrr_percentage": nrr_pct,
                "quality_tier": tier,
                "eligible_for_retention_kicker": nrr_pct >= 105.0
            })

        return sorted(results, key=lambda x: x["cohort_nrr_percentage"], reverse=True)
