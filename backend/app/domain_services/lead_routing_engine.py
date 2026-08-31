import math
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

class LeadRoutingRule:
    def __init__(
        self,
        rule_id: str,
        name: str,
        criteria: Dict[str, Any],
        assignee_type: str, # user, round_robin_team, territory_pool
        assignee_id: str,
        priority: int = 1
    ):
        self.rule_id = rule_id
        self.name = name
        self.criteria = criteria
        self.assignee_type = assignee_type
        self.assignee_id = assignee_id
        self.priority = priority

    def matches(self, lead_data: Dict[str, Any]) -> bool:
        for key, expected_val in self.criteria.items():
            actual_val = lead_data.get(key)
            if isinstance(expected_val, list):
                if actual_val not in expected_val:
                    return False
            elif isinstance(expected_val, dict):
                # Range comparison (e.g. {"gte": 1000, "lte": 50000})
                if "gte" in expected_val and (actual_val is None or actual_val < expected_val["gte"]):
                    return False
                if "lte" in expected_val and (actual_val is None or actual_val > expected_val["lte"]):
                    return False
            else:
                if actual_val != expected_val:
                    return False
        return True

class RoundRobinRouter:
    def __init__(self, team_members: List[str]):
        self.team_members = team_members
        self._current_index = 0

    def get_next_assignee(self) -> Optional[str]:
        if not self.team_members:
            return None
        assignee = self.team_members[self._current_index % len(self.team_members)]
        self._current_index += 1
        return assignee

class LeadRoutingEngine:
    def __init__(self, rules: List[LeadRoutingRule], round_robin_pools: Optional[Dict[str, List[str]]] = None):
        self.rules = sorted(rules, key=lambda r: r.priority)
        self.round_robin_routers = {
            team_id: RoundRobinRouter(members)
            for team_id, members in (round_robin_pools or {}).items()
        }

    def route_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        timestamp = datetime.now(timezone.utc).isoformat()
        
        for rule in self.rules:
            if rule.matches(lead_data):
                assigned_user = None
                
                if rule.assignee_type == "user":
                    assigned_user = rule.assignee_id
                elif rule.assignee_type == "round_robin_team":
                    router = self.round_robin_routers.get(rule.assignee_id)
                    if router:
                        assigned_user = router.get_next_assignee()

                if assigned_user:
                    return {
                        "status": "routed",
                        "assigned_to": assigned_user,
                        "matched_rule_id": rule.rule_id,
                        "matched_rule_name": rule.name,
                        "routing_timestamp": timestamp
                    }

        return {
            "status": "unassigned",
            "assigned_to": None,
            "matched_rule_id": None,
            "matched_rule_name": "Default Fallback",
            "routing_timestamp": timestamp
        }
