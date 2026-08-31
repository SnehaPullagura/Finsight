from datetime import date
from typing import Any, Dict, List, Optional

class OnboardingMilestoneTracker:
    @staticmethod
    def evaluate_onboarding_health(milestones: List[Dict[str, Any]], elapsed_days: int) -> Dict[str, Any]:
        total = len(milestones)
        completed = sum(1 for m in milestones if m.get("is_completed"))
        completion_pct = round((completed / max(1, total)) * 100.0, 1)

        # Expected milestone completion pacing
        expected_completed = min(total, int((elapsed_days / 30.0) * total))
        is_delayed = completed < expected_completed

        return {
            "total_milestones": total,
            "completed_milestones": completed,
            "completion_percentage": completion_pct,
            "elapsed_days": elapsed_days,
            "is_onboarding_delayed": is_delayed,
            "onboarding_status": "On Schedule" if not is_delayed else "Needs CSM Escalation"
        }
