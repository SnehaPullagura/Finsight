from typing import Any, Dict, List, Optional

class RepDiscountDisciplineModeler:
    @staticmethod
    def evaluate_rep_discounting(reps_deals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for r in reps_deals:
            discounts = r.get("discounts_given_pct", [])
            avg_discount = round(sum(discounts) / float(max(1, len(discounts))), 1) if discounts else 0.0
            rating = "Disciplined (< 10%)" if avg_discount <= 10.0 else "Acceptable (10% - 20%)" if avg_discount <= 20.0 else "Discount Heavy (> 20%)"

            results.append({
                "rep_id": r.get("id"),
                "rep_name": r.get("name"),
                "total_deals_closed": len(discounts),
                "average_discount_percentage": avg_discount,
                "pricing_discipline_rating": rating,
                "requires_manager_override_review": avg_discount > 18.0
            })

        return results
