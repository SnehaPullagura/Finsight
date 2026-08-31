from typing import Any, Dict, List, Optional

class RepRampVelocityModeler:
    @staticmethod
    def calculate_expected_ramp_quota(base_monthly_quota: float, months_tenured: int, full_ramp_months: int = 4) -> Dict[str, Any]:
        ramp_pct = min(1.0, float(months_tenured) / max(1.0, float(full_ramp_months)))
        expected_quota = round(base_monthly_quota * ramp_pct, 2)

        return {
            "full_quota_target": base_monthly_quota,
            "months_tenured": months_tenured,
            "full_ramp_months": full_ramp_months,
            "ramp_attainment_pct": round(ramp_pct * 100.0, 1),
            "expected_ramped_quota": expected_quota,
            "is_fully_ramped": months_tenured >= full_ramp_months
        }
