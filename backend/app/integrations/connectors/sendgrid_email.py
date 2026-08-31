from typing import Any, Dict, List, Optional

class SendGridConnector:
    def __init__(self, api_key: str, default_from_email: str):
        self.api_key = api_key
        self.from_email = default_from_email

    async def send_dynamic_template_email(
        self,
        to_email: str,
        template_id: str,
        template_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            "status": "accepted",
            "provider": "sendgrid",
            "to": to_email,
            "template_id": template_id,
            "message_id": f"sg_msg_{template_id[:8]}"
        }
