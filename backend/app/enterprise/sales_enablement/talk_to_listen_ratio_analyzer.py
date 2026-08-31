from typing import Any, Dict, List, Optional

class TalkToListenRatioAnalyzer:
    """
    Analyzes rep speech cadence:
    Optimal discovery call benchmark is 45% Rep Talk / 55% Customer Listen.
    """
    @staticmethod
    def calculate_cadence(
        rep_speaking_seconds: float,
        customer_speaking_seconds: float,
        silence_seconds: float = 0.0
    ) -> Dict[str, Any]:
        total_time = rep_speaking_seconds + customer_speaking_seconds + silence_seconds
        rep_ratio = round((rep_speaking_seconds / max(1.0, total_time)) * 100.0, 1)
        cust_ratio = round((customer_speaking_seconds / max(1.0, total_time)) * 100.0, 1)

        if rep_ratio <= 48.0:
            rating = "EXCELLENT_ACTIVE_LISTENING"
            coaching = "Superb active listening and question prompting."
        elif rep_ratio <= 60.0:
            rating = "BALANCED_ENGAGEMENT"
            coaching = "Solid conversational exchange; consider leaving more space after questions."
        else:
            rating = "OVER_TALKING_MONOLOGUE"
            coaching = "Rep spoke for majority of call; practice open-ended discovery probing."

        return {
            "rep_talk_percentage": rep_ratio,
            "customer_talk_percentage": cust_ratio,
            "total_call_duration_seconds": total_time,
            "cadence_rating": rating,
            "coaching_feedback": coaching
        }
