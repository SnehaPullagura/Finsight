from typing import Any, Dict, List, Optional

class CSExpansionTargetModeler:
    @staticmethod
    def calculate_portfolio_expansion_runway(accounts: List[Dict[str, Any]], target_expansion_rate_pct: float = 25.0) -> Dict[str, Any]:
        total_base_arr = sum(float(a.get("current_arr", 0.0)) for a in accounts)
        target_expansion_arr = round(total_base_arr * (target_expansion_rate_pct / 100.0), 2)
        projected_total_ending_arr = round(total_base_arr + target_expansion_arr, 2)

        return {
            "total_accounts_count": len(accounts),
            "portfolio_base_arr": total_base_arr,
            "target_expansion_rate_pct": target_expansion_rate_pct,
            "projected_net_expansion_dollars": target_expansion_arr,
            "projected_ending_arr": projected_total_ending_arr,
            "expansion_health": "Target Achievable" if len(accounts) >= 10 else "High Concentration Risk"
        }
