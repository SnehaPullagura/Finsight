from datetime import date
from typing import Any, Dict, List, Optional

class ExecutiveDealBriefingGenerator:
    @staticmethod
    def generate_deal_brief(
        deal: Dict[str, Any],
        company: Dict[str, Any],
        key_stakeholders: List[Dict[str, Any]],
        pricing_quote: Dict[str, Any],
        meddic_evaluation: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            "deal_id": deal.get("id"),
            "deal_name": deal.get("name"),
            "deal_value": float(deal.get("value", 0.0)),
            "probability": int(deal.get("probability", 50)),
            "target_close_date": deal.get("expected_close_date", date.today().isoformat()),
            "company_summary": {
                "name": company.get("name"),
                "industry": company.get("industry"),
                "annual_revenue": company.get("annual_revenue"),
                "tier": company.get("tier", "growth")
            },
            "stakeholders_count": len(key_stakeholders),
            "pricing_summary": {
                "list_price": pricing_quote.get("subtotal", 0.0),
                "discount_percentage": pricing_quote.get("discount_percentage", 0.0),
                "net_contract_value": pricing_quote.get("total_amount", 0.0)
            },
            "qualification_health": {
                "meddic_score": meddic_evaluation.get("total_meddic_score", 0),
                "level": meddic_evaluation.get("qualification_level", "Unqualified")
            },
            "generated_at": date.today().isoformat()
        }
