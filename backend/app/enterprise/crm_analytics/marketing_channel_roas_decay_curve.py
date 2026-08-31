from typing import Any, Dict, List, Optional

class ChannelROASDecayCurve:
    @staticmethod
    def calculate_spend_roas_decay(base_spend: float, base_roas: float, target_spend: float, decay_rate: float = 0.15) -> Dict[str, Any]:
        spend_multiplier = target_spend / max(1.0, base_spend)
        projected_roas = max(1.0, round(base_roas * (spend_multiplier ** (-decay_rate)), 2))
        projected_revenue = round(target_spend * projected_roas, 2)

        return {
            "base_monthly_spend": base_spend,
            "base_roas": base_roas,
            "simulated_monthly_spend": target_spend,
            "projected_roas": projected_roas,
            "projected_gross_revenue": projected_revenue,
            "is_roas_healthy": projected_roas >= 4.0
        }
