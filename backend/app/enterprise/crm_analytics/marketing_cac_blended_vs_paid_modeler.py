from typing import Any, Dict, List, Optional

class CACBlendedVsPaidModeler:
    @staticmethod
    def calculate_cac_ratios(
        paid_marketing_spend: float,
        salaries_and_overhead: float,
        paid_customers_acquired: int,
        organic_customers_acquired: int
    ) -> Dict[str, Any]:
        total_customers = paid_customers_acquired + organic_customers_acquired
        total_acquisition_cost = paid_marketing_spend + salaries_and_overhead

        paid_cac = round(paid_marketing_spend / max(1, paid_customers_acquired), 2)
        blended_cac = round(total_acquisition_cost / max(1, total_customers), 2)
        organic_acquisition_pct = round((organic_customers_acquired / max(1, total_customers)) * 100.0, 1)

        return {
            "paid_marketing_spend": paid_marketing_spend,
            "fully_loaded_acquisition_cost": total_acquisition_cost,
            "paid_customers_acquired": paid_customers_acquired,
            "organic_customers_acquired": organic_customers_acquired,
            "total_customers_acquired": total_customers,
            "paid_customer_acquisition_cost": paid_cac,
            "blended_customer_acquisition_cost": blended_cac,
            "organic_acquisition_percentage": organic_acquisition_pct,
            "organic_leverage_rating": "High Organic Engine (> 40%)" if organic_acquisition_pct >= 40.0 else "Paid-Dependent (< 20%)" if organic_acquisition_pct <= 20.0 else "Balanced Acquisition"
        }
