from datetime import date, timedelta
from typing import Any, Dict, List, Optional

class SalesPipelineDecayAnalyzer:
    @staticmethod
    def calculate_opportunity_decay_rate(
        deal: Dict[str, Any],
        days_inactive: int,
        half_life_days: float = 30.0
    ) -> Dict[str, Any]:
        val = float(deal.get("value", 0.0))
        prob = float(deal.get("probability", 50.0))

        # Exponential probability decay: P(t) = P0 * (0.5 ^ (t / half_life))
        decay_factor = 0.5 ** (days_inactive / float(half_life_days))
        decayed_probability = round(prob * decay_factor, 1)
        decayed_weighted_value = round(val * (decayed_probability / 100.0), 2)

        return {
            "deal_id": deal.get("id"),
            "deal_name": deal.get("name"),
            "original_probability": prob,
            "days_inactive": days_inactive,
            "decayed_probability": decayed_probability,
            "decayed_weighted_value": decayed_weighted_value,
            "is_heavily_decayed": decayed_probability < (prob * 0.5)
        }
