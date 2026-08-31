from typing import Any, Dict, List, Optional
from collections import defaultdict

class RepWinRateDistributionModeler:
    @staticmethod
    def analyze_team_win_rate_distribution(reps_performance: List[Dict[str, Any]]) -> Dict[str, Any]:
        win_rates = []
        tier_distribution = {"top_performers_35_plus": 0, "mid_tier_20_to_35": 0, "underperforming_sub_20": 0}

        for r in reps_performance:
            won = int(r.get("won_deals", 0))
            lost = int(r.get("lost_deals", 0))
            total = won + lost
            rate = round((won / max(1, total)) * 100.0, 1)
            win_rates.append(rate)

            if rate >= 35.0:
                tier_distribution["top_performers_35_plus"] += 1
            elif rate >= 20.0:
                tier_distribution["mid_tier_20_to_35"] += 1
            else:
                tier_distribution["underperforming_sub_20"] += 1

        team_avg_win_rate = round(sum(win_rates) / float(max(1, len(win_rates))), 1)

        return {
            "total_reps_evaluated": len(reps_performance),
            "team_average_win_rate_pct": team_avg_win_rate,
            "distribution_breakdown": tier_distribution,
            "highest_rep_win_rate": max(win_rates) if win_rates else 0.0,
            "lowest_rep_win_rate": min(win_rates) if win_rates else 0.0
        }
