from typing import Any, Dict, List, Optional

class CreativeDecayLifecycleModeler:
    @staticmethod
    def calculate_creative_lifecycle(days_active: int, initial_ctr: float, current_ctr: float) -> Dict[str, Any]:
        fatigue_pct = round(((initial_ctr - current_ctr) / max(0.01, initial_ctr)) * 100.0, 1)

        stage = "Peak Performance (< 14d)" if days_active <= 14 else "Maturity / High Volume (14-45d)" if days_active <= 45 and fatigue_pct < 20 else "Fatigued / Replacement Needed (> 45d)"

        return {
            "days_active": days_active,
            "initial_ctr": initial_ctr,
            "current_ctr": current_ctr,
            "fatigue_percentage": fatigue_pct,
            "lifecycle_stage": stage,
            "requires_refresh": fatigue_pct >= 25.0 or days_active > 60
        }
