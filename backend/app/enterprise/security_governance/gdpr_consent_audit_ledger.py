from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class GDPRConsentAuditLedger:
    @staticmethod
    def record_consent_decision(
        contact_id: str,
        consent_type: str, # marketing_email, data_processing, analytics_cookies
        granted: bool,
        ip_address: str,
        user_agent: str
    ) -> Dict[str, Any]:
        return {
            "consent_id": f"cns_{int(datetime.now(timezone.utc).timestamp() * 1000)}",
            "contact_id": contact_id,
            "consent_type": consent_type,
            "is_consent_granted": granted,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "compliance_proof": "VALID_GDPR_ARTICLE_7_RECORD"
        }
