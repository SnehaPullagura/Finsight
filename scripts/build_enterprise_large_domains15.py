import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/enterprise_migration_templates.py
    write_file("backend/app/enterprise/enterprise_migration_templates.py", """from typing import Any, Dict, List

class EnterpriseMigrationTemplates:
    @staticmethod
    def get_crm_mapping_templates() -> Dict[str, Dict[str, str]]:
        return {
            "salesforce": {
                "AccountId": "company_id",
                "AccountName": "company_name",
                "ContactEmail": "email",
                "FirstName": "first_name",
                "LastName": "last_name",
                "Phone": "phone",
                "OpportunityAmount": "deal_value",
                "StageName": "stage",
                "CloseDate": "expected_close_date",
                "LeadSource": "lead_source",
                "AnnualRevenue": "annual_revenue"
            },
            "hubspot": {
                "hs_object_id": "external_id",
                "email": "email",
                "firstname": "first_name",
                "lastname": "last_name",
                "phone": "phone",
                "company": "company_name",
                "amount": "deal_value",
                "dealstage": "stage",
                "closedate": "expected_close_date",
                "lifecyclestage": "lifecycle_stage"
            },
            "zoho": {
                "Account_Name": "company_name",
                "Email": "email",
                "First_Name": "first_name",
                "Last_Name": "last_name",
                "Phone": "phone",
                "Amount": "deal_value",
                "Stage": "stage",
                "Closing_Date": "expected_close_date",
                "Lead_Source": "lead_source"
            }
        }
""")

    # 2. backend/app/enterprise/enterprise_dunning_manager.py
    write_file("backend/app/enterprise/enterprise_dunning_manager.py", """from datetime import date, timedelta
from typing import Any, Dict, List, Optional

class EnterpriseDunningManager:
    @staticmethod
    def evaluate_invoice_dunning_stage(
        due_date: date,
        amount_due: float,
        current_date: Optional[date] = None
    ) -> Dict[str, Any]:
        today = current_date or date.today()
        days_overdue = (today - due_date).days

        if days_overdue <= 0:
            stage = "current"
            action = "none"
            grace_active = False
        elif days_overdue <= 7:
            stage = "soft_reminder"
            action = "send_gentle_reminder_email"
            grace_active = True
        elif days_overdue <= 14:
            stage = "urgent_reminder"
            action = "send_urgent_past_due_email"
            grace_active = True
        elif days_overdue <= 30:
            stage = "account_warning"
            action = "create_account_manager_task"
            grace_active = False
        else:
            stage = "service_suspension_warning"
            action = "suspend_non_essential_features"
            grace_active = False

        return {
            "due_date": due_date.isoformat(),
            "days_overdue": max(0, days_overdue),
            "amount_due": amount_due,
            "dunning_stage": stage,
            "recommended_action": action,
            "is_grace_period_active": grace_active
        }
""")

    # 3. backend/app/enterprise/enterprise_abac_security_rules.py
    write_file("backend/app/enterprise/enterprise_abac_security_rules.py", """from typing import Any, Dict, List, Optional

class EnterpriseABACSecurityRules:
    @staticmethod
    def get_security_policy_definitions() -> List[Dict[str, Any]]:
        return [
            {
                "policy_id": "pol-deal-export-001",
                "name": "Restrict Deal Pipeline Bulk Export to Executives & Admins",
                "resource": "deals",
                "action": "export",
                "effect": "allow",
                "conditions": {"roles": ["Admin", "VP of Sales", "Executive"]}
            },
            {
                "policy_id": "pol-pii-masking-002",
                "name": "Mask Customer Credit Card & Sensitive PII from Support Tier 1",
                "resource": "contacts.pii",
                "action": "read_unmasked",
                "effect": "deny",
                "conditions": {"roles": ["Support Tier 1", "Guest"]}
            },
            {
                "policy_id": "pol-discount-approval-003",
                "name": "Enforce Multi-Tier Approval on Quote Discounts Exceeding 20%",
                "resource": "quotes",
                "action": "issue_discount_above_20_pct",
                "effect": "allow",
                "conditions": {"roles": ["Sales Manager", "VP of Sales", "Admin"]}
            }
        ]
""")

    print("Created migration templates, dunning manager, and ABAC security rules.")

if __name__ == '__main__':
    run()
