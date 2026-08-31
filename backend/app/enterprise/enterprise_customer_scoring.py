from typing import Any, Dict, List, Optional

class EnterpriseCustomerScoringEngine:
    @staticmethod
    def compute_composite_health_matrix(
        usage_intensity_score: float,   # 0 - 100
        support_satisfaction_score: float, # 0 - 100
        billing_health_score: float,    # 0 - 100
        relationship_score: float       # 0 - 100
    ) -> Dict[str, Any]:
        # Weighted composite: 40% usage, 25% support, 20% relationship, 15% billing
        composite = (usage_intensity_score * 0.40) + (support_satisfaction_score * 0.25) + (relationship_score * 0.20) + (billing_health_score * 0.15)
        final_score = round(max(0.0, min(100.0, composite)), 1)

        tier = "Champion" if final_score >= 85 else "Healthy" if final_score >= 70 else "At Risk" if final_score >= 50 else "Critical"

        return {
            "composite_health_score": final_score,
            "health_tier": tier,
            "components": {
                "usage_intensity": usage_intensity_score,
                "support_satisfaction": support_satisfaction_score,
                "relationship_health": relationship_score,
                "billing_compliance": billing_health_score
            },
            "requires_intervention": final_score < 70
        }
