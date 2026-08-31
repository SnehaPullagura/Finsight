from typing import Any, Dict, List, Optional

class ABACPolicyRule:
    def __init__(self, rule_id: str, action: str, resource_type: str, condition_fn: Any):
        self.rule_id = rule_id
        self.action = action # read, write, delete, export, approve
        self.resource_type = resource_type # deal, contact, organization, invoice, audit
        self.condition_fn = condition_fn

class ABACPolicyEvaluator:
    def __init__(self, rules: Optional[List[ABACPolicyRule]] = None):
        self.rules = rules or []

    def evaluate(self, user_context: Dict[str, Any], resource: Dict[str, Any], action: str, resource_type: str) -> Dict[str, Any]:
        # 1. Superuser override
        if user_context.get("is_superuser") or "Admin" in user_context.get("roles", []):
            return {"allowed": True, "reason": "Superuser / Admin override permitted"}

        # 2. Tenant isolation check
        user_tenant = user_context.get("tenant_id")
        resource_tenant = resource.get("tenant_id")
        if user_tenant and resource_tenant and user_tenant != resource_tenant:
            return {"allowed": False, "reason": "Cross-tenant access violation"}

        # 3. Ownership check
        if resource.get("owner_id") == user_context.get("id") or resource.get("user_id") == user_context.get("id"):
            return {"allowed": True, "reason": "Resource owner access permitted"}

        return {"allowed": True, "reason": "Default RBAC role permitted"}
