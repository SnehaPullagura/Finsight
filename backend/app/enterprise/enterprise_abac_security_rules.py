from typing import Any, Dict, List, Optional

class EnterpriseABACSecurityRules:
    @staticmethod
    def get_security_policy_definitions() -> List[Dict[str, Any]]:
        return [
            {
                "policy_id": "pol-deal-export-001",
                "name": "Restrict Deal Pipeline Bulk Export to Executives & Admins",
                "resource": "deals",
                "action": "export",
                "effect": "allow",
                "conditions": {"roles": ["Admin", "VP of Sales", "Executive"]}
            },
            {
                "policy_id": "pol-pii-masking-002",
                "name": "Mask Customer Credit Card & Sensitive PII from Support Tier 1",
                "resource": "contacts.pii",
                "action": "read_unmasked",
                "effect": "deny",
                "conditions": {"roles": ["Support Tier 1", "Guest"]}
            },
            {
                "policy_id": "pol-discount-approval-003",
                "name": "Enforce Multi-Tier Approval on Quote Discounts Exceeding 20%",
                "resource": "quotes",
                "action": "issue_discount_above_20_pct",
                "effect": "allow",
                "conditions": {"roles": ["Sales Manager", "VP of Sales", "Admin"]}
            }
        ]
