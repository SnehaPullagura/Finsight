from datetime import date, timedelta
from typing import Any, Dict, List, Optional
from collections import defaultdict

class EnterpriseReportingEngine:
    @staticmethod
    def generate_sales_rep_leaderboard(deals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        rep_stats = defaultdict(lambda: {"rep_name": "", "deals_won": 0, "revenue_won": 0.0, "open_deals": 0, "open_pipeline": 0.0})

        for d in deals:
            rep_id = d.get("owner_id") or "unassigned"
            name = d.get("owner_name") or f"Rep {rep_id[:8]}"
            status = (d.get("status") or "open").lower()
            val = float(d.get("value", 0.0))

            rep_stats[rep_id]["rep_name"] = name
            if status == "won":
                rep_stats[rep_id]["deals_won"] += 1
                rep_stats[rep_id]["revenue_won"] += val
            elif status == "open":
                rep_stats[rep_id]["open_deals"] += 1
                rep_stats[rep_id]["open_pipeline"] += val

        leaderboard = []
        for rep_id, s in rep_stats.items():
            win_rate = (s["deals_won"] / max(1, s["deals_won"] + s["open_deals"])) * 100.0
            leaderboard.append({
                "rep_id": rep_id,
                "rep_name": s["rep_name"],
                "deals_won_count": s["deals_won"],
                "total_revenue_won": round(s["revenue_won"], 2),
                "open_pipeline_value": round(s["open_pipeline"], 2),
                "win_rate_percentage": round(win_rate, 1)
            })

        return sorted(leaderboard, key=lambda x: x["total_revenue_won"], reverse=True)
