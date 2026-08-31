from datetime import date
from typing import Any, Dict, List, Optional

class MutualActionPlanTracker:
    """
    Mutual Action Plan (MAP) / Joint Evaluation Framework:
    Synchronizes buyer and seller milestone commitments (Security Review, Tech Sandbox, Legal Redlines, Go-Live).
    """
    @staticmethod
    def evaluate_map_milestones(milestones: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_count = len(milestones)
        completed = [m for m in milestones if m.get("is_completed", False)]
        overdue = [m for m in milestones if not m.get("is_completed", False) and m.get("is_overdue", False)]

        progress_pct = round((len(completed) / max(1, total_count)) * 100.0, 1)

        return {
            "total_milestones": total_count,
            "completed_milestones_count": len(completed),
            "overdue_milestones_count": len(overdue),
            "progress_percentage": progress_pct,
            "deal_execution_health": "ON_SCHEDULE" if not overdue else "RISK_OF_SLIPPAGE",
            "overdue_milestone_titles": [m.get("title") for m in overdue]
        }
