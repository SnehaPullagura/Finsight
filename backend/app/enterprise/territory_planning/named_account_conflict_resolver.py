from typing import Any, Dict, List, Optional

class NamedAccountConflictResolver:
    """
    Resolves multi-rep territory conflicts: Parent/Subsidiary ownership,
    geographic overlap, and holding company splits.
    """
    @staticmethod
    def resolve_overlap(
        parent_account: Dict[str, Any],
        subsidiary_account: Dict[str, Any],
        parent_owner_id: str,
        sub_owner_id: str
    ) -> Dict[str, Any]:
        pname = parent_account.get("name")
        sname = subsidiary_account.get("name")

        # Global Account Rule: Parent company rep retains strategic ownership
        # while subsidiary rep receives split credit
        return {
            "conflict_type": "PARENT_SUBSIDIARY_OVERLAP",
            "parent_account": pname,
            "subsidiary_account": sname,
            "primary_strategic_owner_id": parent_owner_id,
            "local_territory_owner_id": sub_owner_id,
            "resolution_policy": "GLOBAL_ACCOUNT_DIRECTIVE",
            "commission_split": {
                "parent_owner_credit_pct": 70.0,
                "local_owner_credit_pct": 30.0
            },
            "governance_status": "RESOLVED_AUTO_APPROVED"
        }
