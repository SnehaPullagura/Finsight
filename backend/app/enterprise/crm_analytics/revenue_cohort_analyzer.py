from datetime import date
from typing import Any, Dict, List, Optional
from collections import defaultdict

class RevenueCohortAnalyzer:
    @staticmethod
    def calculate_cohort_retention_matrix(
        customer_signups: List[Dict[str, Any]],
        monthly_billings: List[Dict[str, Any]],
        periods_months: int = 12
    ) -> List[Dict[str, Any]]:
        # Cohort calculation: Track initial cohort size and percentage retention over time
        cohorts = defaultdict(lambda: {"initial_count": 0, "initial_mrr": 0.0, "retention_by_period": [0.0] * periods_months})

        for cust in customer_signups:
            cohort_month = cust.get("signup_month", "2026-01")
            cohorts[cohort_month]["initial_count"] += 1
            cohorts[cohort_month]["initial_mrr"] += float(cust.get("initial_mrr", 0.0))

        for bill in monthly_billings:
            cohort_month = bill.get("cohort_month")
            period_idx = int(bill.get("period_index", 0))
            if cohort_month in cohorts and 0 <= period_idx < periods_months:
                cohorts[cohort_month]["retention_by_period"][period_idx] += float(bill.get("mrr_amount", 0.0))

        result_matrix = []
        for cmonth, data in sorted(cohorts.items()):
            init_mrr = max(1.0, data["initial_mrr"])
            pct_retention = [round((p / init_mrr) * 100.0, 1) for p in data["retention_by_period"]]
            result_matrix.append({
                "cohort_month": cmonth,
                "customer_count": data["initial_count"],
                "initial_mrr": round(data["initial_mrr"], 2),
                "retention_percentages": pct_retention
            })

        return result_matrix
