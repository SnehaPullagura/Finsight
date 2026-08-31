from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class SOC2ComplianceValidator:
    @staticmethod
    def audit_security_controls(system_config: Dict[str, Any]) -> Dict[str, Any]:
        controls = [
            {
                "id": "CC6.1",
                "title": "Logical and Physical Access Controls",
                "status": "PASS" if system_config.get("mfa_enforced") and system_config.get("rbac_active") else "FAIL",
                "description": "Multi-Factor Authentication (MFA) and Role-Based Access Control (RBAC) enforced on all administrative endpoints."
            },
            {
                "id": "CC6.6",
                "title": "Encryption in Transit and at Rest",
                "status": "PASS" if system_config.get("tls_enforced") and system_config.get("field_encryption_active") else "FAIL",
                "description": "TLS 1.3 enforced for transport layer; AES-256 field encryption for sensitive customer PII."
            },
            {
                "id": "CC7.2",
                "title": "Security Incident Monitoring & Audit Logging",
                "status": "PASS" if system_config.get("immutable_audit_ledger") else "FAIL",
                "description": "Cryptographically hashed, append-only audit trail recording all user actions."
            },
            {
                "id": "CC8.1",
                "title": "Change Management and Version Control",
                "status": "PASS" if system_config.get("git_controlled") and system_config.get("automated_tests_passing") else "FAIL",
                "description": "All codebase changes tracked in Git history with automated regression test suites."
            }
        ]

        failing_count = sum(1 for c in controls if c["status"] == "FAIL")
        is_compliant = failing_count == 0

        return {
            "evaluation_timestamp": datetime.now(timezone.utc).isoformat(),
            "standard": "AICPA SOC 2 Type II",
            "is_compliant": is_compliant,
            "failing_controls_count": failing_count,
            "controls": controls
        }
