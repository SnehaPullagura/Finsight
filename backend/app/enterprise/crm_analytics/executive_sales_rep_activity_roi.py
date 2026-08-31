from typing import Any, Dict, List, Optional

class RepActivityROIAnalyzer:
    @staticmethod
    def calculate_activity_effectiveness(reps_activities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for r in reps_activities:
            name = r.get("rep_name")
            calls = int(r.get("calls_completed", 0))
            demos = int(r.get("demos_conducted", 0))
            emails = int(r.get("emails_sent", 0))
            won_rev = float(r.get("closed_won_revenue", 0.0))

            total_activities = calls + demos + emails
            rev_per_activity = round(won_rev / max(1, total_activities), 2)
            demo_to_won_rate = round((int(r.get("deals_won_count", 0)) / max(1, demos)) * 100.0, 1)

            results.append({
                "rep_name": name,
                "total_sales_activities": total_activities,
                "closed_won_revenue": won_rev,
                "revenue_per_activity": rev_per_activity,
                "demo_to_won_conversion_pct": demo_to_won_rate,
                "efficiency_tier": "High Leverage" if rev_per_activity >= 500.0 else "Solid Contributor" if rev_per_activity >= 250.0 else "High Volume / Low Conversion"
            })

        return sorted(results, key=lambda x: x["revenue_per_activity"], reverse=True)
