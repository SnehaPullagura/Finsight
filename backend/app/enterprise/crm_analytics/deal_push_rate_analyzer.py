from typing import Any, Dict, List, Optional

class DealPushRateAnalyzer:
    @staticmethod
    def calculate_pipeline_push_rate(deals: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_open = len([d for d in deals if d.get("status") == "open"])
        pushed_deals = [d for d in deals if int(d.get("push_count", 0)) > 0]
        multiple_push_deals = [d for d in deals if int(d.get("push_count", 0)) >= 2]

        push_rate_pct = round((len(pushed_deals) / max(1, total_open)) * 100.0, 1)
        multiple_push_rate_pct = round((len(multiple_push_deals) / max(1, total_open)) * 100.0, 1)

        return {
            "total_open_deals": total_open,
            "pushed_deals_count": len(pushed_deals),
            "multiple_pushed_count": len(multiple_push_deals),
            "push_rate_percentage": push_rate_pct,
            "chronic_slippage_rate_percentage": multiple_push_rate_pct,
            "pipeline_hygiene_status": "Healthy" if push_rate_pct <= 20.0 else "Warning (> 20% Pushed)" if push_rate_pct <= 40.0 else "Critical Pipeline Friction"
        }
