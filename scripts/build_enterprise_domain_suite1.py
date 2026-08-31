import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/domain_services/lead_routing_engine.py
    write_file("backend/app/domain_services/lead_routing_engine.py", """import math
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
""")

    # 2. backend/app/domain_services/data_deduplication_engine.py
    write_file("backend/app/domain_services/data_deduplication_engine.py", """import math
import re
from typing import Any, Dict, List, Set, Tuple

class FuzzyDeduplicationEngine:
    @staticmethod
    def normalize_string(val: Optional[str]) -> str:
        if not val:
            return ""
        # Lowercase, remove special characters and extra whitespace
        cleaned = re.sub(r"[^a-zA-Z0-9\s]", "", val.lower())
        return re.sub(r"\s+", " ", cleaned).strip()

    @staticmethod
    def levenshtein_distance(s1: str, s2: str) -> int:
        if len(s1) < len(s2):
            return FuzzyDeduplicationEngine.levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    @staticmethod
    def similarity_ratio(s1: str, s2: str) -> float:
        n1 = FuzzyDeduplicationEngine.normalize_string(s1)
        n2 = FuzzyDeduplicationEngine.normalize_string(s2)
        if not n1 and not n2:
            return 1.0
        if not n1 or not n2:
            return 0.0
        max_len = max(len(n1), len(n2))
        dist = FuzzyDeduplicationEngine.levenshtein_distance(n1, n2)
        return round((max_len - dist) / max_len, 4)

    @staticmethod
    def find_duplicate_contacts(
        target_contact: Dict[str, Any],
        existing_contacts: List[Dict[str, Any]],
        threshold: float = 0.85
    ) -> List[Dict[str, Any]]:
        matches = []
        target_email = (target_contact.get("email") or "").lower().strip()
        target_name = f"{target_contact.get('first_name', '')} {target_contact.get('last_name', '')}".strip()
        target_phone = re.sub(r"\D", "", target_contact.get("phone") or "")

        for existing in existing_contacts:
            score = 0.0
            reasons = []

            # 1. Exact Email Match (Score 1.0)
            ex_email = (existing.get("email") or "").lower().strip()
            if target_email and ex_email and target_email == ex_email:
                score = 1.0
                reasons.append("Exact Email Match")

            # 2. Exact Phone Match
            ex_phone = re.sub(r"\D", "", existing.get("phone") or "")
            if target_phone and ex_phone and target_phone == ex_phone:
                score = max(score, 0.95)
                reasons.append("Exact Phone Match")

            # 3. Fuzzy Name Similarity
            ex_name = f"{existing.get('first_name', '')} {existing.get('last_name', '')}".strip()
            name_sim = FuzzyDeduplicationEngine.similarity_ratio(target_name, ex_name)
            if name_sim >= threshold and score < 0.90:
                score = max(score, name_sim * 0.90)
                reasons.append(f"Fuzzy Name Match ({name_sim * 100:.1f}%)")

            if score >= threshold:
                matches.append({
                    "candidate_id": existing.get("id"),
                    "matched_contact": existing,
                    "confidence_score": round(score, 2),
                    "match_reasons": reasons
                })

        return sorted(matches, key=lambda x: x["confidence_score"], reverse=True)
""")

    # 3. backend/app/domain_services/dynamic_formula_engine.py
    write_file("backend/app/domain_services/dynamic_formula_engine.py", """import math
import re
from datetime import datetime, date
from typing import Any, Dict, List, Optional, Union

class DynamicFormulaEngine:
    FUNCTIONS = {
        "UPPER": lambda val: str(val).upper() if val is not None else "",
        "LOWER": lambda val: str(val).lower() if val is not None else "",
        "CONCAT": lambda *args: "".join(str(a) for a in args if a is not None),
        "ROUND": lambda num, decimals=2: round(float(num), int(decimals)),
        "ABS": lambda num: abs(float(num)),
        "MAX": lambda *args: max(float(a) for a in args),
        "MIN": lambda *args: min(float(a) for a in args),
        "IF": lambda cond, true_val, false_val: true_val if cond else false_val,
        "NOW": lambda: datetime.utcnow().isoformat(),
        "TODAY": lambda: date.today().isoformat()
    }

    @staticmethod
    def evaluate_formula(formula_str: str, context: Dict[str, Any]) -> Any:
        expression = formula_str.strip()
        
        # Replace context variables enclosed in braces e.g. {deal.value} * {deal.tax_rate}
        def replace_var(match):
            var_name = match.group(1).strip()
            # Support dotted navigation e.g. company.revenue
            parts = var_name.split(".")
            curr = context
            for p in parts:
                if isinstance(curr, dict) and p in curr:
                    curr = curr[p]
                else:
                    return "0"
            return str(curr)

        parsed_expr = re.sub(r"\{([a-zA-Z0-9_\.]+)\}", replace_var, expression)
        
        try:
            # Safe evaluation with restricted globals
            from backend.app.workflow.ast_evaluator import SafeExpressionEvaluator
            return SafeExpressionEvaluator.evaluate(parsed_expr, context)
        except Exception:
            return parsed_expr
""")

    print("Domain services created.")

if __name__ == '__main__':
    run()
