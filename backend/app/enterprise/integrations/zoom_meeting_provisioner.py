import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, Optional

class ZoomMeetingProvisioner:
    def __init__(self, account_id: str, client_id: str, client_secret: str):
        self.account_id = account_id
        self.client_id = client_id
        self.client_secret = client_secret

    async def create_instant_meeting(self, topic: str, start_time_iso: str, duration_minutes: int = 30) -> Dict[str, Any]:
        meeting_id = f"zm_{int(datetime.now(timezone.utc).timestamp() * 1000)}"
        
        return {
            "id": meeting_id,
            "topic": topic,
            "type": 2, # Scheduled meeting
            "start_time": start_time_iso,
            "duration": duration_minutes,
            "join_url": f"https://zoom.us/j/{meeting_id}?pwd=secure_hash_token",
            "password": hashlib.md5(meeting_id.encode()).hexdigest()[:8],
            "status": "waiting"
        }
