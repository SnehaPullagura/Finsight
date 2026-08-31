import re
from typing import Any, Dict, List, Optional

class EnterpriseDataMaskingEngine:
    @staticmethod
    def mask_email(email: Optional[str]) -> str:
        if not email or "@" not in email:
            return "***@***.***"
        name_part, domain = email.split("@", 1)
        if len(name_part) <= 2:
            masked_name = name_part[0] + "*"
        else:
            masked_name = name_part[0] + ("*" * (len(name_part) - 2)) + name_part[-1]
        return f"{masked_name}@{domain}"

    @staticmethod
    def mask_phone(phone: Optional[str]) -> str:
        if not phone:
            return "***-***-****"
        digits = re.sub(r"\D", "", phone)
        if len(digits) >= 4:
            return f"***-***-{digits[-4:]}"
        return "***-***-****"
