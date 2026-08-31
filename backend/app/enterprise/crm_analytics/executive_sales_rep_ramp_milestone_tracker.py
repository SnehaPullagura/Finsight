from datetime import date
from typing import Any, Dict, List, Optional

class RepRampMilestoneTracker:
    @staticmethod
    def audit_onboarding_milestones(reps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for r in reps:
            name = r.get("rep_name")
            tenure_months = int(r.get("tenure_months", 1))
            first_deal_closed = bool(r.get("first_deal_closed", False))
            pipeline_built = float(r.get("pipeline_dollars_built", 0.0))

            if tenure_months <= 3:
                expected_pipeline = 100000.0
            elif tenure_months <= 6:
                expected_pipeline = 300000.0
            else:
                expected_pipeline = 600000.0

            pacing_pct = round((pipeline_built / max(1.0, expected_pipeline)) * 100.0, 1)

            results.append({
                "rep_name": name,
                "tenure_months": tenure_months,
                "first_deal_closed": first_deal_closed,
                "pipeline_built": pipeline_built,
                "expected_pipeline_benchmark": expected_pipeline,
                "ramp_pacing_percentage": pacing_pct,
                "ramp_status": "Ahead of Schedule" if pacing_pct >= 120.0 else "On Track" if pacing_pct >= 90.0 else "Needs Ramp Coaching"
            })

        return sorted(results, key=lambda x: x["ramp_pacing_percentage"], reverse=True)
