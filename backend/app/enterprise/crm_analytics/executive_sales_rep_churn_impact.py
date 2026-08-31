from typing import Any, Dict, List, Optional
from collections import defaultdict

class RepChurnImpactModeler:
    @staticmethod
    def calculate_rep_attributed_churn(accounts_churned: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        rep_churn_map = defaultdict(lambda: {"lost_arr": 0.0, "accounts_count": 0})

        for acc in accounts_churned:
            rep = acc.get("closing_rep_name", "Unassigned")
            arr = float(acc.get("churned_arr", 0.0))
            rep_churn_map[rep]["lost_arr"] += arr
            rep_churn_map[rep]["accounts_count"] += 1

        results = []
        for rep, data in rep_churn_map.items():
            results.append({
                "rep_name": rep,
                "total_lost_arr": round(data["lost_arr"], 2),
                "churned_accounts_count": data["accounts_count"],
                "requires_onboarding_enablement": data["accounts_count"] >= 3
            })

        return sorted(results, key=lambda x: x["total_lost_arr"], reverse=True)
