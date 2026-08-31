from typing import Any, Dict, List, Optional

class MarketingElasticityModeler:
    @staticmethod
    def calculate_spend_elasticity(
        spend_change_pct: float,
        lead_volume_change_pct: float
    ) -> Dict[str, Any]:
        elasticity_coefficient = round(lead_volume_change_pct / max(0.01, spend_change_pct), 2)

        tier = "Elastic / Highly Scalable (> 1.0)" if elasticity_coefficient >= 1.0 else "Inelastic / Diminishing Scale (0.5 - 1.0)" if elasticity_coefficient >= 0.5 else "Highly Inelastic / Saturated (< 0.5)"

        return {
            "spend_change_percentage": spend_change_pct,
            "lead_volume_change_percentage": lead_volume_change_pct,
            "elasticity_coefficient": elasticity_coefficient,
            "channel_scale_readiness": tier,
            "is_spend_expansion_recommended": elasticity_coefficient >= 0.8
        }
