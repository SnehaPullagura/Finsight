import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict

class KafkaMessageSerializer:
    @staticmethod
    def build_event_message(topic: str, key: str, payload: Dict[str, Any], schema_version: str = "v1") -> Dict[str, Any]:
        return {
            "message_id": str(uuid.uuid4()),
            "topic": topic,
            "key": key,
            "headers": {
                "schema_version": schema_version,
                "content_type": "application/json",
                "timestamp": datetime.now(timezone.utc).isoformat()
            },
            "payload": payload
        }
