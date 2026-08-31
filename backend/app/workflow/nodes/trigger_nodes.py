from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class WorkflowTriggerNode:
    def __init__(self, node_id: str, trigger_type: str, configuration: Dict[str, Any]):
        self.node_id = node_id
        self.trigger_type = trigger_type # webhook, entity_created, status_changed, sla_breach, cron
        self.configuration = configuration

    def evaluate_trigger(self, event_data: Dict[str, Any]) -> bool:
        if self.trigger_type == "entity_created":
            return event_data.get("event") == "created" and event_data.get("entity_type") == self.configuration.get("entity_type")
        elif self.trigger_type == "status_changed":
            return (
                event_data.get("entity_type") == self.configuration.get("entity_type") and
                event_data.get("new_status") == self.configuration.get("target_status")
            )
        elif self.trigger_type == "sla_breach":
            return bool(event_data.get("is_breached", False))
        return True
