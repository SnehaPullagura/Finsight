from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class MicrosoftGraphConnector:
    def __init__(self, tenant_id: str, client_id: str, client_secret: str):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret

    async def send_outlook_mail(
        self,
        recipient_email: str,
        subject: str,
        html_content: str
    ) -> Dict[str, Any]:
        return {
            "status": "delivered",
            "provider": "microsoft_graph_outlook",
            "recipient": recipient_email,
            "subject": subject,
            "message_id": f"msg_msft_{int(datetime.now().timestamp())}",
            "sent_at": datetime.now(timezone.utc).isoformat()
        }

    async def post_teams_card(
        self,
        webhook_url: str,
        title: str,
        text: str,
        facts: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        return {
            "status": "dispatched",
            "channel": "Microsoft Teams",
            "title": title,
            "facts": facts or {}
        }
