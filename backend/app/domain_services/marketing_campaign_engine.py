from typing import Any, Dict, List, Optional

class MarketingCampaignEngine:
    @staticmethod
    def calculate_campaign_performance(
        total_recipients: int,
        total_delivered: int,
        total_opened: int,
        total_clicked: int,
        total_converted: int,
        total_cost: float,
        generated_revenue: float
    ) -> Dict[str, float]:
        delivery_rate = round((total_delivered / max(1, total_recipients)) * 100.0, 2)
        open_rate = round((total_opened / max(1, total_delivered)) * 100.0, 2)
        click_rate = round((total_clicked / max(1, total_delivered)) * 100.0, 2)
        click_to_open_rate = round((total_clicked / max(1, total_opened)) * 100.0, 2)
        conversion_rate = round((total_converted / max(1, total_delivered)) * 100.0, 2)
        
        roi_percentage = round(((generated_revenue - total_cost) / max(1.0, total_cost)) * 100.0, 2)
        cost_per_acquisition = round(total_cost / max(1, total_converted), 2)

        return {
            "delivery_rate_pct": delivery_rate,
            "open_rate_pct": open_rate,
            "click_rate_pct": click_rate,
            "click_to_open_rate_pct": click_to_open_rate,
            "conversion_rate_pct": conversion_rate,
            "cost_per_acquisition": cost_per_acquisition,
            "total_revenue_generated": generated_revenue,
            "roi_percentage": roi_percentage
        }
