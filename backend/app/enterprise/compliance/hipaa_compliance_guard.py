import re
from typing import Any, Dict, List, Optional

class HIPAAComplianceGuard:
    PHI_FIELD_PATTERNS = [
        r"(?i)(ssn|social\s*security)",
        r"(?i)(dob|date\s*of\s*birth)",
        r"(?i)(medical|diagnosis|patient|prescription|treatment|health)",
        r"(?i)(insurance|policy\s*num|medicaid|medicare)"
    ]

    @staticmethod
    def sanitize_phi_payload(payload: Dict[str, Any], is_authorized_medical_actor: bool = False) -> Dict[str, Any]:
        if is_authorized_medical_actor:
            return payload

        sanitized = {}
        for k, v in payload.items():
            is_phi = any(re.search(pat, k) for pat in HIPAAComplianceGuard.PHI_FIELD_PATTERNS)
            if is_phi and isinstance(v, str):
                # Redact PHI field
                sanitized[k] = f"[REDACTED_HIPAA_PHI::{k.upper()}]"
            elif isinstance(v, dict):
                sanitized[k] = HIPAAComplianceGuard.sanitize_phi_payload(v, is_authorized_medical_actor)
            else:
                sanitized[k] = v

        return sanitized
