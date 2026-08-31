from typing import Any, Dict, List, Optional

class ContentEngagementAnalytics:
    """
    Ranks marketing and sales enablement assets by conversion correlation.
    """
    @staticmethod
    def rank_asset_effectiveness(assets_engagement: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for a in assets_engagement:
            title = a.get("title")
            views = int(a.get("views_count", 0))
            shares = int(a.get("internal_shares_count", 0))
            won_deals = int(a.get("closed_won_deals_count", 0))

            virality_multiplier = round((shares / max(1, views)) * 100.0, 1)
            win_correlation = round((won_deals / max(1, views)) * 100.0, 1)

            results.append({
                "asset_title": title,
                "views": views,
                "internal_shares": shares,
                "virality_rate_pct": virality_multiplier,
                "win_rate_correlation_pct": win_correlation,
                "collateral_tier": "Power Closer" if win_correlation >= 40.0 else "Solid Engagement"
            })

        return sorted(results, key=lambda x: x["win_rate_correlation_pct"], reverse=True)
