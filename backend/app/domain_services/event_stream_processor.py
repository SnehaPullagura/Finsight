import json
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

class CRMEventEnvelope:
    def __init__(self, event_type: str, tenant_id: str, payload: Dict[str, Any], actor_id: Optional[str] = None):
        self.event_id = f"evt_{int(datetime.now(timezone.utc).timestamp() * 1000)}"
        self.event_type = event_type
        self.tenant_id = tenant_id
        self.payload = payload
        self.actor_id = actor_id
        self.timestamp = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "tenant_id": self.tenant_id,
            "actor_id": self.actor_id,
            "timestamp": self.timestamp,
            "payload": self.payload
        }

class EventStreamProcessor:
    def __init__(self):
        self._handlers = {}
        self._event_journal = []

    def subscribe(self, event_type: str, handler: Callable[[CRMEventEnvelope], Any]):
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    async def publish(self, event: CRMEventEnvelope) -> List[Dict[str, Any]]:
        self._event_journal.append(event.to_dict())
        results = []

        handlers = self._handlers.get(event.event_type, [])
        for h in handlers:
            try:
                res = await h(event) if hasattr(h, "__await__") else h(event)
                results.append({"handler": getattr(h, "__name__", "anonymous"), "status": "success", "result": res})
            except Exception as e:
                results.append({"handler": getattr(h, "__name__", "anonymous"), "status": "error", "error": str(e)})

        return results
