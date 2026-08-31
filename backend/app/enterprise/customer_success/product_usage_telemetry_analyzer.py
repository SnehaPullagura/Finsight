from typing import Any, Dict, List, Optional

class ProductUsageTelemetryAnalyzer:
    @staticmethod
    def analyze_daily_active_ratio(dau: int, mau: int) -> Dict[str, Any]:
        stickiness_pct = round((dau / max(1, mau)) * 100.0, 1)

        rating = "World-Class Stickiness" if stickiness_pct >= 40.0 else "Healthy Engagement" if stickiness_pct >= 20.0 else "Low Engagement Risk"

        return {
            "daily_active_users": dau,
            "monthly_active_users": mau,
            "dau_to_mau_stickiness_pct": stickiness_pct,
            "engagement_rating": rating,
            "is_churn_risk": stickiness_pct < 15.0
        }
