from typing import Any, Dict, List, Optional

class CohortGrossRetentionCube:
    """
    Computes Gross Revenue Retention (GRR) and Net Revenue Retention (NRR) matrices by onboarding quarterly cohorts.
    """
    @staticmethod
    def calculate_cohort_matrix(cohorts_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for c in cohorts_data:
            qtr = c.get("cohort_quarter", "Q1-2025")
            base_arr = float(c.get("initial_arr", 1000000.0))
            churned = float(c.get("churned_arr", 40000.0))
            expanded = float(c.get("expansion_arr", 180000.0))

            grr_pct = round(((base_arr - churned) / max(1.0, base_arr)) * 100.0, 1)
            nrr_pct = round(((base_arr - churned + expanded) / max(1.0, base_arr)) * 100.0, 1)

            results.append({
                "cohort_quarter": qtr,
                "initial_starting_arr": base_arr,
                "churned_arr": churned,
                "expansion_arr": expanded,
                "gross_revenue_retention_pct": grr_pct,
                "net_revenue_retention_pct": nrr_pct,
                "benchmark_rating": "ELITE_TOP_QUARTILE" if nrr_pct >= 115.0 and grr_pct >= 92.0 else "HEALTHY"
            })

        return results
