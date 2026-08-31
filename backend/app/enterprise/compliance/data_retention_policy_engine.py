from datetime import date, timedelta
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
