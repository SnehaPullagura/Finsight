import re
from typing import Any, Dict, List, Union

def mask_account_number(acc_num: str) -> str:
    if not acc_num or len(acc_num) < 4:
        return "XXXX"
    return f"XXXX-XXXX-{acc_num[-4:]}"

def mask_card_number(card_num: str) -> str:
    clean = re.sub(r"\D", "", card_num or "")
    if len(clean) < 4:
        return "•••• •••• •••• ••••"
    return f"•••• •••• •••• {clean[-4:]}"

def mask_email(email: str) -> str:
    if not email or "@" not in email:
        return "u***@domain.com"
    parts = email.split("@", 1)
    username, domain = parts[0], parts[1]
    if len(username) <= 2:
        masked_user = username[0] + "***"
    else:
        masked_user = username[:2] + "***" + username[-1]
    return f"{masked_user}@{domain}"

def mask_pan_or_tax_id(tax_id: str) -> str:
    if not tax_id or len(tax_id) < 4:
        return "XXXXXX"
    return f"{tax_id[:2]}XXXXX{tax_id[-2:]}"

def sanitize_audit_payload(data: Union[Dict[str, Any], List[Any], Any]) -> Any:
    sensitive_keys = {
        "password", "password_hash", "secret", "token", "refresh_token",
        "access_token", "cvv", "card_number", "pin", "api_key"
    }
    if isinstance(data, dict):
        sanitized = {}
        for k, v in data.items():
            if k.lower() in sensitive_keys:
                sanitized[k] = "[REDACTED]"
            elif isinstance(v, (dict, list)):
                sanitized[k] = sanitize_audit_payload(v)
            else:
                sanitized[k] = v
        return sanitized
    elif isinstance(data, list):
        return [sanitize_audit_payload(item) for item in data]
    return data
