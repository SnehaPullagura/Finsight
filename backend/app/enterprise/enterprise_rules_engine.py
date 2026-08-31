import re
from typing import Any, Dict, List, Optional, Tuple, Callable

class EnterpriseRuleCondition:
    def __init__(self, field: str, operator: str, value: Any):
        self.field = field
        self.operator = operator # eq, neq, gt, gte, lt, lte, in, not_in, contains, regex
        self.value = value

    def evaluate(self, entity_data: Dict[str, Any]) -> bool:
        actual = entity_data.get(self.field)
        
        if self.operator == "eq":
            return actual == self.value
        elif self.operator == "neq":
            return actual != self.value
        elif self.operator == "gt":
            return actual is not None and float(actual) > float(self.value)
        elif self.operator == "gte":
            return actual is not None and float(actual) >= float(self.value)
        elif self.operator == "lt":
            return actual is not None and float(actual) < float(self.value)
        elif self.operator == "lte":
            return actual is not None and float(actual) <= float(self.value)
        elif self.operator == "in":
            return actual in self.value if isinstance(self.value, (list, set, tuple)) else False
        elif self.operator == "not_in":
            return actual not in self.value if isinstance(self.value, (list, set, tuple)) else True
        elif self.operator == "contains":
            return str(self.value).lower() in str(actual).lower() if actual is not None else False
        elif self.operator == "regex":
            return bool(re.search(str(self.value), str(actual))) if actual is not None else False
        return False

class EnterpriseBusinessRule:
    def __init__(self, rule_id: str, name: str, conditions: List[EnterpriseRuleCondition], match_type: str = "ALL"):
        self.rule_id = rule_id
        self.name = name
        self.conditions = conditions
        self.match_type = match_type # ALL, ANY

    def matches(self, entity_data: Dict[str, Any]) -> bool:
        if not self.conditions:
            return True
        if self.match_type == "ALL":
            return all(c.evaluate(entity_data) for c in self.conditions)
        else:
            return any(c.evaluate(entity_data) for c in self.conditions)

class EnterpriseRulesEngine:
    def __init__(self, rules: Optional[List[EnterpriseBusinessRule]] = None):
        self.rules = rules or []

    def evaluate_rules(self, entity_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        matched = []
        for rule in self.rules:
            if rule.matches(entity_data):
                matched.append({
                    "rule_id": rule.rule_id,
                    "rule_name": rule.name,
                    "matched": True
                })
        return matched
