import math
from typing import Any, Dict, List, Optional

class LogisticChurnPredictor:
    # Feature weights: [logins_normalized, tickets_normalized, nps_normalized, overdue_invoices]
    WEIGHTS = [-2.5, 1.8, -1.2, 2.2]
    BIAS = 0.5

    @staticmethod
    def predict_churn_probability(
        logins_per_user_per_week: float, # 0 - 20
        open_tickets_count: int,          # 0 - 10
        nps_rating: int,                  # 0 - 10
        has_overdue_invoices: bool
    ) -> Dict[str, Any]:
        # Normalize features to 0-1
        f1 = min(1.0, logins_per_user_per_week / 10.0)
        f2 = min(1.0, open_tickets_count / 5.0)
        f3 = min(1.0, nps_rating / 10.0)
        f4 = 1.0 if has_overdue_invoices else 0.0

        z = (f1 * LogisticChurnPredictor.WEIGHTS[0]) +             (f2 * LogisticChurnPredictor.WEIGHTS[1]) +             (f3 * LogisticChurnPredictor.WEIGHTS[2]) +             (f4 * LogisticChurnPredictor.WEIGHTS[3]) +             LogisticChurnPredictor.BIAS

        prob = 1.0 / (1.0 + math.exp(-z))
        prob_pct = round(prob * 100.0, 1)

        tier = "Critical" if prob_pct >= 70 else "High" if prob_pct >= 40 else "Low"

        return {
            "churn_probability": round(prob, 4),
            "churn_probability_percentage": prob_pct,
            "risk_tier": tier,
            "is_action_required": prob_pct >= 40.0
        }
