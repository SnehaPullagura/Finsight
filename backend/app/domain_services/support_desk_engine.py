from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

class SupportDeskEngine:
    @staticmethod
    def calculate_csat_metrics(ratings: List[int]) -> Dict[str, Any]:
        if not ratings:
            return {"average_csat": 0.0, "csat_percentage": 0.0, "response_count": 0}

        positive_count = sum(1 for r in ratings if r >= 4)
        total_count = len(ratings)
        avg = sum(ratings) / float(total_count)
        pct = (positive_count / float(total_count)) * 100.0

        return {
            "average_csat": round(avg, 2),
            "csat_percentage": round(pct, 1),
            "response_count": total_count,
            "distribution": {
                "5_stars": ratings.count(5),
                "4_stars": ratings.count(4),
                "3_stars": ratings.count(3),
                "2_stars": ratings.count(2),
                "1_star": ratings.count(1)
            }
        }
