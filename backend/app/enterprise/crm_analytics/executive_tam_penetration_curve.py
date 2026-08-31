from typing import Any, Dict, List, Optional

class TAMPenetrationCurveAnalyzer:
    @staticmethod
    def calculate_penetration_pacing(
        total_market_accounts: int,
        acquired_accounts: int,
        pipeline_engaged_accounts: int,
        annual_growth_rate_pct: float
    ) -> Dict[str, Any]:
        penetration_pct = round((acquired_accounts / max(1, total_market_accounts)) * 100.0, 2)
        engaged_pct = round((pipeline_engaged_accounts / max(1, total_market_accounts)) * 100.0, 2)
        unreached_accounts = max(0, total_market_accounts - acquired_accounts - pipeline_engaged_accounts)

        return {
            "total_market_accounts": total_market_accounts,
            "acquired_customers_count": acquired_accounts,
            "current_market_penetration_pct": penetration_pct,
            "pipeline_engaged_accounts": pipeline_engaged_accounts,
            "pipeline_engaged_pct": engaged_pct,
            "unreached_white_space_accounts": unreached_accounts,
            "market_share_tier": "Dominant Player (> 15%)" if penetration_pct >= 15.0 else "Established Challenger (5% - 15%)" if penetration_pct >= 5.0 else "Early Market Entrant (< 5%)"
        }
