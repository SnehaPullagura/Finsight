from typing import Any, Dict, List, Optional

class NetRevenueRetentionAnalyzer:
    @staticmethod
    def calculate_nrr_waterfall(
        beginning_arr: float,
        expansion_arr: float,
        contraction_arr: float,
        churn_arr: float
    ) -> Dict[str, Any]:
        ending_arr = beginning_arr + expansion_arr - contraction_arr - churn_arr
        nrr_pct = round((ending_arr / max(1.0, beginning_arr)) * 100.0, 1)
        gross_retention_pct = round(((beginning_arr - contraction_arr - churn_arr) / max(1.0, beginning_arr)) * 100.0, 1)

        return {
            "beginning_arr": beginning_arr,
            "expansion_arr": expansion_arr,
            "contraction_arr": contraction_arr,
            "churn_arr": churn_arr,
            "ending_arr": ending_arr,
            "net_revenue_retention_pct": nrr_pct,
            "gross_revenue_retention_pct": gross_retention_pct,
            "nrr_health": "World-Class Enterprise (> 120%)" if nrr_pct >= 120.0 else "Healthy (105% - 120%)" if nrr_pct >= 105.0 else "Leaky Bucket (< 100%)"
        }
