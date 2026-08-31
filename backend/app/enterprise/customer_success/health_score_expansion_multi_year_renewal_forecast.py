from typing import Any, Dict, List, Optional

class MultiYearRenewalForecastModeler:
    @staticmethod
    def forecast_cohort_renewals(multi_year_contracts: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_contract_base = sum(float(c.get("annual_contract_value", 0.0)) for c in multi_year_contracts)
        weighted_renewals = sum(float(c.get("annual_contract_value", 0.0)) * (float(c.get("renewal_prob", 85.0)) / 100.0) for c in multi_year_contracts)

        renewal_rate_pct = round((weighted_renewals / max(1.0, total_contract_base)) * 100.0, 1)

        return {
            "contracts_evaluated": len(multi_year_contracts),
            "total_renewable_arr": round(total_contract_base, 2),
            "projected_renewed_arr": round(weighted_renewals, 2),
            "forecasted_gross_renewal_rate_pct": renewal_rate_pct,
            "forecast_confidence": "HIGH_CONFIDENCE (> 90%)" if renewal_rate_pct >= 90.0 else "MODERATE_RENEWAL_PACING"
        }
