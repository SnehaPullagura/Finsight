from typing import Any, Dict, List, Optional
from collections import defaultdict

class WinLossDecisionMatrix:
    @staticmethod
    def analyze_win_loss_patterns(closed_deals: List[Dict[str, Any]]) -> Dict[str, Any]:
        won_reasons = defaultdict(int)
        lost_reasons = defaultdict(int)
        competitor_wins = defaultdict(int)

        total_won = 0
        total_lost = 0

        for d in closed_deals:
            status = (d.get("status") or "").lower()
            reason = d.get("win_loss_reason") or "Not Specified"
            comp = d.get("competitor_lost_to")

            if status == "won":
                total_won += 1
                won_reasons[reason] += 1
            elif status == "lost":
                total_lost += 1
                lost_reasons[reason] += 1
                if comp:
                    competitor_wins[comp] += 1

        overall_win_rate = round((total_won / max(1, total_won + total_lost)) * 100.0, 1)

        return {
            "total_closed_deals": total_won + total_lost,
            "total_won": total_won,
            "total_lost": total_lost,
            "win_rate_percentage": overall_win_rate,
            "top_won_reasons": sorted([{"reason": k, "count": v} for k, v in won_reasons.items()], key=lambda x: x["count"], reverse=True),
            "top_lost_reasons": sorted([{"reason": k, "count": v} for k, v in lost_reasons.items()], key=lambda x: x["count"], reverse=True),
            "competitor_losses": sorted([{"competitor": k, "losses_count": v} for k, v in competitor_wins.items()], key=lambda x: x["losses_count"], reverse=True)
        }
