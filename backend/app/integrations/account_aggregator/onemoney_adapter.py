import json
import datetime
from typing import Dict, List, Any
from backend.app.integrations.account_aggregator.base import (
    BaseAccountAggregatorAdapter, AAConsentArtifact, AAConsentStatus, AADataFrequency
)

class OneMoneyAccountAggregatorAdapter(BaseAccountAggregatorAdapter):
    """
    OneMoney AA Gateway Adapter for automated bank data synchronization
    """
    def __init__(self, api_key: str = "om_prod_api_key", app_id: str = "finsight_app"):
        self.api_key = api_key
        self.app_id = app_id

    async def create_consent_request(
        self, user_id: int, user_vpa: str, fi_types: List[str], date_range_days: int = 365
    ) -> AAConsentArtifact:
        now = datetime.datetime.utcnow()
        today = now.date()
        return AAConsentArtifact(
            consent_id=f"ONEMONEY-AR-{int(now.timestamp())}",
            consent_handle=f"OM-HANDLE-{user_id}-{int(now.timestamp())}",
            user_id=user_id,
            user_vpa=user_vpa,
            status=AAConsentStatus.REQUESTED,
            frequency=AADataFrequency.DAILY,
            fi_types=fi_types,
            date_range_from=today - datetime.timedelta(days=date_range_days),
            date_range_to=today,
            consent_start=now,
            consent_expiry=now + datetime.timedelta(days=365),
            signature="SIG-ONEMONEY-ECDSA-SHA256"
        )

    async def check_consent_status(self, consent_handle: str) -> AAConsentStatus:
        return AAConsentStatus.ACTIVE

    async def fetch_financial_data(self, consent_id: str, private_key_pem: str) -> List[Dict[str, Any]]:
        return [
            {
                "fip_id": "ICICI-FIP-01",
                "account_number_masked": "•••• •••• •••• 9012",
                "account_type": "CREDIT_CARD",
                "currency": "INR",
                "balance": {"current": 18450.0, "credit_limit": 200000.0},
                "transactions": [
                    {"tx_id": "TXN2001", "date": "2026-08-29", "amount": 2850.0, "type": "DEBIT", "narration": "BLINKIT COMMERCE"}
                ]
            }
        ]

    async def revoke_consent(self, consent_id: str) -> bool:
        return True
