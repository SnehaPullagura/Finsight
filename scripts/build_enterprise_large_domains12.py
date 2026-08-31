import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/enterprise_workflow_templates.py
    write_file("backend/app/enterprise/enterprise_workflow_templates.py", """from typing import Any, Dict, List

class EnterpriseWorkflowTemplates:
    @staticmethod
    def get_standard_templates() -> List[Dict[str, Any]]:
        return [
            {
                "id": "tpl-lead-sla-001",
                "name": "High-Priority Lead 15-Minute SLA Auto-Escalation",
                "category": "Sales Operations",
                "trigger": {"type": "entity_created", "entity": "lead", "condition": "lead.qualification_grade == 'A'"},
                "actions": [
                    {"step": 1, "type": "delay", "duration_minutes": 15},
                    {"step": 2, "type": "condition_check", "expression": "lead.status == 'new'"},
                    {"step": 3, "type": "notify_slack", "channel": "#sales-urgent-leads", "message": "URGENT: Grade A Lead has not been contacted within 15 min SLA!"},
                    {"step": 4, "type": "reassign_round_robin", "team_id": "team-enterprise-sdr"}
                ]
            },
            {
                "id": "tpl-deal-won-002",
                "name": "Enterprise Deal Won Handover & Onboarding Trigger",
                "category": "Customer Success",
                "trigger": {"type": "status_changed", "entity": "deal", "target_status": "won"},
                "actions": [
                    {"step": 1, "type": "create_customer_success_plan", "health_score": 100},
                    {"step": 2, "type": "create_onboarding_milestones", "count": 4},
                    {"step": 3, "type": "generate_invoice", "payment_terms": "NET30"},
                    {"step": 4, "type": "notify_slack", "channel": "#sales-wins", "message": "🎉 Enterprise Deal Closed Won!"}
                ]
            },
            {
                "id": "tpl-invoice-dunning-003",
                "name": "Overdue Invoice Dunning & Grace Period Sequence",
                "category": "Finance & Billing",
                "trigger": {"type": "cron", "schedule": "daily_at_0900"},
                "actions": [
                    {"step": 1, "type": "query_overdue_invoices", "grace_days": 7},
                    {"step": 2, "type": "send_email_template", "template_id": "tpl-dunning-first-notice"},
                    {"step": 3, "type": "create_task", "title": "Follow up on overdue invoice", "priority": "high"}
                ]
            },
            {
                "id": "tpl-churn-prevention-004",
                "name": "Customer Health Score Churn Prevention Escalation",
                "category": "Customer Success",
                "trigger": {"type": "health_score_dropped", "threshold": 50},
                "actions": [
                    {"step": 1, "type": "notify_account_manager", "priority": "urgent"},
                    {"step": 2, "type": "create_executive_alignment_task", "due_days": 2},
                    {"step": 3, "type": "flag_at_risk_in_crm", "risk_level": "high"}
                ]
            }
        ]
""")

    # 2. backend/app/enterprise/enterprise_lead_scoring_models.py
    write_file("backend/app/enterprise/enterprise_lead_scoring_models.py", """from typing import Any, Dict, List, Optional

class EnterpriseLeadScoringModel:
    FIT_WEIGHTS = {
        "industry_tier_1": 30, # Software, FinTech, HealthTech
        "industry_tier_2": 20, # Manufacturing, Retail, Professional Services
        "company_size_enterprise": 30, # 1,000+ employees
        "company_size_midmarket": 20,  # 100-999 employees
        "annual_revenue_50m_plus": 25,
        "annual_revenue_10m_plus": 15,
        "target_country_tier_1": 15 # US, UK, CA, DE, FR, AU, SG
    }

    INTENT_WEIGHTS = {
        "pricing_page_visited": 25,
        "security_whitepaper_downloaded": 20,
        "demo_requested": 40,
        "webinar_attended": 15,
        "multiple_stakeholder_visits": 20
    }

    @staticmethod
    def calculate_composite_score(
        fit_signals: List[str],
        intent_signals: List[str],
        decay_factor: float = 1.0
    ) -> Dict[str, Any]:
        fit_score = sum(EnterpriseLeadScoringModel.FIT_WEIGHTS.get(s, 0) for s in fit_signals)
        intent_score = sum(EnterpriseLeadScoringModel.INTENT_WEIGHTS.get(s, 0) for s in intent_signals) * decay_factor

        total_raw = (fit_score * 0.50) + (intent_score * 0.50)
        final_score = max(0, min(100, int(total_raw)))

        grade = "A" if final_score >= 80 else "B" if final_score >= 65 else "C" if final_score >= 45 else "D"

        return {
            "fit_score": fit_score,
            "intent_score": round(intent_score, 1),
            "final_lead_score": final_score,
            "qualification_grade": grade,
            "is_mql": final_score >= 65,
            "is_sql_ready": final_score >= 80
        }
""")

    print("Created workflow templates and lead scoring models.")

if __name__ == '__main__':
    run()
