from typing import Any, Dict, List, Optional
from collections import defaultdict

class DealStageDurationMatrix:
    @staticmethod
    def analyze_stage_duration_trends(deals_history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        stage_durations = defaultdict(list)
        for h in deals_history:
            stg = h.get("stage_name", "Discovery")
            days = float(h.get("days_spent", 0.0))
            stage_durations[stg].append(days)

        results = []
        for stg, durations in stage_durations.items():
            avg_days = sum(durations) / float(len(durations)) if durations else 0.0
            med_days = sorted(durations)[len(durations) // 2] if durations else 0.0
            min_days = min(durations) if durations else 0.0
            max_days = max(durations) if durations else 0.0

            results.append({
                "stage": stg,
                "average_days_in_stage": round(avg_days, 1),
                "median_days": round(med_days, 1),
                "min_days": round(min_days, 1),
                "max_days": round(max_days, 1),
                "sample_deal_count": len(durations)
            })

        return results
