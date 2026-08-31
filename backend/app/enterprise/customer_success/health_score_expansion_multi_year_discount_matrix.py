from typing import Any, Dict, List, Optional

class MultiYearDiscountMatrix:
    @staticmethod
    def calculate_multi_year_terms(annual_contract_value: float) -> List[Dict[str, Any]]:
        tiers = [
            {"term_years": 1, "discount_pct": 0.0, "upfront_payment_pct": 100.0},
            {"term_years": 2, "discount_pct": 10.0, "upfront_payment_pct": 100.0},
            {"term_years": 3, "discount_pct": 17.5, "upfront_payment_pct": 100.0},
            {"term_years": 5, "discount_pct": 25.0, "upfront_payment_pct": 100.0}
        ]

        results = []
        for t in tiers:
            discount = t["discount_pct"]
            years = t["term_years"]
            discounted_annual = annual_contract_value * (1.0 - (discount / 100.0))
            total_tcv = discounted_annual * years

            results.append({
                "commitment_term_years": years,
                "discount_percentage": discount,
                "annualized_rate": round(discounted_annual, 2),
                "total_contract_value": round(total_tcv, 2),
                "total_customer_savings": round((annual_contract_value * years) - total_tcv, 2)
            })

        return results
