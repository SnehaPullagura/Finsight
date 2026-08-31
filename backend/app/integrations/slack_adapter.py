from typing import Any, Dict, List
from backend.app.integrations.base import BaseIntegrationAdapter

class SlackIntegrationAdapter(BaseIntegrationAdapter):
    async def test_connection(self) -> bool:
        return bool(self.config.get("webhook_url"))

    async def sync_data(self, entity_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "dispatched", "channel": self.config.get("channel", "#sales-alerts")}

    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        return True

    @staticmethod
    def format_deal_won_block(deal_name: str, deal_value: float, rep_name: str, currency: str = "USD") -> Dict[str, Any]:
        return {
            "blocks": [
                {
                    "type": "header",
                    "text": {"type": "plain_text", "text": f"🎉 Deal Won: {deal_name}!"}
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*Amount:*
{currency} {deal_value:,.2f}"},
                        {"type": "mrkdwn", "text": f"*Owner:*
{rep_name}"}
                    ]
                }
            ]
        }
