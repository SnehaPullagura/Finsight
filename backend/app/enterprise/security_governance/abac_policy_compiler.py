from typing import Any, Dict, List, Optional

class ABACPolicyCompiler:
    @staticmethod
    def compile_policy_rules(policies: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        compiled = defaultdict(list)
        for p in policies:
            resource = p.get("resource", "*")
            compiled[resource].append(p)
        return dict(compiled)

    @staticmethod
    def evaluate_access(user: Dict[str, Any], resource_name: str, action: str, compiled_policies: Dict[str, List[Dict[str, Any]]]) -> bool:
        user_roles = set(user.get("roles", []))
        if "Admin" in user_roles or user.get("is_superuser"):
            return True

        matching_policies = compiled_policies.get(resource_name, []) + compiled_policies.get("*", [])
        for p in matching_policies:
            if p.get("action") in [action, "*"]:
                allowed_roles = set(p.get("conditions", {}).get("roles", []))
                if allowed_roles and user_roles.intersection(allowed_roles):
                    return p.get("effect", "allow") == "allow"

        return False
