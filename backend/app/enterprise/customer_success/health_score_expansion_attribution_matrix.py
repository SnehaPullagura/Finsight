from typing import Any, Dict, List, Optional

class CSExpansionAttributionMatrix:
    @staticmethod
    def attribute_expansion_revenue(deals: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_expansion = 0.0
        cs_assisted = 0.0
        product_led = 0.0
        sales_outbound = 0.0

        for d in deals:
            val = float(d.get("deal_value", 0.0))
            src = d.get("lead_source", "")
            total_expansion += val

            if "CS Health" in src or "Customer Success" in src:
                cs_assisted += val
            elif "Product" in src or "Self-Service" in src:
                product_led += val
            else:
                sales_outbound += val

        cs_pct = round((cs_assisted / max(1.0, total_expansion)) * 100.0, 1)

        return {
            "total_expansion_revenue": round(total_expansion, 2),
            "cs_health_assisted_revenue": round(cs_assisted, 2),
            "product_led_expansion_revenue": round(product_led, 2),
            "sales_outbound_expansion_revenue": round(sales_outbound, 2),
            "cs_assisted_percentage": cs_pct
        }
