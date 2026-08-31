import hmac
import hashlib
import json
from typing import Any, Dict
from backend.app.integrations.base import BaseIntegrationAdapter

class StripeIntegrationAdapter(BaseIntegrationAdapter):
    async def test_connection(self) -> bool:
        api_key = self.config.get("api_key", "")
        return bool(api_key.startswith("sk_"))

    async def sync_data(self, entity_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        # Mock Stripe Customer / PaymentIntent creation
        return {
            "stripe_id": f"cus_mock_{data.get('id', '001')}",
            "status": "synchronized",
            "provider": "stripe",
            "entity": entity_type
        }

    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        secret = self.config.get("webhook_secret", "whsec_mock")
        computed = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
        return hmac.compare_digest(computed, signature.replace("t=", "").split(",")[-1].replace("v1=", ""))
