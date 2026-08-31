from typing import Any, Dict, List, Optional

class CustomerExpansionOpportunityFinder:
    @staticmethod
    def identify_upsell_candidates(accounts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        expansion_candidates = []

        for acc in accounts:
            seats_used = int(acc.get("seats_used", 0))
            seats_purchased = int(acc.get("seats_purchased", 1))
            health_score = int(acc.get("health_score", 50))
            arr = float(acc.get("current_arr", 0.0))

            utilization_pct = round((seats_used / max(1, seats_purchased)) * 100.0, 1)

            # High utilization (>= 90%) + High health (>= 80) -> Upsell Candidate
            if utilization_pct >= 90.0 and health_score >= 80:
                recommended_add_seats = max(5, int(seats_purchased * 0.25))
                projected_expansion_arr = round(arr * 0.25, 2)

                expansion_candidates.append({
                    "account_id": acc.get("id"),
                    "account_name": acc.get("name"),
                    "utilization_percentage": utilization_pct,
                    "health_score": health_score,
                    "current_arr": arr,
                    "recommended_additional_seats": recommended_add_seats,
                    "projected_expansion_arr": projected_expansion_arr,
                    "signal": "High license utilization approaching ceiling"
                })

        return sorted(expansion_candidates, key=lambda x: x["projected_expansion_arr"], reverse=True)
