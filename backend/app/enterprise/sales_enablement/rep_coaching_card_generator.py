from typing import Any, Dict, List, Optional

class RepCoachingCardGenerator:
    """
    Synthesizes multi-call data into automated weekly rep coaching cards.
    """
    @staticmethod
    def generate_coaching_card(
        rep_name: str,
        calls_analyzed: int,
        avg_talk_ratio: float,
        objection_resolution_rate_pct: float,
        next_steps_secured_pct: float
    ) -> Dict[str, Any]:
        strengths = []
        areas_for_growth = []

        if avg_talk_ratio <= 50.0:
            strengths.append("Exceptional active listening and discovery questioning.")
        else:
            areas_for_growth.append("Reduce talk time below 50% on initial discovery calls.")

        if objection_resolution_rate_pct >= 75.0:
            strengths.append("High-confidence handling of competitive pricing pushback.")
        else:
            areas_for_growth.append("Leverage ROI Battlecard when responding to budget constraints.")

        if next_steps_secured_pct >= 85.0:
            strengths.append("Consistent closing of calendar commitments on every call.")
        else:
            areas_for_growth.append("Reserve 5 minutes at end of call to schedule technical demo.")

        overall_grade = "A" if len(strengths) >= 2 and len(areas_for_growth) <= 1 else "B" if len(strengths) >= 1 else "C"

        return {
            "rep_name": rep_name,
            "calls_analyzed_count": calls_analyzed,
            "coaching_grade": overall_grade,
            "key_strengths": strengths,
            "prescribed_micro_learning": areas_for_growth,
            "recommended_curriculum_module": "Advanced Discovery & Executive Storytelling Masterclass"
        }
