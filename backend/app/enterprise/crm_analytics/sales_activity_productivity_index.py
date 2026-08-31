from typing import Any, Dict, List, Optional

class SalesActivityProductivityIndex:
    ACTIVITY_WEIGHTS = {
        "meeting": 10.0,
        "call": 3.0,
        "email": 1.0,
        "proposal_sent": 15.0,
        "contract_sent": 25.0
    }

    @staticmethod
    def calculate_rep_productivity(rep_activities: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_points = 0.0
        breakdown = {k: 0 for k in SalesActivityProductivityIndex.ACTIVITY_WEIGHTS.keys()}

        for act in rep_activities:
            atype = (act.get("activity_type") or "email").lower()
            weight = SalesActivityProductivityIndex.ACTIVITY_WEIGHTS.get(atype, 1.0)
            total_points += weight
            if atype in breakdown:
                breakdown[atype] += 1

        # Benchmark: 100 points per week is target productivity
        target = 100.0
        productivity_index = round((total_points / target) * 100.0, 1)

        return {
            "total_productivity_points": round(total_points, 1),
            "target_productivity_points": target,
            "productivity_index_pct": productivity_index,
            "activity_counts": breakdown,
            "rating": "High Performer" if productivity_index >= 120 else "On Track" if productivity_index >= 90 else "Underperforming"
        }
