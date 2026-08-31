from typing import Any, Dict, List, Optional

class ExpansionOpportunityDigestBuilder:
    @staticmethod
    def build_weekly_digest(expansion_candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_potential_arr = sum(float(c.get("projected_expansion_arr", 0.0)) for c in expansion_candidates)
        top_candidates = sorted(expansion_candidates, key=lambda x: float(x.get("projected_expansion_arr", 0.0)), reverse=True)[:5]

        return {
            "digest_title": "Weekly Customer Success Expansion & Upsell Intelligence Digest",
            "total_qualified_expansion_accounts": len(expansion_candidates),
            "total_addressable_expansion_pipeline": round(total_potential_arr, 2),
            "top_expansion_opportunities": top_candidates,
            "digest_generated_status": "READY_FOR_SLACK_AND_EMAIL_DISPATCH"
        }
