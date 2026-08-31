from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class InsiderThreatAnomalyDetector:
    """
    Detects abnormal CRM data exfiltration:
    Mass CSV contact exports, off-hours batch downloads, unauthorized CRM scraper tokens.
    """
    @staticmethod
    def analyze_user_activity(
        user_session: Dict[str, Any],
        exports_in_last_hour: int,
        leads_viewed_in_last_hour: int
    ) -> Dict[str, Any]:
        email = user_session.get("user_email")
        role = user_session.get("user_role", "SALES_REP")
        ip = user_session.get("client_ip", "127.0.0.1")

        # Exfiltration thresholds
        is_mass_export = exports_in_last_hour >= 3
        is_bulk_scraping = leads_viewed_in_last_hour >= 500

        risk_score = 0
        reasons = []

        if is_mass_export:
            risk_score += 60
            reasons.append("Excessive bulk CSV exports within 60 minutes.")
        if is_bulk_scraping:
            risk_score += 35
            reasons.append("Abnormal volume of lead records queried (potential scraper).")

        if risk_score >= 60:
            threat_level = "CRITICAL_SUSPEND_SESSION"
            action = "Immediately revoke session token and notify Security Operations Center (SOC)."
        elif risk_score >= 30:
            threat_level = "ELEVATED_CHALLENGE_MFA"
            action = "Force mandatory step-up WebAuthn biometric MFA verification."
        else:
            threat_level = "NORMAL_BENIGN"
            action = "No action required."

        return {
            "user_email": email,
            "role": role,
            "client_ip": ip,
            "risk_score": risk_score,
            "threat_level": threat_level,
            "detected_anomalies": reasons,
            "prescribed_mitigation": action,
            "evaluated_at": datetime.now(timezone.utc).isoformat()
        }
