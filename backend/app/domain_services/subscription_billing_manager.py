from datetime import date, timedelta
from typing import Any, Dict, List, Optional

class SubscriptionBillingManager:
    @staticmethod
    def calculate_mrr_waterfall(
        starting_mrr: float,
        new_customer_mrr: float,
        expansion_mrr: float,
        contraction_mrr: float,
        churned_mrr: float
    ) -> Dict[str, float]:
        net_new_mrr = round(new_customer_mrr + expansion_mrr - contraction_mrr - churned_mrr, 2)
        ending_mrr = round(starting_mrr + net_new_mrr, 2)
        growth_rate_pct = round((net_new_mrr / max(1.0, starting_mrr)) * 100.0, 2)
        gross_revenue_retention = round(((starting_mrr - contraction_mrr - churned_mrr) / max(1.0, starting_mrr)) * 100.0, 2)
        net_revenue_retention = round(((starting_mrr + expansion_mrr - contraction_mrr - churned_mrr) / max(1.0, starting_mrr)) * 100.0, 2)

        return {
            "starting_mrr": starting_mrr,
            "new_customer_mrr": new_customer_mrr,
            "expansion_mrr": expansion_mrr,
            "contraction_mrr": contraction_mrr,
            "churned_mrr": churned_mrr,
            "net_new_mrr": net_new_mrr,
            "ending_mrr": ending_mrr,
            "ending_arr": round(ending_mrr * 12.0, 2),
            "monthly_growth_rate_pct": growth_rate_pct,
            "gross_revenue_retention_pct": max(0.0, gross_revenue_retention),
            "net_revenue_retention_pct": net_revenue_retention
        }
