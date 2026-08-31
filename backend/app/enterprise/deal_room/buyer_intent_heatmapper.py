from typing import Any, Dict, List, Optional

class BuyerIntentHeatmapper:
    """
    Heatmaps buyer document engagement:
    Tracks page-by-page dwell time on proposals, pricing tables, and legal terms.
    """
    @staticmethod
    def compute_document_dwell_heatmap(
        document_id: str,
        page_dwell_events: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        page_totals = {}
        for ev in page_dwell_events:
            p = int(ev.get("page_number", 1))
            sec = int(ev.get("seconds_spent", 0))
            page_totals[p] = page_totals.get(p, 0) + sec

        total_time = sum(page_totals.values())
        hottest_page = max(page_totals, key=page_totals.get) if page_totals else 1

        # Calculate percentages
        page_percentages = {
            p: round((sec / max(1, total_time)) * 100.0, 1)
            for p, sec in page_totals.items()
        }

        return {
            "document_id": document_id,
            "total_dwell_time_seconds": total_time,
            "page_dwell_seconds": page_totals,
            "page_engagement_percentages": page_percentages,
            "hottest_page_number": hottest_page,
            "is_pricing_focused": hottest_page in [3, 4], # Pricing & SLA pages
            "buyer_buying_intent_score": min(100, int((total_time / 600.0) * 100))
        }
