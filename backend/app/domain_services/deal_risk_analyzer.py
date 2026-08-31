from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

class DealRiskAnalyzer:
    @staticmethod
    def evaluate_deal_health(
        deal: Dict[str, Any],
        recent_activities: List[Dict[str, Any]],
        days_in_stage: int,
        stage_sla_days: int = 14
    ) -> Dict[str, Any]:
        risk_signals = []
        health_score = 100

        # 1. Stage SLA Stagnation
        if days_in_stage > stage_sla_days:
            stagnation_days = days_in_stage - stage_sla_days
            penalty = min(35, stagnation_days * 3)
            health_score -= penalty
            risk_signals.append(f"Deal stalled in current stage for {days_in_stage} days (SLA: {stage_sla_days} days)")

        # 2. Activity Recency
        if not recent_activities:
            health_score -= 30
            risk_signals.append("Zero logged customer touchpoints or meetings in the last 14 days")
        else:
            last_activity = recent_activities[0]
            # Check for negative sentiment keywords
            desc = (last_activity.get("description") or "").lower()
            if any(k in desc for k in ["budget cut", "delayed", "evaluating competitor", "freeze", "push to next quarter"]):
                health_score -= 25
                risk_signals.append("Risk signals identified in customer communication notes")

        final_score = max(0, min(100, health_score))
        risk_level = "low" if final_score >= 75 else "medium" if final_score >= 45 else "high"

        return {
            "health_score": final_score,
            "risk_level": risk_level,
            "risk_signals": risk_signals,
            "recommended_next_action": "Schedule executive alignment call" if risk_level == "high" else "Send follow-up proposal review"
        }
