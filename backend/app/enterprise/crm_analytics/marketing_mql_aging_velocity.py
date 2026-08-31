from typing import Any, Dict, List, Optional

class MQLAgingVelocityAnalyzer:
    @staticmethod
    def calculate_mql_decay(mql_leads: List[Dict[str, Any]]) -> Dict[str, Any]:
        buckets = {"sub_24h": 0, "day_1_to_3": 0, "day_3_to_7": 0, "stale_7d_plus": 0}
        total = len(mql_leads)

        for l in mql_leads:
            hours = float(l.get("hours_since_qualification", 0.0))
            if hours <= 24:
                buckets["sub_24h"] += 1
            elif hours <= 72:
                buckets["day_1_to_3"] += 1
            elif hours <= 168:
                buckets["day_3_to_7"] += 1
            else:
                buckets["stale_7d_plus"] += 1

        pct_sub_24h = round((buckets["sub_24h"] / max(1, total)) * 100.0, 1)

        return {
            "total_mql_leads": total,
            "aging_buckets": buckets,
            "pct_contacted_under_24h": pct_sub_24h,
            "velocity_rating": "Elite Response Speed" if pct_sub_24h >= 80.0 else "Acceptable" if pct_sub_24h >= 50.0 else "High SDR Friction"
        }
