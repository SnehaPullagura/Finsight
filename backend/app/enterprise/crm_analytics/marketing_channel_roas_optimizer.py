from typing import Any, Dict, List, Optional

class MarketingROASBudgetOptimizer:
    @staticmethod
    def reallocate_budget(channels: List[Dict[str, Any]], total_budget: float) -> List[Dict[str, Any]]:
        # Proportional budget weighting based on ROAS efficiency squared
        total_roas_weight = sum(float(c.get("roas", 1.0)) ** 2 for c in channels)
        
        results = []
        for c in channels:
            name = c.get("name")
            roas = float(c.get("roas", 1.0))
            weight = (roas ** 2) / max(0.01, total_roas_weight)
            allocated = round(total_budget * weight, 2)
            projected_rev = round(allocated * roas, 2)

            results.append({
                "channel_name": name,
                "historical_roas": roas,
                "recommended_budget_allocation": allocated,
                "allocation_percentage": round(weight * 100.0, 1),
                "projected_revenue": projected_rev
            })

        return sorted(results, key=lambda x: x["recommended_budget_allocation"], reverse=True)
