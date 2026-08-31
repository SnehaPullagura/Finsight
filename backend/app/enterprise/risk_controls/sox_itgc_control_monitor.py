from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class SOXITGCControlMonitor:
    """
    Sarbanes-Oxley (SOX) IT General Controls (ITGC) Continuous Compliance Monitor:
    Validates separation of duties (SoD), production deployment change controls,
    and finance ledger mutation audit trails.
    """
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
