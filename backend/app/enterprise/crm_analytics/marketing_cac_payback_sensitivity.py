from typing import Any, Dict, List, Optional

class CACPaybackSensitivityModeler:
    @staticmethod
    def simulate_churn_sensitivity(
        base_cac: float,
        monthly_arpu: float,
        gross_margin_pct: float,
        churn_rates: List[float] = [0.5, 1.0, 1.5, 2.0, 2.5]
    ) -> List[Dict[str, Any]]:
        results = []
        gp = monthly_arpu * (gross_margin_pct / 100.0)

        for cr in churn_rates:
            payback = round(base_cac / max(1.0, gp), 1)
            ltv = round(gp / max(0.001, cr / 100.0), 2)
            ltv_cac = round(ltv / max(1.0, base_cac), 2)

            results.append({
                "monthly_churn_pct": cr,
                "gross_profit_per_customer": round(gp, 2),
                "payback_months": payback,
                "implied_ltv": ltv,
                "ltv_to_cac_ratio": ltv_cac,
                "economics_health": "Exceptional (> 5.0x)" if ltv_cac >= 5.0 else "Healthy (3.0x - 5.0x)" if ltv_cac >= 3.0 else "Vulnerable (< 3.0x)"
            })

        return results
