import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/compliance/soc2_compliance_validator.py
    write_file("backend/app/enterprise/compliance/soc2_compliance_validator.py", """from datetime import datetime, timezone
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
""")

    # 2. backend/app/enterprise/compliance/data_retention_policy_engine.py
    write_file("backend/app/enterprise/compliance/data_retention_policy_engine.py", """from datetime import date, timedelta
from typing import Any, Dict, List, Optional

class DataRetentionPolicyEngine:
    POLICY_DAYS = {
        "audit_logs": 2555,      # 7 years for compliance audits
        "financial_invoices": 2555, # 7 years for tax accounting
        "transient_sessions": 30,  # 30 days for inactive session tokens
        "marketing_leads": 365,    # 1 year for uncontacted leads
        "deleted_trash": 30        # 30 days soft-delete recovery window
    }

    @staticmethod
    def identify_expired_records(records: List[Dict[str, Any]], record_type: str, current_date: Optional[date] = None) -> List[Dict[str, Any]]:
        today = current_date or date.today()
        retention_days = DataRetentionPolicyEngine.POLICY_DAYS.get(record_type, 365)
        cutoff_date = today - timedelta(days=retention_days)

        expired = []
        for r in records:
            created_str = r.get("created_at") or r.get("date")
            if not created_str:
                continue
            created_date = date.fromisoformat(created_str.split("T")[0])
            if created_date < cutoff_date:
                expired.append({
                    "id": r.get("id"),
                    "created_date": created_date.isoformat(),
                    "age_days": (today - created_date).days,
                    "retention_policy_days": retention_days,
                    "action_required": "purge"
                })

        return expired
""")

    # 3. backend/app/enterprise/customer_success/nps_survey_engine.py
    write_file("backend/app/enterprise/customer_success/nps_survey_engine.py", """from typing import Any, Dict, List, Optional

class NetPromoterScoreEngine:
    @staticmethod
    def calculate_nps(responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not responses:
            return {"nps_score": 0, "promoters_pct": 0.0, "passives_pct": 0.0, "detractors_pct": 0.0, "total_responses": 0}

        promoters = [r for r in responses if int(r.get("score", 0)) >= 9]
        passives = [r for r in responses if 7 <= int(r.get("score", 0)) <= 8]
        detractors = [r for r in responses if int(r.get("score", 0)) <= 6]

        total = len(responses)
        promoters_pct = round((len(promoters) / float(total)) * 100.0, 1)
        passives_pct = round((len(passives) / float(total)) * 100.0, 1)
        detractors_pct = round((len(detractors) / float(total)) * 100.0, 1)

        nps = int(round(promoters_pct - detractors_pct))

        return {
            "nps_score": nps,
            "promoters_count": len(promoters),
            "promoters_percentage": promoters_pct,
            "passives_count": len(passives),
            "passives_percentage": passives_pct,
            "detractors_count": len(detractors),
            "detractors_percentage": detractors_pct,
            "total_responses": total,
            "benchmark_rating": "Excellent" if nps >= 50 else "Good" if nps >= 30 else "Needs Improvement" if nps >= 0 else "Critical"
        }
""")

    print("Created SOC2 validator, data retention, and NPS engine.")

if __name__ == '__main__':
    run()
