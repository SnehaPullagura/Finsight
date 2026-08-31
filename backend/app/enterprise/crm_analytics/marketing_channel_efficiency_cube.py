from typing import Any, Dict, List, Optional
from collections import defaultdict

class MarketingChannelEfficiencyCube:
    @staticmethod
    def calculate_efficiency_metrics(campaign_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        channel_data = defaultdict(lambda: {"spend": 0.0, "leads": 0, "sqls": 0, "won_deals": 0, "revenue": 0.0})

        for camp in campaign_records:
            ch = camp.get("channel", "Organic")
            channel_data[ch]["spend"] += float(camp.get("spend", 0.0))
            channel_data[ch]["leads"] += int(camp.get("leads_generated", 0))
            channel_data[ch]["sqls"] += int(camp.get("sqls_generated", 0))
            channel_data[ch]["won_deals"] += int(camp.get("won_deals_count", 0))
            channel_data[ch]["revenue"] += float(camp.get("attributed_revenue", 0.0))

        results = []
        for ch, d in channel_data.items():
            spend = d["spend"]
            rev = d["revenue"]
            leads = d["leads"]
            won = d["won_deals"]

            cpl = round(spend / max(1, leads), 2)
            cac = round(spend / max(1, won), 2)
            roas = round(rev / max(1.0, spend), 2)

            results.append({
                "channel_name": ch,
                "total_spend": round(spend, 2),
                "leads_generated": leads,
                "cost_per_lead": cpl,
                "won_deals_count": won,
                "customer_acquisition_cost": cac,
                "attributed_revenue": round(rev, 2),
                "roas_multiplier": roas,
                "efficiency_rating": "Top Performer" if roas >= 10.0 else "Solid" if roas >= 4.0 else "Underperforming"
            })

        return sorted(results, key=lambda x: x["attributed_revenue"], reverse=True)
