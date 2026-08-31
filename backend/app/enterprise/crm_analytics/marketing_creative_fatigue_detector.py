from typing import Any, Dict, List, Optional

class AdCreativeFatigueDetector:
    @staticmethod
    def evaluate_creative_fatigue(ad_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        if len(ad_history) < 2:
            return {"status": "insufficient_history"}

        ctr_initial = float(ad_history[0].get("ctr_pct", 2.5))
        ctr_current = float(ad_history[-1].get("ctr_pct", 2.5))
        cpa_initial = float(ad_history[0].get("cpa", 50.0))
        cpa_current = float(ad_history[-1].get("cpa", 50.0))

        ctr_drop_pct = round(((ctr_initial - ctr_current) / max(0.01, ctr_initial)) * 100.0, 1)
        cpa_increase_pct = round(((cpa_current - cpa_initial) / max(1.0, cpa_initial)) * 100.0, 1)

        is_fatigued = ctr_drop_pct >= 25.0 or cpa_increase_pct >= 30.0

        return {
            "initial_ctr": ctr_initial,
            "current_ctr": ctr_current,
            "ctr_drop_percentage": ctr_drop_pct,
            "cpa_increase_percentage": cpa_increase_pct,
            "is_creative_fatigued": is_fatigued,
            "action": "REFRESH_AD_CREATIVE_VARIANTS" if is_fatigued else "MAINTAIN_CURRENT_ROTATION"
        }
