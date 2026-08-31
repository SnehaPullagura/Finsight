import re
from typing import Any, Dict, List, Optional

class DataQualitySanitizer:
    @staticmethod
    def sanitize_phone_number(raw_phone: Optional[str], default_country_code: str = "+1") -> Optional[str]:
        if not raw_phone:
            return None
        digits_only = re.sub(r"\D", "", raw_phone)
        if len(digits_only) == 10:
            return f"{default_country_code}-{digits_only[:3]}-{digits_only[3:6]}-{digits_only[6:]}"
        elif len(digits_only) == 11 and digits_only.startswith("1"):
            return f"+1-{digits_only[1:4]}-{digits_only[4:7]}-{digits_only[7:]}"
        return f"+{digits_only}" if digits_only else None

    @staticmethod
    def clean_company_name(raw_name: Optional[str]) -> str:
        if not raw_name:
            return ""
        cleaned = re.sub(r"(?i)(inc|incorporated|corp|corporation|llc|ltd|limited|gmbh|co)\.?", "", raw_name)
        return re.sub(r"\s+", " ", cleaned).strip().title()
