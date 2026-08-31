from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

class PipelineAutomationService:
    STAGE_PROBABILITIES = {
        "discovery": 20,
        "scoping": 40,
        "proposal": 60,
        "negotiation": 80,
        "closed_won": 100,
        "closed_lost": 0
    }

    @staticmethod
    def evaluate_deal_advancement(
        deal: Dict[str, Any],
        completed_activities: List[Dict[str, Any]],
        has_accepted_proposal: bool = False
    ) -> Dict[str, Any]:
        current_stage = (deal.get("stage") or "discovery").lower()
        deal_id = deal.get("id")

        if current_stage == "discovery":
            # Advance to scoping if at least 1 discovery call was logged
            has_call = any(a.get("activity_type") in ["CALL", "MEETING"] for a in completed_activities)
            if has_call:
                return {"should_advance": True, "target_stage": "scoping", "reason": "Discovery meeting completed"}

        elif current_stage == "scoping":
            # Advance to proposal if scoping document or email sent
            has_scope = any(a.get("activity_type") in ["EMAIL", "NOTE"] for a in completed_activities)
            if has_scope:
                return {"should_advance": True, "target_stage": "proposal", "reason": "Scoping requirements verified"}

        elif current_stage == "proposal":
            if has_accepted_proposal:
                return {"should_advance": True, "target_stage": "negotiation", "reason": "Customer accepted formal proposal"}

        elif current_stage == "negotiation":
            if has_accepted_proposal and deal.get("is_contract_signed"):
                return {"should_advance": True, "target_stage": "closed_won", "reason": "Contract executed by both parties"}

        return {"should_advance": False, "target_stage": current_stage, "reason": "Stage entry criteria not yet satisfied"}
