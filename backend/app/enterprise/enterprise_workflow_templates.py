from typing import Any, Dict, List

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
