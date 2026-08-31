import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/domain_services/sales_velocity_matrix.py
    write_file("backend/app/domain_services/sales_velocity_matrix.py", """import math
from datetime import datetime, date, timedelta
from typing import Any, Dict, List, Optional, Tuple

class SalesVelocityMatrix:
    @staticmethod
    def compute_funnel_conversion_rates(stage_counts: Dict[str, int]) -> Dict[str, Any]:
        stages = ["lead", "discovery", "scoping", "proposal", "negotiation", "won"]
        conversion_steps = []
        
        for i in range(len(stages) - 1):
            curr_stage = stages[i]
            next_stage = stages[i + 1]
            curr_count = stage_counts.get(curr_stage, 0)
            next_count = stage_counts.get(next_stage, 0)
            
            rate = round((next_count / max(1, curr_count)) * 100.0, 2)
            conversion_steps.append({
                "from_stage": curr_stage,
                "to_stage": next_stage,
                "from_count": curr_count,
                "to_count": next_count,
                "conversion_rate_pct": min(100.0, rate)
            })

        overall_lead_count = stage_counts.get("lead", 1)
        overall_won_count = stage_counts.get("won", 0)
        overall_conversion = round((overall_won_count / max(1, overall_lead_count)) * 100.0, 2)

        return {
            "funnel_steps": conversion_steps,
            "overall_conversion_rate": overall_conversion,
            "total_leads_entered": overall_lead_count,
            "total_deals_won": overall_won_count
        }

    @staticmethod
    def calculate_stage_bottlenecks(stage_durations: Dict[str, List[float]], benchmark_days: Dict[str, float]) -> List[Dict[str, Any]]:
        bottlenecks = []
        for stage, durations in stage_durations.items():
            if not durations:
                continue
            avg_duration = sum(durations) / float(len(durations))
            benchmark = benchmark_days.get(stage, 14.0)
            excess = avg_duration - benchmark
            
            is_bottleneck = excess > 3.0
            bottlenecks.append({
                "stage": stage,
                "average_days": round(avg_duration, 1),
                "benchmark_days": benchmark,
                "excess_days": round(excess, 1),
                "is_bottleneck": is_bottleneck,
                "severity": "high" if excess > 7.0 else "medium" if is_bottleneck else "normal"
            })
        return sorted(bottlenecks, key=lambda b: b["excess_days"], reverse=True)
""")

    # 2. backend/app/domain_services/subscription_billing_manager.py
    write_file("backend/app/domain_services/subscription_billing_manager.py", """from datetime import date, timedelta
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
""")

    # 3. backend/app/domain_services/customer_success_engine.py
    write_file("backend/app/domain_services/customer_success_engine.py", """from typing import Any, Dict, List, Optional

class CustomerSuccessLifecycleEngine:
    @staticmethod
    def evaluate_renewal_risk(
        health_score: int,
        days_until_renewal: int,
        unresolved_tickets: int,
        contract_value: float
    ) -> Dict[str, Any]:
        risk_factors = []
        score = health_score

        if days_until_renewal <= 60 and health_score < 70:
            risk_factors.append("Upcoming renewal within 60 days with sub-70 health score")
        if unresolved_tickets >= 3:
            risk_factors.append(f"{unresolved_tickets} unresolved support tickets")
        if health_score < 50:
            risk_factors.append("Critical low product usage engagement")

        risk_category = "high_risk" if len(risk_factors) >= 2 or health_score < 40 else "medium_risk" if risk_factors else "healthy"

        return {
            "contract_value": contract_value,
            "days_until_renewal": days_until_renewal,
            "health_score": health_score,
            "renewal_risk_category": risk_category,
            "risk_factors": risk_factors,
            "requires_executive_sponsor": risk_category == "high_risk"
        }
""")

    # 4. backend/app/domain_services/marketing_campaign_engine.py
    write_file("backend/app/domain_services/marketing_campaign_engine.py", """from typing import Any, Dict, List, Optional

class MarketingCampaignEngine:
    @staticmethod
    def calculate_campaign_performance(
        total_recipients: int,
        total_delivered: int,
        total_opened: int,
        total_clicked: int,
        total_converted: int,
        total_cost: float,
        generated_revenue: float
    ) -> Dict[str, float]:
        delivery_rate = round((total_delivered / max(1, total_recipients)) * 100.0, 2)
        open_rate = round((total_opened / max(1, total_delivered)) * 100.0, 2)
        click_rate = round((total_clicked / max(1, total_delivered)) * 100.0, 2)
        click_to_open_rate = round((total_clicked / max(1, total_opened)) * 100.0, 2)
        conversion_rate = round((total_converted / max(1, total_delivered)) * 100.0, 2)
        
        roi_percentage = round(((generated_revenue - total_cost) / max(1.0, total_cost)) * 100.0, 2)
        cost_per_acquisition = round(total_cost / max(1, total_converted), 2)

        return {
            "delivery_rate_pct": delivery_rate,
            "open_rate_pct": open_rate,
            "click_rate_pct": click_rate,
            "click_to_open_rate_pct": click_to_open_rate,
            "conversion_rate_pct": conversion_rate,
            "cost_per_acquisition": cost_per_acquisition,
            "total_revenue_generated": generated_revenue,
            "roi_percentage": roi_percentage
        }
""")

    print("Created velocity matrix, subscription billing manager, success lifecycle, and campaign engine.")

if __name__ == '__main__':
    run()
