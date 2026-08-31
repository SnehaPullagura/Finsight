import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/enterprise_data_dictionary.py
    write_file("backend/app/enterprise/enterprise_data_dictionary.py", """from typing import Any, Dict, List

class EnterpriseDataDictionary:
    @staticmethod
    def get_complete_entity_dictionary() -> Dict[str, Dict[str, Any]]:
        return {
            "organizations": {
                "table": "organizations",
                "description": "Multi-tenant root entity representing enterprise customer accounts and workspace configurations",
                "fields": ["id", "name", "slug", "domain", "plan_tier", "is_active", "settings", "created_at", "updated_at"]
            },
            "users": {
                "table": "users",
                "description": "Authenticated users, RBAC role mappings, MFA secrets, and login audit timestamps",
                "fields": ["id", "email", "hashed_password", "first_name", "last_name", "phone", "is_active", "is_verified", "is_superuser", "mfa_enabled"]
            },
            "contacts": {
                "table": "contacts",
                "description": "Individual point of contacts, corporate email addresses, lifecycle stages, and lead sources",
                "fields": ["id", "tenant_id", "company_id", "first_name", "last_name", "email", "phone", "title", "lifecycle_stage"]
            },
            "companies": {
                "table": "companies",
                "description": "Customer organizations, parent-child corporate hierarchies, annual revenue, and employee bands",
                "fields": ["id", "tenant_id", "name", "domain", "industry", "annual_revenue", "employee_count", "city", "country"]
            },
            "leads": {
                "table": "leads",
                "description": "Inbound prospects, AI qualification grades (A-F), intent scores (0-100), and conversion handlers",
                "fields": ["id", "tenant_id", "first_name", "last_name", "email", "company_name", "status", "score", "qualification_grade", "estimated_budget"]
            },
            "pipelines": {
                "table": "pipelines",
                "description": "Custom sales processes, weighted probability stages, SLA thresholds, and required fields",
                "fields": ["id", "tenant_id", "name", "is_default", "is_active"]
            },
            "deals": {
                "table": "deals",
                "description": "Sales opportunities, currency amounts, close dates, stage progressions, and win/loss reasons",
                "fields": ["id", "tenant_id", "pipeline_id", "stage_id", "company_id", "contact_id", "name", "value", "currency", "probability", "status"]
            },
            "subscriptions": {
                "table": "billing_subscriptions",
                "description": "Recurring SaaS billing subscriptions, MRR/ARR waterfall tracking, and auto-renew schedules",
                "fields": ["id", "tenant_id", "company_id", "plan_name", "status", "billing_frequency", "mrr_amount", "arr_amount", "start_date"]
            }
        }
""")

    # 2. backend/app/enterprise/enterprise_audit_log_viewer.py
    write_file("backend/app/enterprise/enterprise_audit_log_viewer.py", """from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class EnterpriseAuditLogViewer:
    @staticmethod
    def filter_and_format_audit_trail(
        audit_records: List[Dict[str, Any]],
        actor_id: Optional[str] = None,
        entity_type: Optional[str] = None,
        action: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        filtered = []
        for r in audit_records:
            if actor_id and r.get("actor_id") != actor_id:
                continue
            if entity_type and r.get("entity_type") != entity_type:
                continue
            if action and r.get("action") != action:
                continue

            formatted = dict(r)
            formatted["display_summary"] = f"{r.get('action', 'UPDATED').upper()} on {r.get('entity_type', 'Entity')} [{r.get('entity_id', '')}] by {r.get('actor_email', 'System')}"
            filtered.append(formatted)

        return sorted(filtered, key=lambda x: x.get("timestamp", ""), reverse=True)
""")

    print("Created data dictionary and audit log viewer.")

if __name__ == '__main__':
    run()
