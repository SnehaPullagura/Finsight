from typing import Any, Dict, List, Optional

class MarketingCreativePerformanceIndex:
    @staticmethod
    def calculate_creative_roi(creatives: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for c in creatives:
            spend = float(c.get("spend", 1000.0))
            rev = float(c.get("attributed_revenue", 0.0))
            clicks = int(c.get("clicks", 100))
            impressions = int(c.get("impressions", 10000))

            roas = round(rev / max(1.0, spend), 2)
            ctr = round((clicks / max(1, impressions)) * 100.0, 2)
            cpc = round(spend / max(1, clicks), 2)

            results.append({
                "creative_name": c.get("name"),
                "ad_format": c.get("format", "Video"),
                "roas_multiplier": roas,
                "click_through_rate_pct": ctr,
                "cost_per_click": cpc,
                "performance_tier": "Top Performer (ROAS > 8x)" if roas >= 8.0 else "Solid (4x - 8x)" if roas >= 4.0 else "Underperforming (< 4x)"
            })

        return sorted(results, key=lambda x: x["roas_multiplier"], reverse=True)
