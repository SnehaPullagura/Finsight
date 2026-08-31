from typing import Any, Dict, List, Optional

class FunnelConversionModel:
    @staticmethod
    def calculate_full_funnel_metrics(
        visitor_count: int,
        lead_count: int,
        mql_count: int,
        sql_count: int,
        opportunity_count: int,
        won_deal_count: int
    ) -> Dict[str, Any]:
        v_to_lead = round((lead_count / max(1, visitor_count)) * 100.0, 2)
        lead_to_mql = round((mql_count / max(1, lead_count)) * 100.0, 2)
        mql_to_sql = round((sql_count / max(1, mql_count)) * 100.0, 2)
        sql_to_opp = round((opportunity_count / max(1, sql_count)) * 100.0, 2)
        opp_to_won = round((won_deal_count / max(1, opportunity_count)) * 100.0, 2)
        overall_conversion = round((won_deal_count / max(1, visitor_count)) * 100.0, 3)

        return {
            "funnel_stages": [
                {"stage": "Website Visitors", "count": visitor_count, "conversion_to_next": v_to_lead},
                {"stage": "Inbound Leads", "count": lead_count, "conversion_to_next": lead_to_mql},
                {"stage": "Marketing Qualified (MQL)", "count": mql_count, "conversion_to_next": mql_to_sql},
                {"stage": "Sales Qualified (SQL)", "count": sql_count, "conversion_to_next": sql_to_opp},
                {"stage": "Sales Opportunities", "count": opportunity_count, "conversion_to_next": opp_to_won},
                {"stage": "Closed Won Deals", "count": won_deal_count, "conversion_to_next": 100.0}
            ],
            "overall_visitor_to_customer_pct": overall_conversion,
            "funnel_health": "High Efficiency" if mql_to_sql >= 40.0 and opp_to_won >= 25.0 else "Needs SDR Optimization"
        }
