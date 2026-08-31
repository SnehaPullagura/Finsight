from typing import Any, Dict, List, Tuple

class DealStageGateValidator:
    GATE_REQUIREMENTS = {
        "discovery": ["contact_id", "company_id", "lead_source"],
        "scoping": ["estimated_budget", "decision_maker_identified"],
        "proposal": ["proposal_document_id", "line_items_count"],
        "negotiation": ["legal_review_approved", "contract_terms_agreed"],
        "closed_won": ["signed_contract_id", "payment_method_verified"]
    }

    @staticmethod
    def validate_stage_transition(
        target_stage: str,
        deal_attributes: Dict[str, Any]
    ) -> Tuple[bool, List[str]]:
        stage_key = target_stage.lower()
        required_fields = DealStageGateValidator.GATE_REQUIREMENTS.get(stage_key, [])

        missing_fields = []
        for req in required_fields:
            val = deal_attributes.get(req)
            if val is None or val == "" or val is False:
                missing_fields.append(req)

        is_valid = len(missing_fields) == 0
        return is_valid, missing_fields
