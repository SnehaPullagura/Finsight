import math
from typing import Any, Dict, List, Optional

class MarketingDiminishingReturnsModeler:
    @staticmethod
    def calculate_marginal_cac(current_spend: float, marginal_spend_increase: float, saturation_ceiling: float = 100000.0) -> Dict[str, Any]:
        # Logarithmic saturation model
        def customers_from_spend(spend):
            return saturation_ceiling * (1.0 - math.exp(-spend / max(1.0, saturation_ceiling)))

        base_customers = customers_from_spend(current_spend)
        incremental_customers = customers_from_spend(current_spend + marginal_spend_increase)
        new_customers_added = max(0.01, incremental_customers - base_customers)

        marginal_cac = round(marginal_spend_increase / new_customers_added, 2)
        base_cac = round(current_spend / max(0.01, base_customers), 2)
        cac_inflation_pct = round(((marginal_cac - base_cac) / max(1.0, base_cac)) * 100.0, 1)

        return {
            "current_monthly_spend": current_spend,
            "incremental_spend_tested": marginal_spend_increase,
            "baseline_cac": base_cac,
            "marginal_incremental_cac": marginal_cac,
            "cac_inflation_percentage": cac_inflation_pct,
            "saturation_status": "Near Saturation (High CAC Inflation)" if cac_inflation_pct >= 50.0 else "Healthy Scale" if cac_inflation_pct >= 15.0 else "Underspent / High Margin"
        }
