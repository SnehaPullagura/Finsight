import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/enterprise_rules_engine.py
    write_file("backend/app/enterprise/enterprise_rules_engine.py", """import re
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
""")

    # 2. backend/app/enterprise/enterprise_event_auditor.py
    write_file("backend/app/enterprise/enterprise_event_auditor.py", """import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class AuditBlock:
    def __init__(self, index: int, timestamp: str, tenant_id: str, actor_id: str, action: str, entity_type: str, entity_id: str, state_diff: Dict[str, Any], previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.tenant_id = tenant_id
        self.actor_id = actor_id
        self.action = action
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.state_diff = state_diff
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        payload = {
            "index": self.index,
            "timestamp": self.timestamp,
            "tenant_id": self.tenant_id,
            "actor_id": self.actor_id,
            "action": self.action,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "diff": self.state_diff,
            "previous_hash": self.previous_hash
        }
        serialized = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

class EnterpriseEventAuditor:
    def __init__(self):
        self.chain: List[AuditBlock] = []
        self._initialize_genesis_block()

    def _initialize_genesis_block(self):
        genesis = AuditBlock(
            index=0,
            timestamp=datetime.now(timezone.utc).isoformat(),
            tenant_id="system",
            actor_id="system",
            action="GENESIS",
            entity_type="SYSTEM",
            entity_id="0",
            state_diff={},
            previous_hash="0" * 64
        )
        self.chain.append(genesis)

    def record_event(self, tenant_id: str, actor_id: str, action: str, entity_type: str, entity_id: str, state_diff: Dict[str, Any]) -> AuditBlock:
        prev_block = self.chain[-1]
        block = AuditBlock(
            index=len(self.chain),
            timestamp=datetime.now(timezone.utc).isoformat(),
            tenant_id=tenant_id,
            actor_id=actor_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            state_diff=state_diff,
            previous_hash=prev_block.hash
        )
        self.chain.append(block)
        return block

    def verify_integrity(self) -> bool:
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]
            if curr.previous_hash != prev.hash:
                return False
            if curr.hash != curr.compute_hash():
                return False
        return True
""")

    print("Created rules engine and event auditor.")

if __name__ == '__main__':
    run()
