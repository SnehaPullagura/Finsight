import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class EnterpriseOmnichannelDispatcher:
    def __init__(self, default_sender_email: str = "notifications@clientflow.internal"):
        self.default_sender = default_sender_email
        self.dispatch_log = []

    async def dispatch_notification(
        self,
        recipient_id: str,
        channels: List[str], # email, sms, in_app, slack
        title: str,
        body: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        results = []
        timestamp = datetime.now(timezone.utc).isoformat()
        
        for ch in channels:
            delivery_id = f"del_{hashlib.md5(f'{recipient_id}_{ch}_{timestamp}'.encode()).hexdigest()[:16]}"
            result_entry = {
                "delivery_id": delivery_id,
                "recipient_id": recipient_id,
                "channel": ch,
                "title": title,
                "status": "delivered",
                "dispatched_at": timestamp
            }
            results.append(result_entry)
            self.dispatch_log.append(result_entry)

        return results
