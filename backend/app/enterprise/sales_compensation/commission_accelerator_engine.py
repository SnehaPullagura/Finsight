from typing import Any, Dict, List, Optional

class CommissionAcceleratorEngine:
    @staticmethod
    def calculate_progressive_commission(
        quota: float,
        actual_revenue: float,
        base_rate: float = 0.10
    ) -> Dict[str, Any]:
        attainment_pct = (actual_revenue / max(1.0, quota)) * 100.0

        # Tier 1: 0 - 100% (1.0x accelerator)
        tier1_rev = min(actual_revenue, quota)
        tier1_payout = tier1_rev * base_rate * 1.0

        # Tier 2: 100% - 125% (1.5x accelerator)
        tier2_rev = max(0.0, min(actual_revenue - quota, quota * 0.25))
        tier2_payout = tier2_rev * base_rate * 1.5

        # Tier 3: 125%+ (2.0x accelerator)
        tier3_rev = max(0.0, actual_revenue - (quota * 1.25))
        tier3_payout = tier3_rev * base_rate * 2.0

        total_commission = tier1_payout + tier2_payout + tier3_payout
        effective_rate = (total_commission / max(1.0, actual_revenue)) * 100.0

        return {
            "quota": quota,
            "actual_revenue": actual_revenue,
            "attainment_percentage": round(attainment_pct, 2),
            "tier1_payout": round(tier1_payout, 2),
            "tier2_payout": round(tier2_payout, 2),
            "tier3_payout": round(tier3_payout, 2),
            "total_commission_earned": round(total_commission, 2),
            "effective_commission_rate_pct": round(effective_rate, 2),
            "is_accelerator_unlocked": attainment_pct > 100.0
        }
