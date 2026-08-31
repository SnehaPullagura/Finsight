from typing import Any, Dict, List, Optional

class BuyerIntentScorecard:
    """
    Aggregates multi-session buyer signals across DSR, document downloads,
    pricing page visits, and email link clicks into a unified intent index (0 - 100).
    """
    @staticmethod
    def calculate_intent_index(
        dsr_time_minutes: float,
        proposals_downloaded: int,
        security_whitepapers_viewed: int,
        pricing_calculator_interactions: int
    ) -> Dict[str, Any]:
        score = 0
        if dsr_time_minutes >= 30:
            score += 35
        elif dsr_time_minutes >= 10:
            score += 20
        else:
            score += 5

        score += min(25, proposals_downloaded * 10)
        score += min(20, security_whitepapers_viewed * 10)
        score += min(20, pricing_calculator_interactions * 5)

        final_score = min(100, score)

        return {
            "buyer_intent_score": final_score,
            "buying_stage": "DECISION_READY (HOT)" if final_score >= 75 else "EVALUATION_ACTIVE (WARM)" if final_score >= 45 else "EARLY_DISCOVERY (COLD)",
            "is_contract_send_recommended": final_score >= 70,
            "buyer_engagement_summary": f"{round(dsr_time_minutes, 1)}m spent in DSR, {proposals_downloaded} proposals viewed, {security_whitepapers_viewed} security docs downloaded."
        }
