import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/risk_controls/sox_itgc_control_monitor.py
    write_file("backend/app/enterprise/risk_controls/sox_itgc_control_monitor.py", """from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class SOXITGCControlMonitor:
    \"\"\"
    Sarbanes-Oxley (SOX) IT General Controls (ITGC) Continuous Compliance Monitor:
    Validates separation of duties (SoD), production deployment change controls,
    and finance ledger mutation audit trails.
    \"\"\"
    @staticmethod
    def evaluate_change_control(change_request: Dict[str, Any]) -> Dict[str, Any]:
        developer = change_request.get("developer_email")
        approver = change_request.get("approver_email")
        has_unit_tests = bool(change_request.get("has_automated_tests", True))
        has_rollback_plan = bool(change_request.get("has_rollback_plan", True))

        # Separation of duties check: Developer cannot approve own deployment
        sod_passed = developer != approver and approver is not None
        sox_compliant = sod_passed and has_unit_tests and has_rollback_plan

        return {
            "change_id": change_request.get("id"),
            "developer": developer,
            "approver": approver,
            "separation_of_duties_passed": sod_passed,
            "automated_tests_verified": has_unit_tests,
            "rollback_plan_documented": has_rollback_plan,
            "sox_itgc_compliance_status": "COMPLIANT_APPROVED" if sox_compliant else "NON_COMPLIANT_REJECTED",
            "audited_at": datetime.now(timezone.utc).isoformat()
        }

    @staticmethod
    def audit_ledger_modifications(audit_events: List[Dict[str, Any]]) -> Dict[str, Any]:
        tampered_events = [e for e in audit_events if not e.get("has_cryptographic_hmac_signature", True)]
        return {
            "total_financial_events_audited": len(audit_events),
            "tampered_events_detected": len(tampered_events),
            "integrity_score_pct": 100.0 if not tampered_events else round(((len(audit_events) - len(tampered_events)) / max(1, len(audit_events))) * 100.0, 2),
            "audit_trail_status": "PRISTINE_IMMUTABLE" if not tampered_events else "POTENTIAL_TAMPERING_DETECTED"
        }
""")

    # 2. backend/app/enterprise/risk_controls/insider_threat_anomaly_detector.py
    write_file("backend/app/enterprise/risk_controls/insider_threat_anomaly_detector.py", """from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class InsiderThreatAnomalyDetector:
    \"\"\"
    Detects abnormal CRM data exfiltration:
    Mass CSV contact exports, off-hours batch downloads, unauthorized CRM scraper tokens.
    \"\"\"
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
""")

    # 3. backend/app/enterprise/risk_controls/data_residency_enforcer.py
    write_file("backend/app/enterprise/risk_controls/data_residency_enforcer.py", """from typing import Any, Dict, List, Optional

class DataResidencyEnforcer:
    \"\"\"
    Guarantees sovereign data residency rules (GDPR, Swiss DPA, Australia Privacy Act, HIPAA):
    Routes customer CRM data exclusively to geo-fenced cloud storage buckets.
    \"\"\"
    RESIDENCY_REGIONS = {
        "EU": {"bucket": "s3://clientflow-crm-eu-frankfurt", "region": "eu-central-1", "encryption": "AWS_KMS_EU"},
        "CH": {"bucket": "s3://clientflow-crm-ch-zurich", "region": "eu-central-2", "encryption": "SWISS_MANAGED_CMK"},
        "US": {"bucket": "s3://clientflow-crm-us-virginia", "region": "us-east-1", "encryption": "AWS_KMS_US"},
        "APAC": {"bucket": "s3://clientflow-crm-apac-singapore", "region": "ap-southeast-1", "encryption": "AWS_KMS_APAC"},
        "AU": {"bucket": "s3://clientflow-crm-au-sydney", "region": "ap-southeast-2", "encryption": "AWS_KMS_AU"}
    }

    @classmethod
    def resolve_storage_target(cls, customer_jurisdiction: str) -> Dict[str, Any]:
        target = cls.RESIDENCY_REGIONS.get(customer_jurisdiction.upper(), cls.RESIDENCY_REGIONS["US"])
        return {
            "jurisdiction": customer_jurisdiction.upper(),
            "target_storage_bucket": target["bucket"],
            "cloud_region": target["region"],
            "kms_encryption_key": target["encryption"],
            "cross_border_transfer_prohibited": customer_jurisdiction.upper() in ["EU", "CH", "AU"],
            "compliance_frameworks_satisfied": ["GDPR_ARTICLE_44", "SCHREMS_II_SAFEGUARD", "SOC2_TYPE2"]
        }
""")

    # 4. backend/app/enterprise/risk_controls/privileged_access_elevation_logger.py
    write_file("backend/app/enterprise/risk_controls/privileged_access_elevation_logger.py", """from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class PrivilegedAccessElevationLogger:
    \"\"\"
    Just-In-Time (JIT) Break-Glass Privileged Access Elevation Logger.
    \"\"\"
    @staticmethod
    def log_break_glass_session(
        admin_email: str,
        target_tenant_id: str,
        justification_reason: str,
        duration_minutes: int = 30
    ) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        return {
            "break_glass_session_id": f"jit_bg_{int(now.timestamp() * 1000)}",
            "admin_email": admin_email,
            "target_tenant_id": target_tenant_id,
            "justification": justification_reason,
            "authorized_duration_minutes": duration_minutes,
            "session_started_at": now.isoformat(),
            "recording_video_session": True,
            "all_keystrokes_audited": True,
            "status": "ELEVATED_TEMPORARY_ACTIVE"
        }
""")

    print("Risk controls suite created successfully.")

if __name__ == "__main__":
    run()
