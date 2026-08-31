from typing import Any, Dict, List, Optional

class DistributorVolumeRebateEngine:
    """
    End-of-Quarter Partner Volume Rebate Calculator based on tiered ARR achievement.
    """
    @staticmethod
    def calculate_quarterly_rebate(
        quarterly_revenue: float,
        target_quota: float
    ) -> Dict[str, Any]:
        attainment_pct = round((quarterly_revenue / max(1.0, target_quota)) * 100.0, 1)

        if attainment_pct >= 150.0:
            rebate_rate = 6.0
        elif attainment_pct >= 120.0:
            rebate_rate = 4.5
        elif attainment_pct >= 100.0:
            rebate_rate = 3.0
        elif attainment_pct >= 80.0:
            rebate_rate = 1.5
        else:
            rebate_rate = 0.0

        rebate_amount = round(quarterly_revenue * (rebate_rate / 100.0), 2)

        return {
            "quarterly_revenue": quarterly_revenue,
            "target_quota": target_quota,
            "quota_attainment_pct": attainment_pct,
            "rebate_multiplier_pct": rebate_rate,
            "rebate_payout_amount": rebate_amount,
            "accelerator_status": "SUPER_ATTAINMENT_BONUS" if attainment_pct >= 120.0 else "STANDARD_REBATE" if attainment_pct >= 100.0 else "BASE_OR_BELOW"
        }
