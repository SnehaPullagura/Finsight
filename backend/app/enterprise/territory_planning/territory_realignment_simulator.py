from typing import Any, Dict, List, Optional

class TerritoryRealignmentSimulator:
    """
    Simulates annual sales territory realignments, calculating account reassignments,
    pipeline transfer impact, and rep quota adjustments.
    """
    @staticmethod
    def simulate_realignment(
        current_assignments: List[Dict[str, Any]],
        proposed_assignments: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        transferred_accounts = 0
        transferred_arr = 0.0

        prop_map = {p["account_id"]: p["new_rep_id"] for p in proposed_assignments}

        for cur in current_assignments:
            aid = cur.get("account_id")
            old_rep = cur.get("current_rep_id")
            arr = float(cur.get("account_arr", 0.0))

            if aid in prop_map and prop_map[aid] != old_rep:
                transferred_accounts += 1
                transferred_arr += arr

        disruption_index = round((transferred_accounts / max(1, len(current_assignments))) * 100.0, 1)

        return {
            "total_accounts_analyzed": len(current_assignments),
            "accounts_transferred": transferred_accounts,
            "total_pipeline_transferred": round(transferred_arr, 2),
            "territory_disruption_index_pct": disruption_index,
            "feasibility": "LOW_DISRUPTION (< 20%)" if disruption_index <= 20.0 else "MODERATE_DISRUPTION (20%-40%)" if disruption_index <= 40.0 else "HIGH_DISRUPTION (> 40%)"
        }
