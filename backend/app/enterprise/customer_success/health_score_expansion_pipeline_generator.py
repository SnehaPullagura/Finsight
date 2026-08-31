from typing import Any, Dict, List, Optional

class ExpansionPipelineGenerator:
    @staticmethod
    def generate_expansion_deals(expansion_candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        deals = []
        for cand in expansion_candidates:
            cid = cand.get("account_id")
            cname = cand.get("account_name")
            expansion_arr = float(cand.get("projected_expansion_arr", 25000.0))

            deals.append({
                "deal_name": f"{cname} — Expansion & Add-On License",
                "account_id": cid,
                "pipeline_stage": "Discovery",
                "deal_value": expansion_arr,
                "probability": 75,
                "expected_close_in_days": 30,
                "deal_type": "Existing Customer Expansion",
                "lead_source": "Automated CS Health Signal"
            })

        return deals
