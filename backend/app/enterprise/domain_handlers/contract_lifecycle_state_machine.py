from datetime import date
from typing import Any, Dict, List, Optional, Tuple

class ContractLifecycleStateMachine:
    VALID_TRANSITIONS = {
        "draft": ["internal_review", "discarded"],
        "internal_review": ["approved", "changes_requested", "draft"],
        "approved": ["out_for_signature", "internal_review"],
        "out_for_signature": ["signed", "rejected", "expired"],
        "signed": ["active", "terminated"],
        "active": ["renewal_pending", "amended", "terminated", "expired"],
        "renewal_pending": ["renewed", "expired", "terminated"],
        "amended": ["active"],
        "renewed": ["active"],
        "expired": [],
        "terminated": [],
        "discarded": []
    }

    @staticmethod
    def transition_state(
        current_state: str,
        target_state: str,
        actor_id: str,
        actor_role: str
    ) -> Tuple[bool, Optional[str]]:
        cur = current_state.lower()
        tgt = target_state.lower()

        allowed = ContractLifecycleStateMachine.VALID_TRANSITIONS.get(cur, [])
        if tgt not in allowed:
            return False, f"Invalid transition from state '{cur}' to '{tgt}'."

        # Role-based state transition gates
        if tgt == "approved" and actor_role not in ["Legal", "VP of Sales", "Admin"]:
            return False, "Only Legal Counsel or VP of Sales can approve contracts."

        if tgt == "active" and cur != "signed" and actor_role != "Admin":
            return False, "Contract must be signed by all parties before activation."

        return True, None
