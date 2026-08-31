from typing import Any, Dict, List, Optional

class SessionIPGeofencingGuard:
    @staticmethod
    def validate_client_ip(client_ip: str, client_country: str, allowed_countries: List[str], ip_allowlist: List[str]) -> Dict[str, Any]:
        is_ip_allowed = client_ip in ip_allowlist if ip_allowlist else True
        is_geo_allowed = client_country.upper() in [c.upper() for c in allowed_countries] if allowed_countries else True

        is_authorized = is_ip_allowed and is_geo_allowed

        return {
            "client_ip": client_ip,
            "client_country": client_country,
            "is_ip_explicitly_whitelisted": client_ip in ip_allowlist,
            "is_geographically_permitted": is_geo_allowed,
            "is_session_authorized": is_authorized,
            "action": "ALLOW_LOGIN" if is_authorized else "CHALLENGE_WITH_MFA_OR_BLOCK"
        }
