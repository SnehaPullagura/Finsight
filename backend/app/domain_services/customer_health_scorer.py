from typing import Dict, List, Optional

class CustomerHealthScorer:
    @staticmethod
    def calculate_health_score(
        login_frequency_weekly: int,
        active_user_ratio: float, # 0.0 - 1.0
        open_critical_tickets: int,
        feature_adoption_count: int,
        nps_score: Optional[int] = None
    ) -> Dict[str, Any]:
        score = 50 # Baseline midpoint

        # 1. Login Frequency (+/- 15 pts)
        if login_frequency_weekly >= 5:
            score += 15
        elif login_frequency_weekly >= 2:
            score += 5
        else:
            score -= 15

        # 2. Active User Ratio (+/- 20 pts)
        if active_user_ratio >= 0.80:
            score += 20
        elif active_user_ratio >= 0.50:
            score += 10
        elif active_user_ratio < 0.25:
            score -= 20

        # 3. Support Tickets (-10 per critical)
        score -= min(30, open_critical_tickets * 15)

        # 4. Feature Adoption (+/- 15 pts)
        score += min(15, feature_adoption_count * 3)

        # 5. NPS Score (+/- 10 pts)
        if nps_score is not None:
            if nps_score >= 9:
                score += 10
            elif nps_score <= 6:
                score -= 10

        final_score = max(0, min(100, score))

        if final_score >= 80:
            grade = "good"
            risk_level = "low"
        elif final_score >= 50:
            grade = "average"
            risk_level = "medium"
        else:
            grade = "poor"
            risk_level = "high"

        return {
            "health_score": final_score,
            "health_grade": grade,
            "churn_risk": risk_level,
            "metrics_breakdown": {
                "login_frequency": login_frequency_weekly,
                "active_user_ratio": active_user_ratio,
                "open_critical_tickets": open_critical_tickets,
                "feature_adoption": feature_adoption_count,
                "nps": nps_score
            }
        }
