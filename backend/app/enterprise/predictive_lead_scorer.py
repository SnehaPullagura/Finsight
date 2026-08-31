import math
from typing import Any, Dict, List, Optional

class PredictiveLeadScorer:
    @staticmethod
    def score_lead(lead_profile: Dict[str, Any]) -> Dict[str, Any]:
        score = 20 # Baseline

        # Industry affinity
        industry = (lead_profile.get("industry") or "").lower()
        if industry in ["technology", "finance", "healthcare"]:
            score += 25
        elif industry in ["manufacturing", "retail"]:
            score += 15

        # Employee count
        employees = int(lead_profile.get("employee_count", 0))
        if employees >= 1000:
            score += 25
        elif employees >= 100:
            score += 15
        elif employees >= 20:
            score += 10

        # Budget estimate
        budget = float(lead_profile.get("estimated_budget", 0.0))
        if budget >= 100000:
            score += 20
        elif budget >= 25000:
            score += 10

        # Engagement signals
        views = int(lead_profile.get("page_views", 0))
        score += min(15, views * 2)

        final_score = max(0, min(100, score))
        grade = "A" if final_score >= 80 else "B" if final_score >= 60 else "C" if final_score >= 40 else "D"
        conversion_prob = round(1.0 / (1.0 + math.exp(-((final_score - 50) / 15.0))), 3)

        return {
            "lead_score": final_score,
            "qualification_grade": grade,
            "conversion_probability": conversion_prob,
            "is_sales_ready": final_score >= 70
        }
