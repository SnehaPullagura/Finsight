from typing import Any, Dict, List, Optional

class ExpansionPropensityScorer:
    @staticmethod
    def score_account_expansion(account: Dict[str, Any]) -> Dict[str, Any]:
        health = int(account.get("health_score", 50))
        nps = int(account.get("nps", 8))
        seat_util = float(account.get("seat_utilization_pct", 75.0))
        feature_depth = int(account.get("features_adopted_count", 5))

        # Composite score
        propensity = (health * 0.4) + (seat_util * 0.3) + (nps * 2.0) + (feature_depth * 2.0)
        final_score = min(100, int(propensity))

        tier = "High Expansion Propensity" if final_score >= 80 else "Moderate" if final_score >= 60 else "Low Readiness"

        return {
            "account_id": account.get("id"),
            "account_name": account.get("name"),
            "expansion_propensity_score": final_score,
            "readiness_tier": tier,
            "recommended_play": "Introduce Advanced Analytics & Add-On Modules" if final_score >= 80 else "Drive Daily User Adoption"
        }
