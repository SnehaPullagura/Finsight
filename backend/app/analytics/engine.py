import math
import random
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple

class RevenueForecastingModel:
    @staticmethod
    def calculate_weighted_forecast(deals: List[dict]) -> Dict[str, float]:
        commit_total = 0.0
        best_case_total = 0.0
        pipeline_total = 0.0
        weighted_total = 0.0

        for d in deals:
            val = float(d.get("value", 0.0))
            prob = float(d.get("probability", 0.0))
            weighted_total += val * (prob / 100.0)
            pipeline_total += val

            if prob >= 80:
                commit_total += val
                best_case_total += val
            elif prob >= 40:
                best_case_total += val

        return {
            "unweighted_pipeline": round(pipeline_total, 2),
            "weighted_forecast": round(weighted_total, 2),
            "commit_category": round(commit_total, 2),
            "best_case_category": round(best_case_total, 2),
            "coverage_ratio": round(pipeline_total / max(1.0, commit_total), 2)
        }

    @staticmethod
    def monte_carlo_simulation(deals: List[dict], num_simulations: int = 1000) -> Dict[str, float]:
        if not deals:
            return {"p10_worst_case": 0.0, "p50_expected": 0.0, "p90_optimistic": 0.0, "mean": 0.0}

        results = []
        random.seed(42) # Deterministic seed

        for _ in range(num_simulations):
            sim_revenue = 0.0
            for d in deals:
                val = float(d.get("value", 0.0))
                prob = float(d.get("probability", 0.0)) / 100.0
                if random.random() <= prob:
                    sim_revenue += val
            results.append(sim_revenue)

        results.sort()
        n = len(results)
        p10 = results[int(n * 0.10)]
        p50 = results[int(n * 0.50)]
        p90 = results[int(n * 0.90)]
        mean_val = sum(results) / n

        return {
            "p10_worst_case": round(p10, 2),
            "p50_expected": round(p50, 2),
            "p90_optimistic": round(p90, 2),
            "mean": round(mean_val, 2)
        }

class CohortRetentionAnalysis:
    @staticmethod
    def generate_cohort_matrix(cohort_data: List[dict]) -> List[dict]:
        cohort_table = []
        for c in cohort_data:
            cohort_name = c["cohort_month"]
            initial_count = max(1, c["initial_customers"])
            monthly_active = c.get("active_per_month", [])

            retention_percentages = [
                round((active / initial_count) * 100.0, 1) for active in monthly_active
            ]

            cohort_table.append({
                "cohort": cohort_name,
                "initial_size": initial_count,
                "retention_rates": retention_percentages,
                "nrr_percentage": round(c.get("ending_mrr", 0.0) / max(1.0, c.get("starting_mrr", 1.0)) * 100.0, 1)
            })
        return cohort_table

class MultiTouchAttributionModel:
    @staticmethod
    def calculate_attribution(touchpoints: List[dict], deal_value: float) -> Dict[str, Dict[str, float]]:
        if not touchpoints:
            return {}

        n = len(touchpoints)
        models = {"first_touch": {}, "last_touch": {}, "linear": {}, "position_based": {}}

        # 1. First Touch
        first_channel = touchpoints[0]["channel"]
        models["first_touch"][first_channel] = round(deal_value, 2)

        # 2. Last Touch
        last_channel = touchpoints[-1]["channel"]
        models["last_touch"][last_channel] = round(deal_value, 2)

        # 3. Linear
        linear_val = round(deal_value / n, 2)
        for tp in touchpoints:
            ch = tp["channel"]
            models["linear"][ch] = models["linear"].get(ch, 0.0) + linear_val

        # 4. Position-Based (40% first, 40% last, 20% middle split)
        if n == 1:
            models["position_based"][first_channel] = round(deal_value, 2)
        elif n == 2:
            models["position_based"][first_channel] = round(deal_value * 0.50, 2)
            models["position_based"][last_channel] = models["position_based"].get(last_channel, 0.0) + round(deal_value * 0.50, 2)
        else:
            first_val = round(deal_value * 0.40, 2)
            last_val = round(deal_value * 0.40, 2)
            mid_val = round((deal_value * 0.20) / (n - 2), 2)

            models["position_based"][first_channel] = models["position_based"].get(first_channel, 0.0) + first_val
            models["position_based"][last_channel] = models["position_based"].get(last_channel, 0.0) + last_val
            for tp in touchpoints[1:-1]:
                ch = tp["channel"]
                models["position_based"][ch] = models["position_based"].get(ch, 0.0) + mid_val

        return models

class SalesCompensationEngine:
    @staticmethod
    def calculate_commission(
        quota: float,
        actual_closed: float,
        base_rate_pct: float = 10.0,
        accelerators: Optional[List[dict]] = None
    ) -> Dict[str, float]:
        attainment_pct = round((actual_closed / max(1.0, quota)) * 100.0, 2)
        default_accelerators = accelerators or [
            {"min_pct": 0, "max_pct": 100, "multiplier": 1.0},
            {"min_pct": 100, "max_pct": 120, "multiplier": 1.5},
            {"min_pct": 120, "max_pct": None, "multiplier": 2.0},
        ]

        total_commission = 0.0
        for tier in default_accelerators:
            min_p = tier["min_pct"]
            max_p = tier["max_pct"] or float("inf")
            mult = tier["multiplier"]

            if attainment_pct > min_p:
                portion_pct = min(attainment_pct - min_p, max_p - min_p)
                portion_revenue = quota * (portion_pct / 100.0)
                tier_commission = portion_revenue * (base_rate_pct / 100.0) * mult
                total_commission += tier_commission

        return {
            "quota": quota,
            "actual_closed": actual_closed,
            "attainment_percentage": attainment_pct,
            "total_commission_earned": round(total_commission, 2),
            "effective_commission_rate": round((total_commission / max(1.0, actual_closed)) * 100.0, 2)
        }
