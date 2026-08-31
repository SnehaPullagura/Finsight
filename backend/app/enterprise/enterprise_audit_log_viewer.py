from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class EnterpriseAuditLogViewer:
    @staticmethod
    def filter_and_format_audit_trail(
        audit_records: List[Dict[str, Any]],
        actor_id: Optional[str] = None,
        entity_type: Optional[str] = None,
        action: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        filtered = []
        for r in audit_records:
            if actor_id and r.get("actor_id") != actor_id:
                continue
            if entity_type and r.get("entity_type") != entity_type:
                continue
            if action and r.get("action") != action:
                continue

            formatted = dict(r)
            formatted["display_summary"] = f"{r.get('action', 'UPDATED').upper()} on {r.get('entity_type', 'Entity')} [{r.get('entity_id', '')}] by {r.get('actor_email', 'System')}"
            filtered.append(formatted)

        return sorted(filtered, key=lambda x: x.get("timestamp", ""), reverse=True)
