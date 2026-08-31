import hashlib
import uuid
from typing import Any, Dict, List, Optional

class GDPRAnonymizerService:
    @staticmethod
    def anonymize_contact_record(contact: Dict[str, Any], salt_key: str = "gdpr_crypto_salt") -> Dict[str, Any]:
        cid = contact.get("id", str(uuid.uuid4()))
        anon_hash = hashlib.sha256(f"{cid}_{salt_key}".encode()).hexdigest()[:12]

        anonymized = dict(contact)
        anonymized["first_name"] = "GDPR_ANONYMIZED"
        anonymized["last_name"] = f"USER_{anon_hash}"
        anonymized["email"] = f"erased_{anon_hash}@erasure.internal"
        anonymized["phone"] = "[REDACTED_GDPR_ART_17]"
        anonymized["title"] = "[ANONYMIZED]"
        anonymized["notes"] = "[ALL_COMMUNICATIONS_PURGED_UNDER_GDPR]"
        anonymized["is_anonymized"] = True

        return anonymized
