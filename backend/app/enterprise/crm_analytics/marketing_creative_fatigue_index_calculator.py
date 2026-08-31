from typing import Any, Dict, List, Optional

class CreativeFatigueIndexCalculator:
    @staticmethod
    def calculate_fatigue_index(
        frequency: float,
        ctr_decline_pct: float,
        cpm_increase_pct: float
    ) -> Dict[str, Any]:
        # Composite fatigue index: 0 - 100
        fatigue_score = min(100.0, (frequency * 10.0) + (ctr_decline_pct * 0.4) + (cpm_increase_pct * 0.3))
        rating = "Severe Audience Fatigue (> 70)" if fatigue_score >= 70 else "Moderate Fatigue (40 - 70)" if fatigue_score >= 40 else "Fresh Creative (< 40)"

        return {
            "audience_frequency": frequency,
            "ctr_decline_pct": ctr_decline_pct,
            "cpm_increase_pct": cpm_increase_pct,
            "creative_fatigue_score": round(fatigue_score, 1),
            "fatigue_tier": rating,
            "is_creative_burnout_imminent": fatigue_score >= 60.0
        }
