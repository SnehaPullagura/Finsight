from typing import Any, Dict, List, Optional
from collections import defaultdict

class GeoTerritoryOptimizer:
    """
    Territory Optimizer & Territory Workload Equalization Engine:
    Balances enterprise territories across reps based on Total Addressable Market (TAM),
    account count, and historical win rates.
    """
    @staticmethod
    def balance_territories(
        accounts: List[Dict[str, Any]],
        rep_count: int
    ) -> List[Dict[str, Any]]:
        # Sort accounts by estimated ARR potential descending
        sorted_accs = sorted(accounts, key=lambda x: float(x.get("estimated_arr_potential", 10000.0)), reverse=True)
        territories = [
            {"territory_id": f"TERR-{i+1}", "rep_index": i, "assigned_accounts": [], "total_potential_arr": 0.0}
            for i in range(max(1, rep_count))
        ]

        # Greedy balance allocation
        for acc in sorted_accs:
            arr = float(acc.get("estimated_arr_potential", 10000.0))
            # Pick territory with lowest accumulated ARR
            min_terr = min(territories, key=lambda t: t["total_potential_arr"])
            min_terr["assigned_accounts"].append({
                "account_id": acc.get("id"),
                "account_name": acc.get("name"),
                "state": acc.get("state", "CA"),
                "potential_arr": arr
            })
            min_terr["total_potential_arr"] = round(min_terr["total_potential_arr"] + arr, 2)

        # Compute balance variance
        all_arrs = [t["total_potential_arr"] for t in territories]
        avg_arr = sum(all_arrs) / len(all_arrs) if all_arrs else 0.0

        for t in territories:
            variance_pct = round(((t["total_potential_arr"] - avg_arr) / max(1.0, avg_arr)) * 100.0, 1)
            t["account_count"] = len(t["assigned_accounts"])
            t["tam_variance_from_mean_pct"] = variance_pct
            t["is_balanced"] = abs(variance_pct) <= 15.0

        return territories
