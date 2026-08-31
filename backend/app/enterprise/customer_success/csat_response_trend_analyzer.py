from typing import Any, Dict, List, Optional

class CSATResponseTrendAnalyzer:
    @staticmethod
    def calculate_csat_trend_momentum(monthly_ratings: List[List[int]]) -> Dict[str, Any]:
        monthly_scores = []
        for ratings in monthly_ratings:
            if not ratings:
                monthly_scores.append(0.0)
                continue
            positive = sum(1 for r in ratings if r >= 4)
            pct = round((positive / float(len(ratings))) * 100.0, 1)
            monthly_scores.append(pct)

        trend_delta = round(monthly_scores[-1] - monthly_scores[0], 1) if len(monthly_scores) >= 2 else 0.0

        return {
            "monthly_csat_scores": monthly_scores,
            "current_csat_percentage": monthly_scores[-1] if monthly_scores else 0.0,
            "quarterly_trend_delta": trend_delta,
            "momentum": "Positive Growth" if trend_delta > 2.0 else "Declining" if trend_delta < -2.0 else "Stable"
        }
