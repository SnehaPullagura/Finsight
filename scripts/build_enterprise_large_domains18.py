import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/enterprise_pipeline_simulator.py
    write_file("backend/app/enterprise/enterprise_pipeline_simulator.py", """import math
import random
from typing import Any, Dict, List, Optional

class EnterprisePipelineSimulator:
    @staticmethod
    def simulate_quarter_outcomes(
        deals: List[Dict[str, Any]],
        trials: int = 1000,
        win_rate_adjustment: float = 1.0
    ) -> Dict[str, Any]:
        random.seed(42)
        total_revenues = []

        for _ in range(trials):
            trial_revenue = 0.0
            for d in deals:
                prob = min(1.0, (float(d.get("probability", 50)) / 100.0) * win_rate_adjustment)
                val = float(d.get("value", 0.0))
                if random.random() <= prob:
                    trial_revenue += val
            total_revenues.append(trial_revenue)

        total_revenues.sort()
        n = len(total_revenues)
        p10 = total_revenues[int(n * 0.10)]
        p25 = total_revenues[int(n * 0.25)]
        p50 = total_revenues[int(n * 0.50)]
        p75 = total_revenues[int(n * 0.75)]
        p90 = total_revenues[int(n * 0.90)]
        avg = sum(total_revenues) / float(n)

        return {
            "trials_count": trials,
            "mean_expected_revenue": round(avg, 2),
            "p10_bear_case": round(p10, 2),
            "p25_lower_quartile": round(p25, 2),
            "p50_median_case": round(p50, 2),
            "p75_upper_quartile": round(p75, 2),
            "p90_bull_case": round(p90, 2)
        }
""")

    # 2. backend/app/enterprise/enterprise_subscription_engine.py
    write_file("backend/app/enterprise/enterprise_subscription_engine.py", """from datetime import date, timedelta
from typing import Any, Dict, List, Optional

class EnterpriseSubscriptionEngine:
    @staticmethod
    def calculate_co_terming_schedule(
        base_subscription: Dict[str, Any],
        add_on_items: List[Dict[str, Any]],
        add_on_effective_date: date
    ) -> Dict[str, Any]:
        sub_end = date.fromisoformat(base_subscription.get("current_period_end", date.today().isoformat()))
        sub_start = date.fromisoformat(base_subscription.get("current_period_start", date.today().isoformat()))

        total_period_days = max(1, (sub_end - sub_start).days)
        proration_days = max(0, (sub_end - add_on_effective_date).days)
        proration_fraction = proration_days / float(total_period_days)

        calculated_items = []
        total_prorated_charge = 0.0

        for item in add_on_items:
            unit_price = float(item.get("unit_price", 0.0))
            qty = int(item.get("quantity", 1))
            full_price = unit_price * qty
            prorated = round(full_price * proration_fraction, 2)
            total_prorated_charge += prorated

            calculated_items.append({
                "item_name": item.get("name"),
                "quantity": qty,
                "full_price": full_price,
                "prorated_charge": prorated,
                "effective_days": proration_days
            })

        return {
            "subscription_id": base_subscription.get("id"),
            "effective_date": add_on_effective_date.isoformat(),
            "period_end": sub_end.isoformat(),
            "prorated_items": calculated_items,
            "immediate_total_due": round(total_prorated_charge, 2)
        }
""")

    # 3. backend/app/enterprise/enterprise_customer_scoring.py
    write_file("backend/app/enterprise/enterprise_customer_scoring.py", """from typing import Any, Dict, List, Optional

class EnterpriseCustomerScoringEngine:
    @staticmethod
    def compute_composite_health_matrix(
        usage_intensity_score: float,   # 0 - 100
        support_satisfaction_score: float, # 0 - 100
        billing_health_score: float,    # 0 - 100
        relationship_score: float       # 0 - 100
    ) -> Dict[str, Any]:
        # Weighted composite: 40% usage, 25% support, 20% relationship, 15% billing
        composite = (usage_intensity_score * 0.40) + (support_satisfaction_score * 0.25) + (relationship_score * 0.20) + (billing_health_score * 0.15)
        final_score = round(max(0.0, min(100.0, composite)), 1)

        tier = "Champion" if final_score >= 85 else "Healthy" if final_score >= 70 else "At Risk" if final_score >= 50 else "Critical"

        return {
            "composite_health_score": final_score,
            "health_tier": tier,
            "components": {
                "usage_intensity": usage_intensity_score,
                "support_satisfaction": support_satisfaction_score,
                "relationship_health": relationship_score,
                "billing_compliance": billing_health_score
            },
            "requires_intervention": final_score < 70
        }
""")

    print("Created pipeline simulator, subscription engine, and customer scoring.")

if __name__ == '__main__':
    run()
