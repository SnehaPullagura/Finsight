import asyncio
import json
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

class EventStreamEnvelope:
    def __init__(self, event_id: str, topic: str, tenant_id: str, payload: Dict[str, Any]):
        self.event_id = event_id
        self.topic = topic
        self.tenant_id = tenant_id
        self.payload = payload
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.retry_count = 0

class EnterpriseEventBroker:
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.subscribers = {}
        self.dead_letter_queue = []
        self.journal = []

    def subscribe(self, topic: str, handler: Callable[[EventStreamEnvelope], Any]):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(handler)

    async def publish(self, topic: str, tenant_id: str, payload: Dict[str, Any]) -> str:
        evt_id = f"evt_{int(datetime.now(timezone.utc).timestamp() * 1000)}"
        envelope = EventStreamEnvelope(evt_id, topic, tenant_id, payload)
        self.journal.append(envelope)

        handlers = self.subscribers.get(topic, [])
        for h in handlers:
            try:
                res = await h(envelope) if asyncio.iscoroutinefunction(h) else h(envelope)
            except Exception as e:
                envelope.retry_count += 1
                if envelope.retry_count > self.max_retries:
                    self.dead_letter_queue.append({"envelope": envelope, "error": str(e)})

        return evt_id
