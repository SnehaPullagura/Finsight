import math
from typing import Any, Dict, List, Optional

class EnterpriseCompensationCalculator:
    @staticmethod
    def calculate_rep_payout(
        rep_name: str,
        quota_target: float,
        closed_deals: List[Dict[str, Any]],
        base_commission_rate: float = 0.10,
        accelerator_tier_1: float = 1.0, # 0-100%
        accelerator_tier_2: float = 1.5, # 100-120%
        accelerator_tier_3: float = 2.0  # 120%+
    ) -> Dict[str, Any]:
        total_closed = sum(float(d.get("value", 0.0)) for d in closed_deals if d.get("status") == "won")
        attainment_pct = (total_closed / max(1.0, quota_target)) * 100.0

        commission_earned = 0.0

        # Tier 1: 0 - 100%
        tier_1_max = quota_target
        tier_1_attained = min(total_closed, tier_1_max)
        commission_earned += tier_1_attained * base_commission_rate * accelerator_tier_1

        # Tier 2: 100% - 120%
        if total_closed > quota_target:
            tier_2_max = quota_target * 1.20
            tier_2_attained = min(total_closed, tier_2_max) - quota_target
            commission_earned += tier_2_attained * base_commission_rate * accelerator_tier_2

        # Tier 3: 120%+
        if total_closed > quota_target * 1.20:
            tier_3_attained = total_closed - (quota_target * 1.20)
            commission_earned += tier_3_attained * base_commission_rate * accelerator_tier_3

        effective_rate = (commission_earned / max(1.0, total_closed)) * 100.0

        return {
            "rep_name": rep_name,
            "quota_target": quota_target,
            "total_closed_revenue": round(total_closed, 2),
            "attainment_percentage": round(attainment_pct, 2),
            "total_commission_payout": round(commission_earned, 2),
            "effective_commission_rate_pct": round(effective_rate, 2),
            "is_quota_achieved": attainment_pct >= 100.0
        }
